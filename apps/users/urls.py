from django.urls import path
from .views import MyView

urlPatterns = [
    path('profile/', MyView.as_view(), name='profile')
]