from rest_framework import serializers
from .models import Build

class BuildsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = ['id', 'bikeType', 'components', 'status', 'created_at', 'updated_at']