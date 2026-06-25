import argparse
import csv
import hashlib
import json
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.tracksupermarket.com"

# Scrape targets: (path, component_type, needs_model). `needs_model=True` flags items whose
# category has no matching Django model yet (pedals, hubs, brake levers) — scraped for review
# but not directly importable. Edit this table to add/remove categories.
CATEGORIES = [
    ("/cranks/cranks-chain-rings-bottom-brackets/crank-sets.html", "crankset", False),
    ("/cranks/cranks-chain-rings-bottom-brackets/bottom-brackets.html", "bottom_bracket", False),
    ("/cranks/cranks-chain-rings-bottom-brackets/chainrings.html", "chainring", True),
    ("/cranks/cogs-chains/chains.html", "chain", False),
    ("/cranks/cogs-chains/cogs/fixed-cogs.html", "sprocket", False),
    ("/cranks/cogs-chains/cogs/freewheel-cogs.html", "sprocket", False),
    ("/frames/track-frames.html", "frame", False),
    ("/frames/road-frames.html", "frame", False),
    ("/handlesstemsgrips/handlebars/bullhorn-bars.html", "handlebar", False),
    ("/handlesstemsgrips/handlebars/drop-bars.html", "handlebar", False),
    ("/handlesstemsgrips/handlebars/riser-bars.html", "handlebar", False),
    ("/handlesstemsgrips/handlebars/straight-bars.html", "handlebar", False),
    ("/brakes-117/brake-calipers.html", "brake", False),
    ("/brakes-117/brake-levers.html", "brake", True),
    ("/saddles/saddles.html", "saddle", False),
    ("/saddles/seat-posts.html", "seatpost", False),
    ("/wheels/complete-wheels.html", "wheel", False),
    ("/wheels/tires/clincher-tires.html", "tire", False),
    ("/wheels/tires/tubular-tires.html", "tire", False),
    ("/pedals/pedals.html", "pedal", True),
    ("/pedals/pedal-straps.html", "pedal", True),
    ("/pedals/toe-clips.html", "pedal", True),
    ("/wheels/hubs/hubs.html", "hub", True),
]

# Known brands for the name-based heuristic. Multi-word entries first so they win over a
# single-token fallback. Brand is not a structured field on the site — always review.
BRANDS = [
    "H Plus Son", "Euro Asia", "Rin Project", "Katakura Silk", "Chris King",
    "Nitto", "Sugino", "Shimano", "Campagnolo", "MKS", "HKK", "Izumi", "DID",
    "Kaisei", "Nagasawa", "Cherubim", "Samson", "Dia Compe", "Dia-Compe", "Tange", "Miche",
    "Phil Wood", "Brooks", "Selle", "Velocity", "Continental", "Vittoria", "Panaracer",
    "Kashimax", "Hirame",
]

# Bare requests get a 403; a browser-like UA + Accept-Language returns 200.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

CACHE_DIR = Path(__file__).parent / ".cache"
REQUEST_DELAY_S = 1.5          # polite pause between *network* fetches (not cache hits)
MAX_RETRIES = 3
RETRY_BACKOFF_S = 5            # base wait; grows linearly per retry


def fetch(url: str) -> str:
    """Return page HTML, served from the on-disk cache when available.

    On a cache miss we fetch politely (delay + browser headers) and retry with
    backoff on throttling/server errors before raising.
    """
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / (hashlib.sha1(url.encode()).hexdigest() + ".html")
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

    for attempt in range(1, MAX_RETRIES + 1):
        time.sleep(REQUEST_DELAY_S)
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            cache_file.write_text(resp.text, encoding="utf-8")
            return resp.text
        if resp.status_code not in (403, 429, 500, 502, 503, 504):
            resp.raise_for_status()
        wait = RETRY_BACKOFF_S * attempt
        print(f"  ! {resp.status_code} on {url} — retry {attempt}/{MAX_RETRIES} in {wait}s")
        time.sleep(wait)

    raise RuntimeError(f"Failed to fetch {url} after {MAX_RETRIES} retries")


def parse_price(text: str) -> float | None:
    """'CAD$459.50' -> 459.5. Returns None when no number is present."""
    match = re.search(r"[\d,]+\.?\d*", text.replace(",", ""))
    return float(match.group()) if match else None


def total_pages(soup: BeautifulSoup) -> int:
    """Read 'Page: X of Y' from the Magento pager; default to 1 if absent."""
    pager = soup.find(class_="pager-box")
    if not pager:
        return 1
    match = re.search(r"of\s+(\d+)", pager.get_text())
    return int(match.group(1)) if match else 1


def parse_listing(html: str) -> list[dict]:
    """Extract one page of products: name, product url, image url, list price."""
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for name_el in soup.select("h2.product-name a"):
        block = name_el.find_parent(class_="product-shop") or soup
        img = block.find_previous(class_="product-img-box")
        img_el = img.find("img") if img else None
        price_el = block.select_one(".price-box .price")
        products.append(
            {
                "name": name_el.get("title") or name_el.get_text(strip=True),
                "source_url": name_el.get("href"),
                "image_url": img_el.get("src") if img_el else None,
                "price": parse_price(price_el.get_text()) if price_el else None,
            }
        )
    return products


def collect_listing(category_url: str) -> list[dict]:
    """All products across every paginated page of a category."""
    first = fetch(category_url)
    pages = total_pages(BeautifulSoup(first, "html.parser"))
    products = parse_listing(first)
    for page in range(2, pages + 1):
        sep = "&" if "?" in category_url else "?"
        products += parse_listing(fetch(f"{category_url}{sep}p={page}"))
    return products


def parse_product(html: str) -> dict:
    """Pull the full description and configurable variants from a product page."""
    soup = BeautifulSoup(html, "html.parser")

    # The full description is the plain `.box-collateral`; its sibling `.box-collateral.box-up-sell`
    # is related products, so match the box whose class is exactly ['box-collateral']. Fall back to
    # the short teaser when no full block exists.
    desc_el = next(
        (b for b in soup.select(".product-collateral .box-collateral")
         if b.get("class") == ["box-collateral"]),
        None,
    ) or soup.select_one(".short-description .std")
    description = desc_el.get_text(" ", strip=True) if desc_el else ""
    if description.lower().startswith("details:"):
        description = description[len("details:"):].strip()

    # Variants live in an inline `new Product.Config({... "options":[{"label":..,"price":..}] })`.
    # Option objects are the only place a "label" key is immediately followed by "price".
    variants = []
    config = re.search(r"Product\.Config\((\{.*?\})\);", html, re.DOTALL)
    if config:
        for label, price in re.findall(
            r'"label":"([^"]+)","price":"([^"]*)"', config.group(1)
        ):
            variants.append({"label": label, "price_delta": parse_price(price) or 0.0})

    return {"description": description, "variants": variants}


def guess_brand(name: str) -> str:
    """Best-effort brand from the product name; falls back to the first word. For review."""
    lowered = name.lower()
    for brand in BRANDS:
        if brand.lower() in lowered:
            return brand
    return name.split()[0] if name.split() else ""


def category_path(path: str) -> str:
    return path.strip("/").removesuffix(".html")


def scrape_category(path: str, component_type: str, needs_model: bool, limit: int | None) -> list[dict]:
    listing = collect_listing(f"{BASE_URL}{path}")
    if limit:
        listing = listing[:limit]
    records = []
    for item in listing:
        detail = parse_product(fetch(item["source_url"]))
        records.append(
            {
                "component_type": component_type,
                "needs_model": needs_model,
                "name": item["name"],
                "brand": guess_brand(item["name"]),
                "price": item["price"],
                "currency": "CAD",
                "description": detail["description"],
                "image_url": item["image_url"],
                "source_url": item["source_url"],
                "variants": detail["variants"],
                "category_path": category_path(path),
            }
        )
    return records


def write_outputs(records: list[dict], out_dir: Path) -> None:
    """Write the full JSON and a flat CSV subset for review."""
    (out_dir / "scraped_components.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    csv_cols = ["component_type", "needs_model", "brand", "name", "price", "currency", "source_url"]
    with (out_dir / "scraped_components.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Track Supermarket into a review JSON.")
    parser.add_argument("--only", help="scrape only this component_type (e.g. crankset)")
    parser.add_argument("--limit", type=int, help="max products per category (for quick test runs)")
    args = parser.parse_args()

    targets = [c for c in CATEGORIES if not args.only or c[1] == args.only]
    if not targets:
        raise SystemExit(f"No categories match --only {args.only!r}")

    all_records = []
    summary = []
    for path, component_type, needs_model in targets:
        print(f"-> {component_type:<14} {path}")
        records = scrape_category(path, component_type, needs_model, args.limit)
        if not records:
            print(f"   ! 0 products — category may be a container page, check the URL")
        all_records += records
        summary.append((path, component_type, len(records)))

    out_dir = Path(__file__).parent
    write_outputs(all_records, out_dir)

    print(f"\n{'='*60}\n{len(all_records)} products written to {out_dir/'scraped_components.json'}\n")
    for path, component_type, count in summary:
        print(f"  {count:>4}  {component_type:<14} {path}")


if __name__ == "__main__":
    main()
