# wallet_auth/urls.py

from django.urls import path
from .views import RequestMessageView, VerifySignatureView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginPageView
from .views import ProtectedResourceView

urlpatterns = [
    path('auth/request-message/', RequestMessageView.as_view(), name='request_message'),
    path('auth/verify-signature/', VerifySignatureView.as_view(), name='verify_signature'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('protected-resource/', ProtectedResourceView.as_view(), name='protected_resource'),
]
