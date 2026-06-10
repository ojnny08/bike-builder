from rest_framework.viewsets import ModelViewSet
from .serializer import ComponentsSerializer
from .models import Components


class ComponentsViewSet(ModelViewSet):
    serializer_class = ComponentsSerializer

    def get_queryset(self):
        queryset = Components.objects.all()

        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(component_type=category)

        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset
