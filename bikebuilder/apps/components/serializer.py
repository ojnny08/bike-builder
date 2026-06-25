from rest_framework import serializers
from .models import Components, ComponentType

class ComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Components
        fields = ['id', 'component_type', 'name', 'brand', 'weight_grams', 'price', 'image_url']

class ComponentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentType
        fields = ['id', 'frame']