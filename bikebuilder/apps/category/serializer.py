from rest_framework import serializers
from .models import BikeType, BikeTypeComponentRule


def _get_specs(obj):
    try:
        f = obj.frame
        return {"size": f.size, "material": f.material, "bb_shell": f.bb_shell,
                "head_tube_type": f.head_tube_type, "rear_axle_standard": f.rear_axle_standard,
                "max_tire_clearance_mm": f.max_tire_clearance_mm}
    except Exception:
        pass
    try:
        f = obj.fork
        return {"steerer_diameter": f.steerer_diameter, "front_axle_standard": f.front_axle_standard,
                "travel_mm": f.travel_mm, "max_tire_clearance_mm": f.max_tire_clearance_mm}
    except Exception:
        pass
    try:
        b = obj.bottombracket
        return {"shell_type": b.shell_type, "spindle_interface": b.spindle_interface,
                "shell_width_mm": b.shell_width_mm}
    except Exception:
        pass
    try:
        c = obj.crankset
        return {"spindle_interface": c.spindle_interface, "arm_length_mm": c.arm_length_mm,
                "chainring_count": c.chainring_count, "bcd": c.bcd, "speeds": c.speeds}
    except Exception:
        pass
    try:
        c = obj.cassette
        return {"speeds": c.speeds, "min_cog": c.min_cog, "max_cog": c.max_cog,
                "freehub_standard": c.freehub_standard}
    except Exception:
        pass
    try:
        r = obj.rearderailleur
        return {"speeds": r.speeds, "max_cog_size": r.max_cog_size, "clutch": r.clutch}
    except Exception:
        pass
    try:
        f = obj.frontderailleur
        return {"speeds": f.speeds, "clamp_type": f.clamp_type}
    except Exception:
        pass
    try:
        w = obj.wheel
        return {"wheel_size": w.wheel_size, "position": w.position, "axle_standard": w.axle_standard,
                "max_tire_width_mm": w.max_tire_width_mm, "tubeless_ready": w.tubeless_ready}
    except Exception:
        pass
    try:
        t = obj.tire
        return {"wheel_size": t.wheel_size, "width_mm": t.width_mm,
                "tubeless_ready": t.tubeless_ready, "tread_type": t.tread_type}
    except Exception:
        pass
    try:
        h = obj.handlebar
        return {"bar_type": h.bar_type, "width_mm": h.width_mm,
                "clamp_diameter_mm": str(h.clamp_diameter_mm), "drop_mm": h.drop_mm, "reach_mm": h.reach_mm}
    except Exception:
        pass
    try:
        s = obj.stem
        return {"length_mm": s.length_mm, "bar_clamp_diameter_mm": str(s.bar_clamp_diameter_mm),
                "steerer_clamp_diameter_mm": str(s.steerer_clamp_diameter_mm), "angle_degrees": s.angle_degrees}
    except Exception:
        pass
    try:
        b = obj.brake
        return {"brake_type": b.brake_type, "mount_type": b.mount_type,
                "rotor_size_mm": b.rotor_size_mm, "position": b.position}
    except Exception:
        pass
    try:
        s = obj.saddle
        return {"width_mm": s.width_mm, "rail_type": s.rail_type, "rail_material": s.rail_material}
    except Exception:
        pass
    try:
        s = obj.seatpost
        return {"diameter_mm": str(s.diameter_mm), "length_mm": s.length_mm,
                "offset_mm": s.offset_mm, "post_type": s.post_type}
    except Exception:
        pass
    return {}

class BikeTypeComponentRuleSerializer(serializers.ModelSerializer):
    component_type = serializers.CharField(source="get_component_type_display")

    class Meta:
        model = BikeTypeComponentRule
        fields = ["component_type", "required"]


class BikeTypeSerializer(serializers.ModelSerializer):
    component_rules = BikeTypeComponentRuleSerializer(many=True, read_only=True)

    class Meta:
        model = BikeType
        fields = ["id", "name", "slug", "component_rules"]