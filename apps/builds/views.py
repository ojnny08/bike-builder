from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from auth.authentication import FirebaseAuthentication
from .models import Build
from .serializer import BuildSerializer


class BuildListView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        builds = Build.objects.filter(user=request.user)
        return Response(BuildSerializer(builds, many=True).data)

    def post(self, request):
        serializer = BuildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuildDetailView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Build.objects.get(pk=pk, user=user)
        except Build.DoesNotExist:
            return None

    def get(self, request, pk):
        build = self.get_object(pk, request.user)
        if not build:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(BuildSerializer(build).data)

    def patch(self, request, pk):
        build = self.get_object(pk, request.user)
        if not build:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BuildSerializer(build, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        build = self.get_object(pk, request.user)
        if not build:
            return Response(status=status.HTTP_404_NOT_FOUND)
        build.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
