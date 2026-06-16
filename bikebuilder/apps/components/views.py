from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .serializer import ComponentsSerializer
from .models import Components, Frame, BottomBracket, Crankset, Wheel, Stem, Sprocket
from .compatibility import get_compatible_queryset


def _paginate(queryset, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    page = paginator.paginate_queryset(queryset, request)
    return paginator.get_paginated_response(ComponentsSerializer(page, many=True).data)


class ComponentsViewSet(ViewSet):

    def list(self, request):
        queryset = Components.objects.all()

        component_type = request.query_params.get("component_type")
        if component_type:
            queryset = queryset.filter(component_type=component_type)

        select = request.query_params.get("select")
        if select:
            queryset = queryset.filter(name__icontains=select)

        return _paginate(queryset, request)

    def retrieve(self, request, pk=None):
        try:
            component = Components.objects.get(pk=pk)
        except Components.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ComponentsSerializer(component).data)
   
    @action(detail=False, methods=['get'])
    def compatible(self, request):
        component_type = request.query_params.get('component_type')
        if not component_type:
            return Response({'error': 'component_type is required'}, status=status.HTTP_400_BAD_REQUEST)

        selected = {
            'frame': _fetch(Frame, request, 'frame_id'),
            'bottom_bracket': _fetch(BottomBracket, request, 'bottom_bracket_id'),
            'crankset': _fetch(Crankset, request, 'crankset_id'),
            'wheel': _fetch(Wheel, request, 'wheel_id'),
            'stem': _fetch(Stem, request, 'stem_id'),
            'sprocket': _fetch(Sprocket, request, 'sprocket_id'),
        }

        queryset = get_compatible_queryset(component_type, selected)
        return Response(ComponentsSerializer(queryset, many=True).data)


def _fetch(model, request, param):
    pk = request.query_params.get(param)
    if not pk:
        return None
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None

