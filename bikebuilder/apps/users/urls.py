from django.urls import path
from .views import UserProfileViewSet, PublicProfileViewSet

profile = UserProfileViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})
public_profile = PublicProfileViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    path('', profile, name='profile'),
    path('<int:pk>/', public_profile, name='public-profile'),
]