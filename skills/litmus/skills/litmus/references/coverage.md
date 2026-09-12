# Choose useful coverage

Map changed behaviour to the consequence of failure and the least expensive check that can expose it. Existing unit, integration, contract, or component tests can establish specific invariants; a real journey can establish whether the assembled path works. Neither substitutes for the other by default.

For a smoke pass, exercise the critical path with a clear final assertion. For regression, include affected consumers, shared state, and a plausible adjacent failure. For exploration, state a short question and stop when answered or when the agreed time budget ends. A named charter and a formal risk score are optional, not prerequisites.

Choose relevant states: first use, populated, pending, failure, recovery, expired session, denied permission, offline, or partial completion. Test those the feature can encounter. Confirm that retry does not duplicate a transaction and that navigation or interruption does not lose important work when those are plausible risks.

A strategy request should yield a small mapping of risk, check, environment, and remaining gap. Automate a recurring regression at the lowest layer that faithfully reproduces it. Avoid scaffolding a framework, telemetry pipeline, device matrix, or nightly schedule without a concrete need and scope.

For release readiness, use the project's acceptance criteria and required environments. Report which build was exercised, failed criteria, and untested dependencies. Existing release policy governs the decision; do not invent approval gates, waivers, or universal hardware requirements. Critical device-specific behaviour needs evidence from a representative device before claiming it verified.

Functional success and usability are separate questions. Inspect whether users can discover the next action, understand status, and recover. Report observed task friction with its context; a heuristic opinion is not a failed functional assertion or proof of accessibility compliance. Dedicated visual or accessibility work can use other available skills without making them dependencies.
