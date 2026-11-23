---
type: Requirement Set
title: Viewer interaction
description: Touch navigation, view modes, and browser control requirements.
status: draft
tags: [ecodome, simulator, interaction]
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-23T13:10:00Z" }
stale_after: "2027-05-23T00:00:00Z"
sources:
  - id: ears-spec
    resource: /sources/ears-spec.md
    title: EARS requirements specification
---

# Requirements

These ECD-INT requirements are from the [EARS specification](../sources/ears-spec.md). They govern the browser viewer of the [spatial simulator](spatial-simulator.md). The environments they must not discard are the [immersive content](../dome/immersive-content.md) presets.[^ears-spec]

| ID | Pri | Statement | Acceptance |
| --- | --- | --- | --- |
| ECD-INT-001 | P0 | When a user drags one finger across the 3D viewer, the simulator shall rotate the camera around the dome's center. | Horizontal and vertical touch movement change the viewing angle without unintended browser scrolling. |
| ECD-INT-002 | P0 | When a user pinches with two fingers, the simulator shall change the camera's distance from the dome within configured limits. | Pinching changes zoom smoothly without clipping the camera through the dome shell. |
| ECD-INT-003 | P0 | When a user selects Interior, Exterior, or Cutaway, the simulator shall change to the corresponding camera and model configuration. | All three views are reachable without reloading the application. |
| ECD-INT-004 | P0 | When a user selects Reset, the simulator shall restore the default camera orientation and zoom for the active viewing mode. | Repeated resets produce the same reference view. |
| ECD-INT-005 | P0 | The simulator shall provide touch-accessible controls for view selection, environment selection, model scale, and AR launch. | Primary controls work without a mouse, keyboard, or hover. |
| ECD-INT-006 | P1 | When a user changes viewing mode, the simulator shall keep the selected immersive environment and model configuration where the destination mode supports them. | Switching between exterior and interior does not reset the selected scene. |

Cutaway rendering is also ECD-GEO-004 on the [geometry page](../dome/geometry.md). AR launch from these controls is specified on the [AR page](augmented-reality.md).

[^ears-spec]: EARS requirements specification
