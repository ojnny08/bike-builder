from .models import (
    Components, BottomBracket, Crankset, CrankArm, Chainring, Tire, Handlebar, Stem, Sprocket, Chain
)

RULES = {
    'bottom_bracket': (BottomBracket, 'frame',        lambda f:  {'options__bb_type': f.bb_type, 'bb_width_mm': f.bb_width_mm}),
    'crankset':       (Crankset,      'bottom_bracket', lambda bb: {'spindle_interface_mm': bb.spindle_interface_mm}),
    'crank_arm':      (CrankArm,      'bottom_bracket', lambda bb: {'spindle_interface_mm': bb.spindle_interface_mm}),
    'chainring':      (Chainring,     'crank_arm',      lambda a:  {'bcd': a.bcd}),
    'handlebar':      (Handlebar,     'stem',           lambda s:  {'clamp_diameter_mm': s.bar_clamp_diameter_mm}),
    'sprocket':       (Sprocket,      'wheel',          lambda w:  {'mount_type': w.hub_type}),
    'chain':          (Chain,         'sprocket',       lambda s:  {'chain_width': s.sprocket_width}),
}


def get_compatible_queryset(category, selected):
    if category == 'tire':
        return _filter_tires(selected.get('wheel'), selected.get('frame'))

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
        return Tire.objects.filter(wheel_size=wheel.wheel_size, width_mm__lte=wheel.max_tire_width_mm)
    if frame:
        return Tire.objects.filter(width_mm__lte=frame.max_tire_clearance_mm)
    return Tire.objects.all()
