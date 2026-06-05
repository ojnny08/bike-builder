from django.db import migrations
from decimal import Decimal


def seed(apps, schema_editor):
    Components = apps.get_model("components", "Components")

    Components.objects.create(
        component_type="wheel",
        name="Ellipse Front Wheel",
        brand="Mavic",
        price=Decimal("249.00"),
        weight_grams=990,
        description="Aerodynamic deep-section aluminum track wheel.",
        in_stock=True
    )
    Components.objects.create(
        component_type="wheel",
        name="Ellipse Rear Wheel",
        brand="Mavic",
        price=Decimal("299.00"),
        weight_grams=1100,
        description="Double-sided fixed/fixed flip-flop rear track wheel.",
        in_stock=True
    )
    Components.objects.create(
        component_type="wheel",
        name="Archetype Track Rear",
        brand="H Plus Son",
        price=Decimal("180.00"),
        weight_grams=970,
        description="Classic wide-profile box rim laced to a Gran Compe sealed bearing hub.",
        in_stock=True
    )
    Components.objects.create(
        component_type="tire",
        name="Gatorskin 700x25c",
        brand="Continental",
        price=Decimal("59.99"),
        weight_grams=240,
        description="The standard tire for fixed-gear street riding due to high flat resistance and thick casing.",
        in_stock=True
    )
    Components.objects.create(
        component_type="tire",
        name="Thickslick Comp",
        brand="WTB",
        price=Decimal("38.00"),
        weight_grams=460,
        description="Heavy, ultra-thick rubber compound designed explicitly to endure sliding.",
        in_stock=True
    )
    Components.objects.create(
        component_type="tire",
        name="Pasela PT Tanwall",
        brand="Panaracer",
        price=Decimal("45.00"),
        weight_grams=290,
        description="Classic gumwall styling paired with good puncture protection.",
        in_stock=True
    )


def unseed(apps, schema_editor):
    Components = apps.get_model("components", "Components")
    Components.objects.filter(
        brand__in=["Mavic", "H Plus Son"],
        component_type="wheel"
    ).delete()
    Components.objects.filter(
        brand__in=["WTB", "Panaracer"],
        component_type="tire"
    ).delete()
    Components.objects.filter(
        brand="Continental",
        component_type="tire",
        name="Gatorskin 700x25c"
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("components", "0004_seed_fixed_bottom_brackets"),
    ]

    operations = [
        migrations.RunPython(seed, reverse_code=unseed),
    ]
