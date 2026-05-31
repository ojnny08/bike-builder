from rest_framework import serializers
from .models import BikeType


class BikeTypeSerializer(serializers.ModelSerializer):
    rules = serializers.SerializerMethodField()

    def get_rules(self, obj):
        return obj.get_rules()

    class Meta:
        model = BikeType
        fields = ["id", "name", "slug", "rules"]


        