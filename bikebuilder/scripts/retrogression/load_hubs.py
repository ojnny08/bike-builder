import json
import os
import re
import sys

import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bikebuilder.settings")
django.setup()

from apps.components.models import TrackHub, HubOption, CogInterface, ThreadStandard

HUB_JSON = os.path.join(os.path.dirname(__file__), "extracted", "track_hub.json")

COLORS = ["polished silver", "matte black", "black", "silver", "gold", "polished",
          "raw", "white", "red", "blue", "pink", "orange", "purple", "green"]


def strip_variant(name):
    m = re.match(r"^(.*) - .+$", name)
    return m.group(1) if m else name


def options_of(row):
    o = row["options"]
    return {k.lower(): v for k, v in o.items()} if isinstance(o, dict) else {}


def variant_title(row):
    return row["variant_title"] if isinstance(row["variant_title"], str) else ""


def notes_text(row):
    specs = " ".join(str(v) for v in row["specs"].values())
    return f"{variant_title(row)} {specs} {' '.join(row.get('spec_notes', []))}".lower()


def position_of(name):
    n = name.lower()
    if ("front" in n and "rear" in n) or "set" in n:
        return None
    if "front" in n:
        return "front"
    if "rear" in n:
        return "rear"
    return None


def hole_count_of(row, opts):
    for src in (opts.get("drilling"), row["specs"].get("drilling"), variant_title(row),
                " ".join(row.get("spec_notes", []))):
        m = re.search(r"(\d{2})\s*h\b", (src or "").lower())
        if m:
            return int(m.group(1))
    return None


def cog_of(row, opts):
    text = (opts.get("threads") or variant_title(row) or " ".join(row.get("spec_notes", []))).lower()
    if "fixed/fixed" in text or "fixed / fixed" in text:
        return CogInterface.FLIP_FLOP_FIX_FIX
    if "fixed/free" in text or "fixed / free" in text:
        return CogInterface.FLIP_FLOP_FIX_FREE
    if "single" in text and "fixed" in text:
        return CogInterface.FIXED_SINGLE
    return ""


def color_of(row, opts):
    color = opts.get("color")
    if color:
        return color
    return next((c for c in COLORS if c in variant_title(row).lower()), "")


def spacing_of(group, position):
    for v in group["variants"]:
        m = re.search(r"(\d{3})\s*mm", v["specs"].get("spacing", ""))
        if m:
            return f"{m.group(1)}mm"
    return "100mm" if position == "front" else "120mm"


def threading_of(group, position):
    if position == "front":
        return ""
    text = " ".join(notes_text(v) for v in group["variants"])
    if "njs" in text or "jis" in text:
        return ThreadStandard.NJS_JIS
    if "campagnolo" in text or "italian" in text:
        return ThreadStandard.CAMPAGNOLO
    if "french" in text:
        return ThreadStandard.FRENCH
    if "english" in text or "1.370" in text or "24tpi" in text or "24 tpi" in text:
        return ThreadStandard.ISO_ENGLISH
    return ""


def collapse(rows):
    groups = {}
    for row in rows:
        position = position_of(row["name"])
        if not position:
            continue
        g = groups.setdefault(row["source_url"], {**row, "position": position, "variants": []})
        g["variants"].append(row)
    return list(groups.values())


def load():
    rows = json.load(open(HUB_JSON))
    loaded, options, skipped = 0, 0, []

    for g in collapse(rows):
        position = g["position"]
        hub, _ = TrackHub.objects.update_or_create(
            import_url=g["source_url"],
            defaults=dict(
                component_type="track_hub",
                name=strip_variant(g["name"]),
                brand=g["brand"],
                price=min(v["price"] for v in g["variants"]),
                weight_grams=int(g["weight_grams"]),
                description=g["description"],
                image_url=g["image_url"],
                position=position,
                hub_spacing=spacing_of(g, position),
                threading=threading_of(g, position),
            ),
        )
        hub.options.all().delete()

        for v in g["variants"]:
            opts = options_of(v)
            hole_count = hole_count_of(v, opts)
            if hole_count is None:
                skipped.append((v["name"], "no hole_count"))
                continue
            HubOption.objects.get_or_create(
                track_hub=hub,
                color=color_of(v, opts),
                hole_count=hole_count,
                cog_interface=cog_of(v, opts),
                defaults=dict(price=v["price"]),
            )
            options += 1
        loaded += 1

    print(f"loaded {loaded} hubs, {options} options, skipped {len(skipped)}")
    for name, err in skipped:
        print(" -", name, "|", err)


if __name__ == "__main__":
    load()
