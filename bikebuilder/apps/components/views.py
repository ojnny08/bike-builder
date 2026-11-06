from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.cache import cache
from .serializer import (
    ComponentsSerializer, ComponentSubmissionSerializer,
    CranksetSerializer, CrankArmSerializer, ChainringSerializer, BottomBracketSerializer, TrackHubSerializer,
    RimSerializer, StemSerializer,
    ChainSerializer, HandlebarSerializer, BrakeSerializer, PedalsSerializer,
    SprocketSerializer, TireSerializer, SaddleSerializer, SeatpostSerializer,
    FrameSerializer, FrontSingleWheelSerializer, RearWheelSerializer, WheelSetSerializer,
    CustomWheelSerializer,
)
from .models import (
    Components, ComponentType, Frame, BottomBracket, Crankset, CrankArm, Chainring,
    FrontSingleWheel, RearWheel, Stem, Sprocket, TrackHub, Rim, Chain, Handlebar, Brake, Pedals, Tire, Saddle, Seatpost,
    WheelSet,
)
from .compatibility import get_compatible_queryset
from .signal import _clear_query_caches

TYPE_MODELS = {
    'frame': (Frame, FrameSerializer),
    'front_wheel': (FrontSingleWheel, FrontSingleWheelSerializer),
    'rear_wheel': (RearWheel, RearWheelSerializer),
    'wheelset': (WheelSet, WheelSetSerializer),
    'crankset': (Crankset, CranksetSerializer),
    'crank_arm': (CrankArm, CrankArmSerializer),
    'chainring': (Chainring, ChainringSerializer),
    'bottom_bracket': (BottomBracket, BottomBracketSerializer),
    'track_hub': (TrackHub, TrackHubSerializer),
    'rim': (Rim, RimSerializer),
    'stem': (Stem, StemSerializer),
    'chain': (Chain, ChainSerializer),
    'handlebar': (Handlebar, HandlebarSerializer),
    'brake': (Brake, BrakeSerializer),
    'pedals': (Pedals, PedalsSerializer),
    'sprocket': (Sprocket, SprocketSerializer),
    'tire': (Tire, TireSerializer),
    'saddle': (Saddle, SaddleSerializer),
    'seatpost': (Seatpost, SeatpostSerializer),
}


def _model_and_serializer(component_type):
    return TYPE_MODELS.get(component_type, (Components, ComponentsSerializer))


def _paginate(queryset, request, serializer_class=ComponentsSerializer):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    page = paginator.paginate_queryset(queryset, request)
    return paginator.get_paginated_response(serializer_class(page, many=True).data)


def _cached(key, ttl, compute):
    cached = cache.get(key)
    if cached is not None:
        response = Response(cached)
        response["X-Cache"] = "HIT"
        return response

    data = compute()
    cache.set(key, data, ttl)
    response = Response(data)
    response["X-Cache"] = "MISS"
    return response


class ComponentsViewSet(ViewSet):
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ("import_url", "custom_wheel"):
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request):
        component_type = request.query_params.get("component_type") or ""
        brand = request.query_params.get("brand") or ""
        search = request.query_params.get("search") or ""
        price_max = request.query_params.get("price_max") or ""
        price_min = request.query_params.get("price_min") or ""
        weight_max = request.query_params.get("weight_max") or ""
        weight_min = request.query_params.get("weight_min") or ""
        page = request.query_params.get("page") or "1"
        key = f"components:list:{component_type}:{brand}:{search}:{price_min}:{price_max}:{page}"

        def compute():
            model, serializer_class = _model_and_serializer(component_type)
            queryset = model.objects.all()
            if component_type and model is Components:
                queryset = queryset.filter(component_type=component_type)
            if brand:
                queryset = queryset.filter(brand=brand)
            if price_min:
                queryset = queryset.filter(price__gte=price_min)
            if price_max:
                queryset = queryset.filter(price__lte=price_max)
            if weight_max:
                queryset = queryset.filter(weight_grams__gte=weight_max)
            if weight_min:
                queryset = queryset.filter(weight_grams__gte=weight_min)
            if search:
                queryset = queryset.filter(name__icontains=search)
            return _paginate(queryset, request, serializer_class).data

        return _cached(key, 60 * 15, compute)

    def retrieve(self, request, pk=None):
        key = f"components:detail:{pk}"
        try:
            component_type = Components.objects.values_list("component_type", flat=True).get(pk=pk)
        except Components.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        model, serializer_class = _model_and_serializer(component_type)
        return _cached(key, 60 * 60, lambda: serializer_class(model.objects.get(pk=pk)).data)

    @action(detail=False, methods=['get'])
    def types(self, request):
        data = [{"value": value, "label": label} for value, label in ComponentType.choices]
        return Response(data)

    @action(detail=False, methods=['get'])
    def brands(self, request):
        component_type = request.query_params.get("component_type") or ""
        key = f"components:brands:{component_type}"

        def compute():
            queryset = Components.objects.all()
            if component_type:
                queryset = queryset.filter(component_type=component_type)
            return list(queryset.values_list("brand", flat=True).distinct().order_by("brand"))

        return _cached(key, 60 * 15, compute)
    
    @action(detail=False, methods=['get'])
    def compatible(self, request):
        component_type = request.query_params.get('component_type')
        if not component_type:
            return Response({'error': 'component_type is required'}, status=status.HTTP_400_BAD_REQUEST)

        selected = {
            'frame': _fetch(Frame, request, 'frame_id'),
            'bottom_bracket': _fetch(BottomBracket, request, 'bottom_bracket_id'),
            'crankset': _fetch(Crankset, request, 'crankset_id'),
            'crank_arm': _fetch(CrankArm, request, 'crank_arm_id'),
            'front_wheel': _fetch(FrontSingleWheel, request, 'front_wheel_id'),
            'rear_wheel': _fetch(RearWheel, request, 'rear_wheel_id'),
            'custom_hub': _fetch(TrackHub, request, 'custom_hub_id'),
            'position': request.query_params.get('position'),
            'stem': _fetch(Stem, request, 'stem_id'),
            'sprocket': _fetch(Sprocket, request, 'sprocket_id'),
        }

        queryset = get_compatible_queryset(component_type, selected)
        return Response(ComponentsSerializer(queryset, many=True).data)

    @action(detail=False, methods=['post'])
    def custom_wheel(self, request):
        serializer = CustomWheelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        position = serializer.validated_data['position']
        rim = serializer.validated_data['rim']
        hub = serializer.validated_data['hub']

        defaults = {
            'name': f"{rim} / {hub}",
            'brand': "Custom",
            'price': rim.price + hub.price,
            'weight_grams': rim.weight_grams + hub.weight_grams,
            'image_url': rim.image_url,
            'wheel_size': rim.wheel_size,
            'max_tire_width_mm': rim.max_tire_width_mm,
            'hub_spacing': hub.hub_spacing,
        }

        if position == 'front':
            model, serializer_class = FrontSingleWheel, FrontSingleWheelSerializer
            defaults['component_type'] = ComponentType.FRONT_WHEEL
        else:
            model, serializer_class = RearWheel, RearWheelSerializer
            option = hub.options.exclude(cog_interface="").first()
            cog_interface = option.cog_interface if option else ""
            defaults.update(
                component_type=ComponentType.REAR_WHEEL,
                threading=hub.threading,
                cog_interface=cog_interface,
                hub_type="spline" if cog_interface == "splined" else "threaded",
            )

        wheel, _ = model.objects.update_or_create(
            custom_rim=rim, custom_hub=hub,
            defaults=defaults,
            create_defaults={**defaults, 'submitted_by': request.user},
        )
        cache.delete(f"components:detail:{wheel.pk}")
        _clear_query_caches()
        return Response(serializer_class(wheel).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def import_url(self, request):
        serializer = ComponentSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(submitted_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def _fetch(model, request, param):
    pk = request.query_params.get(param)
    if not pk:
        return None
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None
