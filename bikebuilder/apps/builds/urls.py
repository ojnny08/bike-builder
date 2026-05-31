from django.urls import path
from .views import BuildView

urlpatterns = [
    path("build/", BuildView.as_view())
]