import json
import os
import re
import sys
from pathlib import Path

import django

sys.path.insert(0, str(next(
    p for p in Path(__file__).resolve().parents if (p / "manage.py").exists()
)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bikebuilder.settings")
django.setup()

from apps.components.models import Saddle, SaddleOptiosn

SADDLE_JSON = os.path.join(os.path.dirname(__file__), "extracted", "saddle.json")


def strip_variant(name):
    m = re.match(r"^(.*) - .+$", name)
    return m.group(1) if m else name


def specs(row):
    return {k.lower(): v for k, v in (row.get("specs") or {}).items()}


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


def load():
    rows = json.load(open(SADDLE_JSON))
    Saddle.objects.all().delete()
    loaded, opts = 0, 0
    for g in collapse(rows):
        saddle, _ = Saddle.objects.update_or_create(import_url=g["source_url"], defaults=base(g, "saddle"))
        loaded += 1
        s = specs(g)
        width, length = int_mm(s.get("width")), int_mm(s.get("length"))
        if width or length:
            SaddleOptiosn.objects.get_or_create(saddle=saddle, width_mm=width, length_mm=length)
            opts += 1
    print(f"loaded {loaded} saddles, {opts} options")


if __name__ == "__main__":
    load()
