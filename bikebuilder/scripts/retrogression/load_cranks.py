import json
import os
import re
import sys

import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bikebuilder.settings")
django.setup()

from apps.components.models import Crankset, CrankOption, CrankArm, CrankArmOption, BoltCircle
from apps.components.parsers import parse_spindle, parse_spindle_length

BCD_CHOICES = {b.value for b in BoltCircle}

CRANK_JSON = os.path.join(os.path.dirname(__file__), "extracted", "crankset.json")
ARM_JSON = os.path.join(os.path.dirname(__file__), "extracted", "crank_arm.json")

ARM_CHOICES = {"160mm", "165mm", "167.5mm", "170mm", "172.5mm"}
COLORS = ["black", "silver", "gold", "polished", "raw", "white", "red", "blue", "pink", "orange"]


def strip_variant(name):
    m = re.match(r"^(.*) - .+$", name)
    return m.group(1) if m else name


def options_of(row):
    o = row["options"]
    return {k.lower(): v for k, v in o.items()} if isinstance(o, dict) else {}


def variant_title(row):
    return row["variant_title"] if isinstance(row["variant_title"], str) else ""


def find(pattern, *sources):
    for src in sources:
        m = re.search(pattern, (src or "").lower())
        if m:
            return m.group(1)
    return None


def teeth_of(row, opts):
    t = find(r"(\d{2})\s*t", opts.get("chainring"), variant_title(row),
             row["specs"].get("chainring"), row["specs"].get("chainring size"))
    return int(t) if t else None


def length_of(row, opts):
    mm = find(r"(1[0-9]{2}(?:\.\d)?)\s*mm", opts.get("length"), variant_title(row),
              row["specs"].get("crank arm length"), row["specs"].get("length"))
    return f"{mm}mm" if mm else None


def color_of(row, opts):
    color = opts.get("color") or row["specs"].get("color") or row["specs"].get("colors")
    if color:
        return color
    return next((c for c in COLORS if c in variant_title(row).lower()), "")


def spindle_text(row):
    notes = " ".join(row.get("spec_notes", []))
    return f"{row['name']} {' '.join(str(v) for v in row['specs'].values())} {notes} {row.get('description', '')}"


def length_text(row):
    specs = " ".join(str(v) for v in row["specs"].values())
    notes = " ".join(row.get("spec_notes", []))
    return f"{specs} {notes} {row['name']}"


def collapse(rows):
    cranks = {}
    for row in rows:
        crank = cranks.setdefault(row["source_url"], {**row, "variants": []})
        crank["variants"].append(row)
    return list(cranks.values())


def is_crank_arm(name):
    n = name.lower()
    if "crankset" in n:
        return False
    return "crank arm" in n or re.search(r"\barms?\b", n) is not None


def load():
    rows = json.load(open(CRANK_JSON))
    Crankset.objects.all().delete()
    loaded_cs, loaded_arm, options, skipped = 0, 0, 0, []

    for r in collapse(rows):
        arm = is_crank_arm(r["name"])
        if arm and "bottom bracket" in r["name"].lower():
            skipped.append((r["name"], "crank arm bundles a bottom bracket"))
            continue

        iface = parse_spindle(spindle_text(r))
        Model = CrankArm if arm else Crankset
        crank, _ = Model.objects.update_or_create(
            import_url=r["source_url"],
            defaults=dict(
                component_type="crank_arm" if arm else "crankset",
                name=strip_variant(r["name"]),
                brand=r["brand"],
                price=min(v["price"] for v in r["variants"]),
                weight_grams=int(r["weight_grams"]),
                description=r["description"],
                image_url=r["image_url"],
                spindle_interface_mm=iface,
                spindle_length_mm=parse_spindle_length(length_text(r), iface),
            ),
        )

        for v in r["variants"]:
            opts = options_of(v)
            length = length_of(v, opts)
            if length not in ARM_CHOICES:
                skipped.append((v["name"], f"bad length {length!r}"))
                continue

            if arm:
                CrankArmOption.objects.get_or_create(
                    crank_arm=crank,
                    color=color_of(v, opts),
                    length_mm=length,
                    price=v["price"],
                    defaults={"image_colour_url": v["image_url"] or ""},
                )
            else:
                CrankOption.objects.get_or_create(
                    crankset=crank,
                    color=color_of(v, opts),
                    length_mm=length,
                    chainring_teeth=teeth_of(v, opts),
                    price=v["price"],
                    defaults={"image_colour_url": v["image_url"] or ""},
                )
            options += 1

        if arm:
            loaded_arm += 1
        else:
            loaded_cs += 1

    print(f"loaded {loaded_cs} cranksets, {loaded_arm} crank arms, {options} options, skipped {len(skipped)}")
    for name, err in skipped:
        print(" -", name, "|", err)


def bcd_of(row):
    blob = f"{row['name']} {spindle_text(row)}".lower()
    m = re.search(r"(\d{3})\s*mm\s*bcd|bcd[^0-9]{0,6}(\d{3})|(\d{3})\s*bcd", blob)
    if not m:
        return None
    val = next(g for g in m.groups() if g)
    return val if val in BCD_CHOICES else None


def load_arms():
    rows = json.load(open(ARM_JSON))
    CrankArm.objects.all().delete()
    loaded, options, skipped = 0, 0, []

    for r in collapse(rows):
        iface = parse_spindle(spindle_text(r))
        arm, _ = CrankArm.objects.update_or_create(
            import_url=r["source_url"],
            defaults=dict(
                component_type="crank_arm",
                name=strip_variant(r["name"]),
                brand=r["brand"],
                price=min(v["price"] for v in r["variants"]),
                weight_grams=int(r["weight_grams"]),
                description=r["description"],
                image_url=r["image_url"],
                spindle_interface_mm=iface,
                spindle_length_mm=parse_spindle_length(length_text(r), iface),
                bcd=bcd_of(r),
            ),
        )

        for v in r["variants"]:
            opts = options_of(v)
            length = length_of(v, opts)
            if length not in ARM_CHOICES:
                skipped.append((v["name"], f"bad length {length!r}"))
                continue

            CrankArmOption.objects.get_or_create(
                crank_arm=arm,
                color=color_of(v, opts),
                length_mm=length,
                price=v["price"],
                defaults={"image_colour_url": v["image_url"] or ""},
            )
            options += 1
        loaded += 1

    print(f"loaded {loaded} crank arms, {options} options, skipped {len(skipped)}")
    for name, err in skipped:
        print(" -", name, "|", err)


if __name__ == "__main__":
    load_arms() if len(sys.argv) > 1 and sys.argv[1] == "arms" else load()
