---
type: Requirement Set
title: Performance and reliability
description: Proposed frame-rate, asset-size, quality, and device-test requirements.
status: draft
tags: [ecodome, simulator, performance]
generated: { by: cursor-cloud-agent/grok-4.7, at: "2026-11-23T13:10:00Z" }
stale_after: "2027-05-23T00:00:00Z"
sources:
  - id: ears-spec
    resource: /sources/ears-spec.md
    title: EARS requirements specification
---

# Requirements

The [EARS specification](../sources/ears-spec.md) says the thresholds in this section are proposed engineering targets, subject to validation on physical devices. They apply to the [spatial simulator](spatial-simulator.md).[^ears-spec]

| ID | Pri | Statement | Acceptance |
| --- | --- | --- | --- |
| ECD-PERF-001 | P0 | While the Three.js viewer is active on a supported reference iPhone, the simulator shall maintain a median frame rate of at least 30 frames per second over a 60-second benchmark. | Instrumented logs meet the threshold on a defined reference scene and an agreed test device. |
| ECD-PERF-002 | P0 | The simulator shall provide a tabletop AR asset no larger than 15 MB for the initial lightweight dome configuration. | The deployed USDZ file size does not exceed 15 MB. |
| ECD-PERF-003 | P0 | When sustained rendering performance stays below the configured threshold, the simulator shall reduce nonessential visual detail according to a defined quality profile. | The quality controller reduces resolution or effects without changing the model's physical dimensions. |
| ECD-PERF-004 | P1 | If the enhanced AR runtime loses spatial tracking, the simulator shall suspend interactions that depend on accurate placement until tracking recovers. | Those actions stay disabled while tracking is unavailable and resume after successful relocalization. |
| ECD-PERF-005 | P0 | The simulator shall pass the supported-mode acceptance tests on an agreed set of physical iPhone devices and iOS/Safari versions before public release. | A device-test report records the OS version, device model, AR mode, observed behavior, and pass/fail result for each test. |

The enhanced runtime in ECD-PERF-004 is the P1 mode on the [AR page](augmented-reality.md). The states those failures map onto are in the [architecture](architecture.md). The [acceptance page](acceptance-and-delivery.md) includes the device tests in the definition of done.

[^ears-spec]: EARS requirements specification
