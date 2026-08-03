import json
import os
import re
import sys
from decimal import Decimal

import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bikebuilder.settings")
django.setup()

from apps.components.models import Handlebar, HandlebarOptions

HB_JSON = os.path.join(os.path.dirname(__file__), "extracted", "handlebar.json")


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


def mm_of(raw):
    m = re.search(r"(\d+(?:\.\d+)?)\s*mm", str(raw or ""))
    return float(m.group(1)) if m else None


def int_mm(raw):
    v = mm_of(raw)
    return int(v) if v else None


def bar_type_of(g):
    cat = (g.get("site_category") or "").lower()
    name = g["name"].lower()
    if "drop" in cat:
        return "drop"
    if "bullhorn" in cat:
        return "bullhorn"
    if "townie" in cat or "cruiser" in cat:
        return "riser"
    s = specs(g)
    rise = mm_of(s.get("rise") or s.get("drop/rise"))
    if "riser" in name or "rizer" in name or (rise and rise > 0):
        return "riser"
    return "flat"


def clamp_of(g):
    s = specs(g)
    v = mm_of(s.get("clamp") or s.get("clamp size") or s.get("bar diameter"))
    return Decimal(str(v)) if v else Decimal("31.8")


def widths_of(g):
    widths = {int_mm(options_of(v).get("width") or options_of(v).get("size") or specs(v).get("width"))
              for v in g["variants"]}
    widths = {w for w in widths if w}
    if widths:
        return widths
    w = int_mm(specs(g).get("width"))
    return {w} if w else set()


def load():
    rows = json.load(open(HB_JSON))
    Handlebar.objects.all().delete()
    bars, opts = 0, 0
    for g in collapse(rows):
        s = specs(g)
        bar, _ = Handlebar.objects.update_or_create(
            import_url=g["source_url"],
            defaults=dict(
                bar_type=bar_type_of(g),
                clamp_diameter_mm=clamp_of(g),
                drop_mm=int_mm(s.get("drop")),
                reach_mm=int_mm(s.get("reach")),
                **base(g, "handlebar"),
            ),
        )
        bars += 1
        for w in widths_of(g):
            HandlebarOptions.objects.get_or_create(handlebar=bar, width=w)
            opts += 1
    print(f"loaded {bars} handlebars, {opts} width options")


if __name__ == "__main__":
    load()
