from django.urls import path
from .views import BikeTypeList

urlpatterns = [
    path("bike-types/", BikeTypeList.as_view()),
]
