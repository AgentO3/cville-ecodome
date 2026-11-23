---
type: Attested Computation
title: Pilot budget total
description: Sanctioned sum of the deck's six approximate budget lines, checked against $175,000.
status: draft
tags: [ecodome, pilot, budget, computation]
runtime: python
parameters: []
executor:
  resource: /references/executors/run-python.md
  receipt: [line_items, total]
attester:
  resource: /references/attesters/pilot-budget.py
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-23T13:10:00Z" }
stale_after: "2027-02-01T00:00:00Z"
sources:
  - id: explorers-deck
    resource: /sources/ai-explorers-deck.md
    title: AI Explorers presentation
---

# Computation

```python
from decimal import Decimal

LINE_ITEMS = {
    "dome_engineering": Decimal("70000"),
    "pilot_technology": Decimal("57000"),
    "people_programs_crew": Decimal("33000"),
    "freight_build": Decimal("8000"),
    "power": Decimal("5000"),
    "insurance_permits": Decimal("2000"),
}


def allocation_total() -> dict:
    total = sum(LINE_ITEMS.values(), Decimal("0"))
    return {
        "line_items": {key: str(value) for key, value in LINE_ITEMS.items()},
        "total": str(total),
    }
```

# What this checks

The [AI Explorers deck](../sources/ai-explorers-deck.md) prints six approximate line items and a $175,000 fundraising goal. The line items use an "approximately" mark. The slide says the allocation is proposed and that final costs, scope, and category boundaries remain under review.[^explorers-deck]

This computation does not decide that the budget is approved. It checks the arithmetic the slide presents: the six lines sum to 175000. A consumer runs the fence through [the Python executor](../references/executors/run-python.md). The narrative, the access model, and the sponsor terms are on the [budget page](../pilot/budget-and-sponsorship.md). There are no parameters. A changed figure is a new revision of this concept, not an agent-supplied argument.

[^explorers-deck]: AI Explorers presentation
