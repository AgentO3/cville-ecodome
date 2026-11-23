---
type: Requirement Set
title: Spatially tracked AR
description: iPhone-first placement, scale presets, tracking, and AR fallback requirements.
status: draft
tags: [ecodome, simulator, ar]
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-23T13:10:00Z" }
stale_after: "2027-05-23T00:00:00Z"
sources:
  - id: ears-spec
    resource: /sources/ears-spec.md
    title: EARS requirements specification
---

# Requirements

These are the ECD-AR requirements from the [EARS specification](/sources/ears-spec.md). The product they belong to is the [spatial simulator](/simulator/spatial-simulator.md). The unscaled model is the [15.24 m dome](/dome/geometry.md), produced by the [diameter computation](/computations/dome-diameter.md).[^ears-spec]

| Preset | Scale | Dome diameter |
| --- | --- | --- |
| Tabletop | 1:50 | 0.3048 m |
| Presentation | 1:20 | 0.762 m |
| Full-scale | 1:1 | 15.24 m |

| ID | Pri | Statement | Acceptance |
| --- | --- | --- | --- |
| ECD-AR-001 | P0 | When a user selects View in AR on a supported iPhone, the simulator shall launch a native spatially tracked AR Quick Look experience using a USDZ of the current dome model. | The user sees the physical camera view with the virtual dome placed in the environment, rather than an ordinary browser camera overlay. |
| ECD-AR-002 | P0 | While the dome is placed in an AR session, the experience shall keep its position and orientation relative to the physical environment as the user moves. | In a well-lit, feature-rich test environment, the dome stays anchored during a two-meter walk, within the approved tracking tolerance. |
| ECD-AR-003 | P0 | When the native AR runtime finds a suitable horizontal surface, the experience shall let the user position the dome on that surface. | The dome can be placed on a tabletop or floor using the native AR placement workflow. |
| ECD-AR-004 | P0 | The simulator shall provide the tabletop, presentation, and full-scale presets above before AR launch. | The chosen USDZ matches the corresponding physical dimension within 2 percent. |
| ECD-AR-005 | P0 | While spatial tracking remains available, the experience shall keep the dome's anchored world position independent of the device's orientation. | Rotating or moving the phone changes the view without making the model follow the screen. |
| ECD-AR-006 | P0 | If a supported AR session cannot establish reliable spatial tracking, the experience shall offer recovery or repositioning and shall not present the model as successfully anchored. | A low-feature environment does not produce an unacknowledged or falsely confirmed placement. |
| ECD-AR-007 | P0 | If a device cannot launch a supported spatial AR experience, the simulator shall explain that and provide the interactive 3D viewer instead. | Unsupported devices do not show a nonfunctional AR button or silently substitute a fake AR overlay. |
| ECD-AR-008 | P0 | The AR implementation shall use a supported spatial-tracking engine with positional and rotational tracking, not accelerometer or gyroscope orientation alone. | A device translation produces the corresponding parallax and perspective change around an anchored model. |
| ECD-AR-009 | P1 | Where enhanced interactive AR is available, the simulator shall launch an ARKit-powered App Clip or an equivalent verified six-degree-of-freedom runtime. | The user can interact with live dome content while the dome remains spatially anchored. |
| ECD-AR-010 | P1 | When the user places the dome in enhanced AR mode, the simulator shall create a session-scoped spatial anchor for the dome root. | Later interactions keep that anchor until the user explicitly moves or resets the model. |

Full-scale placement has a safety notice on the [privacy and safety page](/simulator/privacy-accessibility-safety.md). A recorded outdoor placement of a full-scale model is the [outdoor demonstration](/prototypes/outdoor-placement.md); the notes do not say it was this acceptance test. The [architecture](/simulator/architecture.md) says Quick Look does not expose its tracking data to the page. Scenarios that exercise these requirements are on the [acceptance page](/simulator/acceptance-and-delivery.md).

[^ears-spec]: EARS requirements specification
