# wallet_auth/views.py

from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.views.generic import TemplateView

from .services import SolanaAuthService

# Add a view for JWT token refresh
from rest_framework_simplejwt.views import TokenRefreshView

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

class RequestMessageView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Generate a message for the user to sign"""
        try:
            data = request.data
            wallet_address = data.get('wallet_address')
            
            if not wallet_address:
                return Response(
                    {'error': 'Wallet address is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create auth service with your app's details
            auth_service = SolanaAuthService(
                statement="Sign in to MyDjangoApp", 
                domain=request.get_host()
            )
            
            # Create a message
            message_data = auth_service.create_message(wallet_address)
            
            # Store the message and wallet address in session for later verification
            request.session['auth_message'] = message_data['message']
            request.session['auth_wallet'] = wallet_address
            
            return Response({
                'message': message_data['message']
            })
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VerifySignatureView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Verify signature and authenticate user"""
        try:
            data = request.data
            signature = data.get('signature')
            wallet_address = data.get('wallet_address')
            
            if not signature or not wallet_address:
                return Response(
                    {'error': 'Signature and wallet address are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get the original message from session
            message = request.session.get('auth_message')
            stored_wallet = request.session.get('auth_wallet')
            
            if not message or not stored_wallet:
                return Response(
                    {'error': 'No authentication attempt in progress'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify wallet address matches
            if stored_wallet != wallet_address:
                return Response(
                    {'error': 'Wallet address mismatch'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create auth service
            auth_service = SolanaAuthService()
            
            # Verify the signature
            is_valid = auth_service.verify_signature(message, signature, wallet_address)
            
            if is_valid:
                # Get or create user
                user, created = User.objects.get_or_create(wallet_address=wallet_address)
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                
                # Clear the session variables
                request.session.pop('auth_message', None)
                request.session.pop('auth_wallet', None)
                
                return Response({
                    'authenticated': True,
                    'user_id': user.id,
                    'new_user': created,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })
            else:
                return Response(
                    {'authenticated': False, 'error': 'Invalid signature'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginPageView(TemplateView):
    template_name = 'wallet_auth/login.html'


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