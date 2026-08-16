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

from apps.components.models import Brake

BRAKE_JSON = os.path.join(os.path.dirname(__file__), "extracted", "brake.json")


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


def is_lever(g):
    cat = (g.get("site_category") or "").lower()
    return "lever" in cat and "caliper" not in g["name"].lower()


def brake_type_of(g):
    text = f'{g["name"]} {g.get("description", "")}'.lower()
    return "rim_cantilever" if "cantilever" in text or "canti " in text else "rim_caliper"


def load():
    rows = json.load(open(BRAKE_JSON))
    Brake.objects.all().delete()
    loaded, skipped = 0, 0
    for g in collapse(rows):
        if is_lever(g):
            skipped += 1
            continue
        Brake.objects.update_or_create(
            import_url=g["source_url"],
            defaults=dict(brake_type=brake_type_of(g), **base(g, "brake")),
        )
        loaded += 1
    print(f"loaded {loaded} brakes, skipped {skipped} levers")


if __name__ == "__main__":
    load()
