import json
import os
import re
import sys

import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bikebuilder.settings")
django.setup()

from apps.components.models import Chain

CHAIN_JSON = os.path.join(os.path.dirname(__file__), "extracted", "chain.json")


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


def width_of(g):
    text = f'{g["name"]} {g.get("site_category", "")} {specs(g).get("width", "")}'.lower()
    return "1/8" if "1/8" in text else "3/32"


def material_of(g):
    blob = f'{g["name"]} {g.get("description", "")} {" ".join(g.get("spec_notes", []))}'.lower()
    return "chromoly" if any(k in blob for k in ("chromoly", "cro-mo", "cr-mo", "chromo")) else "steel"


def load():
    rows = json.load(open(CHAIN_JSON))
    Chain.objects.all().delete()
    loaded = 0
    for g in collapse(rows):
        Chain.objects.update_or_create(
            import_url=g["source_url"],
            defaults=dict(chain_width=width_of(g), chain_material=material_of(g), **base(g, "chain")),
        )
        loaded += 1
    print(f"loaded {loaded} chains")


if __name__ == "__main__":
    load()
