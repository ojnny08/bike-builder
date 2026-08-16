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

from apps.components.models import BottomBracket, BottomBracketOption, ShellType
from apps.components.parsers import parse_bb_shell, parse_bb_spindle, parse_spindle_length

BRACKET_JSON = os.path.join(os.path.dirname(__file__), "extracted", "bottom_bracket.json")

COLORS = ["black", "silver", "gold", "purple", "blue", "red", "violet",
          "midnight", "punch", "ceramic", "white", "pink", "orange", "matte"]


def strip_variant(name):
    m = re.match(r"^(.*) - .+$", name)
    return m.group(1) if m else name


def variant_title(row):
    return row["variant_title"] if isinstance(row["variant_title"], str) else ""


def is_color(vt):
    return any(c in vt.lower() for c in COLORS)


def spindle_text(row):
    return row["site_category"] + " " + row["name"] + " " + " ".join(str(v) for v in row["specs"].values()) + " " + " ".join(row.get("spec_notes", []))


def shell_of(row):
    vt = variant_title(row).lower()
    if vt == "english":
        return ShellType.BSA, 68
    if vt == "italian":
        return ShellType.ITA, 70
    text = " ".join(row.get("spec_notes", [])) + " " + " ".join(str(v) for v in row["specs"].values()) + " " + row["name"]
    try:
        return parse_bb_shell(text)
    except ValueError:
        return None, None


def collapse(rows):
    groups = {}
    for row in rows:
        shell, width = shell_of(row)
        iface = parse_bb_spindle(spindle_text(row))
        length = parse_spindle_length(spindle_text(row), iface)
        key = row["source_url"]
        g = groups.setdefault(key, {**row, "width": width, "iface": iface, "length": length, "shells": set(), "variants": []})
        if shell is not None:
            g["shells"].add(shell)
        if width is not None and g["width"] is None:
            g["width"] = width
        g["variants"].append(row)
    return list(groups.values())


def load():
    rows = json.load(open(BRACKET_JSON))
    groups = collapse(rows)
    loaded = 0

    for g in groups:
        shells = sorted(g["shells"])
        if not shells:
            continue
        colors = sorted({variant_title(v) for v in g["variants"] if is_color(variant_title(v))}) or [""]
        base_price = min(v["price"] for v in g["variants"])

        bb, _ = BottomBracket.objects.update_or_create(
            import_url=g["source_url"],
            spindle_length_mm=g["length"],
            defaults=dict(
                component_type="bottom_bracket",
                name=strip_variant(g["name"]),
                brand=g["brand"],
                price=base_price,
                weight_grams=int(g["weight_grams"]),
                description=g["description"],
                image_url=g["image_url"],
                bb_width_mm=g["width"],
                spindle_interface_mm=g["iface"],
            ),
        )
        bb.options.all().delete()
        for shell in shells:
            for color in colors:
                BottomBracketOption.objects.create(bottom_bracket=bb, bb_type=shell, color=color, price=base_price)
        loaded += 1

    print(f"loaded {loaded} bottom brackets")


if __name__ == "__main__":
    load()
