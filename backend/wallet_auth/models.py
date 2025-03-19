# wallet_auth/models.py

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class SolanaUserManager(BaseUserManager):
    """Manager for users authenticated with Solana wallets"""

    def create_user(self, wallet_address, password=None, **extra_fields):
        if not wallet_address:
            raise ValueError("Users must have a wallet address")

        wallet_address = wallet_address.lower()
        user = self.model(wallet_address=wallet_address, **extra_fields)

        if user.is_staff or user.is_superuser:
            if not password:
                raise ValueError("Admins must have a password")
            user.set_password(password)
        else:
            user.set_unusable_password()  # Normal users don't have passwords

        user.save(using=self._db)
        return user

    def create_superuser(self, wallet_address, password, **extra_fields):
        """Creates a superuser with a password"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Superuser must have a password")

        return self.create_user(wallet_address, password, **extra_fields)


class SolanaUser(AbstractUser):
    """User model for Solana wallet authentication"""
    username = None  # Remove username
    email = None  # Remove email
    wallet_address = models.CharField(max_length=44, unique=True, primary_key=True)

    display_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)

    USERNAME_FIELD = "wallet_address"
    REQUIRED_FIELDS = []

    objects = SolanaUserManager()

    def get_display_name(self):
        """Returns the display name if available, otherwise returns wallet address"""
        return self.display_name if self.display_name else self.wallet_address

    def __str__(self):
        return self.wallet_address

class Coin(models.Model):
    """Represents a coin on the platform"""
    address = models.CharField(primary_key=True, max_length=44, unique=True, editable=False)
    symbol = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, unique=True)
    creator = models.ForeignKey(SolanaUser, on_delete=models.CASCADE, related_name='coins', to_field="wallet_address")
    created_at = models.DateTimeField(auto_now_add=True)
    total_supply = models.DecimalField(max_digits=20, decimal_places=8)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    # ticker = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    telegram = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)

    current_price = models.DecimalField(max_digits=20, decimal_places=8, default=0)  # Added price field

    def __str__(self):
        return f"{self.name} ({self.symbol})"
    
    # def get_current_price(self): # should we use an external api to get the pricing
    #     # Placeholder: Replace with actual API integration
    #     return 1  # Assuming $1 per coin for now

    def save(self, *args, **kwargs):
        if self.symbol:
            self.symbol = self.symbol.upper()  # Ensure it's always uppercase
        super().save(*args, **kwargs)

    @property
    def total_held(self):
        """Returns the total amount of this coin held by all users."""
        from django.db.models import Sum
        total = self.holders.aggregate(total=Sum('amount_held'))['total']
        return total or 0  # Return 0 if no holdings exist

    @property
    def market_cap(self):
        """Calculates market cap: (Total Supply - Total Held) * Current Price"""
        return (self.total_supply - self.total_held) * self.current_price

    class Meta:
        ordering = ['-created_at']


class UserCoinHoldings(models.Model):
    """Tracks how much of a specific coin a user holds"""
    user = models.ForeignKey(SolanaUser, on_delete=models.CASCADE, related_name="holdings", to_field="wallet_address")
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name="holders", to_field="address")
    amount_held = models.DecimalField(max_digits=20, decimal_places=8, default=0) # add a way to check if the holdings is above the availiable coins

    class Meta:
        unique_together = ('user', 'coin')  # Ensures a user can't have duplicate records for the same coin
    
    def held_percentage(self):
        return (self.amount_held / self.coin.total_supply) * 100

    def __str__(self):
        return f"{self.user.wallet_address} holds {self.held_percentage()} of {self.coin.symbol}"

class Trade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(SolanaUser, on_delete=models.CASCADE, related_name='trades', to_field="wallet_address")
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='trades', to_field="address")
    # Trade type: True for buy, False for sell (or use an Enum if needed)
    trade_type = models.BooleanField()
    coin_amount = models.DecimalField(max_digits=20, decimal_places=8)
    sol_amount = models.DecimalField(max_digits=20, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        trade_type = "Buy" if self.trade_type else "Sell"
        # if user nick name empty replace by address
        return f"{trade_type} Trade by {self.user.get_display_name()} on {self.coin.symbol}"

    class Meta:
        ordering = ['-created_at']
