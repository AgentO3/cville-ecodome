---
type: Architecture
title: Simulator architecture
description: Proposed application layers, asset pipeline, and runtime states.
status: draft
tags: [ecodome, simulator, architecture]
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-23T13:10:00Z" }
stale_after: "2027-05-23T00:00:00Z"
sources:
  - id: ears-spec
    resource: /sources/ears-spec.md
    title: EARS requirements specification
---

# Layers

The [EARS specification](../sources/ears-spec.md) proposes five layers for the [spatial simulator](spatial-simulator.md).[^ears-spec]

The Three.js simulation core holds parameterized [dome geometry](../dome/geometry.md), interior and exterior materials, camera navigation, cutaway rendering, environment selection, and a shared scene configuration.

The asset pipeline holds canonical geometry, glTF/GLB for the browser, USDZ export and validation for iPhone AR, preset scale variants, and optimized textures. The scale presets are specified on the [AR page](augmented-reality.md).

Spatial AR adapters: iOS MVP is Apple AR Quick Look. iOS enhanced is an ARKit-powered App Clip or a validated equivalent. Android is WebXR with hit testing and anchors where supported. Android is a secondary platform in the design baseline, not a P0 requirement of its own.

The presentation layer holds responsive controls, mode and capability detection, error and recovery messages, an experience selector, and the AR launch interface.

# States

| State | Meaning |
| --- | --- |
| INITIALIZING | Loading the runtime and essential assets |
| VIEWER_READY | The interactive browser model is available |
| AR_PREPARING | Validating and preparing the AR entry route |
| AR_ACTIVE | A supported native or enhanced AR experience is active |
| AR_UNAVAILABLE | The required AR capability is unavailable |
| ERROR | A recoverable or unrecoverable application failure |

For AR Quick Look, the native viewer controls the AR session. The website must not claim access to internal tracking data the native viewer does not expose. [Performance](performance.md) targets and the [privacy](privacy-accessibility-safety.md) rules constrain how those states are allowed to behave.

[^ears-spec]: EARS requirements specification
