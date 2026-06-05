from django.db import migrations
from decimal import Decimal


def seed(apps, schema_editor):
    Components = apps.get_model("components", "Components")

    Components.objects.create(
        component_type="handlebar",
        name="B809AA Riser Bar",
        brand="Nitto",
        price=Decimal("68.00"),
        weight_grams=310,
        description="Premium aluminum riser handlebar loved for city filtering.",
        in_stock=True
    )
    Components.objects.create(
        component_type="handlebar",
        name="B123AA NJS Drop Bar",
        brand="Nitto",
        price=Decimal("92.00"),
        weight_grams=380,
        description="Classic deep alloy track drops with NJS certification.",
        in_stock=True
    )
    Components.objects.create(
        component_type="handlebar",
        name="Crononero Bullhorn",
        brand="Deda Elementi",
        price=Decimal("52.00"),
        weight_grams=285,
        description="Aerodynamic aluminum bullhorn bar for urban tracking.",
        in_stock=True
    )
    Components.objects.create(
        component_type="stem",
        name="Elite X4 Stem",
        brand="Thomson",
        price=Decimal("114.00"),
        weight_grams=160,
        description="CNC-machined from a single block of aluminum. Unmatched strength.",
        in_stock=True
    )
    Components.objects.create(
        component_type="stem",
        name="Pearl NJS Quill",
        brand="Nitto",
        price=Decimal("105.00"),
        weight_grams=330,
        description="Forged aluminum quill stem for traditional threaded headsets.",
        in_stock=True
    )


def unseed(apps, schema_editor):
    Components = apps.get_model("components", "Components")
    Components.objects.filter(
        brand="Nitto",
        component_type__in=["handlebar", "stem"]
    ).delete()
    Components.objects.filter(
        brand__in=["Deda Elementi", "Thomson"],
        component_type__in=["handlebar", "stem"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("components", "0005_seed_fixed_wheels_tires"),
    ]

    operations = [
        migrations.RunPython(seed, reverse_code=unseed),
    ]
