---
type: Experience
title: Immersive content
description: Simulator environments, the pilot deck's experiences, and the program pillars on the public site.
status: draft
tags: [ecodome, dome, content]
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-25T16:10:00Z" }
stale_after: "2027-03-01T00:00:00Z"
sources:
  - id: ears-spec
    resource: /sources/ears-spec.md
    title: EARS requirements specification
  - id: explorers-deck
    resource: /sources/ai-explorers-deck.md
    title: AI Explorers presentation
  - id: official-site
    resource: /sources/official-site.md
    title: Official site
  - id: interview
    resource: /sources/canvasrebel-interview.md
    title: CanvasRebel founder interview
  - id: alignable
    resource: /sources/alignable-listing.md
    title: Alignable listing
  - id: holiday-message
    resource: /sources/owen-holiday-message.md
    title: Holiday message, November 25
---

# Pilot experiences

The [AI Explorers deck](../sources/ai-explorers-deck.md) proposes an interior where people explore at their own pace and also create something together. One slide, "Elements, humans, and shared creation," labels water, earth, air, fire, and space. Visitors might discover Fellowship stories, paint with movement, or listen, observe, or rest. At announced times, local interactions pause for an operator-led immersive experience. The slide says the layout and technical delivery are subject to testing, and it credits creative direction to Tina.[^explorers-deck]

NEXTGEN is the deck's name for EcoDome youth experiences. A separate slide proposes a pre-festival hackathon, "a media lab for a day," for Charlottesville makers, builders, tinkerers, and explorers. That proposal is part of the [April 2027 pilot](../pilot/april-2027.md), not a committed program. The deck says five programming concepts have been submitted and does not name the five. Owen's November 25 note names Hackadome as leading into Tom Tom 2027 and does not say it is this hackathon.[^holiday-message]

The deck's readiness list and the [image-to-experience prototype](../prototypes/image-to-experience.md) are the concrete content work it shows. [Dome Tools](../tools/dome-tools.md) is a separate tool mentioned only in the community notes.

# Public site and listings

The [official site](../sources/official-site.md) names six program areas for the venue, without dates or a production schedule: immersive experiences and entertainment (performances and screenings); creative workshops in digital arts, sustainability, and design; education and youth programming; community and cultural events, including wellness, markets, and celebrations; an indoor-outdoor activation space; and a future-ready innovation hub aimed at emerging technology. The vision text adds digital literacy and sustainable living.[^official-site]

The April 2025 interview describes the interior as immersive media, concerts, storytelling, and educational programming, and says the project is meant to widen access to digital literacy tools and creative technology.[^interview]

The [Alignable listing](../sources/alignable-listing.md) is a catalog, not a calendar. Its about text names virtual reality expeditions, cosmic disco dances, and mindfulness meditation soundbaths. The 23 labels include 360 film screenings, concerts, venue rentals, interactive art, workshops, XR/AR/VR training, youth programs, and corporate sessions. The page truncates several blurbs and gives no prices.[^alignable]

NEXTGEN on the deck and "education and youth programming" on the site are related phrases from different sources. Neither source says they are the same program. The [questions page](../questions/open-questions.md) keeps that open.

# Simulator environments

The [EARS specification](../sources/ears-spec.md) requires at least four conceptual environments in the browser viewer: Aurora, Cosmos, Ocean, and AI Network. They are previews of the venue, not a claim that the pilot will use those names.[^ears-spec]

| ID | Pri | Statement | Acceptance |
| --- | --- | --- | --- |
| ECD-VIS-001 | P0 | The simulator shall provide at least four conceptual immersive environments: Aurora, Cosmos, Ocean, and AI Network. | Each environment can be selected independently and produces a visually distinguishable dome interior. |
| ECD-VIS-002 | P0 | When the user selects an immersive environment, the simulator shall display it on the interior dome surface in the Three.js viewer. | The selected content is visible from the interior view without a full-page reload. |
| ECD-VIS-003 | P1 | When a user imports a supported 360-degree equirectangular image, the simulator shall map it onto the interior using the configured projection convention. | A calibrated test image displays with the expected orientation, without incorrect mirroring or unintended seams. |
| ECD-VIS-004 | P1 | Where immersive video playback is enabled, the simulator shall support compatible HTML5 video assets as interior dome textures. | A compatible test video can play, pause, and restart without replacing the dome geometry. |
| ECD-VIS-005 | P1 | Where panel simulation is enabled, the simulator shall display a configurable LED panel grid consistent with the conceptual dome mesh. | The panel overlay remains aligned with the surface during camera movement. |
| ECD-VIS-006 | P1 | When a calibration scene is selected, the simulator shall display reference grids, angular coordinates, and orientation markers. | The markers identify zenith, horizon, and a defined forward direction. |
| ECD-VIS-007 | P2 | Where an AI experience service is connected, the simulator shall allow approved experience parameters to influence rendered content without modifying the dome's spatial anchor. | A predefined test interaction changes the visual environment while anchor transforms remain unchanged. |

How a visitor moves through these views is on the [interaction page](../simulator/interaction.md). The case for a fulldome over a flat screen is [why a dome](../evidence/why-a-dome.md).

[^explorers-deck]: AI Explorers presentation
[^ears-spec]: EARS requirements specification
[^official-site]: Official site
[^interview]: CanvasRebel founder interview
[^alignable]: Alignable listing
[^holiday-message]: Holiday message, November 25
