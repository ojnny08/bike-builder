from datetime import timedelta

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from django.utils import timezone
from .serializer import BuildsSerializer
from .models import Build
from .image_upload import upload_to_s3, delete_from_s3


class PublicBuildsViewSet(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def featured(self, request):
        year, week, _ = timezone.now().isocalendar()
        key = f"builds:featured:{year}-{week:02d}"

        data = cache.get(key)
        if data is None:
            cutoff = timezone.now() - timedelta(days=7)
            builds = (
                Build.objects
                .filter(status=Build.Status.COMPLETE)
                .annotate(score=Coalesce(Sum('votes__value', filter=Q(votes__created_at__gte=cutoff)), 0))
                .order_by('-score', '-created_at')
                .prefetch_related('components')[:3]
            )
            data = BuildsSerializer(builds, many=True).data
            cache.set(key, data, 60 * 60 * 24 * 8)  # 8d safety net; key rotates weekly

        response = Response(data)
        response["Cache-Control"] = "public, max-age=3600, s-maxage=86400"
        return response

    def list(self, request):
        username = request.query_params.get('username')
        progress = request.query_params.get('status')
        limit = request.query_params.get('limit')
        builds = Build.objects.all()
        if username:
            builds = builds.filter(user__username=username)
        if progress:
            builds = builds.filter(status=progress)
        if limit:
            builds = builds[:int(limit)]
        return Response(BuildsSerializer(builds, many=True).data)
    
    def retrieve(self, request, token=None):
        try:
            build = Build.objects.get(share_token=token)
        except Build.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BuildsSerializer(build).data)


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

    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        try:
            build = Build.objects.get(pk=pk, user=request.user)
        except Build.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        file = request.FILES.get('image')
        if not file:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        old_url = build.image_url
        url = upload_to_s3(file, pk)
        build.image_url = url
        build.save(update_fields=['image_url'])
        delete_from_s3(old_url)
        return Response({'image_url': url})
    
        



    
        

