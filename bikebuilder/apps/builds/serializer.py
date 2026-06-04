from rest_framework import serializers
from .models import Build

class BuildsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = ['id', 'name', 'bikeType', 'components', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']