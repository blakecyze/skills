# Browser QA

Inspect the project's existing browser tests and configuration before choosing a runner. Playwright can fit repeatable journeys when available; an existing browser session can establish a live observation without adding a framework. Follow the user's chosen tools.

Confirm the target URL, build, account state, and test data. A server responding on a port does not prove it serves the intended application. Isolate mutable data across tests when concurrent runs could interfere; avoid clearing shared storage as a generic reset.

Use locators derived from the actual DOM and accessible roles, names, or established test identifiers. Wait for an observable state instead of padding with fixed sleeps. Assert a meaningful outcome beyond clicking a control. Check server-side or persisted state when a toast cannot establish the result.

Keep stubbed and integrated checks distinct. A mocked checkout can prove presentation and local handling, not a working payment integration. Controlled time, network, and fixtures help reproduce a condition, but record what was simulated.

For failures, keep the relevant trace, screenshot, console or network evidence when available. Console silence is not a success oracle. Capture before altering the failing environment.

Visual diffs need comparable viewport, fonts, data, and rendering conditions. Investigate whether a difference is a product regression or environment change before updating a baseline. Sample actual interaction for motion and focus; a screenshot cannot establish either.

Run relevant browser and viewport combinations based on supported targets and the change. Accessibility automation covers only its rules; keyboard and assistive-technology claims require the corresponding observations. Do not call a green scan a complete compliance audit.
