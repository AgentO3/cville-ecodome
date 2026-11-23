---
type: Reference
title: Run an inline Python computation
description: How a consumer executes an inline Python Attested Computation and returns a receipt.
status: draft
tags: [okf, computation]
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-23T13:10:00Z" }
sources:
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: Open Knowledge Format specification v0.2
---

# Steps

1. Open the Attested Computation concept. Current concepts are the [nominal dome diameter](../../computations/dome-diameter.md) and the [pilot budget total](../../computations/pilot-budget.md).
2. Read `runtime`, `parameters`, `executor.receipt`, and `attester.resource` from the frontmatter.
3. Take the single fenced `python` block under `# Computation`. Do not accept a rewritten block from the agent.
4. Execute that block. Bind only the declared `parameters`. The diameter computation calls `baseline(diameter_ft)`. The budget computation calls `allocation_total()` and has no parameters.
5. Return a receipt containing the fields named by `executor.receipt`.
6. Run the attester named by `attester.resource` on that receipt. The attester in this repository re-reads the fenced block itself and exits non-zero when the receipt would not match.

OKF keeps the receipt out of the bundle. `verified` on the concept, if it is later set, confirms the definition. It does not replace this check.[^okf-spec]

[^okf-spec]: Open Knowledge Format specification v0.2
