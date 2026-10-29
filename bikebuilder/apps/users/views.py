from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
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

    def destroy(self, request):
        try:
            auth.delete_user(request.user.firebase_uid)
        except auth.UserNotFoundError:
            pass
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublicProfileViewSet(ViewSet):

    def retrieve(self, request, username=None):
        try:
            profile = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserPublicSerializer(profile).data)

