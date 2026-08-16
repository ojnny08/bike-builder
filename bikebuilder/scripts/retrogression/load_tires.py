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

from apps.components.models import Tire, TireOption

TIRE_JSON = os.path.join(os.path.dirname(__file__), "extracted", "tire.json")


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


def wheel_size_of(g):
    text = f'{specs(g).get("size", "")} {specs(g).get("sizes", "")} {g["name"]}'.lower()
    for size in ("700c", "650b", "27.5", "29", "26"):
        if size in text:
            return size
    return "700c"


def width_of(raw):
    m = re.search(r"x?\s*(\d{2})\s*(?:mm|c)", str(raw or "").lower())
    if m:
        return int(m.group(1))
    m = re.search(r"(\d{2})\s*mm", str(raw or ""))
    return int(m.group(1)) if m else None


def load():
    rows = json.load(open(TIRE_JSON))
    Tire.objects.all().delete()
    loaded, opts = 0, 0
    for g in collapse(rows):
        tire, _ = Tire.objects.update_or_create(
            import_url=g["source_url"],
            defaults=dict(wheel_size=wheel_size_of(g), **base(g, "tire")),
        )
        loaded += 1
        widths = {width_of(options_of(v).get("size") or specs(v).get("size")) for v in g["variants"]}
        for w in {w for w in widths if w}:
            TireOption.objects.get_or_create(tire=tire, width_mm=w)
            opts += 1
    print(f"loaded {loaded} tires, {opts} width options")


if __name__ == "__main__":
    load()
