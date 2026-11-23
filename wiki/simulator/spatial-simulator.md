---
type: Product
title: Spatial simulator
description: Browser and iPhone product that explores, places, and previews the EcoDome.
status: draft
tags: [ecodome, simulator]
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-23T13:10:00Z" }
stale_after: "2027-05-23T00:00:00Z"
sources:
  - id: ears-spec
    resource: /sources/ears-spec.md
    title: EARS requirements specification
---

# Purpose

The [EARS specification](../sources/ears-spec.md) defines the EcoDome Spatial Simulator as an interactive digital-twin concept of the proposed venue. It is for desktop and mobile browsers, with spatially tracked augmented reality on supported devices. The stated priority of version 1.0 is true spatially tracked AR on iPhone. Status is "Proposed implementation baseline."[^ears-spec]

Three experiences:

1. Explore. Navigate and inspect the dome as an interactive Three.js model.
2. Place. Position a scaled virtual dome on a physical surface with spatially tracked AR.
3. Experience. Preview the immersive visuals and educational experiences envisioned for the physical venue.

The primary success criterion in the specification: a visitor opens the experience on an iPhone, places a correctly scaled virtual dome on a physical surface, and walks around it while it stays spatially anchored. The spec calls that the minimum acceptable definition of EcoDome WebAR, as opposed to a camera-overlay simulation.

# Design baseline

| Property | Baseline |
| --- | --- |
| Dome | [50 ft / 15.24 m hemisphere](../dome/geometry.md), height assumed |
| Audience in the model | 250 proposed, conceptual |
| Rendering | Three.js, metric, Y-up |
| Primary platform | iPhone / Safari |
| Secondary platforms | Android / Chrome, desktop browsers |
| Deployment | HTTPS |
| Primary AR deliverable | USDZ through AR Quick Look |

A public build identified as an implementation of this spec is the [EARS spatial-simulator build](../prototypes/ears-simulator.md). The spec does not name that URL. The [April 2027 pilot](../pilot/april-2027.md) is a physical showcase, not this software product.

# How requirements are written

EARS patterns used in the specification:

| Pattern | Syntax |
| --- | --- |
| Ubiquitous | The system shall [response]. |
| Event-driven | When [trigger], the system shall [response]. |
| State-driven | While [state], the system shall [response]. |
| Optional feature | Where [feature is present], the system shall [response]. |
| Unwanted behavior | If [failure], then the system shall [response]. |

Priority: P0 is mandatory before initial acceptance, P1 is the next phase, P2 is later. There are 40 requirements, 28 of them P0, 11 P1, and 1 P2. They are filed by topic:

- [Dome geometry](../dome/geometry.md) and [immersive content](../dome/immersive-content.md)
- [Spatially tracked AR](augmented-reality.md)
- [Viewer interaction](interaction.md)
- [Performance and reliability](performance.md)
- [Privacy, accessibility, and safety](privacy-accessibility-safety.md)
- [Acceptance and delivery](acceptance-and-delivery.md)

The proposed layering and state model are the [simulator architecture](architecture.md). The [project overview](../project.md) is the venue this simulator is about.

[^ears-spec]: EARS requirements specification
