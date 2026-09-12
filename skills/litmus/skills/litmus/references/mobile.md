# Mobile QA

Identify the installed app build, target device or simulator, OS, account, and initial app state. A passing build does not establish that the installed app was exercised. Verify the actual target before launching a journey.

Reuse the project's mobile runner. Maestro can serve black-box journeys; native or other existing tools may better fit synchronisation or hardware requirements. Inspect the actual hierarchy before authoring selectors. Verify installed command syntax, supported device types, and binary requirements through help or current official documentation; do not assume simulator and physical-device support are interchangeable.

Exercise relevant transitions: launch, background and return, navigation, permission denial, offline recovery, interrupted work, or an expired session. Reset only the disposable state needed for that check. Device wipes, app-data clears, and account resets can destroy useful evidence or user data; they are not generic first steps.

Prefer state assertions and condition waits over fixed sleeps. Check the intended persisted outcome where the UI alone cannot establish it. Preserve logs or recordings needed to diagnose a failure and distinguish system dialogs from app controls.

Simulators and emulators can establish many functional and layout outcomes. Sensors, device performance, accessories, notifications, and vendor-specific behaviour may need representative hardware. Verify the capability needed for the claim rather than enforcing a universal device matrix. State exactly which virtual or physical environment was used and which paths remain untested.

Do not provision paid device farms, expand a CI matrix, or upload private app binaries merely because a tool supports it. Use the environments authorised by the task and report any remaining verification gap.
