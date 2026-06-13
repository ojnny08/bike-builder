from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializer import ComponentsSerializer
from .models import Components, Frame, BottomBracket, Crankset, Wheel, Handlebar, Stem
from .compatibility import get_compatible_queryset


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

    @action(detail=False, methods=['get'])
    def compatible(self, request):
        category = request.query_params.get('category')
        if not category:
            return Response({'error': 'category is required'}, status=status.HTTP_400_BAD_REQUEST)

        selected = {
            'frame': _fetch(Frame, request, 'frame_id'),
            'bottom_bracket': _fetch(BottomBracket, request, 'bottom_bracket_id'),
            'crankset': _fetch(Crankset, request, 'crankset_id'),
            'wheel': _fetch(Wheel, request, 'wheel_id'),
            'handlebar': _fetch(Handlebar, request, 'handlebar_id'),
            'stem': _fetch(Stem, request, 'stem_id'),
        }

        queryset = get_compatible_queryset(category, selected)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


def _fetch(model, request, param):
    pk = request.query_params.get(param)
    if not pk:
        return None
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None
