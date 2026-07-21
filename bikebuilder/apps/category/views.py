from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializer import BikeTypeSerializer
from .models import BikeType


class BikeTypeList(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        bike_types = BikeType.objects.filter(slug__in=BikeType.RULES.keys())
        return Response(BikeTypeSerializer(bike_types, many=True).data)
