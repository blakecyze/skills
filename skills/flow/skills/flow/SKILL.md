---
name: flow
description: Refine interface layout, typography, colour, controls, copy, accessibility, and motion. Use during UI creation or when improving, polishing, or reviewing a page or component; infer relevant refinements without requiring a named domain.
---

# Flow

Make the interface clearer, coherent, and comfortable to use. Preserve its identity and useful behaviour.

## Controls

`[scope] [review|apply] [focus]`

All are optional. Infer scope from the current page, component, or UI changes. A review or explanation stays read-only; a build, fix, or refinement request authorises applying improvements within that scope. Focus such as `type`, `access`, or `motion` narrows the pass. Ask only when the target or a consequential decision cannot be inferred.

## Pass

Inspect the interface, relevant code, existing tokens, and neighbouring components. Understand the task, action hierarchy, reading order, and density; no ceremonial statement is required. During a build, use these checks as the surface takes shape.

Find the few changes with the most value: restore lost control or readability, clarify hierarchy, then improve consistency and feel. Preserve coherent choices even when another style could work. A broad pass considers relevant domains; it need not edit every domain or manufacture findings on a finished surface.

Load only guidance needed for the work:

| Focus | Reference |
|---|---|
| Layout, type, colour, surface, copy | [visual.md](references/visual.md) |
| Keyboard, semantics, states, responsive stress | [interaction.md](references/interaction.md) |
| Transitions, gestures, timing, reduced motion | [motion.md](references/motion.md) |
| Measuring contrast or discovering repeated style values | [measurement.md](references/measurement.md) |

For a dedicated animation build or accessibility investigation, `flow-motion` and `flow-access` offer focused workflows when installed. The broad pass handles routine motion and access checks itself; neither specialist is a dependency.

Apply the smallest coherent repair using existing components. Copy and accessibility repairs are in scope when they serve the requested refinement. Preserve business rules, data contracts, destinations, and established brand choices. Do not turn a polish pass into a feature rebuild. New identity or exploratory variants require that intent in the brief.

Inspect the rendered result where available, at relevant sizes and states. Exercise affected controls and interruption paths. Source inspection and scanners cannot establish the full visual or accessibility result. Repeat only when changes or unresolved issues justify it; stop when further changes are taste alone.

Report the useful changes or findings, their locations, and checks actually run. For review, prioritise evidence and the smallest repair. No fixed finding count, taxonomy quota, or approval round is needed for already-authorised work.
