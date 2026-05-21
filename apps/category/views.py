from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth.authentication import FirebaseAuthentication
from .serializer import ComponentSerializer
from .models import Component
# Create your views here.

class ComponentsList(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        components = Component.objects.all()

        category = request.query_params.get("category", "")
        if category:
            components = components.filter(category__slug=category)

        search = request.query_params.get("search", "")
        if search:
            components = components.filter(name__icontains=search)

        return Response(ComponentSerializer(components, many=True).data)
