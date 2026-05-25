from django.urls import path
from .views import BuildDetailView, BuildListView

urlpatterns = [
    path("", BuildListView.as_view()),
    path("<int:pk>/", BuildDetailView.as_view()),
]
