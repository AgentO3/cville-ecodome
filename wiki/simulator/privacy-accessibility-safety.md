---
type: Requirement Set
title: Privacy, accessibility, and safety
description: HTTPS, camera privacy, placement safety, and accessibility requirements.
status: draft
tags: [ecodome, simulator, privacy, accessibility, safety]
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-23T13:10:00Z" }
stale_after: "2027-05-23T00:00:00Z"
sources:
  - id: ears-spec
    resource: /sources/ears-spec.md
    title: EARS requirements specification
---

# Requirements

These ECD-SEC and ECD-ACC requirements are from the [EARS specification](../sources/ears-spec.md). They apply to the [spatial simulator](spatial-simulator.md), including its [AR modes](augmented-reality.md).[^ears-spec]

| ID | Pri | Statement | Acceptance |
| --- | --- | --- | --- |
| ECD-SEC-001 | P0 | The simulator shall serve production application content and AR assets over HTTPS. | Production access succeeds over HTTPS without mixed-content errors. |
| ECD-SEC-002 | P0 | The simulator shall not upload, record, or retain camera imagery without a separate explicit user action and consent. | Network inspection during ordinary AR viewing shows no application-originated camera image or video uploads. |
| ECD-SEC-003 | P0 | When the user launches an AR mode, the simulator shall provide guidance for safe spatial placement and movement. | The user sees that guidance before attempting full-scale outdoor placement. |
| ECD-SEC-004 | P0 | When the user selects full-scale mode, the simulator shall present a notice that the virtual model does not verify physical clearance or real-world structural feasibility. | The notice is visible before the full-scale AR experience launches. |
| ECD-ACC-001 | P0 | The browser-based simulator shall expose text labels and accessible names for all primary controls. | Controls can be identified with supported screen-reader navigation in the browser. |
| ECD-ACC-002 | P1 | Where the user has enabled reduced-motion preferences, the browser viewer shall reduce nonessential animated camera transitions and environmental motion. | A reduced-motion preference test produces the documented behavior. |

The specification's definition of done includes camera privacy, HTTPS, and the full-scale safeguard. That checklist is on the [acceptance page](acceptance-and-delivery.md).

[^ears-spec]: EARS requirements specification
