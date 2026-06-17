from rest_framework.routers import DefaultRouter
from .views import MyBuildViewSet

router = DefaultRouter()
router.register('', MyBuildViewSet, basename='build')

urlpatterns = router.urls