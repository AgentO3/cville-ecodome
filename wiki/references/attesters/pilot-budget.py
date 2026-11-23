#!/usr/bin/env python3
"""Attest the April 2027 pilot budget sum.

Runs the fenced Python under '# Computation' in
wiki/computations/pilot-budget.md and checks that the six approximate
line items printed on the deck sum to the stated $175,000 goal.
"""

from __future__ import annotations

import re
import sys
from decimal import Decimal
from pathlib import Path

CONCEPT = Path(__file__).resolve().parents[2] / "computations" / "pilot-budget.md"
EXPECTED = {
    "dome_engineering": Decimal("70000"),
    "pilot_technology": Decimal("57000"),
    "people_programs_crew": Decimal("33000"),
    "freight_build": Decimal("8000"),
    "power": Decimal("5000"),
    "insurance_permits": Decimal("2000"),
}


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
    allocation_total = namespace.get("allocation_total")
    if not callable(allocation_total):
        raise SystemExit("computation does not define allocation_total()")

    receipt = allocation_total()
    items = {key: Decimal(value) for key, value in receipt["line_items"].items()}
    if items != EXPECTED:
        raise SystemExit(f"line items {items} do not match the deck figures {EXPECTED}")
    total = Decimal(receipt["total"])
    if total != sum(EXPECTED.values(), Decimal("0")) or total != Decimal("175000"):
        raise SystemExit(f"total {total} is not 175000")

    print("pilot-budget attestation passed ($175,000)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
