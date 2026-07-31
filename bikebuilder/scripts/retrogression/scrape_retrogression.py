"""
Retrogression Scraper — Track/Fixed Gear Components
====================================================
retro-gression.com is Shopify with a public products.json, so the whole catalog
comes from a handful of paged API calls — no per-product page fetches, no
Cloudflare challenge.

Each product's body_html carries a "Specifications" heading followed by
"• key: value" bullets, which is where clamp diameters, spindle lengths,
thread standards and weights live. Those are split out into `specs`, and the
prose above the heading is kept as `description`.

One record per VARIANT, since each buyable variant (a cog's tooth count, a
stem's length) has its own SKU, price and specs. Any value that could not be
found is False.

Install:
    pip install curl_cffi beautifulsoup4

Run:
    python scrape_retrogression.py
"""

import json
import os
import re

from bs4 import BeautifulSoup
from curl_cffi import requests

BASE = "https://www.retro-gression.com"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENCY = "USD"

# Shopify product_type -> ComponentType. Anything not listed here is skipped
# (stickers, lockrings, tools, tape, spokes, headsets, forks, bolts, apparel).
CATEGORIES = {
    "frame": ["Framesets", "Frames"],
    "wheel": ["Wheelsets", "Single wheels"],
    "tire": ["Tires"],
    "track_hub": ["Hub Sets", "Rear Hubs", "Front Hubs"],
    "crankset": ["Cranksets"],
    "crank_arm": ["Crank Arms"],
    "chainring": ["144mm BCD chainrings", "130mm BCD chainrings"],
    "sprocket": ["Cogs", "Freewheels"],
    "bottom_bracket": [
        "Square Taper Bottom Brackets",
        "External/Outboard Bottom Brackets",
        "Octalink Bottom Brackets",
    ],
    "chain": ['1/8" Chains', '3/32" Chains'],
    "handlebar": [
        "Flat & Riser Handlebars",
        "Drop Handlebars",
        "Bullhorn Handlebars",
        "Townie & Cruiser Handlebars",
    ],
    "stem": ["Threadless Stems", "Quill Stems"],
    "saddle": ["Saddles"],
    "seatpost": ["Seatposts"],
    "brake": ["Brake Levers", "Brake Calipers"],
    "pedals": ["Clipless Pedals & Cleats", "Platform & Urban Pedals", "Track Pedals"],
}

SPEC_HEADING_RE = re.compile(r"specification", re.I)
BULLET_RE = re.compile(r"^[•·*\-•]\s*")
WEIGHT_RE = re.compile(r"(\d[\d.,]*)\s*(kgs?|kilograms?|g|grams?)\b", re.I)

BRAKE_TOKEN_RE = re.compile(r"drill|brake stud", re.I)
BRAKE_COMBINED_RE = re.compile(r"frame\s*(?:&|and|,|/)\s*fork|fork\s*(?:&|and|,|/)\s*frame", re.I)
NEGATION_RE = re.compile(r"\bnot\b|n't")


def product_type_lookup():
    return {
        product_type: component_type
        for component_type, types in CATEGORIES.items()
        for product_type in types
    }


def fetch_catalog():
    session = requests.Session(impersonate="chrome")
    products = []
    page = 1

    while True:
        url = f"{BASE}/products.json?limit=250&page={page}"
        batch = session.get(url, timeout=30).json()["products"]
        if not batch:
            return products
        products += batch
        page += 1


def to_grams(amount, unit):
    """'1,361' + 'g' -> 1361. Commas before three digits are thousands separators."""
    normalised = re.sub(r",(?=\d{3}(\D|$))", "", amount).replace(",", ".").rstrip(".")
    try:
        value = float(normalised)
    except ValueError:
        return None

    grams = value * 1000 if unit.lower().startswith(("kg", "kilo")) else value
    return round(grams) if grams > 0 else None


def split_body(body_html):
    """Return (description, spec_lines) split at the 'Specifications' heading."""
    soup = BeautifulSoup(body_html or "", "html.parser")

    before, after, seen_heading = [], [], False
    for node in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "li", "div", "span"]):
        if node.find(["p", "li", "div"]):
            continue

        text = node.get_text(" ").replace("\xa0", " ").strip()
        if not text:
            continue
        if SPEC_HEADING_RE.search(text) and len(text) < 40:
            seen_heading = True
            continue

        (after if seen_heading else before).append(text)

    if not seen_heading:
        bullets = [t for t in before if BULLET_RE.match(t)]
        prose = [t for t in before if not BULLET_RE.match(t)]
        return prose, bullets
    return before, after


def parse_specs(spec_lines):
    """'• clamp: 31.8mm' -> {'clamp': '31.8mm'}; bullets with no colon are notes."""
    specs, notes = {}, []

    for line in spec_lines:
        text = BULLET_RE.sub("", line).strip()
        if not text:
            continue

        key, sep, value = text.partition(":")
        key, value = key.strip(), value.strip()
        if sep and key and value and len(key) <= 40:
            specs.setdefault(key, value)
        else:
            notes.append(text)

    return specs, notes


def parse_weight_grams(specs, notes):
    for key, value in specs.items():
        if "weight" not in key.lower():
            continue
        match = WEIGHT_RE.search(value)
        if match:
            grams = to_grams(match.group(1), match.group(2))
            if grams:
                return grams

    for note in notes:
        if "weight" not in note.lower():
            continue
        match = WEIGHT_RE.search(note)
        if match:
            grams = to_grams(match.group(1), match.group(2))
            if grams:
                return grams
    return False


def _subject_negated(text, subject):
    idx = text.find(subject)
    return bool(NEGATION_RE.search(text[idx:idx + 40]))


def brake_drilling(specs, notes, description):
    """Return (frame_drilled, fork_drilled) from prose. front->fork, rear->frame."""
    fragments = list(notes or [])
    fork_spec = (specs or {}).get("fork")
    if fork_spec:
        fragments.append(f"fork {fork_spec}")
    fragments += (description or "").split("\n")

    frame_votes, fork_votes = [], []
    for fragment in fragments:
        text = fragment.lower()
        if not BRAKE_TOKEN_RE.search(text):
            continue

        combined = BRAKE_COMBINED_RE.search(text)
        for subject, votes in (("frame", frame_votes), ("fork", fork_votes)):
            if subject not in text:
                continue
            votes.append(True if combined else not _subject_negated(text, subject))

        if not NEGATION_RE.search(text):
            if "rear" in text:
                frame_votes.append(True)
            if "front" in text:
                fork_votes.append(True)

    resolve = lambda votes: False if False in votes else (True in votes)
    return resolve(frame_votes), resolve(fork_votes)


def price_of(raw):
    try:
        return float(raw)
    except (TypeError, ValueError):
        return False


def variant_options(product, variant):
    names = [o["name"] for o in product.get("options", [])]
    values = [variant.get(f"option{i}") for i in range(1, len(names) + 1)]
    options = {
        name: value for name, value in zip(names, values)
        if value and value.lower() != "default title"
    }
    return options or False


def image_for(product, variant):
    for img in product.get("images", []):
        if variant.get("id") in (img.get("variant_ids") or []):
            return img["src"]

    by_id = {img["id"]: img["src"] for img in product.get("images", [])}
    if variant.get("image_id") in by_id:
        return by_id[variant["image_id"]]

    featured = (product.get("images") or [{}])[0].get("src")
    return featured or False


def build_records(product, component_type):
    description_lines, spec_lines = split_body(product.get("body_html"))
    specs, notes = parse_specs(spec_lines)
    description = "\n".join(description_lines)
    weight = parse_weight_grams(specs, notes)
    handle = product["handle"]

    brake_fields = {}
    if component_type == "frame":
        frame_drilled, fork_drilled = brake_drilling(specs, notes, description)
        brake_fields = {
            "frame_brake_drilled": frame_drilled,
            "fork_brake_drilled": fork_drilled,
        }

    records = []
    for variant in product.get("variants", []):
        title = variant.get("title") or ""
        full_name = product["title"]
        if title and title.lower() != "default title":
            full_name = f"{product['title']} - {title}"

        records.append({
            "name": full_name,
            "brand": product.get("vendor") or False,
            "product_code": variant.get("sku") or False,
            "variant_id": variant.get("id") or False,
            "variant_title": title if title.lower() != "default title" else False,
            "component_type": component_type,
            "site_category": product.get("product_type") or False,
            "price": price_of(variant.get("price")),
            "compare_at": price_of(variant.get("compare_at_price")),
            "currency": CURRENCY,
            "weight_grams": weight,
            "shipping_grams": variant.get("grams") or False,
            "options": variant_options(product, variant),
            "specs": specs or False,
            "spec_notes": notes or False,
            "description": description or False,
            "image_url": image_for(product, variant),
            "source_url": f"{BASE}/products/{handle}",
            **brake_fields,
        })
    return records


def main():
    products = fetch_catalog()
    print(f"fetched {len(products)} products")

    lookup = product_type_lookup()
    buckets = {component_type: [] for component_type in CATEGORIES}

    for product in products:
        component_type = lookup.get(product.get("product_type"))
        if not component_type:
            continue
        if component_type == "crank_arm" and "bottom bracket" in (product.get("title") or "").lower():
            continue
        buckets[component_type] += build_records(product, component_type)

    for component_type, records in buckets.items():
        out_path = os.path.join(OUT_DIR, f"{component_type}.json")
        with open(out_path, "w") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        print(f"  {component_type:16} {len(records):>4} variants -> {out_path}")


if __name__ == "__main__":
    main()
