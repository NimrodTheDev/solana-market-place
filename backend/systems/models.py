from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# integrate the score directly into the models
class SolanaUserManager(BaseUserManager):
    """Manager for users authenticated with Solana wallets"""

    def create_user(self, wallet_address, password=None, **extra_fields):
        if not wallet_address:
            raise ValueError("Users must have a wallet address")

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
    
    @property
    def devscore(self):
        """Dynamically retrieve and recalculate the developer score."""
        if hasattr(self, 'developer_score'):
            return self.developer_score.recalculate_score()
        return 0  # Default base score if no score record exists
    
    @property
    def tradescore(self):
        """Dynamically retrieve and recalculate the trade score."""
        if hasattr(self, 'trader_score'):
            return self.trader_score.recalculate_score()
        return 200  # Default base score if no score record exists

class Coin(models.Model): # add a way to make things more strick
    """Represents a coin on the platform"""
    address = models.CharField(primary_key=True, max_length=44, unique=True, editable=False)
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(SolanaUser, on_delete=models.CASCADE, related_name='coins', to_field="wallet_address")
    created_at = models.DateTimeField(auto_now_add=True)
    total_supply = models.DecimalField(max_digits=20, decimal_places=8)
    image_url = models.URLField(max_length=500)
    ticker = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    discord = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)

    current_price = models.DecimalField(max_digits=20, decimal_places=8, default=0)  # Added price field

    def __str__(self):
        return f"{self.name} ({self.ticker})"
    
    def save(self, *args, **kwargs):
        if self.ticker:
            self.ticker = self.ticker.upper()  # Ensure it's always uppercase
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
    
    @property
    def score(self):
        """Dynamically retrieve and recalculate the trade score."""
        if hasattr(self, 'drc_score'):
            return self.drc_score.recalculate_score()
        return 200  # Default base score if no score record exists

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
        return f"{self.user.wallet_address} holds {self.held_percentage()}% of {self.coin.ticker}" # i added %

class Trade(models.Model): # change to transaction hash
    TRADE_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
        ('COIN_CREATE', 'Coin Creation'),
    ]

    transaction_hash = models.CharField(max_length=88, primary_key=True, unique= True, editable= False)
    user = models.ForeignKey(SolanaUser, on_delete=models.CASCADE, related_name='trades', to_field="wallet_address")
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='trades', to_field="address")
    trade_type = models.CharField(max_length=14, choices=TRADE_TYPES)
    coin_amount = models.DecimalField(max_digits=20, decimal_places=8)
    sol_amount = models.DecimalField(max_digits=20, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_trade_type_display()} Trade by {self.user.get_display_name()} on {self.coin.ticker}"

    class Meta:  # error here ordering should be latest trades first
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['coin']),
            models.Index(fields=['created_at']),
        ]


# drc stuffs
class DRCScore(models.Model):
    """Base model for DRC scoring with common fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=200, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    
    class Meta:
        abstract = True

class DeveloperScore(DRCScore):
    """
    Developer reputation score tracking for Solana users who create coins
    """
    # developer = models.OneToOneField('SolanaUser', on_delete=models.CASCADE, 
    #                                 related_name='developer_score', 
    #                                 to_field="wallet_address")
    developer = models.OneToOneField(
        SolanaUser,
        on_delete=models.CASCADE,
        related_name='developer_score',
        to_field="wallet_address"
    )
    
    # Historical performance metrics
    coins_created_count = models.IntegerField(default=0)
    coins_active_24h_plus = models.IntegerField(default=0)
    coins_rugged_count = models.IntegerField(default=0)
    highest_market_cap = models.DecimalField(max_digits=24, decimal_places=8, default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['score']),
            models.Index(fields=['developer']),
        ]
    
    def __str__(self):
        return f"Dev Score for {self.developer.wallet_address}: {self.score}"
    
    def recalculate_score(self):
        """
        Calculate developer reputation based on their coin creation history
        """
        # Base score starts at 200
        base_score = 200
        
        # Get all coins created by this developer
        developer_coins = self.developer.coins.all()
        
        # Update coin counts
        self.coins_created_count = developer_coins.count()
        
        # Count coins that have existed over 24 hours
        one_day_ago = timezone.now() - timezone.timedelta(hours=24)
        self.coins_active_24h_plus = developer_coins.filter(
            created_at__lt=one_day_ago
        ).count()
        
        # Find highest market cap
        for coin in developer_coins:
            if coin.market_cap > self.highest_market_cap:
                self.highest_market_cap = coin.market_cap
        
        # Calculate score components
        longevity_score = min(self.coins_active_24h_plus * 100, 300)
        volume_score = min(self.coins_created_count * 50, 200)
        
        # Calculate rug penalty (determined by CoinRugFlag model)
        self.coins_rugged_count = CoinRugFlag.objects.filter(
            coin__in=developer_coins,
            is_rugged=True
        ).count()
        
        rug_penalty = min(self.coins_rugged_count * 200, 500)

        # Market cap bonus (scaled logarithmically)
        market_cap_bonus = 0
        if self.highest_market_cap > 0: # recheck this
            import math
            # Log base 10 of market cap in SOL, max 100 points
            market_cap_in_sol = float(self.highest_market_cap)
            if market_cap_in_sol > 0:
                market_cap_bonus = min(int(math.log10(market_cap_in_sol) * 25), 100)
        
        # Calculate final score with clamping
        total_score = base_score + longevity_score + volume_score + market_cap_bonus - rug_penalty
        self.score = max(min(total_score, 1000), 200)  # Clamp between 200-1000
        
        self.save()
        return self.score

class TraderScore(DRCScore):
    """
    Trader reputation score tracking for Solana users who trade coins
    """
    trader = models.OneToOneField(SolanaUser, on_delete=models.CASCADE, 
                                 related_name='trader_score',
                                 to_field="wallet_address")
    
    # Trading behavior metrics
    coins_held_count = models.IntegerField(default=0)
    avg_holding_time_hours = models.IntegerField(default=0)
    trades_count = models.IntegerField(default=0)
    quick_dumps_count = models.IntegerField(default=0)
    profitable_trades_percent = models.FloatField(default=0,
                                                 validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    class Meta:
        indexes = [
            models.Index(fields=['score']),
            models.Index(fields=['trader']),
        ]
    
    def __str__(self):
        return f"Trader Score for {self.trader.wallet_address}: {self.score}"
    
    def recalculate_score(self): # recheck 
        """
        Calculate trader reputation based on their trading history
        """
        # Base score starts at 200
        base_score = 200
        
        # Get all trades by this trader
        user_trades = self.trader.trades.all()
        self.trades_count = user_trades.count()
        
        if self.trades_count == 0:
            self.score = base_score
            self.save()
            return self.score
            
        # Get current holdings
        holdings = self.trader.holdings.all()
        self.coins_held_count = holdings.count()
        
        # Calculate average holding time
        total_holding_time = 0
        for holding in holdings:
            # Find the earliest buy trade for this coin
            earliest_buy = user_trades.filter(
                coin=holding.coin,
                trade_type='BUY'
            ).order_by('created_at').first()
            
            if earliest_buy:
                holding_time = (timezone.now() - earliest_buy.created_at).total_seconds() / 3600
                total_holding_time += holding_time
                
        if self.coins_held_count > 0:
            self.avg_holding_time_hours = int(total_holding_time / self.coins_held_count)
        
        # Count quick dumps (selling >50% within 1 hour of buying)
        self.quick_dumps_count = 0
        for coin in set(user_trades.values_list('coin', flat=True)):
            coin_trades = user_trades.filter(coin=coin).order_by('created_at')
            buy_trades = coin_trades.filter(trade_type='BUY')
            sell_trades = coin_trades.filter(trade_type='SELL')
            
            for sell in sell_trades:
                # Find the most recent buy before this sell
                previous_buy = buy_trades.filter(created_at__lt=sell.created_at).order_by('-created_at').first()
                
                if previous_buy:
                    time_diff = (sell.created_at - previous_buy.created_at).total_seconds() / 3600
                    
                    # Calculate what percentage of holdings was sold
                    if previous_buy.coin_amount > 0:
                        sell_percentage = (sell.coin_amount / previous_buy.coin_amount) * 100
                        
                        # If sold >50% within 1 hour, count as quick dump
                        if time_diff < 1 and sell_percentage > 50:
                            self.quick_dumps_count += 1
        
        # Calculate score components
        diversity_bonus = min(self.coins_held_count * 20, 100)
        holding_time_bonus = min(self.avg_holding_time_hours, 168) / 24 * 10  # Max 70 points (7 days)
        activity_bonus = min(self.trades_count, 50) * 2  # Max 100 points
        
        # Penalties
        dump_penalty = min(self.quick_dumps_count * 30, 150)
        
        # Calculate final score with clamping
        total_score = base_score + diversity_bonus + holding_time_bonus + activity_bonus - dump_penalty
        self.score = max(min(total_score, 1000), 0)  # Prevent negative scores, cap at 1000
        
        self.save()
        return self.score

class CoinDRCScore(DRCScore):
    """
    DRC score for individual coins, combining developer reputation, 
    market metrics and contract security
    """
    coin = models.OneToOneField(Coin, on_delete=models.CASCADE, 
                               related_name='drc_score',
                               to_field="address")
    
    # Market metrics
    holders_count = models.IntegerField(default=0)
    age_in_hours = models.IntegerField(default=0)
    trade_volume_24h = models.DecimalField(max_digits=24, decimal_places=8, default=0)
    price_stability_score = models.IntegerField(default=50, 
                                              validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Security metrics
    verified_contract = models.BooleanField(default=False)
    audit_completed = models.BooleanField(default=False)
    audit_score = models.IntegerField(default=0, 
                                     validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    class Meta:
        indexes = [
            models.Index(fields=['score']),
            models.Index(fields=['coin']),
            models.Index(fields=['age_in_hours']),
        ]
    
    def __str__(self):
        return f"DRC Score for {self.coin.name}: {self.score}"
    
    def update_age(self, dont_save: bool = False):
        """Update the age of the coin in hours"""
        if self.coin.created_at:
            self.age_in_hours = int((timezone.now() - self.coin.created_at).total_seconds() / 3600)
            if not dont_save:
                self.save(update_fields=['age_in_hours', 'updated_at'])
        return self.age_in_hours
    
    def update_holders_count(self, dont_save: bool = False):
        """Update the count of holders for this coin"""
        self.holders_count = self.coin.holders.count()
        if not dont_save:
            self.save(update_fields=['holders_count', 'updated_at'])
        return self.holders_count
    
    def recalculate_score(self):
        """
        Calculate DRC score based on coin metrics and developer reputation
        """
        # Make sure age is up to date
        self.update_age(dont_save=True)
        self.update_holders_count(dont_save=True)
        
        # Get developer score
        try:
            dev_score = self.coin.creator.developer_score.score
        except Exception:
            # Create developer score if it doesn't exist
            dev_score = DeveloperScore.objects.create(developer=self.coin.creator).score
        
        # Check if coin is rugged
        is_rugged = CoinRugFlag.objects.filter(coin=self.coin, is_rugged=True).exists()
        
        # Base components
        age_factor = min(self.age_in_hours / 24, 10) * 20  # Max 200 points for age (capped at 10 days)
        holder_factor = min(self.holders_count, 200) / 2  # Max 100 points for holders
        
        # Volume and liquidity factors
        volume_factor = min(float(self.trade_volume_24h), 1000) / 10  # Max 100 points
        
        # Security factors
        contract_bonus = 50 if self.verified_contract else 0
        audit_bonus = self.audit_score / 2 if self.audit_completed else 0  # Max 50 points
        
        # Developer reputation factor (20% influence)
        dev_factor = dev_score * 0.2  # Max 200 points if dev score is 1000
        
        # Price stability (more stable prices get more points)
        stability_factor = self.price_stability_score / 2  # Max 50 points
        
        # Rug penalty
        rug_penalty = 500 if is_rugged else 0
        
        # Calculate total score
        total_score = age_factor + holder_factor + volume_factor + contract_bonus + audit_bonus + dev_factor + stability_factor - rug_penalty
        
        # Ensure score is within bounds
        self.score = max(min(int(total_score), 1000), 0)
        self.save()
        
        return self.score
    
    @property
    def score_breakdown(self):
        """
        Provides a detailed breakdown of the score components
        """
        try:
            dev_score = self.coin.creator.developer_score.score
        except Exception:
            dev_score = 200  # Default score
            
        is_rugged = CoinRugFlag.objects.filter(coin=self.coin, is_rugged=True).exists()
        
        return {
            'age_factor': min(self.age_in_hours / 24, 10) * 20,
            'holder_factor': min(self.holders_count, 200) / 2,
            'volume_factor': min(float(self.trade_volume_24h), 1000) / 10,
            'contract_verified': 50 if self.verified_contract else 0,
            'audit_bonus': self.audit_score / 2 if self.audit_completed else 0,
            'dev_reputation': dev_score * 0.2,
            'stability_factor': self.price_stability_score / 2,
            'rug_penalty': -500 if is_rugged else 0,
            'total': self.score
        }

class CoinRugFlag(models.Model): # remove if they decied for not detailed logs might not be needed
    """
    Tracks whether a coin has been flagged as rugged
    """
    coin = models.OneToOneField('Coin', on_delete=models.CASCADE, 
                               related_name='rug_flag',
                               to_field="address")
    is_rugged = models.BooleanField(default=False)
    rugged_at = models.DateTimeField(null=True, blank=True)
    rug_transaction = models.UUIDField(null=True, blank=True)  # Optional reference to the transaction
    rug_description = models.TextField(blank=True)
    
    def __str__(self):
        status = "RUGGED" if self.is_rugged else "Not rugged"
        return f"{self.coin.name}: {status}"
    
    def mark_as_rugged(self, transaction_id=None, description=""):
        """Mark a coin as rugged with optional transaction ID and description"""
        self.is_rugged = True
        self.rugged_at = timezone.now()
        
        if transaction_id:
            self.rug_transaction = transaction_id
        
        if description:
            self.rug_description = description
            
        self.save()
        
        # Also update the DRC score for this coin
        try:
            drc_score = self.coin.drc_score
            drc_score.recalculate_score()
        except CoinDRCScore.DoesNotExist:
            # Create one if it doesn't exist
            CoinDRCScore.objects.create(coin=self.coin).recalculate_score()
        
        # Update developer score
        try:
            dev_score = self.coin.creator.developer_score
            dev_score.coins_rugged_count += 1
            dev_score.recalculate_score()
        except DeveloperScore.DoesNotExist:
            # Create one if it doesn't exist
            dev_score = DeveloperScore.objects.create(developer=self.coin.creator)
            dev_score.coins_rugged_count = 1
            dev_score.recalculate_score()
