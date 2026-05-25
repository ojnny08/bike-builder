from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth.authentication import FirebaseAuthentication
from .serializer import BikeTypeSerializer, ComponentSerializer
from .models import BikeType, Component


class ComponentsList(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        components = Component.objects.select_related(
            "frame", "fork", "bottombracket", "crankset", "cassette",
            "rearderailleur", "frontderailleur", "wheel", "tire",
            "handlebar", "stem", "brake", "saddle", "seatpost",
        ).all()

        category = request.query_params.get("category", "")
        if category:
            components = components.filter(category__slug=category)

        search = request.query_params.get("search", "")
        if search:
            components = components.filter(name__icontains=search)

        return Response(ComponentSerializer(components, many=True).data)


class BikeTypeList(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bike_types = BikeType.objects.prefetch_related("component_rules").all()
        return Response(BikeTypeSerializer(bike_types, many=True).data)
