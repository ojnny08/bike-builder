from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer, UserPublicSerializer
from .models import User

class UserProfileViewSet(ViewSet):

    def retrieve(self, request):
        return Response(UserSerializer(request.user).data)

    def partial_update(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PublicProfileViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            profile = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserPublicSerializer(profile).data)

