import hashlib
import io
import urllib.request

from PIL import Image, ImageChops
from rembg import new_session, remove

from apps.builds.image_upload import put_bytes

CANVAS = (1200, 900)
CONTENT_RATIO = 0.88
BG = (255, 255, 255)
TRIM_TOLERANCE = 12
LINE_THRESHOLD = 0.005
PROFILE_WIDTH = 900
WHITE_MIN = 235
PLAIN_SHARE = 0.85
ALPHA_THRESHOLD = 16
USER_AGENT = "Mozilla/5.0 (compatible; BikeBuilder image import)"
SESSION = new_session("isnet-general-use")


def _download(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def _flatten(image):
    if image.mode not in ("RGBA", "LA", "P"):
        return image.convert("RGB")
    image = image.convert("RGBA")
    flattened = Image.new("RGB", image.size, BG)
    flattened.paste(image, mask=image.split()[-1])
    return flattened


def _border_pixels(image):
    width, height = image.size
    step = max(1, min(width, height) // 64)
    top = [image.getpixel((x, 0)) for x in range(0, width, step)]
    bottom = [image.getpixel((x, height - 1)) for x in range(0, width, step)]
    left = [image.getpixel((0, y)) for y in range(0, height, step)]
    right = [image.getpixel((width - 1, y)) for y in range(0, height, step)]
    return top + bottom + left + right


def _is_plain_white(image):
    border = _border_pixels(image)
    white = [p for p in border if min(p) >= WHITE_MIN]
    return len(white) >= len(border) * PLAIN_SHARE


def _trim(image):
    scale = min(1.0, PROFILE_WIDTH / image.width)
    small = image.resize((max(1, round(image.width * scale)), max(1, round(image.height * scale))))
    diff = ImageChops.difference(small, Image.new("RGB", small.size, BG))
    mask = diff.convert("L").point(lambda p: 1 if p > TRIM_TOLERANCE else 0)

    width, height = mask.size
    pixels = mask.tobytes()
    rows = [r for r in range(height) if sum(pixels[r * width:(r + 1) * width]) > width * LINE_THRESHOLD]
    columns = [c for c in range(width) if sum(pixels[c::width]) > height * LINE_THRESHOLD]
    if not rows or not columns:
        return image
    box = (columns[0] / scale, rows[0] / scale, (columns[-1] + 1) / scale, (rows[-1] + 1) / scale)
    return image.crop(tuple(round(v) for v in box))


def _cutout(image):
    cut = remove(image, session=SESSION)
    mask = cut.getchannel("A").point(lambda p: 255 if p > ALPHA_THRESHOLD else 0)
    box = mask.getbbox()
    if not box:
        return cut
    return cut.crop(box)


def _content(image):
    flattened = _flatten(image)
    if _is_plain_white(flattened):
        return _trim(flattened).convert("RGBA")
    return _cutout(flattened)


def normalize(raw):
    content = _content(Image.open(io.BytesIO(raw)))
    scale = min(
        CANVAS[0] * CONTENT_RATIO / content.width,
        CANVAS[1] * CONTENT_RATIO / content.height,
    )
    size = (max(1, round(content.width * scale)), max(1, round(content.height * scale)))
    content = content.resize(size, Image.LANCZOS)

    canvas = Image.new("RGB", CANVAS, BG)
    canvas.paste(content, ((CANVAS[0] - size[0]) // 2, (CANVAS[1] - size[1]) // 2), mask=content)

    buffer = io.BytesIO()
    canvas.save(buffer, "JPEG", quality=88, optimize=True)
    return buffer.getvalue()


def normalized_url(source_url, component_type):
    digest = hashlib.sha1(source_url.encode()).hexdigest()[:16]
    key = f"component-image/{component_type}/{digest}.jpg"
    return put_bytes(normalize(_download(source_url)), key, "image/jpeg")
