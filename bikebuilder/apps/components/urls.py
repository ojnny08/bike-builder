from django.urls import path
from .views import ComponentsList

urlpatterns = [
    path('componentsList/', ComponentsList.as_view()),
]