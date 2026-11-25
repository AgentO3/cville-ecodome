---
type: Structure
title: Dome geometry
description: Nominal 50-foot size, with the deck's projection package and the public site's LED-panel wording both on the record.
status: draft
tags: [ecodome, dome, geometry]
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-25T15:45:00Z" }
stale_after: "2027-03-01T00:00:00Z"
sources:
  - id: ears-spec
    resource: /sources/ears-spec.md
    title: EARS requirements specification
  - id: explorers-deck
    resource: /sources/ai-explorers-deck.md
    title: AI Explorers presentation
  - id: community-context
    resource: /sources/community-context.md
    title: Community context notes
  - id: official-site
    resource: /sources/official-site.md
    title: Official site
  - id: interview
    resource: /sources/canvasrebel-interview.md
    title: CanvasRebel founder interview
  - id: feasibility
    resource: /sources/feasibility-research.md
    title: Feasibility research, November 2026
  - id: pacific-brochure
    resource: /sources/pacific-domes-50ft-brochure.md
    title: Pacific Domes 50 ft brochure
---

# Nominal size

Both the [EARS specification](../sources/ears-spec.md) and the [AI Explorers deck](../sources/ai-explorers-deck.md) use a 50-foot dome. The specification states the design baseline in meters as well, and it tells the simulator to model that diameter in unscaled world coordinates.[^ears-spec][^explorers-deck]

| Property | Value | Source |
| --- | --- | --- |
| Diameter | 50 ft / 15.24 m | EARS design baseline |
| Radius | 25 ft / 7.62 m | EARS design baseline |
| Height | 7.62 m, assumed for a hemisphere | EARS design baseline |
| Coordinate system | Metric, Y-up | EARS design baseline |
| Seated capacity | 175, proposed | Pilot deck |
| Standing capacity | 250, proposed | Pilot deck |
| Audience in the simulator | Up to 250, conceptual | EARS GEO-006 |

The meter figures are reconstructed by the [nominal-diameter computation](../computations/dome-diameter.md). Height equals radius only under the hemisphere assumption. The [community notes](../sources/community-context.md) say "~250 audience capacity" and do not split seated from standing.[^community-context]

The deck says capacity depends on layout and approvals. The specification says seating arrangement is not finalized, and that a seating view must be labeled conceptual.

# Other public wordings of the same size

Later and earlier public pages use the 50-foot and 250-person figures without the deck's seated-versus-standing split, and they do not agree on the display technology.

| Wording | Where it appears |
| --- | --- |
| 50-foot LED-panel dome designed to fit 250 people | [Official site](../sources/official-site.md), read 2026-11-23[^official-site] |
| 50-foot interactive dome for gatherings of up to 250 people | Founder interview, April 10, 2025[^interview] |
| Pacific Domes 50-foot suspended projection package; 175 seated and 250 standing, both proposed | Pilot deck[^explorers-deck] |
| 50-foot hemisphere, about 250 people, hemispherical video dome | Community notes[^community-context] |
| LED panel geometry not finalized; panel grid is a simulator option | EARS specification[^ears-spec] |

A [feasibility study](../sources/feasibility-research.md) provided by the project team adds a third display wording and a wider capacity range. It describes multi-projector 360-degree projection onto a liner, not an LED panel, and it quotes other operators at about 150 to 200 seated and 260 to 300 standing. It also says the fire official sets the real load, and that a projection layout holds fewer people than a brochure. Floor area in that study is about 1,905 to 1,962 square feet, and apex height is about 25 feet, which matches the hemisphere height in feet on this page. A frame and cover are described as available to purchase, without liner or AV. None of that is a purchase or a chosen system. Hardware prices are on [dome hardware](hardware.md).[^feasibility]

No source says the Pacific Domes package has been purchased, or that an LED-panel system has been specified. [Site options](../venue/site-options.md) records the matching gap for where a structure would stand. The disagreement stays on the [questions page](../questions/open-questions.md).

# Pacific Domes brochure, retrieved 2026-11-25

The [50-foot event-dome brochure](../sources/pacific-domes-50ft-brochure.md) prints the manufacturer's own figures. It is a product sheet, not an order.[^pacific-brochure]

| Property | Brochure | Already on this page |
| --- | --- | --- |
| Diameter | 50 ft, also labeled 15 m | 50 ft / 15.24 m in the EARS baseline |
| Ceiling height | 24.5 ft, also labeled 7.5 m | 7.62 m under the hemisphere assumption; the study says about 25 ft |
| Floor area | 1,962.5 sq ft (182.3 sq m) | Study range about 1,905 to 1,962 sq ft |
| Standing | 300 | Deck 250; official site and interview 250; study quotes other operators at about 260 to 300 |
| Row seating | 200 | Deck seated proposal 175; study quotes about 150 to 200 seated |
| Buffet / round tables | 170 / 150 | Not in the earlier sources |
| Doors in the standard package | Two round hoop doors | Deck diagram: hoop exit, tunnel entrance, and hoop exit |

The study already says a projection layout holds fewer people than a brochure, and that the fire official sets the load. These seating lines are that brochure. They are not a permit load. Hardware details from the same sheet are on [dome hardware](hardware.md).

# Proposed pilot structure

The deck's structure diagram is captioned as a Pacific Domes suspended complete projection package for the 50-foot dome. The diagram labels three openings: a vertical hoop exit 48 inches from the dome at the top of the hoop, a tunnel entrance with a zipper door, and a hoop exit. The photograph on that slide is credited to Pacific Domes.[^explorers-deck]

The same deck says the technical configuration is to be confirmed. A later slide uses an existing dome photograph with simulated interior projection and says exterior visibility is still to be tested. These pictures are not an as-built EcoDome in Charlottesville.

# Simulator requirements

The specification assumes the exact geometry, mounting height, entrance, structural ribs, LED panel geometry, and seating are not final. The simulator must treat them as conceptual until approved architectural information exists.[^ears-spec]

| ID | Pri | Statement | Acceptance |
| --- | --- | --- | --- |
| ECD-GEO-001 | P0 | The simulator shall represent the nominal dome using a diameter of 15.24 meters in its unscaled world-coordinate model. | An automated geometry test reports an X/Z bounding diameter of 15.24 m, within ±0.01 m. |
| ECD-GEO-002 | P0 | The simulator shall generate a hemispherical dome mesh using configurable radial and vertical subdivisions. | The mesh forms a continuous hemispherical shell without missing faces in the reference rendering. |
| ECD-GEO-003 | P0 | The simulator shall place the dome's geometric ground origin at the center of its footprint with a vertical coordinate of zero. | Exported models rest on a detected horizontal AR plane without an unintended vertical offset. |
| ECD-GEO-004 | P0 | When a user selects Cutaway View, the simulator shall display the interior by hiding or sectioning the exterior shell. | The interior becomes visible without changing the dome's position or scale. |
| ECD-GEO-005 | P1 | Where structural visualization is enabled, the simulator shall render conceptual support ribs, LED panel boundaries, and venue fixtures. | Each architectural layer can be enabled or disabled independently. |
| ECD-GEO-006 | P1 | Where seating visualization is enabled, the simulator shall display a conceptual audience arrangement with capacity markers for up to 250 people. | The configured seating count is displayed accurately and the layout is labeled conceptual. |

The Pacific Domes openings are not yet written into those requirements. The [spatial simulator](../simulator/spatial-simulator.md) and the [open questions](../questions/open-questions.md) record that gap. Scale presets that divide this diameter are on the [AR page](../simulator/augmented-reality.md).

[^ears-spec]: EARS requirements specification
[^explorers-deck]: AI Explorers presentation
[^community-context]: Community context notes
[^official-site]: Official site
[^interview]: CanvasRebel founder interview
[^feasibility]: Feasibility research, November 2026
[^pacific-brochure]: Pacific Domes 50 ft brochure
