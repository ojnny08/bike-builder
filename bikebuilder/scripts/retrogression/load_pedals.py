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

from apps.components.models import Pedals

PEDALS_JSON = os.path.join(os.path.dirname(__file__), "extracted", "pedals.json")


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


def colour_of(g):
    s = specs(g)
    colour = s.get("color") or s.get("colors")
    if colour:
        return colour[:30]
    for v in g["variants"]:
        o = options_of(v)
        if o.get("color"):
            return o["color"][:30]
    return ""


def load():
    rows = json.load(open(PEDALS_JSON))
    Pedals.objects.all().delete()
    loaded = 0
    for g in collapse(rows):
        Pedals.objects.update_or_create(
            import_url=g["source_url"],
            defaults=dict(colour=colour_of(g), **base(g, "pedals")),
        )
        loaded += 1
    print(f"loaded {loaded} pedals")


if __name__ == "__main__":
    load()
