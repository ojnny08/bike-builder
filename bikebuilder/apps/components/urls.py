from django.urls import path
from .views import ComponentsList

urlpatterns = [
    path('components/', ComponentsList.as_view()),
    path('')
]