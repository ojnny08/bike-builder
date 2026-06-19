from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializer import BuildsSerializer
from .models import Build


class PublicBuildsViewSet(ViewSet):

    def list(self, request):
        username = request.query_params.get('username')
        progress = request.query_params.get('status')
        builds = Build.objects.all()
        if username:
            builds = builds.filter(user__username=username)
        if progress:
            builds = builds.filter(status=progress)
        return Response(BuildsSerializer(builds, many=True).data)


class MyBuildViewSet(ViewSet):

    def list(self, request):
        build = Build.objects.filter(user=request.user)
        return Response(BuildsSerializer(build, many=True).data)

    def retrieve(self, request, pk=None):
        try:
            build = Build.objects.get(pk=pk, user=request.user)
        except Build.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BuildsSerializer(build).data)

    def create(self, request):
        serializer = BuildsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            build = Build.objects.get(pk=pk, user=request.user)
        except Build.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        build.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        try:
            build = Build.objects.get(pk=pk, user=request.user)
        except Build.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BuildsSerializer(build, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        



    
        

