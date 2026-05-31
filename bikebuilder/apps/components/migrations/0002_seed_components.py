from django.db import migrations

COMPONENTS = [
    # Frames
    {"component_type": "frame", "name": "Domane SL 6", "brand": "Trek", "price": "2799.99", "weight_grams": 1050},
    {"component_type": "frame", "name": "Roubaix Sport", "brand": "Specialized", "price": "1999.99", "weight_grams": 980},
    {"component_type": "frame", "name": "TCR Advanced", "brand": "Giant", "price": "2499.99", "weight_grams": 920},

    # Forks
    {"component_type": "fork", "name": "Road Fork Carbon", "brand": "Enve", "price": "599.99", "weight_grams": 380},
    {"component_type": "fork", "name": "Future Shock Fork", "brand": "Specialized", "price": "449.99", "weight_grams": 420},
    {"component_type": "fork", "name": "Advanced SL Fork", "brand": "Giant", "price": "349.99", "weight_grams": 395},

    # Bottom Brackets
    {"component_type": "bottom_bracket", "name": "BB-R9100", "brand": "Shimano", "price": "49.99", "weight_grams": 75},
    {"component_type": "bottom_bracket", "name": "DUB BSA", "brand": "SRAM", "price": "59.99", "weight_grams": 70},
    {"component_type": "bottom_bracket", "name": "T47 Road", "brand": "Chris King", "price": "179.99", "weight_grams": 65},

    # Cranksets
    {"component_type": "crankset", "name": "105 FC-R7100", "brand": "Shimano", "price": "179.99", "weight_grams": 710},
    {"component_type": "crankset", "name": "Rival AXS", "brand": "SRAM", "price": "299.99", "weight_grams": 680},
    {"component_type": "crankset", "name": "Chorus Crankset", "brand": "Campagnolo", "price": "349.99", "weight_grams": 660},

    # Cassettes
    {"component_type": "cassette", "name": "CS-R7100 11-34", "brand": "Shimano", "price": "59.99", "weight_grams": 295},
    {"component_type": "cassette", "name": "Rival AXS 10-36", "brand": "SRAM", "price": "89.99", "weight_grams": 270},
    {"component_type": "cassette", "name": "Chorus 11-29", "brand": "Campagnolo", "price": "129.99", "weight_grams": 245},

    # Rear Derailleurs
    {"component_type": "rear_derailleur", "name": "105 RD-R7100", "brand": "Shimano", "price": "109.99", "weight_grams": 253},
    {"component_type": "rear_derailleur", "name": "Rival AXS RD", "brand": "SRAM", "price": "249.99", "weight_grams": 230},
    {"component_type": "rear_derailleur", "name": "Chorus RD", "brand": "Campagnolo", "price": "199.99", "weight_grams": 210},

    # Front Derailleurs
    {"component_type": "front_derailleur", "name": "105 FD-R7100", "brand": "Shimano", "price": "49.99", "weight_grams": 91},
    {"component_type": "front_derailleur", "name": "Rival AXS FD", "brand": "SRAM", "price": "149.99", "weight_grams": 85},
    {"component_type": "front_derailleur", "name": "Chorus FD", "brand": "Campagnolo", "price": "99.99", "weight_grams": 88},

    # Wheels
    {"component_type": "wheel", "name": "Aeolus RSL 37", "brand": "Bontrager", "price": "1499.99", "weight_grams": 1450},
    {"component_type": "wheel", "name": "Roval Alpinist CL", "brand": "Specialized", "price": "1799.99", "weight_grams": 1320},
    {"component_type": "wheel", "name": "SLR 1 Carbon", "brand": "Giant", "price": "999.99", "weight_grams": 1480},

    # Tires
    {"component_type": "tire", "name": "GP5000 700x25", "brand": "Continental", "price": "59.99", "weight_grams": 210},
    {"component_type": "tire", "name": "Turbo Cotton 700x26", "brand": "Specialized", "price": "79.99", "weight_grams": 195},
    {"component_type": "tire", "name": "Corsa Speed 700x28", "brand": "Vittoria", "price": "69.99", "weight_grams": 205},

    # Handlebars
    {"component_type": "handlebar", "name": "Pro Vibe Carbon", "brand": "Shimano", "price": "149.99", "weight_grams": 210},
    {"component_type": "handlebar", "name": "Aerofly II", "brand": "FSA", "price": "129.99", "weight_grams": 225},
    {"component_type": "handlebar", "name": "Cockpit SL Drop", "brand": "Zipp", "price": "199.99", "weight_grams": 195},

    # Stems
    {"component_type": "stem", "name": "Pro Vibe Stem 100mm", "brand": "Shimano", "price": "79.99", "weight_grams": 128},
    {"component_type": "stem", "name": "SL-K Stem 110mm", "brand": "FSA", "price": "99.99", "weight_grams": 118},
    {"component_type": "stem", "name": "SL Sprint 90mm", "brand": "Zipp", "price": "119.99", "weight_grams": 110},

    # Brakes
    {"component_type": "brake", "name": "105 BR-R7000", "brand": "Shimano", "price": "89.99", "weight_grams": 310},
    {"component_type": "brake", "name": "Rival 22 Caliper", "brand": "SRAM", "price": "79.99", "weight_grams": 295},
    {"component_type": "brake", "name": "Chorus Caliper", "brand": "Campagnolo", "price": "149.99", "weight_grams": 280},

    # Saddles
    {"component_type": "saddle", "name": "Power Pro", "brand": "Specialized", "price": "199.99", "weight_grams": 168},
    {"component_type": "saddle", "name": "Antares R3", "brand": "Fi'zi:k", "price": "179.99", "weight_grams": 175},
    {"component_type": "saddle", "name": "Gobi XC", "brand": "Selle Italia", "price": "149.99", "weight_grams": 190},

    # Seatposts
    {"component_type": "seatpost", "name": "Aerofly Carbon 27.2", "brand": "FSA", "price": "149.99", "weight_grams": 185},
    {"component_type": "seatpost", "name": "S-Works Carbon 27.2", "brand": "Specialized", "price": "199.99", "weight_grams": 168},
    {"component_type": "seatpost", "name": "SL7 Carbon 27.2", "brand": "Zipp", "price": "179.99", "weight_grams": 172},
]


def seed(apps, schema_editor):
    Component = apps.get_model("components", "Components")
    for data in COMPONENTS:
        Component.objects.create(**data)


def unseed(apps, schema_editor):
    Component = apps.get_model("components", "Components")
    Component.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("components", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, reverse_code=unseed),
    ]
