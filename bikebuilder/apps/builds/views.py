from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auth.authentication import FirebaseAuthentication
from .serializer import BuildsSerializer
from .models import Build

# Create your views here.

class BuildView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        bike = Build.objects.get(id=pk, user=request.user)
        return Response(BuildsSerializer(bike).data)
    
    def post(self, request):
        serializer = BuildsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=200)
        return Response(serializer.errors)
    
    
        

