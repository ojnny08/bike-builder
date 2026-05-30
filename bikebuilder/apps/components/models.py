from django.db import models
from ..category.models import Category, BikeType
# Create your models here.

class Components(models.Model):
    category = models.Model(Category, on_delete=models.CASCADE)
    bike_type = models.Model(BikeType, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight_grams = models.PositiveIntegerField(help_text="Weight in grams")
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    affiliate_url = models.URLField(blank=True)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['brand', 'name']
    
    def __str__(self):
        return f"{self.brand} {self.name}"
    

class Frame(Components):
    class Material(models.TextChoices):
        CARBON = 'carbon', 'Carbon'
        ALUMINIUM = 'aluminium', 'Aluminium'
        STEEL = 'steel', 'Steel'

    class HeadTube(models.TextChoices):
        STRAIGHT = 'stright', 'Stright'
        TAPERED = 'tapered', 'Tapered'
    
    class BBShell(models.TextChoices):
        THREADED = "threaded", "Threaded (BSA)"
        PRESS_FIT = "press_fit", "Press Fit"
        T47 = "t47", "T47"
        BB30 = "bb30", "BB30"

    class RearAxleFit(models.TextChoices):
        TRACK = 'track_120', 'Track 120mm' 
        QR_130 = 'qr_130', 'Quick Release 130mm' # older road/fixed 
        QR_135 = 'qr_135', 'Quick Release 135mm'
        THRU_142 = 'thru_142', 'Thru Axle 142mm'
        TRU_142 = 'thur_148', 'Thru Axle 148mm'

    size = models.CharField(max_length=10)
    material = models.CharField(max_length=20, choices=Material.choices)
    bb_shell = models.CharField(max_length=20, choices=BBShell.choices)
    head_tube_type = models.CharField(max_length=20, choices=HeadTube.choices)
    rear_axle_standard = models.CharField(max_length=20, choices=RearAxleFit.choices)
    max_tire_clearance_mm = models.PositiveSmallIntegerField()

    class BottomBracket(Components):
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


class Crankset(Components):
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


class Cassette(Components):
    class FreehubStandard(models.TextChoices):
        HG = "hg", "Shimano HG"
        XD = "xd", "SRAM XD"
        XDR = "xdr", "SRAM XDR"
        MICRO_SPLINE = "micro_spline", "Shimano Micro Spline"

    speeds = models.PositiveSmallIntegerField()
    min_cog = models.PositiveSmallIntegerField()
    max_cog = models.PositiveSmallIntegerField()
    freehub_standard = models.CharField(max_length=20, choices=FreehubStandard.choices)


class RearDerailleur(Components):
    speeds = models.PositiveSmallIntegerField()
    max_cog_size = models.PositiveSmallIntegerField()
    clutch = models.BooleanField(default=False)


class FrontDerailleur(Components):
    class ClampType(models.TextChoices):
        BRAZE_ON = "braze_on", "Braze-on"
        MM_28_6 = "28.6mm", "28.6mm Clamp"
        MM_31_8 = "31.8mm", "31.8mm Clamp"
        DIRECT_MOUNT = "direct_mount", "Direct Mount"

    speeds = models.PositiveSmallIntegerField()
    clamp_type = models.CharField(max_length=20, choices=ClampType.choices)


class Wheel(Components):
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


class Tire(Components):
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


class Handlebar(Components):
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


class Stem(Components):
    length_mm = models.PositiveSmallIntegerField()
    bar_clamp_diameter_mm = models.DecimalField(max_digits=4, decimal_places=1)
    steerer_clamp_diameter_mm = models.DecimalField(max_digits=4, decimal_places=1)
    angle_degrees = models.SmallIntegerField()


class Brake(Components):
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


class Saddle(Components):
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


class Seatpost(Components):
    class PostType(models.TextChoices):
        STANDARD = "standard", "Standard"
        DROPPER = "dropper", "Dropper"

    diameter_mm = models.DecimalField(max_digits=4, decimal_places=1)
    length_mm = models.PositiveSmallIntegerField()
    offset_mm = models.PositiveSmallIntegerField(default=0)
    post_type = models.CharField(max_length=20, choices=PostType.choices, default=PostType.STANDARD)