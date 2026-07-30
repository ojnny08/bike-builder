import re
from decimal import Decimal

from .models import Frame, ShellType, SpindleInterface


def parse_tire_clearance(raw):
    nums = [int(n) for n in re.findall(r"(\d{2,3})\s*mm", raw or "")]
    if not nums:
        raise ValueError(f"no tire clearance in {raw!r}")

    return min(nums)


SHELL_ALIASES = {
    "bsa": ShellType.BSA,
    "english": ShellType.BSA,
    "iso": ShellType.BSA,
    "italian": ShellType.ITA,
    "ita": ShellType.ITA,
    "t47": ShellType.T47,
    "bb86": ShellType.PRESS_FIT_86_92,
    "bb92": ShellType.PRESS_FIT_86_92,
    "pf86": ShellType.PRESS_FIT_86_92,
    "pf92": ShellType.PRESS_FIT_86_92,
    "pf30": ShellType.PRESS_FIT_30,
    "bb30": ShellType.BB30,
}

WIDTH_RE = re.compile(r"(?<![a-z0-9])(\d{2})(?:\s*\d{2})?\s*mm")


def parse_bb_shell(raw):
    text = re.sub(r"[^a-z0-9]+", " ", (raw or "").lower())

    shell = next((SHELL_ALIASES[t] for t in text.split() if t in SHELL_ALIASES), None)
    if shell is None:
        raise ValueError(f"unknown bb shell type in {raw!r}")

    width = WIDTH_RE.search(text)
    if not width:
        raise ValueError(f"no bb width in {raw!r}")

    return shell, int(width.group(1))


def parse_fork_type(raw):
    t = (raw or "").lower()
    if "1.5" in t or "tapered" in t:
        return Frame.ForkType.TAPERED
    return Frame.ForkType.STRAIGHT


SEATPOST_SIZES = {"27.2", "30.9", "31.6"}


def parse_seatpost_size(raw):
    m = next((s for s in re.findall(r"\d{2}(?:\.\d)?", raw or "") if s in SEATPOST_SIZES), None)
    return Decimal(m) if m else None


SPINDLE_ALIASES = [
    ("octalink", SpindleInterface.OCTALINK),
    ("isis", SpindleInterface.ISIS),
    ("hollowtech", SpindleInterface.HOLLOWTECH_24),
    ("gxp", SpindleInterface.GXP),
    ("dub", SpindleInterface.DUB),
    ("386", SpindleInterface.MM_30),
    ("bb30", SpindleInterface.MM_30),
    ("30mm", SpindleInterface.MM_30),
    ("24mm", SpindleInterface.HOLLOWTECH_24),
]


def _spindle(text, default):
    t = (text or "").lower()

    if "square" in t and "taper" in t:
        if "iso" in t:
            return SpindleInterface.SQUARE_TAPER_ISO
        return SpindleInterface.SQUARE_TAPER_JIS

    return next((iface for key, iface in SPINDLE_ALIASES if key in t), default)


def parse_spindle(text):
    return _spindle(text, SpindleInterface.SQUARE_TAPER_JIS)


def parse_bb_spindle(text):
    return _spindle(text, SpindleInterface.HOLLOWTECH_24)


TAPER = {SpindleInterface.SQUARE_TAPER_ISO, SpindleInterface.SQUARE_TAPER_JIS}


def parse_spindle_length(text, interface):
    if interface not in TAPER:
        return None

    m = re.search(r"(1[0-1]\d)\s*mm", text or "")
    return int(m.group(1)) if m else None
