from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count

from ...models import (
    SolanaUser, Coin, Trade,
    DeveloperScore, TraderScore, CoinDRCScore
)

class Command(BaseCommand):
    help = 'Initialize DRC scores for all users and coins'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recalculation of existing scores',
        )

    def handle(self, *args, **options):
        force = options['force']
        self.stdout.write(self.style.SUCCESS('Initializing DRC scores...'))
        
        # Get counts
        user_count = SolanaUser.objects.count()
        coin_count = Coin.objects.count()
        
        self.stdout.write(f"Found {user_count} users and {coin_count} coins")
        
        # Initialize developer scores
        self.initialize_developer_scores(force)
        
        # Initialize trader scores
        self.initialize_trader_scores(force)
        
        # Initialize coin scores
        self.initialize_coin_scores(force)
        
        self.stdout.write(self.style.SUCCESS('DRC score initialization complete!'))
    
    def initialize_developer_scores(self, force):
        """Initialize developer scores for all users with coins"""
        # Get users who have created coins
        developers = SolanaUser.objects.annotate(
            coins_count=Count('coins')
        ).filter(coins_count__gt=0)
        
        self.stdout.write(f"Initializing scores for {developers.count()} developers...")
        
        created_count = 0
        updated_count = 0
        
        for developer in developers:
            # Check if score exists
            dev_score, created = DeveloperScore.objects.get_or_create(developer=developer)
            
            if created:
                created_count += 1
            elif force:
                updated_count += 1
            else:
                continue  # Skip if not forcing update
                
            # Recalculate score
            dev_score.recalculate_score()
        
        self.stdout.write(self.style.SUCCESS(
            f"Developer scores: {created_count} created, {updated_count} updated"
        ))
    
    def initialize_trader_scores(self, force):
        """Initialize trader scores for all users with trades"""
        # Get users who have made trades
        traders = SolanaUser.objects.annotate(
            trades_count=Count('trades')
        ).filter(trades_count__gt=0)
        
        self.stdout.write(f"Initializing scores for {traders.count()} traders...")
        
        created_count = 0
        updated_count = 0
        
        for trader in traders:
            # Check if score exists
            trader_score, created = TraderScore.objects.get_or_create(trader=trader)
            
            if created:
                created_count += 1
            elif force:
                updated_count += 1
            else:
                continue  # Skip if not forcing update
                
            # Recalculate score
            trader_score.recalculate_score()
        
        self.stdout.write(self.style.SUCCESS(
            f"Trader scores: {created_count} created, {updated_count} updated"
        ))
    
    def initialize_coin_scores(self, force):
        """Initialize DRC scores for all coins"""
        coins = Coin.objects.all()
        
        self.stdout.write(f"Initializing scores for {coins.count()} coins...")
        
        created_count = 0
        updated_count = 0
        
        for coin in coins:
            # Check if score exists
            coin_score, created = CoinDRCScore.objects.get_or_create(coin=coin)
            
            if created:
                created_count += 1
            elif force:
                updated_count += 1
            else:
                continue  # Skip if not forcing update
            
            # Update basic metrics
            coin_score.update_age()
            coin_score.update_holders_count()
            
            # Calculate trade volume in last 24h
            one_day_ago = timezone.now() - timezone.timedelta(hours=24)
            recent_trades = Trade.objects.filter(
                coin=coin,
                created_at__gte=one_day_ago
            )
            
            if recent_trades.exists():
                volume = sum(t.sol_amount for t in recent_trades)
                coin_score.trade_volume_24h = volume
                coin_score.save(update_fields=['trade_volume_24h'])
            
            # Set verified contract status based on coin model
            # coin_score.verified_contract = coin.contract_verified
            # coin_score.save(update_fields=['verified_contract'])
            
            # Recalculate score
            coin_score.recalculate_score()
        
        self.stdout.write(self.style.SUCCESS(
            f"Coin scores: {created_count} created, {updated_count} updated"
        ))