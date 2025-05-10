from rest_framework import serializers
from .models import (
    DeveloperScore, 
    TraderScore, 
    CoinDRCScore, 
    CoinRugFlag,
    SolanaUser,
    Coin,
    UserCoinHoldings, Trade,
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolanaUser
        fields = ['wallet_address', 'display_name', 'bio']#, 'is_staff']
        read_only_fields = ['wallet_address']#, 'is_staff']

class SolanaUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolanaUser
        fields = ['wallet_address', 'display_name', 'bio']

    def create(self, validated_data):
        return SolanaUser.objects.create_user(**validated_data)

class SolanaUserLoginSerializer(serializers.Serializer):
    wallet_address = serializers.CharField()

    def validate(self, data):
        wallet = data.get("wallet_address", "")
        try:
            user = SolanaUser.objects.get(wallet_address=wallet)
        except SolanaUser.DoesNotExist:
            raise serializers.ValidationError("Wallet address not registered")

        data['user'] = user
        return data

class CoinSerializer(serializers.ModelSerializer):
    creator_display_name = serializers.ReadOnlyField(source='creator.display_name')
    
    class Meta:
        model = Coin
        fields = [
            'address', 'ticker', 'name', 'creator', 'creator_display_name',
            'created_at', 'total_supply', 'image_url',
            'description', 'telegram', 'website', 'twitter',
            'current_price', 'total_held', 'market_cap'
        ]
        read_only_fields = ['address', 'creator', 'creator_display_name', 'created_at']

class UserCoinHoldingsSerializer(serializers.ModelSerializer):
    coin_ticker = serializers.ReadOnlyField(source='coin.ticker')
    coin_name = serializers.ReadOnlyField(source='coin.name')
    current_price = serializers.ReadOnlyField(source='coin.current_price')
    value = serializers.SerializerMethodField()
    
    class Meta:
        model = UserCoinHoldings
        fields = ['user', 'coin', 'coin_ticker', 'coin_name', 'amount_held', 'current_price', 'value']
        read_only_fields = ['user', 'value']
    
    def get_value(self, obj):
        """Calculate the current value of the holdings"""
        return obj.amount_held * obj.coin.current_price

class TradeSerializer(serializers.ModelSerializer):
    coin_symbol = serializers.ReadOnlyField(source='coin.ticker')
    trade_type_display = serializers.SerializerMethodField()
   
    class Meta:
        model = Trade
        fields = [
            'transaction_hash', 'user', 'coin', 'coin_symbol', 'trade_type',
            'trade_type_display', 'coin_amount', 'sol_amount', 'created_at'
        ]
        read_only_fields = ['transaction_hash', 'user', 'created_at']
   
    def get_trade_type_display(self, obj):
        return obj.get_trade_type_display()
       
    def validate(self, data):
        """
        Validate the trade
        - For sells: check if user has enough coins
        - For buys: potentially check if there are enough coins available
        """
        if data['trade_type'] == 'SELL':  # If selling
            try:
                holdings = UserCoinHoldings.objects.get(
                    user=self.context['request'].user,
                    coin=data['coin']
                )
                if holdings.amount_held < data['coin_amount']:
                    raise serializers.ValidationError(
                        "Not enough coins to sell. You have {0} but are trying to sell {1}".format(
                            holdings.amount_held, data['coin_amount']
                        )
                    )
            except UserCoinHoldings.DoesNotExist:
                raise serializers.ValidationError("You don't own any of these coins to sell")
       
        return data

# drc
class DeveloperScoreSerializer(serializers.ModelSerializer):
    developer_address = serializers.CharField(source='developer.wallet_address', read_only=True)
    
    class Meta:
        model = DeveloperScore
        fields = [
            'developer_address', 'score', 'coins_created_count', 
            'coins_active_24h_plus', 'coins_rugged_count', 
            'highest_market_cap', 'created_at', 'updated_at'
        ]

class TraderScoreSerializer(serializers.ModelSerializer):
    trader_address = serializers.CharField(source='trader.wallet_address', read_only=True)
    
    class Meta:
        model = TraderScore
        fields = [
            'trader_address', 'score', 'coins_held_count', 
            'avg_holding_time_hours', 'trades_count', 
            'quick_dumps_count', 'profitable_trades_percent',
            'created_at', 'updated_at'
        ]

class CoinDRCScoreSerializer(serializers.ModelSerializer):
    coin_address = serializers.CharField(source='coin.address', read_only=True)
    coin_name = serializers.CharField(source='coin.name', read_only=True)
    coin_symbol = serializers.CharField(source='coin.ticker', read_only=True)
    developer_score = serializers.SerializerMethodField()
    score_breakdown = serializers.SerializerMethodField()
    is_rugged = serializers.SerializerMethodField()
    
    class Meta:
        model = CoinDRCScore
        fields = [
            'coin_address', 'coin_name', 'coin_symbol', 'score', 
            'holders_count', 'age_in_hours', 'trade_volume_24h',
            'price_stability_score', 'verified_contract', 
            'audit_completed', 'audit_score', 'developer_score',
            'score_breakdown', 'is_rugged', 'created_at', 'updated_at'
        ]
    
    def get_developer_score(self, obj):
        try:
            return obj.coin.creator.developer_score.score
        except Exception:
            return 200  # Default score
    
    def get_score_breakdown(self, obj):
        return obj.score_breakdown
    
    def get_is_rugged(self, obj):
        try:
            return obj.coin.rug_flag.is_rugged
        except Exception:
            return False

class CoinRugFlagSerializer(serializers.ModelSerializer):
    coin_address = serializers.CharField(source='coin.address', read_only=True)
    coin_name = serializers.CharField(source='coin.name', read_only=True)
    
    class Meta:
        model = CoinRugFlag
        fields = [
            'coin_address', 'coin_name', 'is_rugged', 
            'rugged_at', 'rug_transaction', 'rug_description'
        ]
