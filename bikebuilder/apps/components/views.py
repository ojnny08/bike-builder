from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth.authentication import FirebaseAuthentication
from .serializer import ComponentsSerializer
from .models import Components
# Create your views here.
class ComponentsList(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        components = Components.objects.all()

        component_type = request.query_params.get("category", "")
        if component_type:
            components = components.filter(component_type=component_type)

        search = request.query_params.get("search", "")
        if search:
            components = components.filter(name__icontains=search)

        return Response(ComponentsSerializer(components, many=True).data)