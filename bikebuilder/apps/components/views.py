from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ComponentsSerializer
from .models import Components


class ComponentsList(APIView):

    def get(self, request):
        components = Components.objects.all()

        component_type = request.query_params.get("category", "")
        if component_type:
            components = components.filter(component_type=component_type)

        search = request.query_params.get("search", "")
        if search:
            components = components.filter(name__icontains=search)

        return Response(ComponentsSerializer(components, many=True).data)