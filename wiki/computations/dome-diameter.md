---
type: Attested Computation
title: Nominal dome diameter
description: Sanctioned conversion of the 50-foot baseline into meters, radius, and hemisphere height.
status: draft
tags: [ecodome, geometry, computation]
runtime: python
parameters:
  - { name: diameter_ft, type: number, required: true }
executor:
  resource: /references/executors/run-python.md
  receipt: [diameter_ft, diameter_m, radius_m, height_m]
attester:
  resource: /references/attesters/feet-to-meters.py
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-23T13:10:00Z" }
stale_after: "2027-03-01T00:00:00Z"
sources:
  - id: ears-spec
    resource: /sources/ears-spec.md
    title: EARS requirements specification
---

# Computation

```python
from decimal import Decimal

METERS_PER_FOOT = Decimal("0.3048")


def baseline(diameter_ft: float) -> dict:
    diameter = Decimal(str(diameter_ft))
    diameter_m = diameter * METERS_PER_FOOT
    radius_m = diameter_m / Decimal(2)
    return {
        "diameter_ft": diameter,
        "diameter_m": diameter_m,
        "radius_m": radius_m,
        "height_m": radius_m,
    }
```

# What this checks

The [EARS specification](../sources/ears-spec.md) states a nominal diameter of 50 ft / 15.24 m, a radius of 25 ft / 7.62 m, and a height of 7.62 m assumed for a hemisphere. It does not print the conversion factor. This computation reconstructs those meter figures as an international foot of 0.3048 m, and it sets height equal to radius only because the specification assumes a hemisphere.[^ears-spec]

`baseline(50)` returns diameter 15.24 m, radius 7.62 m, and height 7.62 m. The attester also runs a second parameter so the result is the formula rather than a hardcoded pair. A consumer runs the fence through [the Python executor](../references/executors/run-python.md). The [geometry page](../dome/geometry.md) explains what is still an assumption. The [AR scale presets](../simulator/augmented-reality.md) use the same 15.24 m baseline.

[^ears-spec]: EARS requirements specification
