from rest_framework.serializers import serializer
from .models import Components

class ComponentsSerializer(serializer.ModelSerializer):
    class Meta:
        model = Components
        fields = ['id', 'category', 'bike_type', 'name', 'brand', 'weight_grams', 'price', "in_stock", "image_url", "specs"]
        