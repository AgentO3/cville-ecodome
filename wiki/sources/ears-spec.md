---
type: Source Summary
title: EARS requirements specification
description: Summary of the version 1.0 spatial-simulator requirements baseline.
status: draft
tags: [ecodome, source, simulator]
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-23T13:10:00Z" }
stale_after: "2027-05-23T00:00:00Z"
sources:
  - id: ears-file
    resource: ../../raw/ecodome-spatial-simulator-ears-v1.0.txt
    title: EcoDome Spatial Simulator EARS specification v1.0
    sha256: aac98425de40ad67cf96fc34aa7c3c4929641ba42e643fc522995afd0bb0d055
---

# What was filed

The raw file is the EcoDome Spatial Simulator product and software requirements specification, written in EARS (Easy Approach to Requirements Syntax). It is version 1.0, status "Proposed implementation baseline," and its stated priority is true spatially tracked AR on iPhone. The file does not name an author or a calendar date.[^ears-file]

The local copy is [ecodome-spatial-simulator-ears-v1.0.txt](../../raw/ecodome-spatial-simulator-ears-v1.0.txt).

# Scope

The specification defines a browser and mobile [spatial simulator](/simulator/spatial-simulator.md): explore a Three.js model, place a scaled dome in spatially tracked AR, and preview immersive environments. It sets the nominal [dome geometry](/dome/geometry.md), then requirements for [AR](/simulator/augmented-reality.md), [interaction](/simulator/interaction.md), [immersive content](/dome/immersive-content.md), [performance](/simulator/performance.md), and [privacy, accessibility, and safety](/simulator/privacy-accessibility-safety.md). Delivery phases, MVP exclusions, and the definition of done are on the [acceptance page](/simulator/acceptance-and-delivery.md).

It contains 40 numbered requirements: 28 at P0, 11 at P1, and 1 at P2. Each has an identifier and an acceptance check. The geometry, mounting, entrance, ribs, LED panels, and seating are explicitly not finalized. Performance numbers are proposed engineering targets.

# What this file does not contain

The specification does not mention the [April 2027 pilot](/pilot/april-2027.md), Tom Tom, IX Art Park, the published [digital twin](/prototypes/ix-art-park-twin.md), or the [simulator URL](/prototypes/ears-simulator.md). Those come from the [community notes](/sources/community-context.md) and the [AI Explorers deck](/sources/ai-explorers-deck.md).

[^ears-file]: EcoDome Spatial Simulator EARS specification v1.0
