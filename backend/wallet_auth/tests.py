# wallet_auth/tests.py

from decimal import Decimal
from django.test import TestCase
from wallet_auth.models import SolanaUser, Coin, UserCoinHoldings, Trade

class SolanaUserTest(TestCase):
    def test_create_normal_user(self):
        user = SolanaUser.objects.create_user(wallet_address="TestWalletAddress123")
        # self.assertEqual(len(user.wallet_address), 10) 
        self.assertEqual(user.wallet_address, "testwalletaddress123")  # should be lowercased
        self.assertFalse(user.has_usable_password())

    def test_create_superuser(self):
        user = SolanaUser.objects.create_superuser(wallet_address="AdminWalletAddress123", password="strongpass123")
        self.assertEqual(user.wallet_address, "adminwalletaddress123")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.has_usable_password())

    def test_get_display_name(self):
        user = SolanaUser.objects.create_user(wallet_address="wallet123", display_name="CoolUser")
        self.assertEqual(user.get_display_name(), "CoolUser")
        user_no_name = SolanaUser.objects.create_user(wallet_address="wallet456")
        self.assertEqual(user_no_name.get_display_name(), "wallet456")

class CoinTest(TestCase):
    def test_create_coin(self):
        creator = SolanaUser.objects.create_user(wallet_address="creatorwallet")
        coin = Coin.objects.create(
            address="coinaddress123",
            name="Test Coin",
            creator=creator,
            total_supply=Decimal("1000.00"),
            current_price=Decimal("2.50"),
            ticker="tst"
        )
        self.assertEqual(coin.ticker, "TST")  # Should be uppercased
        self.assertEqual(coin.market_cap, Decimal("2500.00"))  # 1000 supply * $2.5 price

    def test_total_held_and_market_cap(self):
        creator = SolanaUser.objects.create_user(wallet_address="creatorwallet")
        user1 = SolanaUser.objects.create_user(wallet_address="userwallet1")
        user2 = SolanaUser.objects.create_user(wallet_address="userwallet2")
        
        coin = Coin.objects.create(
            address="coinaddress456",
            name="Held Coin",
            creator=creator,
            total_supply=Decimal("5000.00"),
            current_price=Decimal("1.00"),
            ticker="hld"
        )
        
        UserCoinHoldings.objects.create(user=user1, coin=coin, amount_held=Decimal("500"))
        UserCoinHoldings.objects.create(user=user2, coin=coin, amount_held=Decimal("1500"))
        
        self.assertEqual(coin.total_held, Decimal("2000"))
        self.assertEqual(coin.market_cap, Decimal("3000"))  # (5000 - 2000) * 1

class UserCoinHoldingsTest(TestCase):
    def test_user_coin_holdings(self):
        user = SolanaUser.objects.create_user(wallet_address="holderwallet")
        coin = Coin.objects.create(
            address="coinaddr789",
            name="Holder Coin",
            creator=user,
            total_supply=Decimal("1000.00"),
            current_price=Decimal("5.00"),
            ticker="hldr"
        )
        
        holdings = UserCoinHoldings.objects.create(user=user, coin=coin, amount_held=Decimal("100"))
        percentage = holdings.held_percentage()
        
        self.assertAlmostEqual(percentage, 10.00, places=2)  # 100 / 1000 * 100
        self.assertEqual(str(holdings), f"{user.wallet_address} holds {percentage} of {coin.ticker}")

class TradeTest(TestCase):
    def test_create_trade(self):
        user = SolanaUser.objects.create_user(wallet_address="traderwallet")
        coin = Coin.objects.create(
            address="coinaddrtrade",
            name="Trade Coin",
            creator=user,
            total_supply=Decimal("2000.00"),
            current_price=Decimal("0.50"),
            ticker="trd"
        )
        
        trade = Trade.objects.create(
            user=user,
            coin=coin,
            trade_type="BUY",
            coin_amount=Decimal("100"),
            sol_amount=Decimal("5")
        )
        
        self.assertEqual(trade.trade_type, "BUY")
        self.assertEqual(trade.coin_amount, Decimal("100"))
        self.assertEqual(trade.sol_amount, Decimal("5"))
        self.assertIn("Buy Trade by", str(trade))
