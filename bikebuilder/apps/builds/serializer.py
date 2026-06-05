from rest_framework import serializers
from .models import Build
from apps.category.serializer import BikeTypeSerializer
from apps.components.serializer import ComponentsSerializer

class BuildsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = ['id', 'name', 'bikeType', 'components', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['bikeType'] = BikeTypeSerializer(instance.bikeType).data
        rep['components'] = ComponentsSerializer(instance.components.all(), many=True).data
        return rep

    def to_internal_value(self, data):
        internal = super().to_internal_value(data)
        if 'bikeType' in data:
            internal['bikeType'] = Build._meta.get_field('bikeType').related_model.objects.get(id=data['bikeType'])
        return internal
