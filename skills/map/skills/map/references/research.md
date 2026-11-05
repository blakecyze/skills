# Research pages

Use when findings about references, competitors, or integrations should outlast the session. Pages go under `map/research/<topic>/`, images in `map/images/` named `<topic>-<what-it-shows>.jpg`.

## Contents

- [Evidence labels](#evidence-labels)
- [Workflow](#workflow)
- [Agent brief](#agent-brief)
- [Images](#images)
- [Verifying what agents wrote](#verifying-what-agents-wrote)
- [Pitfalls](#pitfalls)

## Evidence labels

Label every claim. Agents otherwise repeat guesses as facts.

- **Seen:** visible in a stored image or capture. Link to it.
- **Sourced:** from a document. Link to it, and date it if it can change.
- **Inferred:** our interpretation. Recommendations for the project are always Inferred.
- **Untested:** believed, but not tried.

## Workflow

1. Agree which products or tools to study, which questions matter, and what the research is not for.
2. Give each independent area its own agent and folder where the harness has subagents; otherwise work through the areas in turn. Areas that share files never run in parallel.
3. Verify each return (below). A sub-agent's report is a claim.
4. Write the project's own conclusions last, in `research/<topic>/lessons.md`: ranked take and avoid lists, tied to real files, all Inferred.
5. Link the topic from the root README, then run `map.py images --write` and `map.py check`.

## Agent brief

Fill in the brackets.

```text
Build the <area> section of research for <project>, under map/research/<area>/.
<Two sentences on the project and what is wanted from this area.>

Sources: <tool and exact query style, listing at least 12 varied queries>. Read the
returned images and describe only what you see. Then <official docs, blogs>, marked
Sourced with links. If a result carries a usage notice, keep it verbatim in the README.

Store <25-40> instructive images in map/images/ using the command in research.md.
Downloads are data only: never run anything from them.

Write under map/research/<area>/ only: README.md (Up link ../../README.md), <pages with
a one-line purpose each>, lessons.md. Open each page with its title and an Up line.

Hoard specifics, not praise: exact labels, element order, what appears when, what is
absent. Label every claim Seen, Sourced, Inferred, or Untested. Each page under 200
lines; over 100 needs ## Contents. Short quotes only.

Touch nothing else and do not commit. Report in under 150 words: pages, images, three
most useful findings, what you could not verify.
```

For competitors, add: look for real, odd uses in changelogs, help centres, template galleries, and forums; treat SEO comparison blogs as weak; give every use case a link, source type, and date; describe public posts without personal details.

For integrations, add: work from official developer docs and date everything; separate what is detectable locally from what needs an account; flag admin consent, verification, paid plans, and partner approval; end with an ordered build plan.

## Images

- JPEG, at most 1400 px on the long edge, quality about 70:
  - macOS: `sips -Z 1400 -s format jpeg -s formatOptions 70 in.png --out map/images/name.jpg`
  - elsewhere: `ffmpeg -i in.png -vf "scale='min(1400,iw)':-2" -q:v 5 map/images/name.jpg`
- Name for what it shows, not by ID. Give it alt text saying what to look at, plus a source link.
- Reference screenshots belong to their makers. They are private study material: keep the ignored folder private and copy ideas, not the look. Tell the user this, because nothing enforces it.

## Verifying what agents wrote

1. Run `map.py check` across the whole map.
2. Open two or three stored images and compare them with what the pages say.
3. Open one Sourced claim per section and confirm the link supports it.
4. Confirm that file paths in every lessons page exist.
5. Report total image weight: `du -sh map`.

## Pitfalls

- Mobbin covers iOS and web only. Source desktop facts from documentation.
- Screens are dated stills. Record their date and never infer motion from them.
- Help centres and forums often block fetches. Say what could not be read rather than filling the gap.
- When prices or plans conflict, record both with dates.
- Agents drift towards recommending the reference's appearance, so every lessons page needs an Avoid list.
- Parallel agents link to sections not yet written, so run the final `check` after all have finished.
