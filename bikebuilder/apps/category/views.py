from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth.authentication import FirebaseAuthentication
from .serializer import BikeTypeSerializer
from .models import BikeType


class BikeTypeList(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bike_types = BikeType.objects.prefetch_related("component_rules").all()
        return Response(BikeTypeSerializer(bike_types, many=True).data)
