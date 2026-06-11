from .models import (
    Components, BottomBracket, Crankset, Cassette,
    RearDerailleur, FrontDerailleur, Wheel, Tire, Handlebar, Stem
)


def get_compatible_queryset(category, selected):

    frame = selected.get('frame')
    bottom_bracket = selected.get('bottom_bracket')
    crankset = selected.get('crankset')
    cassette = selected.get('cassette')
    wheel = selected.get('wheel')
    handlebar = selected.get('handlebar')
    stem = selected.get('stem')

    dispatch = {
        'bottom_bracket': lambda: _filter_bottom_brackets(frame),
        'crankset': lambda: _filter_cranksets(bottom_bracket),
        'cassette': lambda: _filter_cassettes(crankset),
        'rear_derailleur': lambda: _filter_rear_derailleurs(cassette),
        'front_derailleur': lambda: _filter_front_derailleurs(crankset),
        'wheel': lambda: _filter_wheels(frame),
        'tire': lambda: _filter_tires(frame, wheel),
        'stem': lambda: _filter_stems(handlebar),
        'handlebar': lambda: _filter_handlebars(stem),
    }

    if category in dispatch:
        return dispatch[category]()

    # saddle, seatpost, brake — no compatibility constraint modeled yet
    return Components.objects.filter(component_type=category)


def _filter_bottom_brackets(frame):
    qs = BottomBracket.objects.all()
    if frame:
        qs = qs.filter(shell_type=frame.bb_shell)
    return qs


def _filter_cranksets(bottom_bracket):
    qs = Crankset.objects.all()
    if bottom_bracket:
        qs = qs.filter(spindle_interface=bottom_bracket.spindle_interface)
    return qs


def _filter_cassettes(crankset):
    qs = Cassette.objects.all()
    if crankset:
        qs = qs.filter(speeds=crankset.speeds)
    return qs


def _filter_rear_derailleurs(cassette):
    qs = RearDerailleur.objects.all()
    if cassette:
        qs = qs.filter(speeds=cassette.speeds, max_cog_size__gte=cassette.max_cog)
    return qs


def _filter_front_derailleurs(crankset):
    qs = FrontDerailleur.objects.all()
    if crankset:
        qs = qs.filter(speeds=crankset.speeds)
    return qs


def _filter_wheels(frame):
    qs = Wheel.objects.all()
    if frame:
        qs = qs.filter(axle_standard=frame.rear_axle_standard)
    return qs


def _filter_tires(frame, wheel):
    qs = Tire.objects.all()
    if wheel:
        # wheel is the tighter constraint: must match size and fit within rim width
        qs = qs.filter(wheel_size=wheel.wheel_size, width_mm__lte=wheel.max_tire_width_mm)
    elif frame:
        qs = qs.filter(width_mm__lte=frame.max_tire_clearance_mm)
    return qs


def _filter_stems(handlebar):
    qs = Stem.objects.all()
    if handlebar:
        qs = qs.filter(bar_clamp_diameter_mm=handlebar.clamp_diameter_mm)
    return qs


def _filter_handlebars(stem):
    qs = Handlebar.objects.all()
    if stem:
        qs = qs.filter(clamp_diameter_mm=stem.bar_clamp_diameter_mm)
    return qs
