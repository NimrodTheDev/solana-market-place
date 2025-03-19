from rest_framework import serializers
from .models import SolanaUser, Coin, UserCoinHoldings, Trade

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolanaUser
        fields = ['wallet_address', 'display_name', 'bio', 'is_staff']
        read_only_fields = ['wallet_address', 'is_staff']

class CoinSerializer(serializers.ModelSerializer):
    creator_display_name = serializers.ReadOnlyField(source='creator.display_name')
    
    class Meta:
        model = Coin
        fields = [
            'address', 'symbol', 'name', 'creator', 'creator_display_name',
            'created_at', 'total_supply', 'image_url',
            'description', 'telegram', 'website', 'twitter',
            'current_price', 'total_held', 'market_cap'
        ]
        read_only_fields = ['address', 'creator', 'creator_display_name', 'created_at']

class UserCoinHoldingsSerializer(serializers.ModelSerializer):
    coin_symbol = serializers.ReadOnlyField(source='coin.symbol')
    coin_name = serializers.ReadOnlyField(source='coin.name')
    current_price = serializers.ReadOnlyField(source='coin.current_price')
    value = serializers.SerializerMethodField()
    
    class Meta:
        model = UserCoinHoldings
        fields = ['user', 'coin', 'coin_symbol', 'coin_name', 'amount_held', 'current_price', 'value']
        read_only_fields = ['user', 'value']
    
    def get_value(self, obj):
        """Calculate the current value of the holdings"""
        return obj.amount_held * obj.coin.current_price

class TradeSerializer(serializers.ModelSerializer):
    coin_symbol = serializers.ReadOnlyField(source='coin.symbol')
    trade_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Trade
        fields = [
            'id', 'user', 'coin', 'coin_symbol', 'trade_type', 
            'trade_type_display', 'coin_amount', 'sol_amount', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
    
    def get_trade_type_display(self, obj):
        return "Buy" if obj.trade_type else "Sell"
        
    def validate(self, data):
        """
        Validate the trade
        - For sells: check if user has enough coins
        - For buys: potentially check if there are enough coins available
        """
        if not data['trade_type']:  # If selling
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