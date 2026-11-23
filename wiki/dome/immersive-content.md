---
type: Experience
title: Immersive content
description: Simulator environments and the pilot deck's proposed in-dome experiences.
status: draft
tags: [ecodome, dome, content]
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-23T13:10:00Z" }
stale_after: "2027-03-01T00:00:00Z"
sources:
  - id: ears-spec
    resource: /sources/ears-spec.md
    title: EARS requirements specification
  - id: explorers-deck
    resource: /sources/ai-explorers-deck.md
    title: AI Explorers presentation
---

# Pilot experiences

The [AI Explorers deck](/sources/ai-explorers-deck.md) proposes an interior where people explore at their own pace and also create something together. One slide, "Elements, humans, and shared creation," labels water, earth, air, fire, and space. Visitors might discover Fellowship stories, paint with movement, or listen, observe, or rest. At announced times, local interactions pause for an operator-led immersive experience. The slide says the layout and technical delivery are subject to testing, and it credits creative direction to Tina.[^explorers-deck]

NEXTGEN is the deck's name for EcoDome youth experiences. A separate slide proposes a pre-festival hackathon, "a media lab for a day," for Charlottesville makers, builders, tinkerers, and explorers. That proposal is part of the [April 2027 pilot](/pilot/april-2027.md), not a committed program. The deck says five programming concepts have been submitted and does not name the five.

The deck's readiness list and the [image-to-experience prototype](/prototypes/image-to-experience.md) are the concrete content work it shows. [Dome Tools](/tools/dome-tools.md) is a separate tool mentioned only in the community notes.

# Simulator environments

The [EARS specification](/sources/ears-spec.md) requires at least four conceptual environments in the browser viewer: Aurora, Cosmos, Ocean, and AI Network. They are previews of the venue, not a claim that the pilot will use those names.[^ears-spec]

| ID | Pri | Statement | Acceptance |
| --- | --- | --- | --- |
| ECD-VIS-001 | P0 | The simulator shall provide at least four conceptual immersive environments: Aurora, Cosmos, Ocean, and AI Network. | Each environment can be selected independently and produces a visually distinguishable dome interior. |
| ECD-VIS-002 | P0 | When the user selects an immersive environment, the simulator shall display it on the interior dome surface in the Three.js viewer. | The selected content is visible from the interior view without a full-page reload. |
| ECD-VIS-003 | P1 | When a user imports a supported 360-degree equirectangular image, the simulator shall map it onto the interior using the configured projection convention. | A calibrated test image displays with the expected orientation, without incorrect mirroring or unintended seams. |
| ECD-VIS-004 | P1 | Where immersive video playback is enabled, the simulator shall support compatible HTML5 video assets as interior dome textures. | A compatible test video can play, pause, and restart without replacing the dome geometry. |
| ECD-VIS-005 | P1 | Where panel simulation is enabled, the simulator shall display a configurable LED panel grid consistent with the conceptual dome mesh. | The panel overlay remains aligned with the surface during camera movement. |
| ECD-VIS-006 | P1 | When a calibration scene is selected, the simulator shall display reference grids, angular coordinates, and orientation markers. | The markers identify zenith, horizon, and a defined forward direction. |
| ECD-VIS-007 | P2 | Where an AI experience service is connected, the simulator shall allow approved experience parameters to influence rendered content without modifying the dome's spatial anchor. | A predefined test interaction changes the visual environment while anchor transforms remain unchanged. |

How a visitor moves through these views is on the [interaction page](/simulator/interaction.md). The case for a fulldome over a flat screen is [why a dome](/evidence/why-a-dome.md).

[^explorers-deck]: AI Explorers presentation
[^ears-spec]: EARS requirements specification
