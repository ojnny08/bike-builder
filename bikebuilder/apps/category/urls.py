from django.urls import path
from .views import BikeTypeList, ComponentsList

urlpatterns = [
    path("components/", ComponentsList.as_view()),
    path("bike-types/", BikeTypeList.as_view()),
]
