from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth.authentication import FirebaseAuthentication
from .serializer import BuildsSerializer
from .models import Build

# Create your views here.

class Build(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        bike = Build.objects.filter(id=pk)
        return Response(BuildsSerializer(bike))
    
    def post(self, request):
        serializer = request.data
        bike = BuildsSerializer(serializer)
        return
    
        

