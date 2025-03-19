# wallet_auth/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'coins', views.CoinViewSet)
router.register(r'holdings', views.UserCoinHoldingsViewSet)
router.register(r'trades', views.TradeViewSet)

urlpatterns = [
    # Authentication endpoints
    path('auth/request-message/', views.RequestMessageView.as_view(), name='request-message'),
    path('auth/verify-signature/', views.VerifySignatureView.as_view(), name='verify-signature'),
    path('auth/token/refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
    
    # Login page
    path('login/', views.LoginPageView.as_view(), name='login'),
    
    # API endpoints
    path('api/', include(router.urls)),
]
