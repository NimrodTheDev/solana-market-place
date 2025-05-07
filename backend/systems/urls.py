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
# router.register(r'coin-scores', views.CoinDRCScoreViewSet)
router.register(r'rug-flags', views.CoinRugFlagViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
