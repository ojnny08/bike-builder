from rest_framework.serializers import serializers
from .models import Build

class BuildsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = ['id', 'user', 'bikeType', 'components', 'status', 'created_at', 'updated_at']