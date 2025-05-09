from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'coins', views.CoinViewSet)
router.register(r'holdings', views.UserCoinHoldingsViewSet)
router.register(r'trades', views.TradeViewSet)
# drc stuff
router.register(r'developer-scores', views.DeveloperScoreViewSet)
router.register(r'trader-scores', views.TraderScoreViewSet)
router.register(r'coin-scores', views.CoinDRCScoreViewSet)
router.register(r'rug-flags', views.CoinRugFlagViewSet)

auth_urls = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("me/", views.MeView.as_view(), name="me"),
]

urlpatterns = [
    path("api/", include(auth_urls)),
    path("api/", include(router.urls)),
]
