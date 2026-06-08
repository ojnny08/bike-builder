from rest_framework.routers import DefaultRouter
from .views import BuildViewSet

router = DefaultRouter()
router.register('', BuildViewSet, basename='build')

urlpatterns = router.urls