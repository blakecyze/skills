# Evidence and reporting

A useful result connects expectation, action, observation, and environment. A runner result or captured tool output can be evidence; every check does not need a screenshot, charter ID, hash manifest, or separate report file.

Use enough detail to reproduce or assess the claim:

- **Passed:** the stated assertion was executed and its expected outcome observed.
- **Failed:** an observed result contradicted the expectation; include reproducible steps and impact.
- **Blocked or inconclusive:** an unavailable environment, ambiguous expectation, or missing observation prevents a verdict.
- **Not run:** planned coverage that was not executed.

Keep these statuses per check when outcomes differ. Do not average failures into an overall pass. Record retries and the initial result; a later success does not erase an intermittent failure.

For a bug, include the build/environment, starting state, steps, expected versus actual result, and the most useful evidence location. Distinguish reproduction from a suspected cause. Severity follows user impact and reach, not a mandatory number assigned by a template.

For a repair, report the before/after evidence and regression checks. Separate unit, browser, installed-app, hardware, and production observations. A result from one environment is not evidence for another.

Keep evidence files scoped and avoid capturing unrelated personal data or credentials. Link existing artifacts rather than copying an entire trace into prose. Use structured JSON, a session sheet, or a persistent report only when a downstream consumer or the task needs it.
