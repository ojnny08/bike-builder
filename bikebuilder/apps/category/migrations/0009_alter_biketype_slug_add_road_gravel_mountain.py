from django.db import migrations, models


def seed_missing_bike_types(apps, schema_editor):
    BikeType = apps.get_model("category", "BikeType")
    BikeType.objects.get_or_create(slug="road-gravel", defaults={"name": "Road & Gravel"})
    BikeType.objects.get_or_create(slug="mountain",    defaults={"name": "Mountain"})


def unseed_missing_bike_types(apps, schema_editor):
    BikeType = apps.get_model("category", "BikeType")
    BikeType.objects.filter(slug__in=["road-gravel", "mountain"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0008_alter_biketype_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="biketype",
            name="slug",
            field=models.SlugField(
                choices=[
                    ("fixed",       "Fixed Gear"),
                    ("road-gravel", "Road & Gravel"),
                    ("mountain",    "Mountain"),
                ]
            ),
        ),
        migrations.RunPython(seed_missing_bike_types, reverse_code=unseed_missing_bike_types),
    ]
