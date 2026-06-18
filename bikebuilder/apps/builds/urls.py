from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import MyBuildViewSet, PublicBuildsViewSet

router = DefaultRouter()
router.register('', MyBuildViewSet, basename='build')

public_builds = PublicBuildsViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('public/', public_builds, name='public-builds'),
] + router.urls