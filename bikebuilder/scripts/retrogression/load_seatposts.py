import json
import os
import re
import sys
from decimal import Decimal

import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bikebuilder.settings")
django.setup()

from apps.components.models import Seatpost, SeatPostOptions

SEATPOST_JSON = os.path.join(os.path.dirname(__file__), "extracted", "seatpost.json")

DIAMETERS = {"25.4", "26.8", "27.2", "28.6", "30.9", "31.6", "31.8", "34.9"}


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


def diameter_of(raw):
    for d in re.findall(r"\d{2}(?:\.\d)?", str(raw or "")):
        if d in DIAMETERS:
            return Decimal(d)
    return None


def diameters_of(g):
    diams = {diameter_of(specs(v).get("diameter") or specs(v).get("size")) for v in g["variants"]}
    diams = {d for d in diams if d}
    if diams:
        return diams
    d = diameter_of(specs(g).get("diameter") or specs(g).get("size"))
    return {d} if d else set()


def load():
    rows = json.load(open(SEATPOST_JSON))
    Seatpost.objects.all().delete()
    loaded, opts, skipped = 0, 0, 0
    for g in collapse(rows):
        diams = diameters_of(g)
        if not diams:
            skipped += 1
            continue
        post, _ = Seatpost.objects.update_or_create(import_url=g["source_url"], defaults=base(g, "seatpost"))
        loaded += 1
        length = int_mm(specs(g).get("length"))
        for d in diams:
            SeatPostOptions.objects.get_or_create(seatpost=post, diameter_mm=d, length_mm=length)
            opts += 1
    print(f"loaded {loaded} seatposts, {opts} options, skipped {skipped} without a diameter")


if __name__ == "__main__":
    load()
