# wallet_auth/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class SolanaUserManager(BaseUserManager):
    """Manager for users authenticated with Solana wallets"""
    
    def create_user(self, wallet_address, **extra_fields):
        if not wallet_address:
            raise ValueError('Users must have a wallet address')
        
        # Normalize wallet address (all lowercase)
        wallet_address = wallet_address.lower()
        
        # Create user
        user = self.model(wallet_address=wallet_address, **extra_fields)
        user.set_unusable_password()  # No password needed
        user.save(using=self._db)
        return user
    
    def create_superuser(self, wallet_address, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(wallet_address, **extra_fields)

class SolanaUser(AbstractUser):
    """User model for Solana wallet authentication"""
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    wallet_address = models.CharField(max_length=44, unique=True)
    
    # Additional profile fields you might want
    display_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    
    USERNAME_FIELD = 'wallet_address'
    REQUIRED_FIELDS = []
    
    objects = SolanaUserManager()
    
    def __str__(self):
        return self.wallet_address