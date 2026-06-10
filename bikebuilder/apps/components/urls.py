from rest_framework.routers import DefaultRouter
from .views import ComponentsViewSet

router = DefaultRouter()
router.register('', ComponentsViewSet, basename='components')

urlpatterns = router.urls
