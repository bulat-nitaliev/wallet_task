from rest_framework import routers
from wallet.views import WalletViewSet, UserVievSet


router = routers.DefaultRouter()

router.register('wallets', WalletViewSet, 'wallet')
router.register('users', UserVievSet, 'users')

urlpatterns = router.urls