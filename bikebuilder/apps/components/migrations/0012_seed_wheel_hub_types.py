from django.db import migrations
from decimal import Decimal


def seed(apps, schema_editor):
    Wheel = apps.get_model("components", "Wheel")

    # Set hub types on existing fixed gear wheels — all use standard threaded track hubs
    Wheel.objects.filter(name="Ellipse Front Wheel", brand="Mavic").update(hub_type="threaded")
    Wheel.objects.filter(name="Ellipse Rear Wheel", brand="Mavic").update(hub_type="threaded")
    Wheel.objects.filter(name="Archetype Track Rear", brand="H Plus Son").update(hub_type="threaded")

    # Add spline hub track wheels so spline sprockets have compatible options
    Wheel.objects.create(
        component_type="wheel",
        name="Dura-Ace Track Front",
        brand="Shimano",
        price=Decimal("320.00"),
        weight_grams=880,
        in_stock=True,
        wheel_size="700c",
        position="front",
        axle_standard="qr_100",
        hub_type="spline",
        max_tire_width_mm=25,
        tubeless_ready=False,
    )
    Wheel.objects.create(
        component_type="wheel",
        name="Dura-Ace Track Rear",
        brand="Shimano",
        price=Decimal("380.00"),
        weight_grams=980,
        in_stock=True,
        wheel_size="700c",
        position="rear",
        axle_standard="track_120",
        hub_type="spline",
        max_tire_width_mm=25,
        tubeless_ready=False,
    )


def unseed(apps, schema_editor):
    Wheel = apps.get_model("components", "Wheel")
    Wheel.objects.filter(brand="Shimano", name__in=["Dura-Ace Track Front", "Dura-Ace Track Rear"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0011_add_wheel_hub_type'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
