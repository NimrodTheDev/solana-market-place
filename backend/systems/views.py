from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Coin, UserCoinHoldings, Trade, SolanaUser
from .serializers import (
    CoinSerializer, 
    UserCoinHoldingsSerializer, 
    TradeSerializer, 
    UserSerializer
)

User = get_user_model()

class CoinViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Coins
    """
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'address'
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    @action(detail=True, methods=['get'])
    def holders(self, request, address=None):
        """Get all holders of a specific coin"""
        coin = self.get_object()
        holders = coin.holders.all()
        serializer = UserCoinHoldingsSerializer(holders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def trades(self, request, address=None):
        """Get all trades for a specific coin"""
        coin = self.get_object()
        trades = coin.trades.all()
        serializer = TradeSerializer(trades, many=True)
        return Response(serializer.data)

class UserCoinHoldingsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for User Coin Holdings
    """
    queryset = UserCoinHoldings.objects.all()
    serializer_class = UserCoinHoldingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter to only show the current user's holdings unless staff"""
        if self.request.user.is_staff:
            return UserCoinHoldings.objects.all()
        return UserCoinHoldings.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set user to current authenticated user"""
        serializer.save(user=self.request.user)

class TradeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Trades
    """
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Will change to ReadOnly later
    lookup_field = 'id'  # Should eventually be changed to transaction_hash
    
    def perform_create(self, serializer):
        """Set user to current authenticated user"""
        serializer.save(user=self.request.user)
        
        # Update holdings after a trade
        coin = serializer.validated_data['coin']
        amount = serializer.validated_data['coin_amount']
        trade_type = serializer.validated_data['trade_type']
        
        # Get or create holdings for this user and coin
        holdings, created = UserCoinHoldings.objects.get_or_create(
            user=self.request.user,
            coin=coin,
            defaults={'amount_held': 0}
        )
        
        # Update holdings based on trade type
        if trade_type in ['BUY', 'COIN_CREATE']:
            holdings.amount_held += amount
        elif trade_type == 'SELL':
            if holdings.amount_held < amount:
                raise serializer.ValidationError("Not enough coins to sell")
            holdings.amount_held -= amount
            
        holdings.save()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Solana Users
    """
    queryset = SolanaUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'wallet_address'
    
    @action(detail=True, methods=['get'])
    def holdings(self, request, wallet_address=None):
        """Get all coin holdings for a specific user"""
        user = self.get_object()
        # Check permissions - users can only see their own holdings
        if user.wallet_address != request.user.wallet_address and not request.user.is_staff:
            return Response(
                {"error": "You don't have permission to view this user's holdings"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        holdings = user.holdings.all()
        serializer = UserCoinHoldingsSerializer(holdings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def trades(self, request, wallet_address=None):
        """Get all trades for a specific user"""
        user = self.get_object()
        # Check permissions - users can only see their own trades
        if user.wallet_address != request.user.wallet_address and not request.user.is_staff:
            return Response(
                {"error": "You don't have permission to view this user's trades"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        trades = user.trades.all()
        serializer = TradeSerializer(trades, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def created_coins(self, request, wallet_address=None):
        """Get all coins created by a specific user"""
        user = self.get_object()
        coins = user.coins.all()
        from .serializers import CoinSerializer
        serializer = CoinSerializer(coins, many=True)
        return Response(serializer.data)