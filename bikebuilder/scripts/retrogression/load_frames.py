import json
import os
import re
import sys

import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bikebuilder.settings")
django.setup()

from apps.components.models import Frame, FrameOption
from apps.components.parsers import parse_axle_spacing, parse_bb_shell

FRAME_JSON = os.path.join(os.path.dirname(__file__), "retrogression", "frame.json")


def strip_size(name):
    m = re.match(r"^(.*) - .+$", name)
    return m.group(1) if m else name


def tire_clearance(specs):
    text = " ".join(v for k, v in specs.items() if "tire" in k.lower() or "clear" in k.lower())
    nums = [int(n) for n in re.findall(r"(\d{2,3})\s*mm", text)]
    return min(nums) if nums else None


def collapse(rows):
    frames = {}
    for row in rows:
        frame = frames.setdefault(row["source_url"], {**row, "sizes": []})
        frame["sizes"].append(row["variant_title"])
    return list(frames.values())


def load():
    rows = json.load(open(FRAME_JSON))
    loaded, skipped = 0, []

    for r in collapse(rows):
        specs = r["specs"]
        clearance = tire_clearance(specs)
        try:
            rear_axle = parse_axle_spacing(specs.get("frame/fork spacing"))
        except ValueError as e:
            skipped.append((r["name"], str(e)))
            continue
        if clearance is None:
            skipped.append((r["name"], "no tire clearance"))
            continue

        try:
            bb_type, bb_width = parse_bb_shell(specs.get("BB"))
        except ValueError:
            bb_type, bb_width = None, None

        frame, _ = Frame.objects.update_or_create(
            import_url=r["source_url"],
            defaults=dict(
                component_type="frame",
                name=strip_size(r["name"]),
                brand=r["brand"],
                price=r["price"],
                weight_grams=int(r["weight_grams"]),
                description=r["description"],
                image_url=r["image_url"],
                rear_axle_standard=rear_axle,
                max_tire_clearance_mm=clearance,
                bb_type=bb_type,
                bb_width_mm=bb_width,
                frame_brake_drilled=bool(r["frame_brake_drilled"]),
                fork_brake_drilled=bool(r["fork_brake_drilled"]),
            ),
        )
        for size in r["sizes"]:
            FrameOption.objects.get_or_create(frame=frame, size=size)
        loaded += 1

    print(f"loaded {loaded} frames, skipped {len(skipped)}")
    for name, err in skipped:
        print(" -", name, "|", err)


if __name__ == "__main__":
    load()
