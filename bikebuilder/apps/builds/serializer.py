from rest_framework import serializers
from .models import Build
from apps.category.serializer import BikeTypeSerializer
from apps.components.serializer import ComponentsSerializer
from apps.users.serializer import UserPublicSerializer

class BuildsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = ['id', 'user', 'name', 'bikeType', 'components', 'status', 'image_url', 'share_token', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'share_token', 'created_at', 'updated_at']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = UserPublicSerializer(instance.user).data
        rep['bikeType'] = BikeTypeSerializer(instance.bikeType).data
        rep['components'] = ComponentsSerializer(instance.components.all(), many=True).data
        return rep

    def to_internal_value(self, data):
        internal = super().to_internal_value(data)
        if 'bikeType' in data:
            internal['bikeType'] = Build._meta.get_field('bikeType').related_model.objects.get(id=data['bikeType'])
        return internal
