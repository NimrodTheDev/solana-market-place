from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum
from decimal import Decimal

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

    current_price = models.DecimalField(max_digits=20, decimal_places=8, default=0)  # Added price field # start calculating

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

    @property
    def liquidity(self):
        return (self.total_held * self.current_price)

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
    score = models.IntegerField(default=150) #, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    
    class Meta:
        abstract = True
    
    @property
    def rank(self):
        match self.score:
            case x if x < 150:
                return 1
            case x if x < 500:
                return 2
            case x if x < 1000:
                return 3
            case x if x < 2000:
                return 4
            case x if x >= 2000:
                return 5

# fix some parts
class CoinDRCScore(DRCScore):
    """
    DRC score for individual coins, combining developer reputation, 
    market metrics and contract security
    """
    coin = models.OneToOneField(
        Coin, 
        on_delete=models.CASCADE, 
        related_name='drc_score',
        to_field="address"
    )
    
    # Market metrics
    holders_count = models.IntegerField(default=0)
    age_in_hours = models.IntegerField(default=0)
    max_volume_recorded = models.DecimalField(max_digits=24, decimal_places=8, default=0)
    
    # Price tracking
    price_breakouts_per_month = models.IntegerField(default=0)
    last_recorded_price = models.DecimalField(max_digits=24, decimal_places=8, default=0) # was integer before
    last_price = models.DecimalField(max_digits=24, decimal_places=8, default=0)
    
    # Holder metrics
    holder_retention_months = models.IntegerField(default=0)
    last_recorded_holders = models.IntegerField(default=0)
    
    # Flags for abandonment detection
    team_abandonment = models.BooleanField(default=False)
    token_abandonment = models.BooleanField(default=False)
    pump_and_dump_activity = models.BooleanField(default=False)
    
    # Tracking for periodic calculations
    last_monthly_update = models.DateTimeField(auto_now_add=True)
    last_biweekly_update = models.DateTimeField(auto_now_add=True)
    last_daily_update = models.DateTimeField(null=True, blank=True)    

    class Meta:
        indexes = [
            models.Index(fields=['score']),
            models.Index(fields=['coin']),
            models.Index(fields=['age_in_hours']),
            models.Index(fields=['last_monthly_update']),
            models.Index(fields=['last_biweekly_update']),
        ]
    
    def __str__(self):
        return f"DRC Score for {self.coin.name}: {self.score}"
    
    def update_age(self, save=True):
        """Update the age of the coin in hours"""
        if self.coin.created_at:
            self.age_in_hours = int((timezone.now() - self.coin.created_at).total_seconds() / 3600)
            if save:
                self.save(update_fields=['age_in_hours', 'updated_at'])
        return self.age_in_hours

    def update_price_breakouts(self, old_price, new_price, save=True):
        """Detect and record price breakouts (changes exceeding 10%)"""
        if old_price <= 0:
            return
            
        pct_change = abs((new_price - old_price) / old_price)
        
        if pct_change > 0.1:  # 10% breakout threshold
            self.price_breakouts_per_month += 1
            if save:
                self.save(update_fields=['price_breakouts_per_month', 'updated_at'])
    
    def update_holders_count(self, save=True):
        """Update the count of holders for this coin"""
        self.holders_count = self.coin.holders.count()
        if save:
            self.save(update_fields=['holders_count', 'updated_at'])
        return self.holders_count
    
    def daily_checkup(self):
        """Perform daily score maintenance tasks"""
        now = timezone.now()
        
        # Skip if already updated today
        if (self.last_daily_update and 
            self.last_daily_update.date() == now.date()):
            return
        
        # Update basic metrics
        self.update_age(save=False)
        self.update_holders_count(save=False)
        
        # Check for price breakouts
        if self.last_price > 0:
            self.update_price_breakouts(
                self.last_price, 
                self.coin.current_price, 
                save=False
            )
        
        # Update last price
        self.last_price = self.coin.current_price
        # Check abandonment conditions
        self._check_dev_dumping(save=False)
        self._check_token_abandonment(save=False)
        self._check_pump_and_dump(save=False)
        
        # Update timestamp
        self.last_daily_update = now
        
        # Save all changes
        self.save(update_fields=[
            'age_in_hours', 'holders_count', 'pump_and_dump_activity',
            'price_breakouts_per_month', 'last_price', 'team_abandonment',
            'token_abandonment', 'score', 'last_daily_update', 'updated_at'
        ])
        
        # Recalculate score with daily factors
        self._apply_daily_score_adjustments()

    def monthly_recalculation(self):
        """Perform comprehensive monthly score recalculation"""
        now = timezone.now()
        
        # Skip if already updated this month
        if (self.last_monthly_update and 
            self.last_monthly_update.month == now.month and
            self.last_monthly_update.year == now.year):
            return
        
        # Calculate monthly factors
        fair_trading_bonus = self._calculate_fair_trading_bonus()
        price_growth_bonus = self._calculate_price_growth_bonus()
        retention_bonus = self._calculate_retention_bonus()
        
        # Apply bonuses
        total_bonus = (
            fair_trading_bonus + 
            price_growth_bonus + 
            retention_bonus
        )
        
        # Cap the bonus to prevent excessive score inflation
        capped_bonus = min(total_bonus, 300)
        self.score = max(0, self.score + int(capped_bonus))
        
        # Reset monthly counters
        self._reset_monthly_counters()
        
        # Update timestamp
        self.last_monthly_update = now
        
        self.save(update_fields=[
            'score', 'price_breakouts_per_month', 'last_recorded_price',
            'last_recorded_holders', 'holder_retention_months',
            'last_monthly_update', 'updated_at'
        ])

    def biweekly_checkup(self):
        """Perform bi-weekly score maintenance and holder quality assessment"""
        now = timezone.now()
        
        # Skip if already updated this bi-weekly period
        if self._is_same_biweekly_period(self.last_biweekly_update, now):
            return
        
        holder_rank_bonus = self._calculate_holder_rank_bonus()
        # Apply bi-weekly bonuses
        total_biweekly_bonus = (
            holder_rank_bonus
        )
        
        # Cap the bi-weekly bonus
        capped_bonus = min(total_biweekly_bonus, 50)
        self.score = max(0, self.score + int(capped_bonus))
        
        self._update_biweekly_metrics()
        
        # Update timestamp
        self.last_biweekly_update = now
        
        self.save(update_fields=[
            'score', 'last_biweekly_update', 'updated_at'
        ])

    def _is_same_biweekly_period(self, last_update, current_time):
        """Check if we're in the same bi-weekly period"""
        if not last_update:
            return False
        
        # Calculate days since last update
        days_diff = (current_time - last_update).days
        
        # If less than 14 days, we're in the same period
        return days_diff < 14

    def _calculate_fair_trading_bonus(self):
        cutoff_time = timezone.now() - timezone.timedelta(days=30)
        volume_data = self.coin.trades.filter(
            created_at__gte=cutoff_time
        ).aggregate(
            total_volume=Sum('sol_amount')
        )
        """Calculate bonus for fair trading patterns (low volatility)"""
        if self.price_breakouts_per_month <= 6 and volume_data['total_volume'] != None:  # Max 6 breakouts considered fair
            if volume_data['total_volume'] >= 15:
                return 50 
        return 0

    def _calculate_price_growth_bonus(self): # issues use liqidity for now
        """Calculate bonus for sustained price growth"""
        if self.last_recorded_price <= 0:
            return 0
            
        growth_ratio = float(self.coin.current_price / self.last_recorded_price)
        # Reward gradual growth (50-300% growth)
        if 1.5 <= growth_ratio <= 4.0: # wrong + 1.5 and above
            return 50
        # Smaller bonus for moderate growth
        # elif 1.2 <= growth_ratio < 1.5: # remove
        #     return 25
        return 0

    def _calculate_retention_bonus(self): # check this properly # this wrong
        """Calculate bonus for holder retention"""
        if self.last_recorded_holders <= 0:
            return 0
            
        current_holders = self.holders_count
        retention_rate = current_holders / self.last_recorded_holders
        # were else is it been checked
        # Bonus for maintaining or growing holder base
        if retention_rate >= 1.1:  # 10% growth
            self.holder_retention_months += 1
            return min(self.holder_retention_months * 10, 100)
        elif retention_rate >= 0.9:  # Stable within 10%
            return 20
        return 0
    
    def _check_pump_and_dump(self, save=True): # fix
        if (self.pump_and_dump_activity or 
            self.age_in_hours >= (30 * 24)):  # After 3 months
            return
        
        # calculate pump and dump

        if self.pump_and_dump_activity and save:
            self.score = max(0, self.score - 100)
            self.save(update_fields=[
                'pump_and_dump_activity', 'score', 'updated_at'
            ])

    def _calculate_holder_rank_bonus(self):
        """Calculate bonus based on holder quality (rank distribution)"""
        if self.holders_count == 0:
            return 0
        
        # Get holders with trader scores
        holders_with_scores = self.coin.holders.select_related('user__trader_score')
        
        rank_counts = {3: 0, 4: 0, 5: 0}
        total_ranked = 0
        
        for holding in holders_with_scores:
            if hasattr(holding.user, 'trader_score'):
                rank = holding.user.trader_score.rank
                if rank in rank_counts:
                    rank_counts[rank] += 1
                    total_ranked += 1
        
        if total_ranked == 0:
            return 0
        
        # Calculate percentages
        rank_3_pct = rank_counts[3] / total_ranked
        rank_4_pct = rank_counts[4] / total_ranked
        rank_5_pct = rank_counts[5] / total_ranked
        
        # Award bonuses for high-quality holder concentrations
        # if rank_5_pct > 0.3:  # 30%+ rank 5 holders
        #     return 50
        # elif rank_4_pct > 0.4:  # 40%+ rank 4 holders
        #     return 30
        # elif rank_3_pct > 0.5:  # 50%+ rank 3 holders
        #     return 20
        if rank_5_pct > 0.5:
            return 50
        elif rank_4_pct > 0.5:
            return 30
        elif rank_3_pct > 0.5:
            return 20
        return 0

    def _check_dev_dumping(self, save=True):
        """Check if developer has dumped their tokens early"""
        if (self.team_abandonment or 
            self.age_in_hours >= (30 * 24 * 3)):  # After 3 months
            return
        
        try:
            dev_holding = self.coin.holders.get(
                user__wallet_address=self.coin.creator.wallet_address
            )
            dev_percentage = dev_holding.held_percentage()
            
            # Flag as abandoned if dev holds less than 1%
            if dev_percentage < 1.0:
                self.team_abandonment = True
                self.score = max(0, self.score - 100)
                if save:
                    self.save(update_fields=[
                        'team_abandonment', 'score', 'updated_at'
                    ])
        except self.coin.holders.model.DoesNotExist: # hmm
            # Dev has no holdings - definitely abandoned
            self.team_abandonment = True
            self.score = max(0, self.score - 100)
            if save:
                self.save(update_fields=[
                    'team_abandonment', 'score', 'updated_at'
                ])

    def _check_token_abandonment(self, save=True): # inactivity for 2 weeks a little to on good trades # this is sell numbers not acutal amounts
        """Check if token shows signs of abandonment (low activity)"""
        if (self.token_abandonment or 
            self.age_in_hours >= (30 * 24)):  # After 1 month
            return
        
        # Get trade statistics
        total_trades = self.coin.trades.count()
        sell_trades = self.coin.trades.filter(trade_type='SELL').count()
        
        # Token is considered abandoned if:
        # 1. Very few trades (< 20) after reasonable time, OR
        # 2. Sell ratio is too high (> 70%) indicating dump 
        if total_trades < 20 and self.age_in_hours > (7 * 24):  # After 1 week
            self.token_abandonment = True
            self.score = max(0, self.score - 200)
        elif total_trades >= 20 and (sell_trades / total_trades) > 0.7:
            self.token_abandonment = True
            self.score = max(0, self.score - 200)
        
        if self.token_abandonment and save:
            self.save(update_fields=[
                'token_abandonment', 'score', 'updated_at'
            ])

    def _apply_daily_score_adjustments(self):
        """Apply daily volume and activity bonuses"""
        fields = ['score', 'updated_at']
        if self.max_volume_recorded < 100:
            volume_data = self.coin.trades.all().aggregate(
                total_volume=Sum('sol_amount')
            )
            volume_recorded = min(volume_data['total_volume'] or Decimal('0'), Decimal('100'))
            volume_bonus = 0
            # Update max volume if exceeded # nonsense
            if self.max_volume_recorded > volume_recorded:
                volume_bonus = volume_recorded - self.max_volume_recorded
                self.max_volume_recorded = volume_recorded
            # Apply bonus
            self.score = max(0, self.score + int(volume_bonus))
            fields = ['score', 'max_volume_recorded', 'updated_at']
        self.save(update_fields=fields)

    def _reset_monthly_counters(self):
        """Reset counters for the new month"""
        self.price_breakouts_per_month = 0
        self.last_recorded_price = self.coin.current_price
        self.last_recorded_holders = self.holders_count

    def recalculate_score(self):
        """Main entry point for score recalculation"""
        # Ensure we have fresh data
        self.update_age(save=False)
        self.update_holders_count(save=False)
        
        # Apply daily checks if needed
        now = timezone.now()
        if (not self.last_daily_update or 
            self.last_daily_update.date() != now.date()):
            self.daily_checkup()
        
        # Apply bi-weekly checks if needed
        if (not self.last_biweekly_update or 
            not self._is_same_biweekly_period(self.last_biweekly_update, now)):
            self.biweekly_checkup()

        # Apply monthly recalculation if needed
        if (not self.last_monthly_update or 
            self.last_monthly_update.month != now.month or
            self.last_monthly_update.year != now.year):
            self.monthly_recalculation()
        
        return self.score

class DeveloperScore(DRCScore):
    """
    Developer reputation score tracking for Solana users who create coins
    """
    developer = models.OneToOneField(
        SolanaUser,
        on_delete=models.CASCADE,
        related_name='developer_score',
        to_field="wallet_address"
    )
    
    # new meteric
    successful_launch = models.IntegerField(default=0) # +100 
    abandoned_projects = models.IntegerField(default=0) # -150 # check in drs score if the token is adandoned
    rug_pull_or_sell_off = models.IntegerField(default=0) # -100 no rug pull + 100 how to check rug pull - coin count

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
        
        # Calculate final score with clamping
        total_score = base_score
        self.score = max(total_score, 200)  # Clamp between 200-1000
        
        self.save()
        return self.score

class TraderScore(DRCScore): # work on it tommorow
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
    profitable_trades_percent = models.FloatField(default=0, # for fancy
                                                 validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # new meterics
    held_tokens_per_month =models.IntegerField(default=0)
    # increase portfolio
    quick_pump_and_dumps_count = models.IntegerField(default=0)
    sniping_and_dumps_count = models.IntegerField(default=0)

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

class CoinRugFlag(models.Model): # remove if they decide a detailed logs might not be needed
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
