---
type: Requirement Set
title: Acceptance and delivery
description: MVP scenarios, delivery phases, exclusions, and the definition of done.
status: draft
tags: [ecodome, simulator, acceptance]
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-23T13:10:00Z" }
stale_after: "2027-05-23T00:00:00Z"
sources:
  - id: ears-spec
    resource: /sources/ears-spec.md
    title: EARS requirements specification
---

# MVP scenarios

The [EARS specification](/sources/ears-spec.md) gives five acceptance scenarios for the [spatial simulator](/simulator/spatial-simulator.md).[^ears-spec]

| Scenario | Given | When | Then | Pass |
| --- | --- | --- | --- | --- |
| A. iPhone tabletop | A supported iPhone and a well-lit tabletop | The visitor chooses the 1:50 model and launches View in AR | Native AR allows placement of an approximately 30.48 cm dome on the tabletop | The visitor can walk around the table and inspect the stationary, anchored dome |
| B. Translation tracking | A dome already on the tabletop | The visitor moves the iPhone laterally by one meter | The dome shows the expected positional parallax and does not translate with the phone | The experience shows positional tracking, not orientation tracking alone |
| C. Interior preview | The Three.js viewer is open | The visitor selects Cutaway and Cosmos | The interior is shown with the Cosmos environment | The scene updates without reloading |
| D. Unsupported AR | A browser without a supported spatial AR path | The visitor selects an AR feature | The simulator explains the limit and offers the 3D viewer | No non-spatial camera overlay is presented as true AR |
| E. Enhanced interactive AR | A supported enhanced ARKit runtime | The visitor places the dome and changes its immersive content | Visible content updates without changing the world-space anchor | Content changes while placement stays stable |

Scenario A uses the tabletop preset on the [AR page](/simulator/augmented-reality.md). Scenario C uses cutaway and an environment from [immersive content](/dome/immersive-content.md). The 30.48 cm figure is the specification's own wording for the 1:50 model; the preset table states 0.3048 m.

# Phases

| Phase | Deliverable | Milestone |
| --- | --- | --- |
| 1. Foundation | Responsive Three.js dome and consistent GLB/USDZ assets | Accurate scaled model |
| 2. iPhone AR MVP | True tracked placement via Quick Look | Physical-device placement tests pass |
| 3. Experience preview | Cutaway, visuals, media previews | Interactive browser demo passes |
| 4. Enhanced AR | ARKit/App Clip interactive spatial experience | Live content changes while anchored |
| 5. Digital twin | Refined geometry, seating, LED mapping | Approved venue design fidelity |

Phase 5 is the specification's name for a later software fidelity milestone. It is not the [IX Art Park digital twin](/prototypes/ix-art-park-twin.md) already published, and it is not the [April 2027 pilot](/pilot/april-2027.md).

# Explicit MVP exclusions

The first release does not require real-time AI-generated imagery inside AR Quick Look; arbitrary JavaScript inside Apple's native Quick Look viewer; persistent anchors shared across devices or sessions; architectural or structural engineering certification; exact LED manufacturing specifications; multiplayer synchronization or collaborative remote AR; or live audience tracking. The specification says those need separate requirements, validated platform capabilities, or later architectural decisions.

The community notes' idea of virtual watch parties, recorded on the [Dome Tools](/tools/dome-tools.md) page, sits outside this exclusion until someone writes a requirement for it. [Performance](/simulator/performance.md) device tests and the [privacy](/simulator/privacy-accessibility-safety.md) rules are inside the first release.

# Definition of done

The iPhone-first MVP is ready for acceptance only when:

1. The dome renders correctly in the mobile Three.js viewer.
2. The 50-foot dimensions and all prescribed scales are validated.
3. An iPhone can launch genuine spatially tracked AR.
4. A visitor can place the scaled model on a physical surface.
5. Walking around the model changes perspective without the model following the camera.
6. Unsupported devices receive an honest fallback.
7. Touch controls and basic immersive scene previews work in the browser.
8. Camera privacy, HTTPS deployment, and full-scale placement safeguards are verified.
9. The reference-device compatibility and performance tests have been completed.
10. All P0 requirements have passed their acceptance tests.

[^ears-spec]: EARS requirements specification
