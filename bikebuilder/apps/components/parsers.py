import re

from .models import Frame, ShellType

AXLE_BY_WIDTH = {
    120: Frame.RearAxleFit.TRACK,
    130: Frame.RearAxleFit.QR_130,
    135: Frame.RearAxleFit.QR_135,
    142: Frame.RearAxleFit.THRU_142,
    148: Frame.RearAxleFit.THRU_148,
}


def parse_axle_spacing(raw):
    nums = re.findall(r"\d{3}", raw or "")
    if not nums:
        raise ValueError(f"no rear spacing in {raw!r}")

    width = int(nums[0])
    if width not in AXLE_BY_WIDTH:
        raise ValueError(f"unknown rear spacing {width} in {raw!r}")

    return AXLE_BY_WIDTH[width]


def parse_tire_clearance(raw):
    nums = [int(n) for n in re.findall(r"(\d{2,3})\s*mm", raw or "")]
    if not nums:
        raise ValueError(f"no tire clearance in {raw!r}")

    return min(nums)

SHELL_ALIASES = {
    "bsa": ShellType.THREADED_BSA,
    "english": ShellType.THREADED_BSA,
    "iso": ShellType.THREADED_BSA,
    "italian": ShellType.THREADED_ITA,
    "ita": ShellType.THREADED_ITA,
    "t47": ShellType.T47,
    "bb86": ShellType.PRESS_FIT_86_92,
    "bb92": ShellType.PRESS_FIT_86_92,
    "pf86": ShellType.PRESS_FIT_86_92,
    "pf92": ShellType.PRESS_FIT_86_92,
    "pf30": ShellType.PRESS_FIT_30,
    "bb30": ShellType.BB30,
}

WIDTH_RE = re.compile(r"(?<![a-z0-9])(\d{2,3})(?:\s*\d{2,3})?\s*mm")


def parse_bb_shell(raw):
    text = re.sub(r"[^a-z0-9]+", " ", (raw or "").lower())

    shell = next((SHELL_ALIASES[t] for t in text.split() if t in SHELL_ALIASES), None)
    if shell is None:
        raise ValueError(f"unknown bb shell type in {raw!r}")

    width = WIDTH_RE.search(text)
    if not width:
        raise ValueError(f"no bb width in {raw!r}")

    return shell, int(width.group(1))
