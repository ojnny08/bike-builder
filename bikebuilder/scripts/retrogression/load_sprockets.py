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

from apps.components.models import Sprocket, SprocketOption

SPROCKET_JSON = os.path.join(os.path.dirname(__file__), "extracted", "sprocket.json")


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


def width_of(g):
    text = f'{specs(g).get("chain compatibility", "")} {g["name"]}'.lower()
    return "1/8" if "1/8" in text else "3/32"


def mount_of(g):
    text = f'{g.get("site_category", "")} {g["name"]} {g.get("description", "")}'.lower()
    if "freewheel" in text:
        return "threaded"
    if "spline" in text or "miche" in text or "shimano" in text:
        return "spline"
    return "threaded"


def teeth_of(raw):
    m = re.search(r"(\d{1,2})\s*t", str(raw or "").lower())
    return int(m.group(1)) if m else None


def load():
    rows = json.load(open(SPROCKET_JSON))
    Sprocket.objects.all().delete()
    loaded, opts = 0, 0
    for g in collapse(rows):
        teeth = {teeth_of(options_of(v).get("size") or specs(v).get("size")) for v in g["variants"]}
        teeth = {t for t in teeth if t}
        main = min(teeth) if teeth else teeth_of(specs(g).get("size"))
        sp, _ = Sprocket.objects.update_or_create(
            import_url=g["source_url"],
            defaults=dict(
                mount_type=mount_of(g),
                sprocket_width=width_of(g),
                sprocket_teeth=main,
                **base(g, "sprocket"),
            ),
        )
        loaded += 1
        for t in teeth:
            SprocketOption.objects.get_or_create(sprocket=sp, teeth=t)
            opts += 1
    print(f"loaded {loaded} sprockets, {opts} teeth options")


if __name__ == "__main__":
    load()
