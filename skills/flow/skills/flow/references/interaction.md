# Interaction and stress checks

Exercise the paths affected by the refinement. Choose realistic edge cases rather than building a separate stress tool for every pass.

- **Keyboard and focus:** controls are reachable and operable, focus remains visible, dialogs handle entry and return, and decorative layers do not intercept input. Prefer native semantics and established components.
- **Meaning:** names and labels describe actions; essential status has an accessible equivalent. Announcements should convey useful changes without repeating every render.
- **States:** inspect relevant pending, success, failure, disabled, empty, and populated states. Preserve input on failure and offer the recovery the product actually supports.
- **Targets and input:** check touch and pointer use on the actual surface, including spacing around small controls. Hover cannot be the only access path to essential content.
- **Adaptivity:** try narrow and wide layouts, zoom or enlarged text, long content, and missing media where applicable. Preserve reading order and avoid hiding necessary actions to make a screenshot fit.

A missing code branch does not prove missing behaviour when a shared component owns it. Inspect that component before reporting a defect. A screenshot cannot verify keyboard operation or screen-reader output. State the coverage actually achieved.
