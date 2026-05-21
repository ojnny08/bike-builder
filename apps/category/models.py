from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class BikeType(models.Model):
    class Slug(models.TextChoices):
        ROAD = "road", "Road"
        MOUNTAIN = "mountain", "Mountain"
        GRAVEL = "gravel", "Gravel"
        FIXED = "fixed", "Fixed Gear"

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, choices=Slug.choices)

    def __str__(self):
        return self.name


class BikeTypeComponentRule(models.Model):
    class ComponentType(models.TextChoices):
        FRAME = "frame", "Frame"
        FORK = "fork", "Fork"
        BOTTOM_BRACKET = "bottom_bracket", "Bottom Bracket"
        CRANKSET = "crankset", "Crankset"
        CASSETTE = "cassette", "Cassette"
        REAR_DERAILLEUR = "rear_derailleur", "Rear Derailleur"
        FRONT_DERAILLEUR = "front_derailleur", "Front Derailleur"
        WHEEL = "wheel", "Wheel"
        TIRE = "tire", "Tire"
        HANDLEBAR = "handlebar", "Handlebar"
        STEM = "stem", "Stem"
        BRAKE = "brake", "Brake"
        SADDLE = "saddle", "Saddle"
        SEATPOST = "seatpost", "Seatpost"

    bike_type = models.ForeignKey(BikeType, on_delete=models.CASCADE, related_name="component_rules")
    component_type = models.CharField(max_length=30, choices=ComponentType.choices)
    required = models.BooleanField()

    class Meta:
        unique_together = ("bike_type", "component_type")

    def __str__(self):
        status = "required" if self.required else "optional"
        return f"{self.bike_type} — {self.get_component_type_display()} ({status})"


class Component(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="components")
    bike_types = models.ManyToManyField(BikeType, blank=True)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight_grams = models.PositiveIntegerField(help_text="Weight in grams")
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    affiliate_url = models.URLField(blank=True)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["brand", "name"]

    def __str__(self):
        return f"{self.brand} {self.name}"


class Frame(Component):
    class Material(models.TextChoices):
        CARBON = "carbon", "Carbon"
        ALUMINUM = "aluminum", "Aluminum"
        STEEL = "steel", "Steel"
        TITANIUM = "titanium", "Titanium"

    class BBShell(models.TextChoices):
        THREADED = "threaded", "Threaded (BSA)"
        PRESS_FIT = "press_fit", "Press Fit"
        T47 = "t47", "T47"
        BB30 = "bb30", "BB30"

    class HeadTubeType(models.TextChoices):
        TAPERED = "tapered", "Tapered"
        STRAIGHT = "straight", "Straight"

    class RearAxleStandard(models.TextChoices):
        QR_135 = "qr_135", "Quick Release 135mm"
        THRU_142 = "thru_142", "Thru Axle 142mm"
        THRU_148 = "thru_148", "Thru Axle 148mm (Boost)"

    size = models.CharField(max_length=10)
    material = models.CharField(max_length=20, choices=Material.choices)
    bb_shell = models.CharField(max_length=20, choices=BBShell.choices)
    head_tube_type = models.CharField(max_length=20, choices=HeadTubeType.choices)
    rear_axle_standard = models.CharField(max_length=20, choices=RearAxleStandard.choices)
    max_tire_clearance_mm = models.PositiveSmallIntegerField()


class Fork(Component):
    class SteererDiameter(models.TextChoices):
        STRAIGHT = "straight", 'Straight (1 1/8")'
        TAPERED = "tapered", "Tapered"

    class FrontAxleStandard(models.TextChoices):
        QR_100 = "qr_100", "Quick Release 100mm"
        THRU_100 = "thru_100", "Thru Axle 100mm"
        THRU_110 = "thru_110", "Thru Axle 110mm (Boost)"

    steerer_diameter = models.CharField(max_length=20, choices=SteererDiameter.choices)
    front_axle_standard = models.CharField(max_length=20, choices=FrontAxleStandard.choices)
    travel_mm = models.PositiveSmallIntegerField(null=True, blank=True)
    max_tire_clearance_mm = models.PositiveSmallIntegerField()


class BottomBracket(Component):
    class ShellType(models.TextChoices):
        THREADED = "threaded", "Threaded (BSA)"
        PRESS_FIT = "press_fit", "Press Fit"
        T47 = "t47", "T47"
        BB30 = "bb30", "BB30"

    class SpindleInterface(models.TextChoices):
        SQUARE_TAPER = "square_taper", "Square Taper"
        ISIS = "isis", "ISIS/Octalink"
        MM_24 = "24mm", "24mm (Shimano/SRAM)"
        MM_30 = "30mm", "30mm (BB30)"
        DUB = "dub", "SRAM DUB"

    shell_type = models.CharField(max_length=20, choices=ShellType.choices)
    spindle_interface = models.CharField(max_length=20, choices=SpindleInterface.choices)
    shell_width_mm = models.PositiveSmallIntegerField()


class Crankset(Component):
    class SpindleInterface(models.TextChoices):
        SQUARE_TAPER = "square_taper", "Square Taper"
        ISIS = "isis", "ISIS/Octalink"
        MM_24 = "24mm", "24mm (Shimano)"
        MM_30 = "30mm", "30mm (SRAM)"
        DUB = "dub", "SRAM DUB"

    spindle_interface = models.CharField(max_length=20, choices=SpindleInterface.choices)
    arm_length_mm = models.PositiveSmallIntegerField()
    chainring_count = models.PositiveSmallIntegerField()
    bcd = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Bolt circle diameter in mm, null for direct mount")
    speeds = models.PositiveSmallIntegerField(help_text="1 for single speed / fixed")


class Cassette(Component):
    class FreehubStandard(models.TextChoices):
        HG = "hg", "Shimano HG"
        XD = "xd", "SRAM XD"
        XDR = "xdr", "SRAM XDR"
        MICRO_SPLINE = "micro_spline", "Shimano Micro Spline"

    speeds = models.PositiveSmallIntegerField()
    min_cog = models.PositiveSmallIntegerField()
    max_cog = models.PositiveSmallIntegerField()
    freehub_standard = models.CharField(max_length=20, choices=FreehubStandard.choices)


class RearDerailleur(Component):
    speeds = models.PositiveSmallIntegerField()
    max_cog_size = models.PositiveSmallIntegerField()
    clutch = models.BooleanField(default=False)


class FrontDerailleur(Component):
    class ClampType(models.TextChoices):
        BRAZE_ON = "braze_on", "Braze-on"
        MM_28_6 = "28.6mm", "28.6mm Clamp"
        MM_31_8 = "31.8mm", "31.8mm Clamp"
        DIRECT_MOUNT = "direct_mount", "Direct Mount"

    speeds = models.PositiveSmallIntegerField()
    clamp_type = models.CharField(max_length=20, choices=ClampType.choices)


class Wheel(Component):
    class WheelSize(models.TextChoices):
        TWENTY_SIX = "26", '26"'
        TWENTY_SEVEN_FIVE = "27.5", '27.5"'
        TWENTY_NINE = "29", '29"'
        SEVEN_HUNDRED = "700c", "700c"
        SIX_FIFTY = "650b", "650b"

    class Position(models.TextChoices):
        FRONT = "front", "Front"
        REAR = "rear", "Rear"

    class AxleStandard(models.TextChoices):
        QR_FRONT = "qr_100", "Quick Release Front (100mm)"
        QR_REAR = "qr_135", "Quick Release Rear (135mm)"
        THRU_FRONT = "thru_100", "Thru Axle Front (100mm)"
        THRU_FRONT_BOOST = "thru_110", "Thru Axle Front Boost (110mm)"
        THRU_REAR = "thru_142", "Thru Axle Rear (142mm)"
        THRU_REAR_BOOST = "thru_148", "Thru Axle Rear Boost (148mm)"

    wheel_size = models.CharField(max_length=10, choices=WheelSize.choices)
    position = models.CharField(max_length=10, choices=Position.choices)
    axle_standard = models.CharField(max_length=20, choices=AxleStandard.choices)
    max_tire_width_mm = models.PositiveSmallIntegerField()
    tubeless_ready = models.BooleanField(default=False)


class Tire(Component):
    class WheelSize(models.TextChoices):
        TWENTY_SIX = "26", '26"'
        TWENTY_SEVEN_FIVE = "27.5", '27.5"'
        TWENTY_NINE = "29", '29"'
        SEVEN_HUNDRED = "700c", "700c"
        SIX_FIFTY = "650b", "650b"

    class TreadType(models.TextChoices):
        SLICK = "slick", "Slick"
        SEMI_SLICK = "semi_slick", "Semi-Slick"
        KNOBBY = "knobby", "Knobby"

    wheel_size = models.CharField(max_length=10, choices=WheelSize.choices)
    width_mm = models.PositiveSmallIntegerField()
    tubeless_ready = models.BooleanField(default=False)
    tread_type = models.CharField(max_length=20, choices=TreadType.choices)


class Handlebar(Component):
    class BarType(models.TextChoices):
        DROP = "drop", "Drop"
        FLAT = "flat", "Flat"
        RISER = "riser", "Riser"
        BULLHORN = "bullhorn", "Bullhorn"

    bar_type = models.CharField(max_length=20, choices=BarType.choices)
    width_mm = models.PositiveSmallIntegerField()
    clamp_diameter_mm = models.DecimalField(max_digits=4, decimal_places=1)
    drop_mm = models.PositiveSmallIntegerField(null=True, blank=True)
    reach_mm = models.PositiveSmallIntegerField(null=True, blank=True)


class Stem(Component):
    length_mm = models.PositiveSmallIntegerField()
    bar_clamp_diameter_mm = models.DecimalField(max_digits=4, decimal_places=1)
    steerer_clamp_diameter_mm = models.DecimalField(max_digits=4, decimal_places=1)
    angle_degrees = models.SmallIntegerField()


class Brake(Component):
    class BrakeType(models.TextChoices):
        RIM_CALIPER = "rim_caliper", "Rim Caliper"
        RIM_CANTILEVER = "rim_cantilever", "Rim Cantilever"
        DISC_MECHANICAL = "disc_mechanical", "Disc Mechanical"
        DISC_HYDRAULIC = "disc_hydraulic", "Disc Hydraulic"

    class MountType(models.TextChoices):
        FLAT_MOUNT = "flat_mount", "Flat Mount"
        POST_MOUNT = "post_mount", "Post Mount"
        IS_MOUNT = "is_mount", "IS Mount"

    class Position(models.TextChoices):
        FRONT = "front", "Front"
        REAR = "rear", "Rear"

    brake_type = models.CharField(max_length=20, choices=BrakeType.choices)
    mount_type = models.CharField(max_length=20, choices=MountType.choices, blank=True)
    rotor_size_mm = models.PositiveSmallIntegerField(null=True, blank=True)
    position = models.CharField(max_length=10, choices=Position.choices)


class Saddle(Component):
    class RailType(models.TextChoices):
        ROUND = "round", "Round"
        OVAL = "oval", "Oval"

    class RailMaterial(models.TextChoices):
        STEEL = "steel", "Steel"
        TITANIUM = "titanium", "Titanium"
        CARBON = "carbon", "Carbon"

    width_mm = models.PositiveSmallIntegerField()
    rail_type = models.CharField(max_length=10, choices=RailType.choices)
    rail_material = models.CharField(max_length=20, choices=RailMaterial.choices)


class Seatpost(Component):
    class PostType(models.TextChoices):
        STANDARD = "standard", "Standard"
        DROPPER = "dropper", "Dropper"

    diameter_mm = models.DecimalField(max_digits=4, decimal_places=1)
    length_mm = models.PositiveSmallIntegerField()
    offset_mm = models.PositiveSmallIntegerField(default=0)
    post_type = models.CharField(max_length=20, choices=PostType.choices, default=PostType.STANDARD)
