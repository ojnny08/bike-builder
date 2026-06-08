from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserSerializer


class MyView(APIView):

    def get(self, request):
        return Response(UserSerializer(request.user).data)
