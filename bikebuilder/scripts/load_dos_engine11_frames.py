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

from apps.components.models import Frame, FrameOption
from apps.components.parsers import parse_bb_shell, parse_fork_type, parse_seatpost_size

FILES = [
    ("Dosnoventa", os.path.join(os.path.dirname(__file__), "dosnoventa_all.json")),
    ("Engine11", os.path.join(os.path.dirname(__file__), "engine11_frames.json")),
]

DEFAULT_SIZES = ["S", "M", "L"]


def parse_weight(row):
    specs = row["specs"]
    for text in [row.get("weight"), specs.get("Frame"), specs.get("Weight"), specs.get("FRAME WEIGHT")]:
        m = re.search(r"(\d{3,4})\s*g", text or "", re.I)
        if m:
            return int(m.group(1))
    return 0


def parse_tire_clearance(specs):
    text = " ".join(v for k, v in specs.items() if "tire" in k.lower() or "clear" in k.lower())
    m = re.search(r"(\d{2})\s*c\b", text, re.I)
    return int(m.group(1)) if m else None


def spec(specs, *keys):
    for k in keys:
        for sk, v in specs.items():
            if sk.lower().strip().lstrip("-").strip() == k.lower():
                return v
    return None


def load():
    loaded = 0
    for brand, path in FILES:
        rows = [r for r in json.load(open(path)) if r["category"] == "frames"]
        for r in rows:
            specs = r["specs"]
            try:
                bb_type, bb_width = parse_bb_shell(spec(specs, "bb"))
            except ValueError:
                bb_type, bb_width = None, None

            frame, _ = Frame.objects.update_or_create(
                import_url=r["source_url"],
                defaults=dict(
                    component_type="frame",
                    name=r["name"],
                    brand=brand,
                    price=r["price"],
                    weight_grams=parse_weight(r),
                    description=r["description"],
                    image_url=r["image_url"],
                    fork_type=parse_fork_type(spec(specs, "fork")),
                    seatpost_size=parse_seatpost_size(spec(specs, "seat tube", "seatpost size", "seat post size")),
                    max_tire_clearance_mm=parse_tire_clearance(specs),
                    bb_type=bb_type,
                    bb_width_mm=bb_width,
                ),
            )
            for size in DEFAULT_SIZES:
                FrameOption.objects.get_or_create(frame=frame, size=size)
            loaded += 1
        print(f"{brand}: {len(rows)} frames")

    print(f"loaded/updated {loaded} frames")


if __name__ == "__main__":
    load()
