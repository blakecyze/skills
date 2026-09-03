---
name: flow-explain
description: "Use when the user wants to understand how an interface is built rather than change it: \"how does this component work\", \"explain this animation\", \"how did they build this effect\", \"decode this UI\". Read-only teaching pass over a component, a page, or a described effect."
argument-hint: "<component, file, or effect to explain>"
---

# flow-explain

Takes an interface apart in words. Read-only: it explains construction, it changes nothing. Approach adapted from jakub.kr/skills (explain-interface) in Flow's terms.

## The pass

1. **Identify the subject.** A file in the repo, a rendered component, or an effect the user describes. If it is external and only described, say the explanation is a reconstruction, not a reading.
2. **Structure first.** What elements exist, how they nest, which one carries each visual job. Name the load-bearing decision: the one choice the rest hangs off.
3. **Then the mechanics, by domain.** Layout (how it holds at different widths), surface (radii, depth, alignment tricks), type, colour, state handling, motion. Use Flow's vocabulary: when a technique matches a reference file's rule, cite it, so the explanation doubles as a map of the system.
4. **Then the little things.** The optical nudge, the tabular numerals, the peek that signals scroll; craft is mostly the details nobody mentions, and naming them is the point.
5. **End with the trade.** What this construction buys, what it costs, and the one thing to check before copying it into another product.

## Output

Prose with the component's actual class names, properties, and values quoted. Short. A diagram in a fenced block when nesting is the story. No findings, no tiers, no gate; this skill teaches, it does not judge. If the user asks "should we do this too", that is a design question: run the intent gate before answering.

## What this skill never does

- Edit anything, or produce a findings report (that is `flow-audit`).
- Guess a value it could read from the source; unread values are named as assumptions.
- Turn the explanation into a critique unless asked, and then by handing over to `flow-audit`.
