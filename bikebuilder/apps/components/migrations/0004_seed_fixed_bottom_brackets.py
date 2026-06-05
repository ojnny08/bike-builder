from django.db import migrations
from decimal import Decimal


def seed(apps, schema_editor):
    Components = apps.get_model("components", "Components")

    Components.objects.create(
        component_type="bottom_bracket",
        name="75 Super Lap ISO",
        brand="Sugino",
        price=Decimal("175.00"),
        weight_grams=245,
        description="High-end ISO taper bottom bracket featuring mirror-polished races for smooth spinning.",
        in_stock=True
    )
    Components.objects.create(
        component_type="bottom_bracket",
        name="LN-7611 JIS 110mm",
        brand="Tange Seiki",
        price=Decimal("35.00"),
        weight_grams=290,
        description="Affordable and durable sealed cartridge JIS square taper bottom bracket.",
        in_stock=True
    )
    Components.objects.create(
        component_type="bottom_bracket",
        name="Dura-Ace BB-7710 Octalink",
        brand="Shimano",
        price=Decimal("95.00"),
        weight_grams=240,
        description="NJS approved splined track bottom bracket, strictly compatible with V1 Octalink cranks.",
        in_stock=True
    )
    Components.objects.create(
        component_type="bottom_bracket",
        name="Evo Max BSA",
        brand="Miche",
        price=Decimal("42.00"),
        weight_grams=135,
        description="Outboard bearing bottom bracket designed for modern 24mm axle track cranksets.",
        in_stock=True
    )
    Components.objects.create(
        component_type="bottom_bracket",
        name="GXP Team BSA",
        brand="SRAM",
        price=Decimal("45.00"),
        weight_grams=105,
        description="The standard external bearing bottom bracket paired with classic SRAM Omnium cranks.",
        in_stock=True
    )


def unseed(apps, schema_editor):
    Components = apps.get_model("components", "Components")
    Components.objects.filter(
        brand__in=["Sugino", "Tange Seiki", "Miche"],
        component_type="bottom_bracket"
    ).delete()
    Components.objects.filter(
        brand="Shimano",
        component_type="bottom_bracket",
        name="Dura-Ace BB-7710 Octalink"
    ).delete()
    Components.objects.filter(
        brand="SRAM",
        component_type="bottom_bracket",
        name="GXP Team BSA"
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("components", "0003_seed_fixed_frames"),
    ]

    operations = [
        migrations.RunPython(seed, reverse_code=unseed),
    ]
