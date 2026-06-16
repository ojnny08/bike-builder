from django.db import migrations, models
from decimal import Decimal


def seed(apps, schema_editor):
    Sprocket = apps.get_model("components", "Sprocket")
    Chain = apps.get_model("components", "Chain")

    # Threaded sprockets
    Sprocket.objects.create(
        component_type="sprocket", name="Dura-Ace Track Cog 16T", brand="Shimano",
        price=Decimal("35.99"), weight_grams=78, in_stock=True,
        mount_type="threaded", sprocket_width="1/8", sprocket_teeth=16,
    )
    Sprocket.objects.create(
        component_type="sprocket", name="Track Cog 17T", brand="Surly",
        price=Decimal("22.00"), weight_grams=95, in_stock=True,
        mount_type="threaded", sprocket_width="1/8", sprocket_teeth=17,
    )
    Sprocket.objects.create(
        component_type="sprocket", name="Zen Track Cog 15T", brand="Paul Components",
        price=Decimal("48.00"), weight_grams=72, in_stock=True,
        mount_type="threaded", sprocket_width="1/8", sprocket_teeth=15,
    )

    # Spline sprockets
    Sprocket.objects.create(
        component_type="sprocket", name="Spline Drive Cog 16T", brand="Shimano",
        price=Decimal("29.99"), weight_grams=82, in_stock=True,
        mount_type="spline", sprocket_width="1/8", sprocket_teeth=16,
    )
    Sprocket.objects.create(
        component_type="sprocket", name="Spline Cog 18T", brand="IRD",
        price=Decimal("34.00"), weight_grams=88, in_stock=True,
        mount_type="spline", sprocket_width="1/8", sprocket_teeth=18,
    )
    Sprocket.objects.create(
        component_type="sprocket", name="Spline Track Cog 15T", brand="Miche",
        price=Decimal("26.50"), weight_grams=79, in_stock=True,
        mount_type="spline", sprocket_width="1/8", sprocket_teeth=15,
    )

    # Chains
    Chain.objects.create(
        component_type="chain", name="Dura-Ace Track Chain", brand="Shimano",
        price=Decimal("42.99"), weight_grams=290, in_stock=True,
        chain_width="1/8", chain_material="chromoly",
    )
    Chain.objects.create(
        component_type="chain", name="Z610 HX Single Speed Chain", brand="KMC",
        price=Decimal("19.99"), weight_grams=310, in_stock=True,
        chain_width="1/8", chain_material="steel",
    )
    Chain.objects.create(
        component_type="chain", name="Izumi Super Toughness Chain", brand="Izumi",
        price=Decimal("34.00"), weight_grams=298, in_stock=True,
        chain_width="1/8", chain_material="chromoly",
    )


def unseed(apps, schema_editor):
    Sprocket = apps.get_model("components", "Sprocket")
    Chain = apps.get_model("components", "Chain")
    Sprocket.objects.all().delete()
    Chain.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0009_remove_frontderailleur_components_ptr_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sprocket',
            fields=[
                ('components_ptr', models.OneToOneField(auto_created=True, on_delete=models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='components.components')),
                ('mount_type', models.CharField(choices=[('threaded', 'Threaded'), ('spline', 'Spline')], max_length=10)),
                ('sprocket_width', models.CharField(choices=[('1/8', '1/8'), ('3/32', '3/32')], max_length=10)),
                ('sprocket_teeth', models.PositiveSmallIntegerField()),
            ],
            bases=('components.components',),
        ),
        migrations.CreateModel(
            name='Chain',
            fields=[
                ('components_ptr', models.OneToOneField(auto_created=True, on_delete=models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='components.components')),
                ('chain_width', models.CharField(choices=[('1/8', '1/8'), ('3/32', '3/32')], max_length=10)),
                ('chain_material', models.CharField(choices=[('chromoly', 'Chromoly'), ('steel', 'Steel')], max_length=20)),
            ],
            bases=('components.components',),
        ),
        migrations.AlterField(
            model_name='components',
            name='component_type',
            field=models.CharField(
                choices=[
                    ('frame', 'Frame'), ('bottom_bracket', 'Bottom Bracket'),
                    ('crankset', 'Crankset'), ('wheel', 'Wheel'), ('tire', 'Tire'),
                    ('handlebar', 'Handlebar'), ('stem', 'Stem'), ('brake', 'Brake'),
                    ('saddle', 'Saddle'), ('seatpost', 'Seatpost'),
                    ('sprocket', 'Sprocket'), ('chain', 'Chain'),
                ],
                max_length=30,
            ),
        ),
        migrations.RunPython(seed, unseed),
    ]
