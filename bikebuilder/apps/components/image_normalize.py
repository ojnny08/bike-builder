import hashlib
import io
import urllib.request

from PIL import Image, ImageChops

from apps.builds.image_upload import put_bytes

CANVAS = (1200, 900)
CONTENT_RATIO = 0.88
BG = (255, 255, 255)
TRIM_TOLERANCE = 12
LINE_THRESHOLD = 0.005
PROFILE_WIDTH = 900
USER_AGENT = "Mozilla/5.0 (compatible; BikeBuilder image import)"


def _download(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def _border_pixels(image):
    edge = image.convert("RGB")
    width, height = edge.size
    step = max(1, min(width, height) // 64)
    top = [edge.getpixel((x, 0)) for x in range(0, width, step)]
    bottom = [edge.getpixel((x, height - 1)) for x in range(0, width, step)]
    left = [edge.getpixel((0, y)) for y in range(0, height, step)]
    right = [edge.getpixel((width - 1, y)) for y in range(0, height, step)]
    return top + bottom + left + right


def _trim(image):
    border = _border_pixels(image)
    channels = list(zip(*border))
    background = tuple(sorted(c)[len(c) // 2] for c in channels)
    spread = max(max(c) - min(c) for c in channels)
    tolerance = max(TRIM_TOLERANCE, spread + TRIM_TOLERANCE)

    scale = min(1.0, PROFILE_WIDTH / image.width)
    small = image.resize((max(1, round(image.width * scale)), max(1, round(image.height * scale))))
    diff = ImageChops.difference(small, Image.new("RGB", small.size, background))
    mask = diff.convert("L").point(lambda p: 1 if p > tolerance else 0)

    width, height = mask.size
    pixels = mask.tobytes()
    rows = [r for r in range(height) if sum(pixels[r * width:(r + 1) * width]) > width * LINE_THRESHOLD]
    columns = [c for c in range(width) if sum(pixels[c::width]) > height * LINE_THRESHOLD]
    if not rows or not columns:
        return image
    box = (columns[0] / scale, rows[0] / scale, (columns[-1] + 1) / scale, (rows[-1] + 1) / scale)
    return image.crop(tuple(round(v) for v in box))


def normalize(raw):
    image = Image.open(io.BytesIO(raw))
    if image.mode in ("RGBA", "LA", "P"):
        image = image.convert("RGBA")
        flattened = Image.new("RGB", image.size, BG)
        flattened.paste(image, mask=image.split()[-1])
        image = flattened
    else:
        image = image.convert("RGB")

    content = _trim(image)
    scale = min(
        CANVAS[0] * CONTENT_RATIO / content.width,
        CANVAS[1] * CONTENT_RATIO / content.height,
    )
    size = (max(1, round(content.width * scale)), max(1, round(content.height * scale)))
    content = content.resize(size, Image.LANCZOS)

    canvas = Image.new("RGB", CANVAS, BG)
    canvas.paste(content, ((CANVAS[0] - size[0]) // 2, (CANVAS[1] - size[1]) // 2))

    buffer = io.BytesIO()
    canvas.save(buffer, "JPEG", quality=88, optimize=True)
    return buffer.getvalue()


def normalized_url(source_url, component_type):
    digest = hashlib.sha1(source_url.encode()).hexdigest()[:16]
    key = f"component-image/{component_type}/{digest}.jpg"
    return put_bytes(normalize(_download(source_url)), key, "image/jpeg")


def resolve_image(source_url, component_type):
    if not source_url:
        return ""
    try:
        return normalized_url(source_url, component_type)
    except Exception as exc:
        print(f"  image normalize failed ({type(exc).__name__}): {source_url}")
        return source_url
