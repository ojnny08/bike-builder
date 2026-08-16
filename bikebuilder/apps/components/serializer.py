from rest_framework import serializers
from urllib.parse import urlparse
from .models import (
    Components, ComponentSubmission,
    Crankset, CrankOption, CrankArm, CrankArmOption, Chainring, ChainringOption,
    BottomBracket, BottomBracketOption, TrackHub, HubOption,
    Rim, RimOptions, Stem, StemOptions,
    Chain, Handlebar, HandlebarOptions, Brake, Pedals,
    Sprocket, SprocketOption, Tire, TireOption,
    Saddle, SaddleOptiosn, Seatpost, SeatPostOptions,
    Frame, FrameOption, SingleWheel, WheelSet,
)

ALLOWED_HOSTS = {
    # --- Major online bike retailers ---
    "amazon.com",
    "chainreactioncycles.com",
    "wiggle.com",
    "competitivecyclist.com",
    "backcountry.com",
    "jensonusa.com",
    "universalcycles.com",
    "worldwidecyclery.com",
    "modernbike.com",
    "probikekit.com",
    "merlincycles.com",
    "sigmasports.com",
    "tredz.co.uk",
    "evanscycles.com",
    "planetx.co.uk",
    "ribblecycles.co.uk",
    "rosebikes.com",
    "canyon.com",
    "bike24.com",
    "bike-discount.de",
    "bike-components.de",
    "r2-bike.com",
    "bikeinn.com",
    "theproscloset.com",

    # --- Fixed-gear / track specialists ---
    "statebicycle.com",
    "velosolo.co.uk",
    "brothercycles.com",
    "wabicycles.com",
    "surlybikes.com",
    "allcitycycles.com",

    # --- Component & parts manufacturers ---
    "shimano.com",
    "sram.com",
    "campagnolo.com",
    "zipp.com",
    "fullspeedahead.com",   # FSA
    "raceface.com",
    "eastoncycling.com",
    "ritcheylogic.com",
    "dedaelementi.com",
    "thomsonbike.com",
    "chrisking.com",
    "whiteind.com",         # White Industries
    "paulcomp.com",         # Paul Components
    "philwood.com",
    "hopetech.com",
    "tektro.com",
    "trpcycling.com",
    "kmcchain.com",
    "micheusa.com",
    "velocityusa.com",
    "enve.com",
    "dtswiss.com",
    "mavic.com",

    "dosnoventa.com",         # Dosnoventa (Spain) — fairly confident
    "engine11.com",           # VERIFY — could be .cc / .co.uk
    "xfixxibikes.com",        # VERIFY — possibly xfixxi.com / xfixxi.ca
    "tsunamibike.com",        # VERIFY — Tsunami (aluminium track frames)
    "skream.cc",              # VERIFY — Skream aero fixed-gear

    # --- Track rims / wheels ---
    "velocityusa.com",        # Deep V / track rims
    "hplusson.com",           # H Plus Son — TB14, Archetype track rims
    "mavic.com",              # Ellipse track wheelset

    # --- Tires / saddles / finishing kit ---
    "schwalbe.com",
    "continental-tires.com",
    "vittoria.com",
    "maxxis.com",
    "panaracer.com",
    "fizik.com",
    "selleitalia.com",
    "brooksengland.com",
    "wtb.com",

    "leaderbikesusa.com",     # VERIFY — Leader (735TR, 725)
    "aventon.com",            # Aventón (track roots; now mostly e-bikes)
    "volumebikes.com",        # VERIFY — Volume (Cutter)
    "affinitycycles.com",     # VERIFY — Affinity (NYC track)
}

class ComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Components
        fields = ['id', 'component_type', 'name', 'brand', 'weight_grams', 'price', 'image_url', 'import_url']

    def validate_import_url(self, value):
        if not value:
            raise serializers.ValidationError("A product link is required")
        host = (urlparse(value).hostname or "").lower()
        # match domain and its subdomains (www.amazon.com, etc.)
        if not any(host == d or host.endswith("." + d) for d in ALLOWED_HOSTS):
            raise serializers.ValidationError("Link must point to an approved retailer.")
        return value

BASE_FIELDS = ['id', 'component_type', 'name', 'brand', 'weight_grams', 'price', 'image_url', 'import_url']


class CrankOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrankOption
        fields = ['id', 'color', 'length_mm', 'chainring_teeth', 'price', 'image_colour_url']


class CranksetSerializer(serializers.ModelSerializer):
    options = CrankOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Crankset
        fields = BASE_FIELDS + ['spindle_interface_mm', 'spindle_length_mm', 'options']


class CrankArmOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrankArmOption
        fields = ['id', 'color', 'length_mm', 'price', 'image_colour_url']


class CrankArmSerializer(serializers.ModelSerializer):
    options = CrankArmOptionSerializer(many=True, read_only=True)

    class Meta:
        model = CrankArm
        fields = BASE_FIELDS + ['spindle_interface_mm', 'spindle_length_mm', 'bcd', 'options']


class ChainringOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChainringOption
        fields = ['id', 'color', 'chainring_teeth', 'price', 'image_colour_url']


class ChainringSerializer(serializers.ModelSerializer):
    options = ChainringOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Chainring
        fields = BASE_FIELDS + ['bcd', 'options']


class BottomBracketOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BottomBracketOption
        fields = ['id', 'bb_type', 'color', 'price', 'image_colour_url']


class BottomBracketSerializer(serializers.ModelSerializer):
    options = BottomBracketOptionSerializer(many=True, read_only=True)

    class Meta:
        model = BottomBracket
        fields = BASE_FIELDS + ['bb_width_mm', 'spindle_interface_mm', 'spindle_length_mm', 'options']


class HubOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HubOption
        fields = ['id', 'color', 'hole_count', 'cog_interface', 'price', 'image_colour_url']


class TrackHubSerializer(serializers.ModelSerializer):
    options = HubOptionSerializer(many=True, read_only=True)

    class Meta:
        model = TrackHub
        fields = BASE_FIELDS + ['position', 'hub_spacing', 'threading', 'options']


class RimOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RimOptions
        fields = ['id', 'color', 'hole_count', 'image_colour_url']


class RimSerializer(serializers.ModelSerializer):
    options = RimOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Rim
        fields = BASE_FIELDS + ['wheel_size', 'max_tire_width_mm', 'options']


class StemOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StemOptions
        fields = ['id', 'color', 'length_mm', 'image_colour_url']


class StemSerializer(serializers.ModelSerializer):
    options = StemOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Stem
        fields = BASE_FIELDS + ['bar_clamp_diameter_mm', 'steerer_clamp_diameter_mm', 'angle_degrees', 'options']


class ChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chain
        fields = BASE_FIELDS + ['chain_width', 'chain_material']


class HandlebarOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandlebarOptions
        fields = ['id', 'width']


class HandlebarSerializer(serializers.ModelSerializer):
    options = HandlebarOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Handlebar
        fields = BASE_FIELDS + ['bar_type', 'clamp_diameter_mm', 'drop_mm', 'reach_mm', 'options']


class BrakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brake
        fields = BASE_FIELDS + ['brake_type', 'mount_type', 'rotor_size_mm']


class PedalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedals
        fields = BASE_FIELDS + ['colour']


class SprocketOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SprocketOption
        fields = ['id', 'teeth']


class SprocketSerializer(serializers.ModelSerializer):
    options = SprocketOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Sprocket
        fields = BASE_FIELDS + ['mount_type', 'sprocket_width', 'sprocket_teeth', 'options']


class TireOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TireOption
        fields = ['id', 'width_mm']


class TireSerializer(serializers.ModelSerializer):
    options = TireOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Tire
        fields = BASE_FIELDS + ['wheel_size', 'options']


class SaddleOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaddleOptiosn
        fields = ['id', 'width_mm', 'length_mm']


class SaddleSerializer(serializers.ModelSerializer):
    options = SaddleOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Saddle
        fields = BASE_FIELDS + ['options']


class SeatpostOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatPostOptions
        fields = ['id', 'diameter_mm', 'length_mm']


class SeatpostSerializer(serializers.ModelSerializer):
    options = SeatpostOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Seatpost
        fields = BASE_FIELDS + ['options']


class FrameOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameOption
        fields = ['id', 'size']


class FrameSerializer(serializers.ModelSerializer):
    options = FrameOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Frame
        fields = BASE_FIELDS + [
            'fork_type', 'bb_type', 'bb_width_mm', 'fork_brake_drilled',
            'frame_brake_drilled', 'seatpost_size', 'max_tire_clearance_mm', 'options',
        ]


class SingleWheelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleWheel
        fields = BASE_FIELDS + [
            'wheel_size', 'max_tire_width_mm', 'hub_type', 'cog_interface',
            'position', 'hub_spacing', 'threading',
        ]


class WheelSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WheelSet
        fields = BASE_FIELDS + [
            'wheel_size', 'max_tire_width_mm', 'rim_name', 'hub_name',
            'rear_hub_spacing', 'cog_interface',
        ]


def _is_trusted(url):
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in ALLOWED_HOSTS)


class ComponentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentSubmission
        fields = ['id', 'url', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_url(self, value):
        if not _is_trusted(value):
            raise serializers.ValidationError("Link must point to an approved retailer.")
        return value

