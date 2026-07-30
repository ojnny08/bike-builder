import json
import os
import re
import sys

import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bikebuilder.settings")
django.setup()

from apps.components.models import (
    WheelSet, SingleWheel, WheelSize, HubSpacing, CogInterface, ThreadStandard,
)

WHEEL_JSON = os.path.join(os.path.dirname(__file__), "extracted", "wheel.json")


def strip_variant(name):
    m = re.match(r"^(.*) - .+$", name)
    return m.group(1) if m else name


def label(name):
    n = name.lower()
    if "wheelset" in n:
        return "wheelset"
    if "single wheel" in n or "track wheel" in n or "front" in n or "rear" in n:
        return "single"
    return "wheelset"


def notes_text(row):
    specs = " ".join(str(v) for v in row["specs"].values())
    return f"{specs} {' '.join(row.get('spec_notes', []))}".lower()


def wheel_size_of(row):
    text = notes_text(row)
    for value in ("700c", "650b", "27.5", "29", "26"):
        if value in text:
            return value
    return WheelSize.SEVEN_HUNDRED


def max_tire_of(row):
    src = row["specs"].get("max tire size") or row["specs"].get("max tire width") or ""
    m = re.search(r"(\d{2})", src)
    return int(m.group(1)) if m else 0


def cog_of(row):
    text = notes_text(row)
    if "fixed/fixed" in text or "fixed / fixed" in text:
        return CogInterface.FLIP_FLOP_FIX_FIX
    if "fixed/free" in text or "fixed / free" in text:
        return CogInterface.FLIP_FLOP_FIX_FREE
    if "single" in text and "fixed" in text:
        return CogInterface.FIXED_SINGLE
    return ""


def threading_of(row):
    text = notes_text(row)
    if "njs" in text or "jis" in text:
        return ThreadStandard.NJS_JIS
    if "campagnolo" in text or "italian" in text:
        return ThreadStandard.CAMPAGNOLO
    if "french" in text:
        return ThreadStandard.FRENCH
    if "english" in text or "iso" in text or "1.37" in text or "24 tpi" in text:
        return ThreadStandard.ISO_ENGLISH
    return ""


def rear_spacing_of(row):
    specs = row["specs"]
    m = re.search(r"(\d{3})\s*mm\s*rear", specs.get("spacing", ""))
    if m:
        return f"{m.group(1)}mm"
    m = re.search(r"(\d{3})", specs.get("rear spacing", ""))
    return f"{m.group(1)}mm" if m else ""


def rim_hub_names(name):
    base = strip_variant(name)
    if "/" in base:
        rim, hub = base.split("/", 1)
        return rim.strip(), hub.strip()
    return base.strip(), ""


def single_position(name):
    n = name.lower()
    tail = n.split("front or rear")[-1]
    if "rear" in tail:
        return "rear"
    if "front" in tail:
        return "front"
    if "rear" in n:
        return "rear"
    return "front"


def collapse(rows, keyfn):
    groups = {}
    for row in rows:
        key = keyfn(row)
        g = groups.setdefault(key, {**row, "variants": []})
        g["variants"].append(row)
    return list(groups.values())


def base(g):
    return dict(
        name=strip_variant(g["name"]),
        brand=g["brand"],
        price=min(v["price"] for v in g["variants"]),
        weight_grams=int(g["weight_grams"]),
        description=g["description"],
        image_url=g["image_url"],
        wheel_size=wheel_size_of(g),
        max_tire_width_mm=max_tire_of(g),
    )


def load():
    rows = json.load(open(WHEEL_JSON))
    wheelset_rows = [r for r in rows if label(r["name"]) == "wheelset"]
    single_rows = [r for r in rows if label(r["name"]) == "single"]

    sets = 0
    for g in collapse(wheelset_rows, lambda r: r["source_url"]):
        rim, hub = rim_hub_names(g["name"])
        WheelSet.objects.update_or_create(
            import_url=g["source_url"],
            defaults=dict(
                component_type="wheelset",
                rim_name=rim,
                hub_name=hub,
                rear_hub_spacing=rear_spacing_of(g),
                cog_interface=cog_of(g),
                **base(g),
            ),
        )
        sets += 1

    singles = 0
    for g in collapse(single_rows, lambda r: (r["source_url"], single_position(r["name"]))):
        position = single_position(g["name"])
        SingleWheel.objects.update_or_create(
            import_url=g["source_url"],
            position=position,
            defaults=dict(
                component_type="wheel",
                position=position,
                hub_spacing=HubSpacing.FRONT_100MM if position == "front" else HubSpacing.REAR_120MM,
                threading=threading_of(g),
                cog_interface=cog_of(g) if position == "rear" else "",
                **base(g),
            ),
        )
        singles += 1

    print(f"loaded {sets} wheelsets, {singles} single wheels")


if __name__ == "__main__":
    load()
