from rest_framework import serializers
from urllib.parse import urlparse
from .models import (
    Components, ComponentType, ComponentSubmission,
    Crankset, CrankOption, CrankArm, CrankArmOption, Chainring, ChainringOption,
    BottomBracket, BottomBracketOption, TrackHub, HubOption,
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
        fields = ['id', 'color', 'length_mm', 'chainring_teeth', 'price']


class CranksetSerializer(serializers.ModelSerializer):
    options = CrankOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Crankset
        fields = BASE_FIELDS + ['spindle_interface_mm', 'spindle_length_mm', 'options']


class CrankArmOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrankArmOption
        fields = ['id', 'color', 'length_mm', 'price']


class CrankArmSerializer(serializers.ModelSerializer):
    options = CrankArmOptionSerializer(many=True, read_only=True)

    class Meta:
        model = CrankArm
        fields = BASE_FIELDS + ['spindle_interface_mm', 'spindle_length_mm', 'options']


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
        fields = ['id', 'bb_type', 'color', 'price']


class BottomBracketSerializer(serializers.ModelSerializer):
    options = BottomBracketOptionSerializer(many=True, read_only=True)

    class Meta:
        model = BottomBracket
        fields = BASE_FIELDS + ['bb_width_mm', 'spindle_interface_mm', 'spindle_length_mm', 'options']


class HubOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HubOption
        fields = ['id', 'color', 'hole_count', 'cog_interface', 'price']


class TrackHubSerializer(serializers.ModelSerializer):
    options = HubOptionSerializer(many=True, read_only=True)

    class Meta:
        model = TrackHub
        fields = BASE_FIELDS + ['position', 'hub_spacing', 'threading', 'options']


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

