from django.db import migrations
from decimal import Decimal


def seed(apps, schema_editor):
    Components = apps.get_model("components", "Components")

    Components.objects.create(
        component_type="frame",
        name="4130 Core Line",
        brand="State Bicycle Co.",
        price=Decimal("299.99"),
        weight_grams=2400,
        description="Classic 4130 Chromoly steel frame built for urban commuting and street riding.",
        in_stock=True
    )
    Components.objects.create(
        component_type="frame",
        name="Vigorelli Track",
        brand="Cinelli",
        price=Decimal("899.00"),
        weight_grams=1570,
        description="High-performance Columbus Airplane aluminum track frame designed for crit racing.",
        in_stock=True
    )
    Components.objects.create(
        component_type="frame",
        name="Pre Cursa",
        brand="Dolan",
        price=Decimal("350.00"),
        weight_grams=1780,
        description="The quintessential entry-level track racing frame, known for absolute durability.",
        in_stock=True
    )
    Components.objects.create(
        component_type="frame",
        name="Crit-D Track",
        brand="Engine 11",
        price=Decimal("750.00"),
        weight_grams=1480,
        description="Lightweight aluminum frame with a carbon fork, engineered for aggressive crit racing.",
        in_stock=True
    )
    Components.objects.create(
        component_type="frame",
        name="Rush",
        brand="Soma",
        price=Decimal("629.99"),
        weight_grams=2100,
        description="Tange Prestige heat-treated steel street track frame with traditional geometry.",
        in_stock=True
    )


def unseed(apps, schema_editor):
    Components = apps.get_model("components", "Components")
    Components.objects.filter(
        brand__in=["State Bicycle Co.", "Cinelli", "Dolan", "Engine 11", "Soma"],
        component_type="frame"
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("components", "0002_seed_components"),
    ]

    operations = [
        migrations.RunPython(seed, reverse_code=unseed),
    ]
