from django.db import models
from ..category.models import BikeType


class ComponentType(models.TextChoices):
    FRAME = "frame", "Frame"
    BOTTOM_BRACKET = "bottom_bracket", "Bottom Bracket"
    CRANKSET = "crankset", "Crankset"
    CHAINRING = "chainring", "Chainring"
    SPROCKET = "sprocket", "Sprocket"
    CHAIN = "chain", "Chain"
    WHEEL = "wheel", "Wheel"
    TRACKHUB = "track_hub", "Track Hub"
    TIRE = "tire", "Tire"
    HANDLEBAR = "handlebar", "Handlebar"
    STEM = "stem", "Stem"
    BRAKE = "brake", "Brake"
    SADDLE = "saddle", "Saddle"
    SEATPOST = "seatpost", "Seatpost"
    PEDALS = "pedals", "Pedals"
   


class Components(models.Model):
    component_type = models.CharField(max_length=30, choices=ComponentType.choices)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight_grams = models.PositiveIntegerField(help_text="Weight in grams")
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ['brand', 'name']
        indexes = [
            models.Index(fields=['component_type', 'brand', 'name']),
        ]

    def __str__(self):
        return f"{self.brand} {self.name}"
    

class Frame(Components):
    class Generation(models.TextChoices):
        MODERN = "modern", "Modern"
        VINTAGE = "vintage", "Vintage"

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
        THRU_148 = 'thur_148', 'Thru Axle 148mm'

    size = models.CharField(max_length=10)
    bb_shell = models.CharField(max_length=20, choices=BBShell.choices)
    rear_axle_standard = models.CharField(max_length=20, choices=RearAxleFit.choices)
    max_tire_clearance_mm = models.PositiveSmallIntegerField()


class BottomBracket(Components):
    class ShellType(models.TextChoices):
        THREADED_BSA = "threaded_bsa", "Threaded (BSA/English)"
        THREADED_ITA = "threaded_ita", "Threaded (Italian)"
        T47 = "t47", "T47 Threaded"
        
        PRESS_FIT_86_92 = "pf86_92", "Press Fit (BB86/BB92)"
        PRESS_FIT_30 = "pf30", "PressFit 30"
        BB30 = "bb30", "BB30"

    class SpindleInterface(models.TextChoices):
        # Square Taper
        SQUARE_TAPER_ISO = "square_taper_iso", "Square Taper ISO"
        SQUARE_TAPER_JIS = "square_taper_jis", "Square Taper JIS"
        
        OCTALINK = "octalink", "Shimano Octalink"
        ISIS = "isis", "ISIS Drive"
        
        MM_24 = "24mm", "24mm (Shimano Hollowtech II)"
        GXP = "gxp", "SRAM GXP (24mm/22mm stepped)"
        MM_30 = "30mm", "30mm (BB30/386EVO)"
        DUB = "dub", "SRAM DUB (28.99mm)"

    shell_type = models.CharField(max_length=20, choices=ShellType.choices)
    spindle_interface = models.CharField(max_length=20, choices=SpindleInterface.choices)
    shell_width_mm = models.PositiveSmallIntegerField()


class Crankset(Components):
    class SpindleInterface(models.TextChoices):
        # Square Taper
        SQUARE_TAPER_ISO = "square_taper_iso", "Square Taper ISO"
        SQUARE_TAPER_JIS = "square_taper_jis", "Square Taper JIS"
        
        OCTALINK = "octalink", "Shimano Octalink"
        ISIS = "isis", "ISIS Drive"
        
        MM_24 = "24mm", "24mm (Shimano Hollowtech II)"
        GXP = "gxp", "SRAM GXP (24mm/22mm stepped)"
        MM_30 = "30mm", "30mm (BB30/386EVO)"
        DUB = "dub", "SRAM DUB (28.99mm)"
    
    class ArmLength(models.TextChoices):
        ARM_160mm = "160mm", "160mm"
        ARM_165mm = "165mm", "165mm"
        ARM_170mm = "170mm", "170mm"

    spindle_interface = models.CharField(max_length=20, choices=SpindleInterface.choices)
    arm_length_mm = models.CharField(max_length=5, choices=ArmLength.choices)

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
        TRACK = "track_120", "Track 120mm"
        QR_FRONT = "qr_100", "Quick Release Front (100mm)"
        QR_130 = "qr_130", "Quick Release (130mm)"   
        QR_135 = "qr_135", "Quick Release (135mm)"    
        THRU_FRONT_100 = "thru_100", "Thru Axle Front (100mm)"
        THRU_FRONT_110 = "thru_110", "Thru Axle Front Boost (110mm)"
        THRU_142 = "thru_142", "Thru Axle (142mm)"    
        THRU_148 = "thru_148", "Thru Axle Boost (148mm)"
    
    class HubType(models.TextChoices):
        THREADED = "threaded", "Threaded"
        SPLINE = "spline", "Spline"
    

    wheel_size = models.CharField(max_length=10, choices=WheelSize.choices)
    position = models.CharField(max_length=10, choices=Position.choices)
    axle_standard = models.CharField(max_length=20, choices=AxleStandard.choices)
    hub_type = models.CharField(max_length=10, choices=HubType.choices, default="threaded")
    max_tire_width_mm = models.PositiveSmallIntegerField()
    tubeless_ready = models.BooleanField(default=False)

class Sprocket(Components):
    class MountType(models.TextChoices):
        THREADED = "threaded", "Threaded",
        SPLINE = "spline", "Spline"

    class Widths(models.TextChoices):
        WIDTH_1_8 = "1/8", "1/8",
        WIDTH_3_32 = "3/32", "3/32",

    mount_type = models.CharField(max_length=10, choices=MountType.choices)
    sprocket_width = models.CharField(max_length=10, choices=Widths.choices)
    sprocket_teeth = models.PositiveSmallIntegerField()

class Chain(Components):
    class Widths(models.TextChoices):
        WIDTH_1_8 = "1/8", "1/8",
        WIDTH_3_32 = "3/32", "3/32",

    class Material(models.TextChoices):
        CHROMOLY = "chromoly", "Chromoly",
        STEEL = "steel", "Steel",
    chain_width = models.CharField(max_length=10, choices=Widths.choices)
    chain_material = models.CharField(max_length=20, choices=Material.choices)

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

    class MountType(models.TextChoices):
        FLAT_MOUNT = "flat_mount", "Flat Mount"
        POST_MOUNT = "post_mount", "Post Mount"
        IS_MOUNT = "is_mount", "IS Mount"

    brake_type = models.CharField(max_length=20, choices=BrakeType.choices)
    mount_type = models.CharField(max_length=20, choices=MountType.choices, blank=True)
    rotor_size_mm = models.PositiveSmallIntegerField(null=True, blank=True)


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


class TrackHub(Components):
    class HubPosition(models.TextChoices):
        FRONT = "front", "Front Hub"
        REAR = "rear", "Rear Hub"

    class AxleType(models.TextChoices):
        BOLT_ON_M9 = "bolt_on_m9", "Bolt-On M9 (Standard Front Axle)"
        BOLT_ON_M10 = "bolt_on_m10", "Bolt-On M10 (Standard Rear Axle)"
        FEMALE_BOLT = "female_bolt", "Female Allen Bolt System"

    class HubSpacing(models.TextChoices):
        FRONT_100MM = "100mm", "100mm (Standard Front)"
        REAR_120MM = "120mm", "120mm (Standard Track Rear)"
        REAR_110MM = "110mm", "110mm (Vintage NJS / Keirin Rear)"
        REAR_130MM = "130mm", "130mm (Single-Speed Conversion Rear)"

    class CogInterface(models.TextChoices):
        FIXED_SINGLE = "fixed_single", "Single-Sided Fixed"
        FLIP_FLOP_FIX_FREE = "flip_flop_fix_free", "Flip-Flop (Fixed / Freewheel)"
        FLIP_FLOP_FIX_FIX = "flip_flop_fix_fix", "Flip-Flop (Fixed / Fixed)"
        SPLINED_TRACK = "splined", "Splined Track (e.g., Miche / Shimano)"

    class ThreadStandard(models.TextChoices):
        ISO_ENGLISH = "iso_english", "Standard English/ISO (1.37 x 24 TPI)"
        NJS_JIS = "njs_jis", "NJS/JIS (Keirin standard)"
        CAMPAGNOLO = "campagnolo", "Campagnolo Threading"
        FRENCH = "french", "Vintage French Threading"
