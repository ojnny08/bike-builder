import json
import os
import re
import sys

import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bikebuilder.settings")
django.setup()

from apps.components.models import Chainring, ChainringOption, BoltCircle

RING_JSON = os.path.join(os.path.dirname(__file__), "chainring.json")
BCD_CHOICES = {b.value for b in BoltCircle}


def strip_variant(name):
    m = re.match(r"^(.*) - .+$", name)
    return m.group(1) if m else name


def collapse(rows):
    rings = {}
    for row in rows:
        ring = rings.setdefault(row["source_url"], {**row, "variants": []})
        ring["variants"].append(row)
    return list(rings.values())


def teeth_of(row):
    opts = row["options"] if isinstance(row["options"], dict) else {}
    specs = row["specs"] if isinstance(row["specs"], dict) else {}
    text = f"{opts.get('size', '')} {row['variant_title'] or ''} {specs.get('size', '')} {row['name']}"
    m = re.search(r"(\d{2,3})\s*t\b", text.lower())
    return int(m.group(1)) if m else None


def bcd_of(row):
    m = re.match(r"(\d{3})", row["site_category"] or "")
    return m.group(1) if m and m.group(1) in BCD_CHOICES else None


def colour_of(row):
    opts = row["options"] if isinstance(row["options"], dict) else {}
    return (opts.get("color") or "")[:40]


def load():
    rows = json.load(open(RING_JSON))
    Chainring.objects.all().delete()
    loaded, options, skipped = 0, 0, []

    for r in collapse(rows):
        prices = [v["price"] for v in r["variants"] if v["price"]]
        if not prices:
            skipped.append((r["name"], "no priced variants"))
            continue

        ring = Chainring.objects.create(
            component_type="chainring",
            name=strip_variant(r["name"]),
            brand=r["brand"] or "",
            price=min(prices),
            weight_grams=int(r["weight_grams"] or 0),
            description=r["description"] or "",
            image_url=r["image_url"] or "",
            import_url=r["source_url"],
            bcd=bcd_of(r),
        )

        for v in r["variants"]:
            teeth = teeth_of(v)
            if not teeth or not v["price"]:
                skipped.append((v["name"], f"teeth={teeth!r} price={v['price']!r}"))
                continue
            ChainringOption.objects.create(
                chainring=ring,
                color=colour_of(v),
                chainring_teeth=teeth,
                price=v["price"],
            )
            options += 1
        loaded += 1

    print(f"loaded {loaded} chainrings, {options} options, skipped {len(skipped)}")
    for name, err in skipped:
        print(" -", name, "|", err)


if __name__ == "__main__":
    load()
