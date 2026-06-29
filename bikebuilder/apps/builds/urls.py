from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import MyBuildViewSet, PublicBuildsViewSet

router = DefaultRouter()
router.register('', MyBuildViewSet, basename='build')

public_builds = PublicBuildsViewSet.as_view({'get': 'list'})
shared_build = PublicBuildsViewSet.as_view({'get': 'retrieve'})
featured_builds = PublicBuildsViewSet.as_view({'get': 'featured'})

urlpatterns = [
    path('featured/', featured_builds, name='featured-builds'),
    path('public/', public_builds, name='public-builds'),
    path('public/<str:token>/', shared_build, name='shared-build'),
] + router.urls