from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
import uuid
from datetime import timedelta
from unittest import mock

from .models import (
    SolanaUser,
    Coin,
    UserCoinHoldings,
    Trade,
    DeveloperScore,
    TraderScore,
    CoinDRCScore,
    CoinRugFlag,
    initialize_drc_system
)

# class CoinDRCScoreTests(TestCase):
#     """Tests for the CoinDRCScore model"""

#     def setUp(self):
#         self.creator = SolanaUser.objects.create_user(
#             wallet_address="8xdf6UGnJKEZzL8XnTT8qTzVNJqL9Zwx5bYDnF4bQEDK"
#         )
#         # Create developer score
#         self.dev_score = DeveloperScore.objects.create(
#             developer=self.creator,
#             score=500  # Medium developer score
#         )
        
#         # Create a coin
#         self.coin = Coin.objects.create(
#             address="TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
#             name="Test Coin",
#             creator=self.creator,
#             total_supply=Decimal("1000000.0"),
#             image_url="https://example.com/coin.png",
#             ticker="TEST",
#             current_price=Decimal("1.0")
#         )
        
#         # Create rug flag (not rugged)
#         self.rug_flag = CoinRugFlag.objects.create(
#             coin=self.coin,
#             is_rugged=False
#         )
        
#         # Create coin DRC score
#         self.coin_score = CoinDRCScore.objects.create(
#             coin=self.coin,
#             price_stability_score=70,  # Good stability
#             verified_contract=True,    # Contract is verified
#             audit_completed=True,      # Audit completed
#             audit_score=80             # Good audit score
#         )

#     def test_update_age(self): # doesn't work
#         """Test updating the age of the coin"""
#         # Set coin creation time to 48 hours ago
#         two_days_ago = timezone.now() - timedelta(hours=48)
#         Coin.objects.filter(address=self.coin.address).update(created_at=two_days_ago)
#         age_hours = self.coin_score.update_age()
        
#         # Age should be approximately 48 hours
#         self.assertAlmostEqual(age_hours, 48, delta=1)

#     def test_update_holders_count(self):
#         """Test updating the holders count"""
#         # Create two holders
#         holder1 = SolanaUser.objects.create_user(
#             wallet_address="5MYGMMafYr7G3aw8qUJKmvea4oLfVCSSZb7iEEXRFD5"
#         )
#         holder2 = SolanaUser.objects.create_user(
#             wallet_address="J6JZMDxUHvh7XyHx3zxbHhDNPGEDyaKFmTk9NE7zJCR"
#         )
        
#         UserCoinHoldings.objects.create(
#             user=holder1,
#             coin=self.coin,
#             amount_held=Decimal("1000.0")
#         )
        
#         UserCoinHoldings.objects.create(
#             user=holder2,
#             coin=self.coin,
#             amount_held=Decimal("2000.0")
#         )
        
#         holders_count = self.coin_score.update_holders_count()
        
#         self.assertEqual(holders_count, 2)

#     def test_recalculate_score(self):
#         """Test recalculating the DRC score"""
#         # Set up test conditions
#         two_days_ago = timezone.now() - timedelta(hours=48)
#         Coin.objects.filter(address=self.coin.address).update(created_at=two_days_ago) # doesn't work
        
#         # Create two holders
#         holder1 = SolanaUser.objects.create_user(
#             wallet_address="5MYGMMafYr7G3aw8qUJKmvea4oLfVCSSZb7iEEXRFD5"
#         )
#         holder2 = SolanaUser.objects.create_user(
#             wallet_address="J6JZMDxUHvh7XyHx3zxbHhDNPGEDyaKFmTk9NE7zJCR"
#         )
        
#         UserCoinHoldings.objects.create(
#             user=holder1,
#             coin=self.coin,
#             amount_held=Decimal("1000.0")
#         )
        
#         UserCoinHoldings.objects.create(
#             user=holder2,
#             coin=self.coin,
#             amount_held=Decimal("2000.0")
#         )
        
#         # Set 24h volume
#         self.coin_score.trade_volume_24h = Decimal("5000.0")
#         self.coin_score.save()
        
#         score = self.coin_score.recalculate_score()
        
#         # Score should include:
#         # - Age factor: min(48/24, 10) * 20 = 40
#         # - Holder factor: min(2, 200) / 2 = 1
#         # - Volume factor: min(5000, 1000) / 10 = 100
#         # - Contract bonus: 50
#         # - Audit bonus: 80 / 2 = 40
#         # - Dev factor: 500 * 0.2 = 100
#         # - Stability factor: 70 / 2 = 35
#         # - No rug penalty
#         # Total: ~366
#         self.assertGreater(score, 350)

#     def test_score_breakdown(self):
#         """Test the score breakdown method"""
#         # Set up test conditions
#         two_days_ago = timezone.now() - timedelta(hours=48)
#         Coin.objects.filter(address=self.coin.address).update(created_at=two_days_ago)
#         self.coin_score.update_age()
        
#         # Create a holder
#         holder = SolanaUser.objects.create_user(
#             wallet_address="5MYGMMafYr7G3aw8qUJKmvea4oLfVCSSZb7iEEXRFD5"
#         )
        
#         UserCoinHoldings.objects.create(
#             user=holder,
#             coin=self.coin,
#             amount_held=Decimal("1000.0")
#         )
        
#         self.coin_score.update_holders_count()
        
#         # Get the breakdown
#         breakdown = self.coin_score.score_breakdown
        
#         # Check that all components are present
#         self.assertIn('age_factor', breakdown)
#         self.assertIn('holder_factor', breakdown)
#         self.assertIn('volume_factor', breakdown)
#         self.assertIn('contract_verified', breakdown)
#         self.assertIn('audit_bonus', breakdown)
#         self.assertIn('dev_reputation', breakdown)
#         self.assertIn('stability_factor', breakdown)
#         self.assertIn('rug_penalty', breakdown)
#         self.assertIn('total', breakdown)
        
#         # Check that contract_verified is 50 (as set in setUp)
#         self.assertEqual(breakdown['contract_verified'], 50)
        
#         # Check that the total matches the score
#         self.assertEqual(breakdown['total'], self.coin_score.score)


class CoinRugFlagTests(TestCase):
    """Tests for the CoinRugFlag model"""

    def setUp(self):
        self.creator = SolanaUser.objects.create_user(
            wallet_address="8xdf6UGnJKEZzL8XnTT8qTzVNJqL9Zwx5bYDnF4bQEDK"
        )
        # Create developer score
        self.dev_score = DeveloperScore.objects.create(
            developer=self.creator,
            score=500  # Medium developer score
        )
        
        # Create a coin
        self.coin = Coin.objects.create(
            address="TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
            name="Test Coin",
            creator=self.creator,
            total_supply=Decimal("1000000.0"),
            image_url="https://example.com/coin.png",
            ticker="TEST"
        )
        
        # Create coin DRC score
        self.coin_score = CoinDRCScore.objects.create(
            coin=self.coin
        )