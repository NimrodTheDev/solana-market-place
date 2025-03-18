# wallet_auth/views.py

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
import json

from .services import SolanaAuthService

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


# Add to wallet_auth/views.py



class ProtectedResourceView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'You have access to this protected resource',
            'user_wallet': request.user.wallet_address
        })


# Add a view for JWT token refresh
from rest_framework_simplejwt.views import TokenRefreshView