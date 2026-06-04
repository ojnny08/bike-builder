from django.urls import path
from .views import BuildView, BuildViewAll

urlpatterns = [
    path("build/", BuildView.as_view()),
    path("build/<int:pk>/", BuildView.as_view()),
    path("build-all/", BuildViewAll.as_view()),
]