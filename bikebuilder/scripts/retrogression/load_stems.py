import json
import os
import re
import sys
from pathlib import Path
from decimal import Decimal

import django

sys.path.insert(0, str(next(
    p for p in Path(__file__).resolve().parents if (p / "manage.py").exists()
)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bikebuilder.settings")
django.setup()

from apps.components.models import Stem, StemOptions

STEM_JSON = os.path.join(os.path.dirname(__file__), "extracted", "stem.json")


def strip_variant(name):
    m = re.match(r"^(.*) - .+$", name)
    return m.group(1) if m else name


def specs(row):
    return {k.lower(): v for k, v in (row.get("specs") or {}).items()}


def options_of(row):
    o = row.get("options")
    return {k.lower(): v for k, v in o.items()} if isinstance(o, dict) else {}


def weight_of(row):
    if row.get("weight_grams"):
        return int(row["weight_grams"])
    blob = f'{specs(row).get("weight", "")} {" ".join(row.get("spec_notes") or [])}'
    m = re.search(r"(\d+(?:\.\d+)?)\s*g", blob)
    return int(float(m.group(1))) if m else 0


def collapse(rows):
    groups = {}
    for row in rows:
        g = groups.setdefault(row["source_url"], {**row, "variants": []})
        g["variants"].append(row)
    return list(groups.values())


def base(g, ctype):
    return dict(
        component_type=ctype,
        name=strip_variant(g["name"]),
        brand=g["brand"],
        price=min(v["price"] for v in g["variants"]),
        weight_grams=weight_of(g),
        description=g.get("description", ""),
        image_url=g.get("image_url", ""),
    )


def int_mm(raw):
    m = re.search(r"(\d+(?:\.\d+)?)\s*mm", str(raw or ""))
    return int(float(m.group(1))) if m else None


def clamp_of(g):
    m = re.search(r"(\d+(?:\.\d+)?)\s*mm", str(specs(g).get("clamp") or ""))
    return Decimal(m.group(1)) if m else Decimal("31.8")


def steerer_of(g):
    text = f'{g.get("site_category", "")} {specs(g).get("steerer", "")} {g["name"]}'.lower()
    if "quill" in text:
        return Decimal("22.2")
    if "1.5" in text or "1-1/2" in text:
        return Decimal("38.1")
    return Decimal("28.6")


def angle_of(g):
    m = re.search(r"(\d{1,2})", str(specs(g).get("angle") or ""))
    return int(m.group(1)) if m else 0


def color_of(row):
    s = specs(row)
    return (options_of(row).get("color") or s.get("color") or s.get("colors") or "")[:40]


def load():
    rows = json.load(open(STEM_JSON))
    Stem.objects.all().delete()
    loaded, opts = 0, 0
    for g in collapse(rows):
        stem, _ = Stem.objects.update_or_create(
            import_url=g["source_url"],
            defaults=dict(
                bar_clamp_diameter_mm=clamp_of(g),
                steerer_clamp_diameter_mm=steerer_of(g),
                angle_degrees=angle_of(g),
                **base(g, "stem"),
            ),
        )
        loaded += 1
        for v in g["variants"]:
            length = int_mm(options_of(v).get("length") or specs(v).get("length"))
            StemOptions.objects.get_or_create(
                stem=stem,
                length_mm=length,
                color=color_of(v),
                defaults={"image_colour_url": v.get("image_url") or ""},
            )
            opts += 1
    print(f"loaded {loaded} stems, {opts} options")


if __name__ == "__main__":
    load()
