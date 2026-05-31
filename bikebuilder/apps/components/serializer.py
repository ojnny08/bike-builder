from rest_framework import serializers
from .models import Components

class ComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Components
        fields = ['id', 'component_type', 'name', 'brand', 'weight_grams', 'price', 'in_stock', 'image_url']
        