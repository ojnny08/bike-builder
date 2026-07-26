import json
import os
import re
import sys

import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bikebuilder.settings")
django.setup()

from apps.components.models import BottomBracket, ShellType
from apps.components.parsers import parse_bb_shell, parse_bb_spindle

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


def shell_of(row):
    vt = variant_title(row).lower()
    if vt == "english":
        return ShellType.THREADED_BSA, 68
    if vt == "italian":
        return ShellType.THREADED_ITA, 70
    text = " ".join(row.get("spec_notes", [])) + " " + " ".join(str(v) for v in row["specs"].values()) + " " + row["name"]
    try:
        return parse_bb_shell(text)
    except ValueError as e:
        return None, str(e)


def collapse(rows):
    groups = {}
    skipped = []
    for row in rows:
        shell, width = shell_of(row)
        if shell is None:
            skipped.append((row["name"], width))
            continue
        key = (row["source_url"], shell)
        groups.setdefault(key, {**row, "shell": shell, "width": width, "variants": []})["variants"].append(row)
    return list(groups.values()), skipped


def load():
    rows = json.load(open(BRACKET_JSON))
    groups, skipped = collapse(rows)
    loaded = 0

    for g in groups:
        colors = sorted({variant_title(v) for v in g["variants"] if is_color(variant_title(v))})
        BottomBracket.objects.update_or_create(
            import_url=g["source_url"],
            bb_type=g["shell"],
            defaults=dict(
                component_type="bottom_bracket",
                name=strip_variant(g["name"]),
                brand=g["brand"],
                price=min(v["price"] for v in g["variants"]),
                weight_grams=int(g["weight_grams"]),
                description=g["description"],
                image_url=g["image_url"],
                bb_width_mm=g["width"],
                spindle_interface=parse_bb_spindle(g["site_category"], g["name"]),
                colors=colors,
            ),
        )
        loaded += 1

    print(f"loaded {loaded} bottom brackets, skipped {len(skipped)}")
    for name, err in skipped:
        print(" -", name, "|", err)


if __name__ == "__main__":
    load()
