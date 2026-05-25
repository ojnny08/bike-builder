from rest_framework import serializers
from .models import Build

_COMPONENT_SLOTS = [
    "frame", "fork", "bottom_bracket", "crankset", "cassette",
    "rear_derailleur", "front_derailleur",
    "front_wheel", "rear_wheel", "front_tire", "rear_tire",
    "handlebar", "stem", "front_brake", "rear_brake",
    "saddle", "seatpost",
]


class BuildSerializer(serializers.ModelSerializer):
    compatibility_issues = serializers.SerializerMethodField()

    class Meta:
        model = Build
        fields = [
            "id", "name", "description", "bike_type",
            "frame", "fork",
            "bottom_bracket", "crankset", "cassette", "rear_derailleur", "front_derailleur",
            "front_wheel", "rear_wheel", "front_tire", "rear_tire",
            "handlebar", "stem",
            "front_brake", "rear_brake",
            "saddle", "seatpost",
            "compatibility_issues", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "compatibility_issues", "created_at", "updated_at"]

    def get_compatibility_issues(self, obj):
        return obj.get_compatibility_issues()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for slot in _COMPONENT_SLOTS:
            obj = getattr(instance, slot)
            if obj is not None:
                rep[slot] = {"id": obj.id, "name": obj.name, "brand": obj.brand}
        return rep
