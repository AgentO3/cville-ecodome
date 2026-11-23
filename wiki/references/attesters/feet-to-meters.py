#!/usr/bin/env python3
"""Attest the nominal dome-diameter computation.

Runs the fenced Python under '# Computation' in
wiki/computations/dome-diameter.md. The receipt must reproduce the
international-foot conversion for the 50-foot baseline and for a second
parameter, and it must set hemisphere height equal to radius.
"""

from __future__ import annotations

import re
import sys
from decimal import Decimal
from pathlib import Path

CONCEPT = Path(__file__).resolve().parents[2] / "computations" / "dome-diameter.md"
METERS_PER_FOOT = Decimal("0.3048")


def fenced_python(text: str) -> str:
    match = re.search(r"^# Computation\s*$", text, re.MULTILINE)
    if not match:
        raise SystemExit("no # Computation section")
    section = text[match.end() :]
    fence = re.search(r"```python\n(.*?)```", section, re.DOTALL)
    if not fence:
        raise SystemExit("no python fence under # Computation")
    return fence.group(1)


def main() -> int:
    namespace: dict = {}
    exec(compile(fenced_python(CONCEPT.read_text(encoding="utf-8")), str(CONCEPT), "exec"), namespace)
    baseline = namespace.get("baseline")
    if not callable(baseline):
        raise SystemExit("computation does not define baseline()")

    for diameter_ft, expected_m in ((Decimal("50"), Decimal("15.24")), (Decimal("10"), Decimal("3.048"))):
        receipt = baseline(diameter_ft)
        diameter_m = Decimal(receipt["diameter_m"])
        radius_m = Decimal(receipt["radius_m"])
        height_m = Decimal(receipt["height_m"])
        if diameter_m != expected_m:
            raise SystemExit(f"{diameter_ft} ft -> {diameter_m} m, expected {expected_m} m")
        if diameter_m != diameter_ft * METERS_PER_FOOT:
            raise SystemExit("diameter does not follow the international foot")
        if radius_m != diameter_m / Decimal(2) or height_m != radius_m:
            raise SystemExit("hemisphere height is not the radius")
        if Decimal(receipt["diameter_ft"]) != diameter_ft:
            raise SystemExit("receipt changed the input diameter")

    print("dome-diameter attestation passed (50 ft = 15.24 m; height = radius)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
