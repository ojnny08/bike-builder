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

FRAME_JSON = os.path.join(os.path.dirname(__file__), "extracted", "frame.json")


def strip_size(name):
    m = re.match(r"^(.*) - .+$", name)
    return m.group(1) if m else name


def notes_matching(notes, *keywords):
    return " ".join(n for n in notes if any(k in n.lower() for k in keywords))


def tire_clearance(specs, notes):
    text = " ".join(v for k, v in specs.items() if "tire" in k.lower() or "clear" in k.lower())
    nums = re.findall(r"(\d{2,3})\s*mm", text)
    if not nums:
        nums = re.findall(r"(\d{2,3})\s*mm", notes_matching(notes, "clear", "tire"))
    return min(int(n) for n in nums) if nums else None


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
        notes = r.get("spec_notes", [])
        clearance = tire_clearance(specs, notes)
        if clearance is None:
            skipped.append((r["name"], "no tire clearance"))
            continue

        try:
            bb_type, bb_width = parse_bb_shell(specs.get("BB") or notes_matching(notes, "bsa", "english", "italian", "threaded", "bracket shell"))
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
                fork_type=parse_fork_type(specs.get("fork") or notes_matching(notes, "fork", "steerer", "tapered")),
                seatpost_size=parse_seatpost_size(specs.get("seatpost size") or notes_matching(notes, "seatpost", "seat post")),
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
