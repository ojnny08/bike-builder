from django.db import migrations
from decimal import Decimal


def seed(apps, schema_editor):
    Components = apps.get_model("components", "Components")
    Frame = apps.get_model("components", "Frame")
    BottomBracket = apps.get_model("components", "BottomBracket")
    Crankset = apps.get_model("components", "Crankset")
    Cassette = apps.get_model("components", "Cassette")
    RearDerailleur = apps.get_model("components", "RearDerailleur")
    FrontDerailleur = apps.get_model("components", "FrontDerailleur")
    Wheel = apps.get_model("components", "Wheel")
    Tire = apps.get_model("components", "Tire")
    Handlebar = apps.get_model("components", "Handlebar")
    Stem = apps.get_model("components", "Stem")
    Brake = apps.get_model("components", "Brake")
    Saddle = apps.get_model("components", "Saddle")
    Seatpost = apps.get_model("components", "Seatpost")

    Components.objects.all().delete()

    # ── Frames ────────────────────────────────────────────────────────────────

    # Road frames
    Frame.objects.create(
        component_type="frame",
        name="Domane SL 6",
        brand="Trek",
        price=Decimal("2799.99"),
        weight_grams=1050,
        in_stock=True,
        size="56cm",
        material="carbon",
        bb_shell="threaded",
        head_tube_type="tapered",
        rear_axle_standard="thru_142",
        max_tire_clearance_mm=35,
    )
    Frame.objects.create(
        component_type="frame",
        name="Roubaix Sport",
        brand="Specialized",
        price=Decimal("1999.99"),
        weight_grams=980,
        in_stock=True,
        size="56cm",
        material="carbon",
        bb_shell="threaded",
        head_tube_type="tapered",
        rear_axle_standard="thru_142",
        max_tire_clearance_mm=33,
    )
    Frame.objects.create(
        component_type="frame",
        name="TCR Advanced",
        brand="Giant",
        price=Decimal("2499.99"),
        weight_grams=920,
        in_stock=True,
        size="M",
        material="carbon",
        bb_shell="press_fit",
        head_tube_type="tapered",
        rear_axle_standard="thru_142",
        max_tire_clearance_mm=28,
    )

    # Fixed gear frames
    Frame.objects.create(
        component_type="frame",
        name="4130 Core Line",
        brand="State Bicycle Co.",
        price=Decimal("299.99"),
        weight_grams=2400,
        description="Classic 4130 Chromoly steel frame built for urban commuting and street riding.",
        in_stock=True,
        size="58cm",
        material="steel",
        bb_shell="threaded",
        head_tube_type="stright",
        rear_axle_standard="track_120",
        max_tire_clearance_mm=28,
    )
    Frame.objects.create(
        component_type="frame",
        name="Vigorelli Track",
        brand="Cinelli",
        price=Decimal("899.00"),
        weight_grams=1570,
        description="High-performance Columbus Airplane aluminum track frame designed for crit racing.",
        in_stock=True,
        size="55cm",
        material="aluminium",
        bb_shell="threaded",
        head_tube_type="stright",
        rear_axle_standard="track_120",
        max_tire_clearance_mm=25,
    )
    Frame.objects.create(
        component_type="frame",
        name="Pre Cursa",
        brand="Dolan",
        price=Decimal("350.00"),
        weight_grams=1780,
        description="The quintessential entry-level track racing frame, known for absolute durability.",
        in_stock=True,
        size="57cm",
        material="aluminium",
        bb_shell="threaded",
        head_tube_type="stright",
        rear_axle_standard="track_120",
        max_tire_clearance_mm=25,
    )
    Frame.objects.create(
        component_type="frame",
        name="Crit-D Track",
        brand="Engine 11",
        price=Decimal("750.00"),
        weight_grams=1480,
        description="Lightweight aluminum frame with a carbon fork, engineered for aggressive crit racing.",
        in_stock=True,
        size="55cm",
        material="aluminium",
        bb_shell="threaded",
        head_tube_type="stright",
        rear_axle_standard="track_120",
        max_tire_clearance_mm=25,
    )
    Frame.objects.create(
        component_type="frame",
        name="Rush",
        brand="Soma",
        price=Decimal("629.99"),
        weight_grams=2100,
        description="Tange Prestige heat-treated steel street track frame with traditional geometry.",
        in_stock=True,
        size="58cm",
        material="steel",
        bb_shell="threaded",
        head_tube_type="stright",
        rear_axle_standard="track_120",
        max_tire_clearance_mm=28,
    )

    # ── Forks (no subclass model — base component only) ───────────────────────

    for name, brand, price, weight in [
        ("Road Fork Carbon", "Enve", "599.99", 380),
        ("Future Shock Fork", "Specialized", "449.99", 420),
        ("Advanced SL Fork", "Giant", "349.99", 395),
    ]:
        Components.objects.create(
            component_type="fork",
            name=name,
            brand=brand,
            price=Decimal(price),
            weight_grams=weight,
            in_stock=True,
        )

    # ── Bottom Brackets ───────────────────────────────────────────────────────

    # Road BBs
    BottomBracket.objects.create(
        component_type="bottom_bracket",
        name="BB-R9100",
        brand="Shimano",
        price=Decimal("49.99"),
        weight_grams=75,
        in_stock=True,
        shell_type="threaded",
        spindle_interface="24mm",
        shell_width_mm=68,
    )
    BottomBracket.objects.create(
        component_type="bottom_bracket",
        name="DUB BSA",
        brand="SRAM",
        price=Decimal("59.99"),
        weight_grams=70,
        in_stock=True,
        shell_type="threaded",
        spindle_interface="dub",
        shell_width_mm=68,
    )
    BottomBracket.objects.create(
        component_type="bottom_bracket",
        name="T47 Road",
        brand="Chris King",
        price=Decimal("179.99"),
        weight_grams=65,
        in_stock=True,
        shell_type="t47",
        spindle_interface="24mm",
        shell_width_mm=68,
    )

    # Fixed gear BBs
    BottomBracket.objects.create(
        component_type="bottom_bracket",
        name="75 Super Lap ISO",
        brand="Sugino",
        price=Decimal("175.00"),
        weight_grams=245,
        description="High-end ISO taper bottom bracket featuring mirror-polished races for smooth spinning.",
        in_stock=True,
        shell_type="threaded",
        spindle_interface="square_taper",
        shell_width_mm=110,
    )
    BottomBracket.objects.create(
        component_type="bottom_bracket",
        name="LN-7611 JIS 110mm",
        brand="Tange Seiki",
        price=Decimal("35.00"),
        weight_grams=290,
        description="Affordable and durable sealed cartridge JIS square taper bottom bracket.",
        in_stock=True,
        shell_type="threaded",
        spindle_interface="square_taper",
        shell_width_mm=110,
    )
    BottomBracket.objects.create(
        component_type="bottom_bracket",
        name="Dura-Ace BB-7710 Octalink",
        brand="Shimano",
        price=Decimal("95.00"),
        weight_grams=240,
        description="NJS approved splined track bottom bracket, strictly compatible with V1 Octalink cranks.",
        in_stock=True,
        shell_type="threaded",
        spindle_interface="isis",
        shell_width_mm=110,
    )
    BottomBracket.objects.create(
        component_type="bottom_bracket",
        name="Evo Max BSA",
        brand="Miche",
        price=Decimal("42.00"),
        weight_grams=135,
        description="Outboard bearing bottom bracket designed for modern 24mm axle track cranksets.",
        in_stock=True,
        shell_type="threaded",
        spindle_interface="24mm",
        shell_width_mm=68,
    )
    BottomBracket.objects.create(
        component_type="bottom_bracket",
        name="GXP Team BSA",
        brand="SRAM",
        price=Decimal("45.00"),
        weight_grams=105,
        description="The standard external bearing bottom bracket paired with classic SRAM Omnium cranks.",
        in_stock=True,
        shell_type="threaded",
        spindle_interface="dub",
        shell_width_mm=68,
    )

    # ── Cranksets ─────────────────────────────────────────────────────────────

    Crankset.objects.create(
        component_type="crankset",
        name="105 FC-R7100",
        brand="Shimano",
        price=Decimal("179.99"),
        weight_grams=710,
        in_stock=True,
        spindle_interface="24mm",
        arm_length_mm=172,
        chainring_count=2,
        bcd=110,
        speeds=12,
    )
    Crankset.objects.create(
        component_type="crankset",
        name="Rival AXS",
        brand="SRAM",
        price=Decimal("299.99"),
        weight_grams=680,
        in_stock=True,
        spindle_interface="dub",
        arm_length_mm=172,
        chainring_count=2,
        bcd=None,
        speeds=12,
    )
    Crankset.objects.create(
        component_type="crankset",
        name="Chorus Crankset",
        brand="Campagnolo",
        price=Decimal("349.99"),
        weight_grams=660,
        in_stock=True,
        spindle_interface="24mm",
        arm_length_mm=172,
        chainring_count=2,
        bcd=112,
        speeds=12,
    )

    # ── Cassettes ─────────────────────────────────────────────────────────────

    Cassette.objects.create(
        component_type="cassette",
        name="CS-R7100 11-34",
        brand="Shimano",
        price=Decimal("59.99"),
        weight_grams=295,
        in_stock=True,
        speeds=12,
        min_cog=11,
        max_cog=34,
        freehub_standard="hg",
    )
    Cassette.objects.create(
        component_type="cassette",
        name="Rival AXS 10-36",
        brand="SRAM",
        price=Decimal("89.99"),
        weight_grams=270,
        in_stock=True,
        speeds=12,
        min_cog=10,
        max_cog=36,
        freehub_standard="xdr",
    )
    Cassette.objects.create(
        component_type="cassette",
        name="Chorus 11-29",
        brand="Campagnolo",
        price=Decimal("129.99"),
        weight_grams=245,
        in_stock=True,
        speeds=12,
        min_cog=11,
        max_cog=29,
        freehub_standard="hg",
    )

    # ── Rear Derailleurs ──────────────────────────────────────────────────────

    RearDerailleur.objects.create(
        component_type="rear_derailleur",
        name="105 RD-R7100",
        brand="Shimano",
        price=Decimal("109.99"),
        weight_grams=253,
        in_stock=True,
        speeds=12,
        max_cog_size=34,
        clutch=False,
    )
    RearDerailleur.objects.create(
        component_type="rear_derailleur",
        name="Rival AXS RD",
        brand="SRAM",
        price=Decimal("249.99"),
        weight_grams=230,
        in_stock=True,
        speeds=12,
        max_cog_size=36,
        clutch=False,
    )
    RearDerailleur.objects.create(
        component_type="rear_derailleur",
        name="Chorus RD",
        brand="Campagnolo",
        price=Decimal("199.99"),
        weight_grams=210,
        in_stock=True,
        speeds=12,
        max_cog_size=29,
        clutch=False,
    )

    # ── Front Derailleurs ─────────────────────────────────────────────────────

    FrontDerailleur.objects.create(
        component_type="front_derailleur",
        name="105 FD-R7100",
        brand="Shimano",
        price=Decimal("49.99"),
        weight_grams=91,
        in_stock=True,
        speeds=12,
        clamp_type="braze_on",
    )
    FrontDerailleur.objects.create(
        component_type="front_derailleur",
        name="Rival AXS FD",
        brand="SRAM",
        price=Decimal("149.99"),
        weight_grams=85,
        in_stock=True,
        speeds=12,
        clamp_type="braze_on",
    )
    FrontDerailleur.objects.create(
        component_type="front_derailleur",
        name="Chorus FD",
        brand="Campagnolo",
        price=Decimal("99.99"),
        weight_grams=88,
        in_stock=True,
        speeds=12,
        clamp_type="braze_on",
    )

    # ── Wheels ────────────────────────────────────────────────────────────────

    # Road wheels
    Wheel.objects.create(
        component_type="wheel",
        name="Aeolus RSL 37",
        brand="Bontrager",
        price=Decimal("1499.99"),
        weight_grams=1450,
        in_stock=True,
        wheel_size="700c",
        position="rear",
        axle_standard="thru_142",
        max_tire_width_mm=32,
        tubeless_ready=True,
    )
    Wheel.objects.create(
        component_type="wheel",
        name="Roval Alpinist CL",
        brand="Specialized",
        price=Decimal("1799.99"),
        weight_grams=1320,
        in_stock=True,
        wheel_size="700c",
        position="rear",
        axle_standard="thru_142",
        max_tire_width_mm=30,
        tubeless_ready=True,
    )
    Wheel.objects.create(
        component_type="wheel",
        name="SLR 1 Carbon",
        brand="Giant",
        price=Decimal("999.99"),
        weight_grams=1480,
        in_stock=True,
        wheel_size="700c",
        position="rear",
        axle_standard="thru_142",
        max_tire_width_mm=28,
        tubeless_ready=True,
    )

    # Fixed gear wheels
    Wheel.objects.create(
        component_type="wheel",
        name="Ellipse Front Wheel",
        brand="Mavic",
        price=Decimal("249.00"),
        weight_grams=990,
        description="Aerodynamic deep-section aluminum track wheel.",
        in_stock=True,
        wheel_size="700c",
        position="front",
        axle_standard="qr_100",
        max_tire_width_mm=25,
        tubeless_ready=False,
    )
    Wheel.objects.create(
        component_type="wheel",
        name="Ellipse Rear Wheel",
        brand="Mavic",
        price=Decimal("299.00"),
        weight_grams=1100,
        description="Double-sided fixed/fixed flip-flop rear track wheel.",
        in_stock=True,
        wheel_size="700c",
        position="rear",
        axle_standard="qr_135",
        max_tire_width_mm=25,
        tubeless_ready=False,
    )
    Wheel.objects.create(
        component_type="wheel",
        name="Archetype Track Rear",
        brand="H Plus Son",
        price=Decimal("180.00"),
        weight_grams=970,
        description="Classic wide-profile box rim laced to a Gran Compe sealed bearing hub.",
        in_stock=True,
        wheel_size="700c",
        position="rear",
        axle_standard="qr_135",
        max_tire_width_mm=28,
        tubeless_ready=False,
    )

    # ── Tires ─────────────────────────────────────────────────────────────────

    # Road tires
    Tire.objects.create(
        component_type="tire",
        name="GP5000 700x25",
        brand="Continental",
        price=Decimal("59.99"),
        weight_grams=210,
        in_stock=True,
        wheel_size="700c",
        width_mm=25,
        tubeless_ready=True,
        tread_type="slick",
    )
    Tire.objects.create(
        component_type="tire",
        name="Turbo Cotton 700x26",
        brand="Specialized",
        price=Decimal("79.99"),
        weight_grams=195,
        in_stock=True,
        wheel_size="700c",
        width_mm=26,
        tubeless_ready=True,
        tread_type="slick",
    )
    Tire.objects.create(
        component_type="tire",
        name="Corsa Speed 700x28",
        brand="Vittoria",
        price=Decimal("69.99"),
        weight_grams=205,
        in_stock=True,
        wheel_size="700c",
        width_mm=28,
        tubeless_ready=True,
        tread_type="slick",
    )

    # Fixed gear tires
    Tire.objects.create(
        component_type="tire",
        name="Gatorskin 700x25c",
        brand="Continental",
        price=Decimal("59.99"),
        weight_grams=240,
        description="The standard tire for fixed-gear street riding due to high flat resistance and thick casing.",
        in_stock=True,
        wheel_size="700c",
        width_mm=25,
        tubeless_ready=False,
        tread_type="slick",
    )
    Tire.objects.create(
        component_type="tire",
        name="Thickslick Comp",
        brand="WTB",
        price=Decimal("38.00"),
        weight_grams=460,
        description="Heavy, ultra-thick rubber compound designed explicitly to endure sliding.",
        in_stock=True,
        wheel_size="700c",
        width_mm=32,
        tubeless_ready=False,
        tread_type="slick",
    )
    Tire.objects.create(
        component_type="tire",
        name="Pasela PT Tanwall",
        brand="Panaracer",
        price=Decimal("45.00"),
        weight_grams=290,
        description="Classic gumwall styling paired with good puncture protection.",
        in_stock=True,
        wheel_size="700c",
        width_mm=28,
        tubeless_ready=False,
        tread_type="semi_slick",
    )

    # ── Handlebars ────────────────────────────────────────────────────────────

    # Road handlebars
    Handlebar.objects.create(
        component_type="handlebar",
        name="Pro Vibe Carbon",
        brand="Shimano",
        price=Decimal("149.99"),
        weight_grams=210,
        in_stock=True,
        bar_type="drop",
        width_mm=420,
        clamp_diameter_mm=Decimal("31.8"),
        drop_mm=125,
        reach_mm=80,
    )
    Handlebar.objects.create(
        component_type="handlebar",
        name="Aerofly II",
        brand="FSA",
        price=Decimal("129.99"),
        weight_grams=225,
        in_stock=True,
        bar_type="drop",
        width_mm=420,
        clamp_diameter_mm=Decimal("31.8"),
        drop_mm=128,
        reach_mm=75,
    )
    Handlebar.objects.create(
        component_type="handlebar",
        name="Cockpit SL Drop",
        brand="Zipp",
        price=Decimal("199.99"),
        weight_grams=195,
        in_stock=True,
        bar_type="drop",
        width_mm=420,
        clamp_diameter_mm=Decimal("31.8"),
        drop_mm=128,
        reach_mm=78,
    )

    # Fixed gear handlebars
    Handlebar.objects.create(
        component_type="handlebar",
        name="B809AA Riser Bar",
        brand="Nitto",
        price=Decimal("68.00"),
        weight_grams=310,
        description="Premium aluminum riser handlebar loved for city filtering.",
        in_stock=True,
        bar_type="riser",
        width_mm=560,
        clamp_diameter_mm=Decimal("25.4"),
    )
    Handlebar.objects.create(
        component_type="handlebar",
        name="B123AA NJS Drop Bar",
        brand="Nitto",
        price=Decimal("92.00"),
        weight_grams=380,
        description="Classic deep alloy track drops with NJS certification.",
        in_stock=True,
        bar_type="drop",
        width_mm=420,
        clamp_diameter_mm=Decimal("26.0"),
        drop_mm=120,
        reach_mm=75,
    )
    Handlebar.objects.create(
        component_type="handlebar",
        name="Crononero Bullhorn",
        brand="Deda Elementi",
        price=Decimal("52.00"),
        weight_grams=285,
        description="Aerodynamic aluminum bullhorn bar for urban tracking.",
        in_stock=True,
        bar_type="bullhorn",
        width_mm=420,
        clamp_diameter_mm=Decimal("26.0"),
    )

    # ── Stems ─────────────────────────────────────────────────────────────────

    # Road stems
    Stem.objects.create(
        component_type="stem",
        name="Pro Vibe Stem 100mm",
        brand="Shimano",
        price=Decimal("79.99"),
        weight_grams=128,
        in_stock=True,
        length_mm=100,
        bar_clamp_diameter_mm=Decimal("31.8"),
        steerer_clamp_diameter_mm=Decimal("28.6"),
        angle_degrees=6,
    )
    Stem.objects.create(
        component_type="stem",
        name="SL-K Stem 110mm",
        brand="FSA",
        price=Decimal("99.99"),
        weight_grams=118,
        in_stock=True,
        length_mm=110,
        bar_clamp_diameter_mm=Decimal("31.8"),
        steerer_clamp_diameter_mm=Decimal("28.6"),
        angle_degrees=6,
    )
    Stem.objects.create(
        component_type="stem",
        name="SL Sprint 90mm",
        brand="Zipp",
        price=Decimal("119.99"),
        weight_grams=110,
        in_stock=True,
        length_mm=90,
        bar_clamp_diameter_mm=Decimal("31.8"),
        steerer_clamp_diameter_mm=Decimal("28.6"),
        angle_degrees=-6,
    )

    # Fixed gear stems
    Stem.objects.create(
        component_type="stem",
        name="Elite X4 Stem",
        brand="Thomson",
        price=Decimal("114.00"),
        weight_grams=160,
        description="CNC-machined from a single block of aluminum. Unmatched strength.",
        in_stock=True,
        length_mm=100,
        bar_clamp_diameter_mm=Decimal("31.8"),
        steerer_clamp_diameter_mm=Decimal("28.6"),
        angle_degrees=0,
    )
    Stem.objects.create(
        component_type="stem",
        name="Pearl NJS Quill",
        brand="Nitto",
        price=Decimal("105.00"),
        weight_grams=330,
        description="Forged aluminum quill stem for traditional threaded headsets.",
        in_stock=True,
        length_mm=100,
        bar_clamp_diameter_mm=Decimal("25.4"),
        steerer_clamp_diameter_mm=Decimal("25.4"),
        angle_degrees=0,
    )

    # ── Brakes ────────────────────────────────────────────────────────────────

    Brake.objects.create(
        component_type="brake",
        name="105 BR-R7000",
        brand="Shimano",
        price=Decimal("89.99"),
        weight_grams=310,
        in_stock=True,
        brake_type="rim_caliper",
        mount_type="",
        position="front",
    )
    Brake.objects.create(
        component_type="brake",
        name="Rival 22 Caliper",
        brand="SRAM",
        price=Decimal("79.99"),
        weight_grams=295,
        in_stock=True,
        brake_type="rim_caliper",
        mount_type="",
        position="front",
    )
    Brake.objects.create(
        component_type="brake",
        name="Chorus Caliper",
        brand="Campagnolo",
        price=Decimal("149.99"),
        weight_grams=280,
        in_stock=True,
        brake_type="rim_caliper",
        mount_type="",
        position="front",
    )

    # ── Saddles ───────────────────────────────────────────────────────────────

    Saddle.objects.create(
        component_type="saddle",
        name="Power Pro",
        brand="Specialized",
        price=Decimal("199.99"),
        weight_grams=168,
        in_stock=True,
        width_mm=143,
        rail_type="round",
        rail_material="carbon",
    )
    Saddle.objects.create(
        component_type="saddle",
        name="Antares R3",
        brand="Fi'zi:k",
        price=Decimal("179.99"),
        weight_grams=175,
        in_stock=True,
        width_mm=140,
        rail_type="round",
        rail_material="carbon",
    )
    Saddle.objects.create(
        component_type="saddle",
        name="Gobi XC",
        brand="Selle Italia",
        price=Decimal("149.99"),
        weight_grams=190,
        in_stock=True,
        width_mm=130,
        rail_type="round",
        rail_material="steel",
    )

    # ── Seatposts ─────────────────────────────────────────────────────────────

    Seatpost.objects.create(
        component_type="seatpost",
        name="Aerofly Carbon 27.2",
        brand="FSA",
        price=Decimal("149.99"),
        weight_grams=185,
        in_stock=True,
        diameter_mm=Decimal("27.2"),
        length_mm=350,
        offset_mm=0,
        post_type="standard",
    )
    Seatpost.objects.create(
        component_type="seatpost",
        name="S-Works Carbon 27.2",
        brand="Specialized",
        price=Decimal("199.99"),
        weight_grams=168,
        in_stock=True,
        diameter_mm=Decimal("27.2"),
        length_mm=350,
        offset_mm=20,
        post_type="standard",
    )
    Seatpost.objects.create(
        component_type="seatpost",
        name="SL7 Carbon 27.2",
        brand="Zipp",
        price=Decimal("179.99"),
        weight_grams=172,
        in_stock=True,
        diameter_mm=Decimal("27.2"),
        length_mm=400,
        offset_mm=0,
        post_type="standard",
    )


def unseed(apps, schema_editor):
    Components = apps.get_model("components", "Components")
    Components.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("components", "0006_seed_fixed_handlebars_stems"),
    ]

    operations = [
        migrations.RunPython(seed, reverse_code=unseed),
    ]
