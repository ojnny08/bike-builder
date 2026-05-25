from django.db import migrations

# (component_type, required)
_ROAD = [
    ("frame", True), ("fork", True), ("bottom_bracket", True), ("crankset", True),
    ("cassette", True), ("rear_derailleur", True), ("front_derailleur", False),
    ("wheel", True), ("tire", True), ("handlebar", True), ("stem", True),
    ("brake", True), ("saddle", True), ("seatpost", True),
]

_MOUNTAIN = [
    ("frame", True), ("fork", True), ("bottom_bracket", True), ("crankset", True),
    ("cassette", True), ("rear_derailleur", True), ("front_derailleur", False),
    ("wheel", True), ("tire", True), ("handlebar", True), ("stem", True),
    ("brake", True), ("saddle", True), ("seatpost", True),
]

_GRAVEL = [
    ("frame", True), ("fork", True), ("bottom_bracket", True), ("crankset", True),
    ("cassette", True), ("rear_derailleur", True), ("front_derailleur", False),
    ("wheel", True), ("tire", True), ("handlebar", True), ("stem", True),
    ("brake", True), ("saddle", True), ("seatpost", True),
]

_FIXED = [
    ("frame", True), ("fork", True), ("bottom_bracket", True), ("crankset", True),
    ("cassette", False), ("rear_derailleur", False), ("front_derailleur", False),
    ("wheel", True), ("tire", True), ("handlebar", True), ("stem", True),
    ("brake", False), ("saddle", True), ("seatpost", True),
]

_RULES = {
    "road": _ROAD,
    "mountain": _MOUNTAIN,
    "gravel": _GRAVEL,
    "fixed": _FIXED,
}


def seed(apps, schema_editor):
    BikeType = apps.get_model("category", "BikeType")
    BikeTypeComponentRule = apps.get_model("category", "BikeTypeComponentRule")
    for slug, rules in _RULES.items():
        try:
            bike_type = BikeType.objects.get(slug=slug)
        except BikeType.DoesNotExist:
            continue
        for component_type, required in rules:
            BikeTypeComponentRule.objects.get_or_create(
                bike_type=bike_type,
                component_type=component_type,
                defaults={"required": required},
            )


def unseed(apps, schema_editor):
    BikeTypeComponentRule = apps.get_model("category", "BikeTypeComponentRule")
    BikeTypeComponentRule.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0004_alter_biketype_slug"),
    ]

    operations = [
        migrations.RunPython(seed, reverse_code=unseed),
    ]
