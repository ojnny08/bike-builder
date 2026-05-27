from django.urls import path
from .views import MyView

urlpatterns = [
    path('me/', MyView.as_view(), name='me')
]