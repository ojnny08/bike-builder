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

    def post(self, request):
        serializer = BuildsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, pk):
        build = Build.objects.get(id=pk, user=request.user)
        return Response(BuildsSerializer(build).data)

    def delete(self, request, pk):
        build = Build.objects.get(id=pk, user=request.user)
        build.delete()
        return Response(status=204)
    
    def patch(self, request, pk):
        build = Build.objects.get(id=pk, user=request.user)
        serializer = BuildsSerializer(build, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)



class BuildViewAll(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        builds = Build.objects.all()
        return Response(BuildsSerializer(builds, many=True).data)

    
        

