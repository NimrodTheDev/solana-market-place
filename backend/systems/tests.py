from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from django.db import IntegrityError
from .models import SolanaUser, Coin, CoinDRCScore, UserCoinHoldings, Trade, DeveloperScore


class CoinDRCScoreTestCase(TestCase):
    """Test cases for CoinDRCScore model"""

    def setUp(self):
        """Set up test data"""
        # Create test users
        self.creator = SolanaUser.objects.create_user(
            wallet_address="1234567890123456789012345678901234567890123",
            display_name="Test Creator"
        )
        
        self.trader1 = SolanaUser.objects.create_user(
            wallet_address="2234567890123456789012345678901234567890123",
            display_name="Trader 1"
        )
        
        self.trader2 = SolanaUser.objects.create_user(
            wallet_address="3234567890123456789012345678901234567890123",
            display_name="Trader 2"
        )
        # Create test coin
        self.coin = Coin.objects.create(
            address="COIN123456789012345678901234567890123456789",
            name="Test Coin",
            creator=self.creator,
            total_supply=Decimal('1000000'),
            image_url="https://example.com/image.png",
            ticker="TEST",
            description="A test coin",
            current_price=Decimal('0.001')
        )

    # def test_coin_drc_score_creation(self):
    #     """Test creating a CoinDRCScore instance"""
    #     drc_score, _ = CoinDRCScore.objects.get_or_create(coin=self.coin)
        
    #     self.assertEqual(drc_score.score, 200)  # Default score
    #     self.assertEqual(drc_score.coin, self.coin)
    #     self.assertEqual(drc_score.holders_count, 0)
    #     self.assertEqual(drc_score.age_in_hours, 0)
    #     self.assertEqual(drc_score.trade_volume_24h, Decimal('0'))
    #     self.assertFalse(drc_score.team_abandonment)
    #     self.assertFalse(drc_score.token_abandonment)

    # def test_rank_property(self):
    #     """Test the rank property calculation"""
    #     drc_score, _ = CoinDRCScore.objects.get_or_create(coin=self.coin)
        
    #     # Test different score ranges
    #     drc_score.score = 100
    #     self.assertEqual(drc_score.rank, 1)
        
    #     drc_score.score = 300
    #     self.assertEqual(drc_score.rank, 2)
        
    #     drc_score.score = 750
    #     self.assertEqual(drc_score.rank, 3)
        
    #     drc_score.score = 1500
    #     self.assertEqual(drc_score.rank, 4)
        
    #     drc_score.score = 2500
    #     self.assertEqual(drc_score.rank, 5)

    # def test_update_age(self):
    #     """Test age calculation functionality"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
        
    #     # Mock the coin's created_at to be 5 hours ago
    #     five_hours_ago = timezone.now() - timedelta(hours=5)
    #     self.coin.created_at = five_hours_ago
    #     self.coin.save()
        
    #     age = drc_score.update_age()
        
    #     # Should be approximately 5 hours (allowing for small time differences)
    #     self.assertGreaterEqual(age, 4)
    #     self.assertLessEqual(age, 6)
    #     self.assertEqual(drc_score.age_in_hours, age)

    # def test_update_holders_count(self):
    #     """Test holders count update"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
        
    #     # Initially no holders
    #     count = drc_score.update_holders_count()
    #     self.assertEqual(count, 0)
        
    #     Trade.objects.create(
    #         transaction_hash = "32345678901678901234567890123478901234567890134567890123",
    #         user=self.trader1,
    #         coin=self.coin,
    #         coin_amount = 1000,
    #         sol_amount = 2,
    #         trade_type = "BUY",
    #     )

    #     Trade.objects.create(
    #         transaction_hash = "323456789016732345678901234567890123456789012534567890123",
    #         user=self.trader2,
    #         coin=self.coin,
    #         coin_amount = 500,
    #         sol_amount = 2,
    #         trade_type = "BUY",
    #     )
    #     # never directly create holding
    #     count = drc_score.update_holders_count()
    #     self.assertEqual(count, 2)
    #     self.assertEqual(drc_score.holders_count, 2)

    # def test_update_price_breakouts(self):
    #     """Test price breakout detection"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
        
    #     # Test no breakout (less than 10% change)
    #     initial_breakouts = drc_score.price_breakouts_per_month
    #     drc_score.update_price_breakouts(Decimal('1.0'), Decimal('1.05'))  # 5% change
    #     self.assertEqual(drc_score.price_breakouts_per_month, initial_breakouts)
        
    #     # Test breakout (more than 10% change)
    #     drc_score.update_price_breakouts(Decimal('1.0'), Decimal('1.15'))  # 15% change
    #     self.assertEqual(drc_score.price_breakouts_per_month, initial_breakouts + 1)
        
    #     # Test negative breakout
    #     drc_score.update_price_breakouts(Decimal('1.0'), Decimal('0.8'))  # 20% drop
    #     self.assertEqual(drc_score.price_breakouts_per_month, initial_breakouts + 2)

    # def test_check_dev_dumping(self): # it should check the devs amount
    #     """Test developer dumping detection"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
    #     initial_score = drc_score.score 

    #     Trade.objects.create(
    #         transaction_hash="HASH2234567890123456789012345678901234567890123456789012345678901234567890",
    #         user=self.creator,
    #         coin=self.coin,
    #         trade_type='COIN_CREATE',
    #         coin_amount=Decimal('5000'),
    #         sol_amount=Decimal('5'),
    #     )
        
    #     drc_score._check_dev_dumping()
        
    #     # Should flag as team abandonment and reduce score
    #     self.assertTrue(drc_score.team_abandonment)
    #     self.assertEqual(drc_score.score, initial_score - 100)

    # def test_check_dev_dumping_no_holdings(self):
    #     """Test developer dumping when dev has no holdings"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
    #     initial_score = drc_score.score
        
    #     # No holdings for the creator
    #     drc_score._check_dev_dumping()
        
    #     # Should flag as team abandonment
    #     self.assertTrue(drc_score.team_abandonment)
    #     self.assertEqual(drc_score.score, initial_score - 100)

    # def test_check_token_abandonment_low_trades(self):
    #     """Test token abandonment detection with low trade count"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
        
    #     # Set age to more than 1 week
    #     drc_score.age_in_hours = 8 * 24  # 8 days
        
    #     # Create very few trades (< 20)
    #     for i in range(5):
    #         Trade.objects.create(
    #             transaction_hash=f"HASH{i}234567890123456789012345678901234567890123456789012345678901234567890",
    #             user=self.trader1,
    #             coin=self.coin,
    #             trade_type='BUY',
    #             coin_amount=Decimal('10'),
    #             sol_amount=Decimal('1')
    #         )
        
    #     initial_score = drc_score.score
    #     drc_score._check_token_abandonment()
        
    #     self.assertTrue(drc_score.token_abandonment)
    #     self.assertEqual(drc_score.score, initial_score - 200)

    # def test_check_token_abandonment_high_sell_ratio(self):
    #     """Test token abandonment detection with high sell ratio"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
    #     initial_score = drc_score.score
        
    #     # Create trades with high sell ratio (>70%)
    #     # 8 sell trades, 2 buy trades = 80% sell ratio
    #     for i in range(8*2):
    #         Trade.objects.create(
    #             transaction_hash=f"SELL{i}234567890123456789012345678901234567890123456789012345678901234567890",
    #             user=self.trader1,
    #             coin=self.coin,
    #             trade_type='SELL',
    #             coin_amount=Decimal('10'),
    #             sol_amount=Decimal('1')
    #         )
        
    #     for i in range(2*2):
    #         Trade.objects.create(
    #             transaction_hash=f"BUY{i}2345678901234567890123456789012345678901234567890123456789012345678901",
    #             user=self.trader2,
    #             coin=self.coin,
    #             trade_type='BUY',
    #             coin_amount=Decimal('10'),
    #             sol_amount=Decimal('1')
    #         )
        
    #     drc_score._check_token_abandonment()
        
    #     self.assertTrue(drc_score.token_abandonment)
    #     self.assertEqual(drc_score.score, initial_score - 200)

    # def test_calculate_fair_trading_bonus(self):
    #     """Test fair trading bonus calculation"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
        
    #     # Low breakouts should give bonus
    #     drc_score.price_breakouts_per_month = 3
    #     bonus = drc_score._calculate_fair_trading_bonus()
    #     self.assertEqual(bonus, 50)
        
    #     # High breakouts should give no bonus
    #     drc_score.price_breakouts_per_month = 10
    #     bonus = drc_score._calculate_fair_trading_bonus()
    #     self.assertEqual(bonus, 0)

    # def test_str_method(self):
    #     """Test string representation"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
    #     expected_str = f"DRC Score for {self.coin.name}: {drc_score.score}"
    #     self.assertEqual(str(drc_score), expected_str)

    # def test_one_to_one_relationship(self):
    #     """Test that each coin can only have one DRC score"""
    #     CoinDRCScore.objects.get(coin=self.coin)
        
    #     # Attempting to create another should raise IntegrityError
    #     with self.assertRaises(IntegrityError):
    #         CoinDRCScore.objects.create(coin=self.coin)

    # def test_reset_monthly_counters(self):
    #     """Test monthly counter reset"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
        
    #     # Set some values
    #     drc_score.price_breakouts_per_month = 5
    #     drc_score.holders_count = 10
    #     self.coin.current_price = Decimal('2.0')
    #     self.coin.save()
        
    #     drc_score._reset_monthly_counters()
    #     self.assertEqual(drc_score.price_breakouts_per_month, 0)
    #     self.assertEqual(drc_score.last_recorded_price, self.coin.current_price)
    #     self.assertEqual(drc_score.last_recorded_holders, drc_score.holders_count)

    # def test_apply_daily_score_adjustments(self):
    #     """Test daily score adjustments"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
    #     initial_score = drc_score.score
        
    #     # Set trade volume
    #     drc_score.trade_volume_24h = Decimal('500')  # Should give 5 point bonus
    #     drc_score._apply_daily_score_adjustments()
        
    #     # Score should increase (5 for volume + 2 for activity = 7)
    #     self.assertEqual(drc_score.score, initial_score + 12)

    # def test_max_volume_record_bonus(self):
    #     """Test bonus for new volume records"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
    #     initial_score = drc_score.score
        
    #     # Set new record volume
    #     drc_score.trade_volume_24h = Decimal('1000')
    #     drc_score.max_volume_recorded = Decimal('500')  # Previous max
        
    #     drc_score._apply_daily_score_adjustments()
        
    #     # Should get volume bonus (10) + activity bonus (2) + record bonus (5) = 17
    #     self.assertEqual(drc_score.score, initial_score + 17)
    #     self.assertEqual(drc_score.max_volume_recorded, Decimal('1000'))

    # def test_score_bounds(self):
    #     """Test that score doesn't go below 0"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
    #     drc_score.score = 50  # Low score
        
    #     # Trigger both abandonment penalties
    #     drc_score.team_abandonment = True
    #     drc_score.token_abandonment = True
    #     drc_score.score = max(0, drc_score.score - 300)  # Simulate penalties
        
    #     self.assertGreaterEqual(drc_score.score, 0)

    # def test_daily_checkup(self):
    #     """Test daily checkup functionality"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
        
    #     # Mock the coin creation time
    #     self.coin.created_at = timezone.now() - timedelta(hours=25)
    #     self.coin.save()
        
    #     # Add some holdings and trades
    #     UserCoinHoldings.objects.create(
    #         user=self.trader1,
    #         coin=self.coin,
    #         amount_held=Decimal('1000')
    #     )
        
    #     Trade.objects.create(
    #         transaction_hash="DAILY123456789012345678901234567890123456789012345678901234567890123456789",
    #         user=self.trader1,
    #         coin=self.coin,
    #         trade_type='BUY',
    #         coin_amount=Decimal('100'),
    #         sol_amount=Decimal('10')
    #     )
        
    #     # Perform daily checkup
    #     drc_score.daily_checkup()
        
    #     # Verify updates
    #     self.assertGreater(drc_score.age_in_hours, 0)
    #     self.assertEqual(drc_score.holders_count, 1)
    #     self.assertEqual(drc_score.trade_volume_24h, Decimal('10'))
    #     self.assertIsNotNone(drc_score.last_daily_update)

    # errors
    # def test_update_trade_volume_24h(self): # faileed but not for normal reasons
    #     """Test 24h trade volume calculation"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
        
    #     # Create trades - some within 24h, some older
    #     now = timezone.now()
        
    #     # Trade within 24 hours
    #     Trade.objects.create(
    #         transaction_hash="HASH1234567890123456789012345678901234567890123456789012345678901234567890",
    #         user=self.trader1,
    #         coin=self.coin,
    #         trade_type='BUY',
    #         coin_amount=Decimal('100'),
    #         sol_amount=Decimal('10'),
    #         created_at=now - timedelta(hours=12)
    #     )
        
    #     # Another trade within 24 hours
    #     Trade.objects.create(
    #         transaction_hash="HASH2234567890123456789012345678901234567890123456789012345678901234567890",
    #         user=self.trader2,
    #         coin=self.coin,
    #         trade_type='SELL',
    #         coin_amount=Decimal('50'),
    #         sol_amount=Decimal('5'),
    #         created_at=now - timedelta(hours=6)
    #     )
        
    #     # Trade older than 24 hours (should be excluded)
    #     Trade.objects.create(
    #         transaction_hash="HASH3234567890123456789012345678901234567890123456789012345678901234567890",
    #         user=self.trader1,
    #         coin=self.coin,
    #         trade_type='BUY',
    #         coin_amount=Decimal('200'),
    #         sol_amount=Decimal('20'),
    #         created_at=now - timedelta(hours=30)
    #     )
        
    #     volume = drc_score.update_trade_volume_24h()
    #     # print(volume)
    #     # problem the 7 points dasheed just like that.
    #     self.assertEqual(volume, Decimal('15'))  # 10 + 5, excluding the 30h old trade

    # def test_calculate_price_growth_bonus(self): # wrong use liquidity instead, issues with saving
    #     """Test price growth bonus calculation"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
        
    #     # Test optimal growth (2x = 100% growth)
    #     drc_score.last_recorded_price = Decimal('1.0')
    #     self.coin.current_price = Decimal('2.0') # wrong
    #     self.coin.save()
    #     bonus = drc_score._calculate_price_growth_bonus()
    #     self.assertEqual(bonus, 50)

    #     # Test moderate growth (1.3x = 30% growth)
    #     self.coin.current_price = Decimal('1.3')
    #     self.coin.save()
    #     print(self.coin.current_price)
    #     bonus = drc_score._calculate_price_growth_bonus()
    #     self.assertEqual(bonus, 25)
        
    #     # Test excessive growth (10x = 900% growth)
    #     self.coin.current_price = Decimal('10.0')
    #     self.coin.save()
    #     bonus = drc_score._calculate_price_growth_bonus()
    #     self.assertEqual(bonus, 0)

    # def test_monthly_recalculation(self): # bonus no no check
    #     """Test monthly recalculation"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
    #     initial_score = drc_score.score

    #     Trade.objects.create(
    #         transaction_hash="HASH2234567890123456789012345678901234567890123456789012345678901234567890",
    #         user=self.creator,
    #         coin=self.coin,
    #         trade_type='BUY',
    #         coin_amount=Decimal('50000'),
    #         sol_amount=Decimal('50'),
    #     )
        
    #     # Set up conditions for bonuses
    #     drc_score.price_breakouts_per_month = 3  # Fair trading
    #     drc_score.last_recorded_price = Decimal('1.0')
    #     self.coin.current_price = Decimal('2.0')  # Good growth
        
    #     drc_score.monthly_recalculation()
        
    #     # Score should have increased due to bonuses
    #     self.assertGreater(drc_score.score, initial_score)
    #     self.assertIsNotNone(drc_score.last_monthly_update)
    #     self.assertEqual(drc_score.price_breakouts_per_month, 0)  # Reset

    def test_monthly_recalculation(self): # bonus no no check
        """Test monthly recalculation"""
        dev_score = DeveloperScore.objects.get(developer= self.creator) #self.creator.devscore
        drs_score = CoinDRCScore.objects.get(coin= self.coin)
        Trade.objects.create(
            transaction_hash="HASH2234567890123456789012345678901234567890123456789012345678901234567890",
            user=self.creator,
            coin=self.coin,
            trade_type='BUY',
            coin_amount=Decimal('200000'),
            sol_amount=Decimal('5000'),
        )
        Trade.objects.create(
            transaction_hash="HASH2634567890123456789012345678901234567890123456789012345678901234567890",
            user=self.creator,
            coin=self.coin,
            trade_type='BUY',
            coin_amount=Decimal('500000'),
            sol_amount=Decimal('5000'),
        )
        drs_score._calculate_retention_bonus()
        # dev_score.recalculate_score()
        print(dev_score.score)

    # def test_recalculate_score_integration(self): # nonsense
    #     """Test the main recalculate_score method"""
    #     drc_score = CoinDRCScore.objects.get(coin=self.coin)
        
    #     # Set up some test data
    #     self.coin.created_at = timezone.now() - timedelta(hours=48)
    #     self.coin.save()
        
    #     UserCoinHoldings.objects.create(
    #         user=self.trader1,
    #         coin=self.coin,
    #         amount_held=Decimal('1000')
    #     )
        
    #     Trade.objects.create(
    #         transaction_hash="RECALC12345678901234567890123456789012345678901234567890123456789012345678",
    #         user=self.trader1,
    #         coin=self.coin,
    #         trade_type='BUY',
    #         coin_amount=Decimal('100'),
    #         sol_amount=Decimal('10')
    #     )
        
    #     score = drc_score.recalculate_score()
        
    #     # Should return the current score
    #     self.assertEqual(score, drc_score.score)
    #     self.assertGreater(drc_score.age_in_hours, 0)
