"""
Velodrome.Shop Scraper — Track Components
==========================================
velodrome.shop sits behind Cloudflare, so plain `requests` gets a 403 challenge.
curl_cffi impersonates a real Chrome TLS fingerprint and passes straight through.

Writes one JSON file per ComponentType into this directory.

The shop puts its spec sheet inside the description body as bolded label/value
pairs ("Key Features at a Glance"), so specs are pulled from there rather than
from a spec table. The full description is kept too, for anything not captured.
Any value that could not be found is False.

Install:
    pip install curl_cffi beautifulsoup4

Run:
    python scrape_velodrome.py
"""

import json
import os
import re
import time

from bs4 import BeautifulSoup
from curl_cffi import requests

BASE = "https://www.velodrome.shop"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DELAY = 0.3

CATEGORIES = {
    "frame": ["track-cycling-frames"],
    "complete_bikes": ["track-cycling-bikes"],
    "wheel": ["track-wheels"],
    "tire": ["track-clinchers", "track-tubulars"],
    "track_hub": ["track-hubs"],
    "crankset": ["144bcd-chainsets", "130bcd-chainsets"],
    "chainring": ["144bcd-chainrings", "200bcd-chainrings", "130bcd-chainrings"],
    "sprocket": ["track-sprockets", "freewheel-sprockets"],
    "bottom_bracket": ["square-taper-jis/iso", "octalink", "outboard"],
    "chain": ["track-chains"],
    "handlebar": ["sprint-bars", "endurance-bars"],
    "stem": ["stems"],
    "saddle": ["saddles"],
    "brake": ["brakesets", "brake-calipers", "brake-levers"],
    "pedals": ["pedals"],
}

# Parent/landing paths that live under a category path but are not products
NOT_PRODUCTS = {
    "/track-wheels/tyres/",
    "/track-bikes/frames/",
    "/components/accessories/",
    "/inner-tubes/spares/",
    "/spokes/skewers/",
    "/track-pedals/straps/",
    "/cleats/spares/",
}

# Longest-first, so "Black Inc" matches before a bare first word would
BRANDS = [
    "Princeton CarbonWorks", "Bridgestone Anchor", "TA Specialites",
    "Sturmey Archer", "CeramicSpeed", "gebioMized", "Dia-Compe", "DT Swiss",
    "Black Inc", "BlackInc", "Phil Wood", "Chris King", "Dura Ace",
    "Velodrome.Shop", "Velodrome Shop", "Bridgestone", "Colnago", "Factor",
    "Look", "Ridley", "Halo", "Corima", "Campagnolo", "Mavic", "Shimano",
    "Miche", "Izumi", "EAI", "FSA", "Digirit", "Runwell", "Sugino", "Dixna",
    "Hozan", "KMC", "Continental", "Vittoria", "Michelin", "Challenge",
    "Veloflex", "Schwalbe", "Dugast", "Selle", "Fizik", "Prologo", "Rotor",
    "SRAM", "Token", "Novatec", "Zipp", "Vision", "Origin8", "MKS", "Wellgo",
    "Speedplay", "Tioga", "Kalloy", "Deda", "3T", "Nitto", "Thomson", "Cinelli",
    "Soma", "ITM", "Bontrager", "Tektro", "Promax", "TRP", "Renold", "Genetic",
    "Nanko", "Paloma", "Garmin", "FMB", "DID", "GBR", "PRO",
]

# Titles starting with a material or part noun are Velodrome.Shop house products
HOUSE_BRAND = "Velodrome.Shop"
GENERIC_FIRST_WORDS = {
    "alloy", "carbon", "ceramic", "track", "sprocket", "handlebar", "heavy",
    "singlespeed", "steel", "titanium", "aero",
}

SPEC_SEPARATORS = "：:–—-"
# Spec labels are short; anything longer is prose that happened to be bolded
SPEC_KEY_RE = re.compile(r"^[A-Za-z0-9][\w /()&.,'\"+-]{1,40}$")
MAX_KEY_WORDS = 5
WEIGHT_RE = re.compile(
    r"(\d[\d.,]*)\s*(kgs?|kilograms?|g|grams?|gr)\b", re.I
)
# In free prose, only trust a number that follows a weight cue
WEIGHT_CUE_RE = re.compile(
    r"(?:weigh\w*|scales?\s+at|tipping\s+the\s+scales\s+at)\D{0,40}?"
    r"(\d[\d.,]*)\s*(kgs?|kilograms?|g|grams?|gr)\b",
    re.I,
)
# "800 grams lighter than" is a comparison, not this product's weight
COMPARATIVE_RE = re.compile(r"lighter|heavier|less than|more than|compared|than", re.I)
MAX_WEIGHT_LINE_WORDS = 8

session = requests.Session(impersonate="chrome")


def get(path):
    url = path if path.startswith("http") else BASE + path
    res = session.get(url, timeout=30)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")


def text_of(node):
    if node is None:
        return ""
    raw = node.get_text("\n").replace("\xa0", " ")
    lines = [ln.strip() for ln in raw.split("\n")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def flat_text(node):
    return re.sub(r"\s+", " ", node.get_text(" ").replace("\xa0", " ")).strip()


def brand_of(name):
    lowered = name.lower()
    for brand in BRANDS:
        if lowered.startswith(brand.lower()):
            return brand

    first = name.split()[0] if name else ""
    return HOUSE_BRAND if first.lower() in GENERIC_FIRST_WORDS else first


def category_paths():
    return {f"/{cat}/" for cats in CATEGORIES.values() for cat in cats} | NOT_PRODUCTS


def product_urls(category):
    skip = category_paths()
    prefix = f"{BASE}/{category}/"
    seen, urls = set(), []
    page = 1

    while True:
        suffix = f"?page={page}" if page > 1 else ""
        soup = get(f"/{category}/{suffix}")

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if not href.startswith(prefix) or "?" in href:
                continue
            path = href[len(BASE):]
            if path in skip or path in seen:
                continue
            seen.add(path)
            urls.append(path)

        numbers = [
            int(a.get_text(strip=True))
            for a in soup.select(".pagination .page-link")
            if a.get_text(strip=True).isdigit()
        ]
        if page >= max(numbers or [1]):
            return urls
        page += 1


def clean_key(raw):
    return raw.strip().strip(SPEC_SEPARATORS + " ").strip()


def clean_value(raw):
    return raw.strip().lstrip(SPEC_SEPARATORS + " ").strip().rstrip(" .,;")


def add_spec(specs, key, value):
    key, value = clean_key(key), clean_value(value)
    if not key or not value or not SPEC_KEY_RE.match(key):
        return
    if len(key.split()) > MAX_KEY_WORDS:
        return
    specs.setdefault(key, value)


def specs_from_bold(desc, specs):
    """<li><strong>Weight</strong>: ~818g</li> — the shop's spec-sheet pattern."""
    for tag in desc.find_all(["strong", "b"]):
        key = flat_text(tag)
        if not key:
            continue

        trailing = "".join(
            sib if isinstance(sib, str) else sib.get_text(" ")
            for sib in tag.next_siblings
        )
        add_spec(specs, key, re.sub(r"\s+", " ", trailing.replace("\xa0", " ")))


def specs_from_tables(desc, specs):
    for row in desc.find_all("tr"):
        cells = row.find_all(["td", "th"])
        if len(cells) == 2:
            add_spec(specs, flat_text(cells[0]), flat_text(cells[1]))


def specs_from_lines(desc, specs):
    """Fallback for products written as plain 'Thread Size - 1.37x24Tpi' lines.

    Dashes must be space-separated so hyphenated words ("Halo Fix-T Cover",
    "solid-forged") are not mistaken for a label/value split.
    """
    patterns = (
        re.compile(r"^([^:]{2,40}?)\s*:\s*(.+)$"),
        re.compile(r"^(.{2,40}?)\s+[–—-]\s+(.+)$"),
    )
    for line in text_of(desc).split("\n"):
        for pattern in patterns:
            match = pattern.match(line)
            if match:
                add_spec(specs, match.group(1), match.group(2))
                break


def parse_specs(desc):
    if desc is None:
        return {}

    specs = {}
    specs_from_bold(desc, specs)
    specs_from_tables(desc, specs)
    specs_from_lines(desc, specs)
    return specs


def to_grams(amount, unit):
    """'1,980' + 'g' -> 1980. Commas before three digits are thousands, not decimals."""
    normalised = re.sub(r",(?=\d{3}(\D|$))", "", amount).replace(",", ".").rstrip(".")
    try:
        value = float(normalised)
    except ValueError:
        return None

    grams = value * 1000 if unit.lower().startswith(("kg", "kilo")) else value
    return round(grams) if grams > 0 else None


def parse_weight_grams(specs, description):
    """Weight in grams from a spec entry, else from a cued phrase in the prose."""
    for key, value in specs.items():
        if "weight" not in key.lower():
            continue
        match = WEIGHT_RE.search(str(value))
        if match:
            grams = to_grams(match.group(1), match.group(2))
            if grams:
                return grams

    match = WEIGHT_CUE_RE.search(description or "")
    if match:
        grams = to_grams(match.group(1), match.group(2))
        if grams:
            return grams

    # Short spec-like lines such as "~400g" or "Available sizes: 700x23c (187g)".
    # Long lines are prose, where a gram figure usually describes something else.
    for line in (description or "").split("\n"):
        if len(line.split()) > MAX_WEIGHT_LINE_WORDS or COMPARATIVE_RE.search(line):
            continue
        match = WEIGHT_RE.search(line)
        if match:
            grams = to_grams(match.group(1), match.group(2))
            if grams:
                return grams
    return False


def parse_options(form):
    if form is None:
        return {}

    options = {}
    for select in form.find_all("select"):
        label = form.find("label", attrs={"for": select.get("id")})
        key = text_of(label) if label else select.get("name", "Option")
        values = [o.get_text(strip=True) for o in select.find_all("option")]
        options[key] = [v for v in values if v]
    return options


def main_price_block(soup):
    for block in soup.select(".product-price"):
        if not block.find_parent(class_="product-info"):
            return block
    return None


def parse_prices(block):
    if block is None:
        return False, False

    text = block.get_text(" ")
    amounts = [
        float(m.replace("£", "").replace(",", ""))
        for m in re.findall(r"£[\d,]+\.?\d*", text)
    ]
    if not amounts:
        return False, False
    if re.search(r"sale price", text, re.I) and len(amounts) > 1:
        return amounts[0], amounts[1]
    return amounts[0], False


def main_image(soup):
    candidates = [
        img["src"] for img in soup.find_all("img", src=True)
        if "images/products/" in img["src"]
        and "thumbs" not in img["src"]
        and "preview" not in img["src"]
    ]
    primary = [src for src in candidates if "secondary" not in src]

    for src in primary or candidates:
        return f"{BASE}/{src.split('?')[0]}"
    return False


def hidden_value(form, field):
    if form is None:
        return False
    node = form.find("input", attrs={"name": field})
    return node.get("value") or False if node else False


def scrape_product(path, component_type, site_category):
    soup = get(path)

    forms = soup.select("form.form-add-to-cart")
    form = max(forms, key=lambda f: len(str(f))) if forms else None
    price, compare_at = parse_prices(main_price_block(soup))

    name = text_of(soup.find("h1"))
    desc = soup.select_one(".product-description-content")
    description = text_of(desc)
    specs = parse_specs(desc)

    return {
        "name": name or False,
        "brand": brand_of(name) or False,
        "product_code": hidden_value(form, "oa_id"),
        "pid": hidden_value(form, "pid"),
        "component_type": component_type,
        "site_category": site_category,
        "price": price,
        "compare_at": compare_at,
        "currency": "GBP",
        "weight_grams": parse_weight_grams(specs, description),
        "options": parse_options(form) or False,
        "specs": specs or False,
        "description": description or False,
        "image_url": main_image(soup),
        "source_url": BASE + path,
    }


def scrape_component(component_type, categories):
    items = []

    for category in categories:
        paths = product_urls(category)
        print(f"  {category}: {len(paths)} products")

        for path in paths:
            try:
                items.append(scrape_product(path, component_type, category))
            except Exception as exc:
                print(f"    FAILED {path}: {exc}")
            time.sleep(DELAY)

    return items


def main():
    for component_type, categories in CATEGORIES.items():
        print(f"{component_type}")
        items = scrape_component(component_type, categories)

        out_path = os.path.join(OUT_DIR, f"{component_type}.json")
        with open(out_path, "w") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"  -> {out_path} ({len(items)} items)\n")


if __name__ == "__main__":
    main()
