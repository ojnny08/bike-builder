from rest_framework.viewsets import ModelViewSet
from .serializer import BuildsSerializer
from .models import Build


class BuildViewSet(ModelViewSet):
    serializer_class = BuildsSerializer

    def get_queryset(self):
        return Build.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
        

