---
name: wipe
description: "Use when a UI is being iterated over several passes and each pass should be kept, compared, or shown: \"wipe as we go\", \"snapshot this version\", \"compare before and after\", \"which pass was better\", \"show me what changed in the UI\", \"make a before/after GIF or video\". Works for web pages and for native app screenshots. Not for visual regression testing, pass/fail screenshot checks, or CI gating."
argument-hint: "[snap|show|clip] [route…] [note]"
---

# Wipe

Keep every UI pass as a version, compare any two on a slider page, and render a before/after clip from the same captures.

## Controls

`[snap|show|clip] [route…] [note]`

All optional. `snap` saves the current UI as the next version with the note. `show` opens the compare page for the latest two versions. `clip` renders an MP4 and a GIF that wipe through the versions. With no verb, a run that has no versions yet gets a baseline `snap`; otherwise it is `show`. Routes such as `/pricing` name the pages to capture.

## Rules

- **Baseline first.** When the user starts iterating with Wipe, snap v0 with the note `before` before the first edit. If edits already happened with no v0, the current state is not "before". Rebuild the pre-edit code instead: `base HEAD` when the edits are uncommitted, or the commit before the work (`base main`, `base HEAD~1`) when they are committed. Run `wipe.py` from the project's own folder, never from inside the base worktree, or the capture lands in a different run. Install and start that copy on a free port, started the same way the project's server runs (dev or build) when a receipt is wanted, snap it as v0 with `--url` pointing at it, stop that server, then snap the current state as v1 with `--url` back on the project's server.
- **One version per pass.** After each pass that changes what the user sees, snap once. Write the note in the user's terms ("tightened card spacing"), never as a diff summary. Skip broken in-between states.
- **Same conditions.** The first snap of a run fixes the viewport, theme, and routes. Later snaps reuse them and the last `--url`, so repeat none of them. Keep data, sign-in state, and scroll position the same too; Wipe cannot check those. If snap prints a `warning:`, tell the user the comparison is uneven and why, then fix it, usually by snapping again with matching settings. To leave an uneven version out of a clip, pass `clip --versions`.
- **Native apps.** Take the screenshot with the platform's own tool and pass the file with `--image`: `xcrun simctl io booted screenshot <temp>/s.png` for the iOS Simulator, `adb exec-out screencap -p > <temp>/s.png` for an Android emulator, or your own simulator tool. Use the same device and orientation every pass.
- **Clean up.** Stop every server you started. Run `clean` once a `base` worktree is no longer needed. `.wipe/` is kept out of git through `.git/info/exclude`: never stage or commit it, and never edit `.gitignore` for it.

## Commands

Run `python3 <skill>/scripts/wipe.py <command>` from inside the project, with `<skill>` resolved from this file's folder. Every command except `list` takes `--run <name>`; the default run is the current branch, or `default` outside git.

| Command | Does |
|---|---|
| `snap [routes] --note "<note>" --url <base>` | Captures `<base>` plus each route as the next version (a route without a leading `/` gets one). With no routes, later snaps reuse the run's routes against `<base>`; only a run with no routes captures `<base>` as given, which suits a `file://` page |
| `snap [routes] --note "<note>" --image <png>` | Saves PNG screenshots you already took (convert others first, for example `sips -s format png in.jpg --out out.png` on macOS), one `--image` per route in order. With no route and none saved in the run, the capture is called `screen` |
| `show [A B] [--route R] [--no-open]` | Writes `.wipe/<run>/index.html` comparing A and B (default: the latest two), opens it, and prints its path. Modes: wipe, side by side, onion skin, diff |
| `clip [--versions 0,2,3] [--routes /,/pricing]` | Writes `clip.mp4` and `clip.gif` to `.wipe/<run>/` or `--out`. Also `--receipt`, `--outro "<text>"`, `--open-moving`, `--scroll`, `--no-loop`, `--ground <hex>`, `--gif-width <px>` |
| `embed A B [--route R] [--out <dir>]` | Writes a standalone before/after snippet for docs or a portfolio |
| `base <ref>` | Checks `<ref>` out in a temporary worktree and prints its path; rerunning it moves a reused worktree to the ref's current commit |
| `clean [--all]` | Removes the run's worktrees; `--all` also deletes its `.wipe/` folder |
| `list` | Shows every run, its versions and notes |

More `snap` flags: `--viewport 1280x800` (the default), `--theme light|dark|both`, `--full` and `--measure` (both need Playwright), `--production` (with `--measure`, only when the user says the URL is a production build), `--method auto|playwright|chrome`.

Exit codes: 0 done, 1 runtime error (read stderr), 2 bad command (fix it and rerun), 3 missing optional dependency. On 3, tell the user what was not made and why, pass on the install line from the error, and offer to run the install line. Never install anything globally without asking.

## Report

- After `snap`: the version label, its note, the capture method from the output, and every `warning:` in plain words.
- After `show` or `embed`: the path. If nothing opened, open it in your browser or give the path.
- After `clip`: both files with their sizes, and any `note:` about the receipt.
- Whenever something was not made, say what and why. Never claim a video, a full-page capture, or numbers that do not exist.

## Limits

- Headless Chrome, the no-install method, captures the viewport only. `--full` needs Playwright; without it Wipe captures the viewport and warns, and you say so.
- `--measure` needs Playwright and a `--url`, and measures only the first route.
- A receipt needs the clip's first and last versions both measured on the same host, any port, and the clip must show the measured route. Otherwise the clip renders without it and prints a `note:`.
- Numbers from localhost or a local file are labelled as such on the card. Never present them as production numbers; the card says `production build` only when both versions were snapped with `--production`.
- The diff view highlights changed pixels and gives no percentage, so quote none.
- Clips loop by default: they end by sweeping back to the first version, and a clip of several routes cuts back to the first route. `--no-loop` ends on the last version.
- `clip` without ffmpeg builds the compare page instead and exits 3; without Pillow it exits 3.
- Wipe keeps and shows versions. It sets no thresholds and passes or fails nothing.
