from django.db import models
from django.conf import settings
from django.core.validators import URLValidator
from ..category.models import BikeType


class ComponentType(models.TextChoices):
    FRAME = "frame", "Frame"
    BOTTOM_BRACKET = "bottom_bracket", "Bottom Bracket"
    CRANKSET = "crankset", "Crankset"
    CRANK_ARM = "crank_arm", "Crank Arm"
    CHAINRING = "chainring", "Chainring"
    SPROCKET = "sprocket", "Sprocket"
    CHAIN = "chain", "Chain"
    WHEEL = "wheel", "Wheel"
    WHEELSET = "wheelset", "Wheelset"
    RIM = "rim", "Rim"
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
    import_url = models.URLField(
        blank=True,
        validators=[URLValidator(schemes=["http", "https"])]
        )
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submitted_components",
    )

    class Meta:
        ordering = ['brand', 'name']
        indexes = [
            models.Index(fields=['component_type', 'brand', 'name']),
        ]

    def __str__(self):
        return f"{self.brand} {self.name}"


class ShellType(models.TextChoices):
    BSA = "bsa", "BSA"
    ITA = "ita", "Italian"
    T47 = "t47", "T47"
    
    PRESS_FIT_86_92 = "pf86_92", "Press Fit (BB86/BB92)"
    PRESS_FIT_30 = "pf30", "PressFit 30"
    BB30 = "bb30", "BB30"

class Frame(Components):
    class Generation(models.TextChoices):
        MODERN = "modern", "Modern"
        VINTAGE = "vintage", "Vintage"

    class ForkType(models.TextChoices):
        TAPERED = "tapered", "Tapered"
        STRAIGHT = "straight", "Straight"

    fork_type = models.CharField(max_length=10, choices=ForkType.choices, null=True, blank=True )
    bb_type = models.CharField(max_length=20, choices=ShellType.choices, null=True, blank=True)
    bb_width_mm = models.SmallIntegerField(null=True, blank=True)
    fork_brake_drilled = models.BooleanField(default=False)
    frame_brake_drilled = models.BooleanField(default=False)
    seatpost_size = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    max_tire_clearance_mm = models.PositiveSmallIntegerField(null=True, blank=True)
 

class FrameOption(models.Model):
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE, related_name="options")
    size = models.CharField(max_length=20)

    class Meta:
        ordering = ["frame", "size"]

    def __str__(self):
        return f"{self.frame} — {self.size}"

class SpindleInterface(models.TextChoices):
        # Square Taper
        SQUARE_TAPER_ISO = "square_taper_iso", "Square Taper ISO"
        SQUARE_TAPER_JIS = "square_taper_jis", "Square Taper JIS"
        
        OCTALINK = "octalink", "Shimano Octalink"
        ISIS = "isis", "ISIS Drive"
        
        HOLLOWTECH_24 = "24mm", "24mm (Shimano Hollowtech II)"
        GXP = "gxp", "SRAM GXP (24mm/22mm stepped)"
        MM_30 = "30mm", "30mm (BB30/386EVO)"
        DUB = "dub", "SRAM DUB (28.99mm)"

class BottomBracket(Components):
    spindle_interface_mm = models.CharField(max_length=20, choices=SpindleInterface.choices)
    spindle_length_mm = models.PositiveSmallIntegerField(null=True, blank=True)
    bb_width_mm= models.PositiveSmallIntegerField(null=True, blank=True)


class BottomBracketOption(models.Model):
    bottom_bracket = models.ForeignKey(BottomBracket, on_delete=models.CASCADE, related_name="options")
    bb_type = models.CharField(max_length=20, choices=ShellType.choices)
    color = models.CharField(max_length=40, blank=True)
    image_colour_url = models.URLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["bottom_bracket", "color", "bb_type"]

    def __str__(self):
        return f"{self.bottom_bracket} — {self.color} {self.bb_type}".strip()

class ArmLength(models.TextChoices):
    ARM_160mm = "160mm", "160mm"
    ARM_165mm = "165mm", "165mm"
    ARM_1675mm = "167.5mm", "167.5mm"
    ARM_170mm = "170mm", "170mm"
    ARM_1725mm = "172.5mm", "172.5mm"

class BoltCircle(models.TextChoices):
    BCD_144 = "144", "144mm BCD"
    BCD_130 = "130", "130mm BCD"
    BCD_110 = "110", "110mm BCD"
    BCD_135 = "135", "135mm BCD"
    BCD_104 = "104", "104mm BCD"

class Crankset(Components):
    spindle_interface_mm = models.CharField(max_length=20, choices=SpindleInterface.choices)
    spindle_length_mm = models.PositiveSmallIntegerField(null=True, blank=True)

class CrankOption(models.Model):
    crankset = models.ForeignKey(Crankset, on_delete=models.CASCADE, related_name="options")
    color = models.CharField(max_length=40, blank=True)
    length_mm = models.CharField(max_length=10, choices=ArmLength.choices)
    chainring_teeth = models.PositiveSmallIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_colour_url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["crankset", "color", "chainring_teeth", "length_mm"]

    def __str__(self):
        return f"{self.crankset} — {self.color} {self.length_mm}".strip()

class CrankArm(Components):
    spindle_interface_mm = models.CharField(max_length=20, choices=SpindleInterface.choices)
    spindle_length_mm = models.PositiveSmallIntegerField(null=True, blank=True)
    bcd = models.CharField(max_length=4, choices=BoltCircle.choices, null=True, blank=True)

class CrankArmOption(models.Model):
    crank_arm = models.ForeignKey(CrankArm, on_delete=models.CASCADE, related_name="options")
    color = models.CharField(max_length=40, blank=True)
    length_mm = models.CharField(max_length=10, choices=ArmLength.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_colour_url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["crank_arm", "color", "length_mm"]

    def __str__(self):
        return f"{self.crank_arm} — {self.color} {self.length_mm}".strip()

class Chainring(Components):
    bcd = models.CharField(max_length=4, choices=BoltCircle.choices, null=True, blank=True)

class ChainringOption(models.Model):
    chainring = models.ForeignKey(Chainring, on_delete=models.CASCADE, related_name="options")
    color = models.CharField(max_length=40, blank=True)
    chainring_teeth = models.PositiveSmallIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_colour_url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["chainring", "chainring_teeth", "color"]

    def __str__(self):
        return f"{self.chainring} — {self.chainring_teeth}t {self.color}".strip()
    
class WheelSize(models.TextChoices):
    TWENTY_SIX = "26", '26"'
    TWENTY_SEVEN_FIVE = "27.5", '27.5"'
    TWENTY_NINE = "29", '29"'
    SEVEN_HUNDRED = "700c", "700c"
    SIX_FIFTY = "650b", "650b"

class HubPosition(models.TextChoices):
    FRONT = "front", "Front"
    REAR = "rear", "Rear"

class HubSpacing(models.TextChoices):
    FRONT_100MM = "100mm", "100mm"
    REAR_110MM = "110mm", "110mm"
    REAR_120MM = "120mm", "120mm"
    REAR_130MM = "130mm", "130mm"

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


class WheelSpecs(models.Model):
    wheel_size = models.CharField(max_length=10, choices=WheelSize.choices)
    max_tire_width_mm = models.PositiveSmallIntegerField(null=True, blank=True)
    

    class Meta:
        abstract = True

class Rim(Components, WheelSpecs):
    pass

class RimOptions(models.Model):
    rim = models.ForeignKey(Rim, on_delete=models.CASCADE, related_name="options")
    color = models.CharField(max_length=40, blank=True)
    hole_count = models.PositiveSmallIntegerField(null=True, blank=True)
    image_colour_url = models.URLField(null=True, blank=True)

class HubSpecs(models.Model):
    position = models.CharField(max_length=10, choices=HubPosition.choices, blank=True, default="")
    hub_spacing = models.CharField(max_length=6, choices=HubSpacing.choices, blank=True, default="")
    threading = models.CharField(max_length=25, choices=ThreadStandard.choices, blank=True, default="")

    class Meta:
        abstract = True

class TrackHub(Components, HubSpecs):
    pass

class HubOption(models.Model):
    track_hub = models.ForeignKey(TrackHub, on_delete=models.CASCADE, related_name="options")
    color = models.CharField(max_length=40, blank=True)
    hole_count = models.PositiveSmallIntegerField(null=True, blank=True)
    cog_interface = models.CharField(max_length=20, choices=CogInterface.choices, blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_colour_url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ["track_hub", "color", "hole_count", "cog_interface"]

    def __str__(self):
        return f"{self.track_hub} — {self.color} {self.hole_count}h {self.cog_interface}".strip()

class SingleWheel(Components, WheelSpecs, HubSpecs):
    class HubType(models.TextChoices):
        THREADED = "threaded", "Threaded"
        SPLINE = "spline", "Spline"

    hub_type = models.CharField(max_length=10, choices=HubType.choices, default="threaded")
    cog_interface = models.CharField(max_length=20, choices=CogInterface.choices, blank=True, default="")

class WheelSet(Components, WheelSpecs):
    rim_name = models.CharField(max_length=200, blank=True)
    hub_name = models.CharField(max_length=200, blank=True)
    rear_hub_spacing = models.CharField(max_length=6, choices=HubSpacing.choices, blank=True)
    cog_interface = models.CharField(max_length=20, choices=CogInterface.choices, blank=True)

class Sprocket(Components):
    class MountType(models.TextChoices):
        THREADED = "threaded", "Threaded",
        SPLINE = "spline", "Spline"

    class Widths(models.TextChoices):
        WIDTH_1_8 = "1/8", "1/8",
        WIDTH_3_32 = "3/32", "3/32",

    mount_type = models.CharField(max_length=10, choices=MountType.choices)
    sprocket_width = models.CharField(max_length=10, choices=Widths.choices)
    sprocket_teeth = models.PositiveSmallIntegerField(null=True, blank=True)

class SprocketOption(models.Model):
    sprocket = models.ForeignKey(Sprocket, on_delete=models.CASCADE, related_name="options")
    teeth = models.PositiveSmallIntegerField(null=True, blank=True)

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

    wheel_size = models.CharField(max_length=10, choices=WheelSize.choices)

class TireOption(models.Model):
    tire = models.ForeignKey(Tire, on_delete=models.CASCADE, related_name="options")
    width_mm = models.PositiveSmallIntegerField(null=True, blank=True)


class Handlebar(Components):
    class BarType(models.TextChoices):
        DROP = "drop", "Drop"
        FLAT = "flat", "Flat"
        RISER = "riser", "Riser"
        BULLHORN = "bullhorn", "Bullhorn"

    bar_type = models.CharField(max_length=20, choices=BarType.choices)
    clamp_diameter_mm = models.DecimalField(max_digits=4, decimal_places=1)
    drop_mm = models.PositiveSmallIntegerField(null=True, blank=True)
    reach_mm = models.PositiveSmallIntegerField(null=True, blank=True)

class HandlebarOptions(models.Model):
    handlebar = models.ForeignKey(Handlebar, on_delete=models.CASCADE, related_name="options")
    width = models.PositiveSmallIntegerField(null=True, blank=True)

class Stem(Components):
    bar_clamp_diameter_mm = models.DecimalField(max_digits=4, decimal_places=1)
    steerer_clamp_diameter_mm = models.DecimalField(max_digits=4, decimal_places=1)
    angle_degrees = models.SmallIntegerField()

class StemOptions(models.Model):
    stem = models.ForeignKey(Stem, on_delete=models.CASCADE, related_name="options")
    length_mm = models.PositiveSmallIntegerField(null=True, blank=True)
    color = models.CharField(max_length=40, blank=True)
    image_colour_url = models.URLField(null=True, blank=True)

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
    pass

class SaddleOptiosn(models.Model):
    saddle = models.ForeignKey(Saddle, on_delete=models.CASCADE, related_name="options")
    width_mm = models.PositiveSmallIntegerField(null=True, blank=True)
    length_mm = models.PositiveSmallIntegerField(null=True, blank=True)


class Seatpost(Components):
    pass

class SeatPostOptions(models.Model):
    seatpost = models.ForeignKey(Seatpost, on_delete=models.CASCADE, related_name="options")
    diameter_mm = models.DecimalField(max_digits=4, decimal_places=1)
    length_mm = models.PositiveSmallIntegerField(null=True, blank=True)

class Pedals(Components):
    class PedalType(models.TextChoices):
        FLAT = "flat", "Flats"
        CLIPS = "clips", "Clips"
        CLIPLESS = "clipless", "Clipless"

    colour = models.CharField(max_length=30)

class ComponentSubmission(models.Model):
    """A user-submitted product URL awaiting manual entry in the admin."""
    url = models.URLField(validators=[URLValidator(schemes=["http", "https"])])
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="component_submissions",
    )
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.url


