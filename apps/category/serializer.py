from rest_framework.serializers import serializer
from .models import Component

class ComponentSerializer(serializer.ModelSerializer):
    class Meta:
        model = Component
        fields = ["id", "name", "brand", "weight_grams", "category", "in_stock", "image_url"]