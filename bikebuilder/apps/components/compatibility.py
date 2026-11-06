from .models import (
    Components, BottomBracket, Crankset, CrankArm, Chainring, Tire, Handlebar, Sprocket, Chain, TrackHub, Rim, HubSpacing
)

RULES = {
    'bottom_bracket': (BottomBracket, 'frame',        lambda f:  {'options__bb_type': f.bb_type, 'bb_width_mm': f.bb_width_mm}),
    'crankset':       (Crankset,      'bottom_bracket', lambda bb: {'spindle_interface_mm': bb.spindle_interface_mm}),
    'crank_arm':      (CrankArm,      'bottom_bracket', lambda bb: {'spindle_interface_mm': bb.spindle_interface_mm}),
    'chainring':      (Chainring,     'crank_arm',      lambda a:  {'bcd': a.bcd}),
    'handlebar':      (Handlebar,     'stem',           lambda s:  {'clamp_diameter_mm': s.bar_clamp_diameter_mm}),
    'sprocket':       (Sprocket,      'rear_wheel',     lambda w:  {'mount_type': w.hub_type}),
    'chain':          (Chain,         'sprocket',       lambda s:  {'chain_width': s.sprocket_width}),
}


def get_compatible_queryset(category, selected):
    if category == 'tire':
        return _filter_tires(selected.get('rear_wheel') or selected.get('front_wheel'), selected.get('frame'))
    if category == 'track_hub':
        return _filter_hubs(selected.get('position'))
    if category == 'rim':
        return _filter_rims(selected.get('custom_hub'))

    rule = RULES.get(category)
    if not rule:
        return Components.objects.filter(component_type=category)

    model, dep_key, get_filters = rule
    dep = selected.get(dep_key)
    if not dep:
        return model.objects.all()
    return model.objects.filter(**get_filters(dep)).distinct()


def _filter_tires(wheel, frame):
    if wheel:
        tires = Tire.objects.filter(wheel_size=wheel.wheel_size)
        if not wheel.max_tire_width_mm:
            return tires
        return tires.filter(width_mm__lte=wheel.max_tire_width_mm)
    if frame:
        return Tire.objects.filter(width_mm__lte=frame.max_tire_clearance_mm)
    return Tire.objects.all()


def _filter_hubs(position):
    hubs = TrackHub.objects.all()
    if position == 'front':
        return hubs.filter(hub_spacing=HubSpacing.FRONT_100MM)
    if position == 'rear':
        return hubs.exclude(hub_spacing=HubSpacing.FRONT_100MM)
    return hubs


def _filter_rims(hub):
    rims = Rim.objects.all()
    if not hub:
        return rims
    holes = hub.options.exclude(hole_count=None).values('hole_count')
    if not holes.exists():
        return rims
    return rims.filter(options__hole_count__in=holes).distinct()
