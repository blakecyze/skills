---
name: flow-access
description: Perform a focused accessibility review or repair of an interface, including keyboard paths, semantics, focus, announcements, and enlarged content. Use for explicit accessibility work or a substantial access defect; routine UI refinement belongs to flow.
---

# Flow access

Trace whether users can understand and complete the task through the supported input and output paths. Infer review versus repair from the request; a review does not edit.

## Inspect the task path

Read the relevant component and shared primitives before diagnosing a missing feature. Identify the actions, state changes, and recovery route. Choose checks from actual risks, rather than requiring every assistive technology for every component.

- Follow keyboard entry, order, activation, escape, and focus return. Inspect focus visibility and any trapping or unexpected movement.
- Inspect native semantics, accessible names, labels, roles, and state exposure. Prefer correcting the native element to layering redundant ARIA over it.
- Check whether status and errors are perceivable without relying on colour, animation, or sound alone. Announcements should describe useful changes without repeating every render.
- Inspect zoom or enlarged text, narrow layouts, long content, and touch access. Hidden or clipped actions still need a usable route.
- For contrast, establish the actual rendered colours, compositing, element purpose, and applicable threshold. Use available measurement tools; do not infer compliance from a screenshot or literal colour scan.

When assessing a named accessibility standard, consult its current authoritative requirements and distinguish normative criteria from design recommendations. Do not report blanket compliance from a partial pass.

## Repair and verify

Fix the shared source when it owns the defect. Preserve product rules and destinations while restoring semantics, focus, labels, or usable presentation. Do not create a parallel custom interaction when an existing accessible primitive fits.

Re-run the failed path after the repair. Use accessibility-tree or screen-reader inspection when the finding concerns exposed meaning or announcements; source code alone does not prove the spoken result. Record untested environments as coverage gaps, not demonstrated failures.

Report actionable findings or repairs with location, evidence, impact, and verification. No fixed finding quota or extra approval round for already-authorised fixes.
