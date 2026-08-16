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

from apps.components.models import (
    Handlebar, HandlebarOptions, Stem, StemOptions,
    Seatpost, SeatPostOptions, WheelSet,
)

JSON_PATH = os.path.join(os.path.dirname(__file__), "dosnoventa_all.json")
BRAND = "Dosnoventa"


def spec(specs, *keys):
    for k in keys:
        for sk, v in specs.items():
            if sk.lower().strip() == k.lower():
                return v
    return None


def decimal_of(raw):
    m = re.search(r"(\d+(?:[.,]\d+)?)", str(raw or ""))
    return Decimal(m.group(1).replace(",", ".")) if m else None


def int_of(raw):
    d = decimal_of(raw)
    return int(d) if d is not None else None


def grams(raw):
    return sum(int(n) for n in re.findall(r"(\d+)\s*gr?\b", str(raw or ""), re.I))


def base(row, ctype, weight):
    return dict(
        component_type=ctype,
        name=row["name"],
        brand=BRAND,
        price=row["price"],
        weight_grams=weight,
        description=row["description"],
        image_url=row["image_url"],
    )


def load_handlebar(row, bar_type):
    s = row["specs"]
    bar, _ = Handlebar.objects.update_or_create(
        import_url=row["source_url"],
        defaults=dict(
            bar_type=bar_type,
            clamp_diameter_mm=decimal_of(spec(s, "clamp diameter (hb)")),
            drop_mm=int_of(spec(s, "drop")),
            reach_mm=int_of(spec(s, "reach")),
            **base(row, "handlebar", grams(spec(s, "weight"))),
        ),
    )
    width = int_of(spec(s, "width"))
    if width:
        HandlebarOptions.objects.get_or_create(handlebar=bar, width=width)


def load_stem(row):
    s = row["specs"]
    stem, _ = Stem.objects.update_or_create(
        import_url=row["source_url"],
        defaults=dict(
            bar_clamp_diameter_mm=decimal_of(spec(s, "clamp diameter (hb)")),
            steerer_clamp_diameter_mm=decimal_of(spec(s, "fork steerer")),
            angle_degrees=int_of(spec(s, "angle")) or 0,
            **base(row, "stem", grams(spec(s, "weight"))),
        ),
    )
    StemOptions.objects.get_or_create(stem=stem, length_mm=int_of(spec(s, "length")), color="")


def load_seatpost(row):
    s = row["specs"]
    post, _ = Seatpost.objects.update_or_create(
        import_url=row["source_url"],
        defaults=base(row, "seatpost", grams(spec(s, "weight"))),
    )
    SeatPostOptions.objects.get_or_create(
        seatpost=post,
        diameter_mm=decimal_of(spec(s, "diameter")),
        length_mm=int_of(spec(s, "length")),
    )


def load_wheelset(row):
    s = row["specs"]
    WheelSet.objects.update_or_create(
        import_url=row["source_url"],
        defaults=dict(
            wheel_size="700c",
            max_tire_width_mm=int_of(spec(s, "optimal tire size")),
            rim_name=row["name"],
            hub_name=(spec(s, "hub") or "").split(".")[0].strip(),
            **base(row, "wheelset", grams(spec(s, "wheel weight"))),
        ),
    )


LOADERS = {
    "DSNV®101 DROP BAR": lambda r: load_handlebar(r, "drop"),
    "DSNV®102 FLAT BAR": lambda r: load_handlebar(r, "flat"),
    "DSNV®103 STEM": load_stem,
    "DSNV®105 SEATPOST": load_seatpost,
    "DSNV®106 WHEEL SET": load_wheelset,
}


def load():
    rows = [r for r in json.load(open(JSON_PATH)) if r["category"] == "components"]
    loaded = 0
    for r in rows:
        loader = LOADERS.get(r["name"])
        if not loader:
            print("no loader for", r["name"])
            continue
        loader(r)
        loaded += 1
    print(f"loaded {loaded} components")


if __name__ == "__main__":
    load()
