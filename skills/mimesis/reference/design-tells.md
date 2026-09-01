# The design tells

A catalogue of the aesthetic defaults that mark an interface as machine-built.
Distilled from research on AI design fingerprints. This is the L1 corpus for
`mimesis-design`, read on every design-audit run.

The root cause is training-data convergence, not any one model's taste. React
plus Tailwind plus shadcn/ui is a near-monoculture, so every tool that learned
design from it ships the same five patterns. You cannot prompt your way out of a
corpus. You override it with explicit tokens and an anti-pattern list, which is
what this file is.

Each tell is tagged **[grep]** if ripgrep can catch it in supplied markup or CSS,
or **[judgement]** if it needs the model to look at the rendered or described UI.
The audit runs the grep set first, then applies judgement to the rest.

## Colour

- **Purple-to-indigo gradient hero. [grep] [judgement].** The single most
  recognised tell. Violet (`#7C3AED` is v0's literal default) fading to indigo,
  often via pink or cyan, white centred text, gradient CTA. grep for
  `from-purple`, `to-indigo`, `via-pink`, `#7C3AED`, `bg-gradient-to-`,
  `conic-gradient`, `radial-gradient` on a hero.
- **Cyan-on-dark and neon glows. [grep].** The second colour tell. grep for
  `box-shadow` with a saturated colour on a dark background, `shadow-cyan`,
  `shadow-[0_0_`, `drop-shadow` glows, neon green/pink/cyan on near-black.
- **Gradient text on headings. [grep].** Decorative gradient fills on display
  text and KPI numbers. grep for `bg-clip-text`, `text-transparent`,
  `background-clip: text`.
- **Grey text on a coloured surface. [grep].** Low-contrast washed-out look.
  grep for `text-gray-*` / `text-slate-*` sitting on a non-neutral `bg-*`.
- **Pure `#000000` and `#FFFFFF` with no tint. [grep].** Untinted neutrals.
  Intentional palettes tint neutrals toward the brand hue, ideally in OKLCH.
- **Reflexive cream or beige background. [grep].** `#fafaf9` and friends used as
  the safe "tasteful off-white". Now itself a tell.
- **The Vercel monochrome reflex. [judgement].** Black as the primary accent with
  a Vercel-style mono palette, v0's default even when a brand palette was asked
  for.

## Typography

- **Inter at weight 700. [grep].** Display headings in Inter 700 with about
  `-0.02em` tracking. grep for `font-inter`, `Inter`, `font-bold` /
  `font-extrabold` on display text. The fix is weight 500 or 400 and let size do
  the work, or a real display face.
- **The overused-face rotation. [grep].** Each becomes a cliche as the corpus
  updates: Inter, then Geist, Space Grotesk, Instrument Serif, Fraunces. grep the
  font stack for these names used reflexively.
- **One font for everything. [grep] [judgement].** A single family across
  headings, body, labels and buttons. No pairing, no hierarchy of voice.
- **Flat type hierarchy. [grep].** Scale steps closer than a 1.25 ratio. grep the
  type scale tokens.
- **Crushed letter-spacing. [grep].** Tighter than about `-0.04em` on body text,
  which costs legibility. grep `tracking-tighter`, `letter-spacing: -0.0[4-9]`.
- **Oversized full-sentence hero headline. [judgement].** A whole sentence at
  display size, eating the viewport, nothing else above the fold.
- **Italic serif display hero. [judgement].** Oversized italic serif as the
  primary hero face reads as taste in isolation but has become the universal AI
  startup hero. Editorial registers may earn it; a SaaS landing page does not.
- **All-caps body text. [grep].** grep `uppercase` on paragraph-length content.

## Layout and components

- **The three-card feature row. [judgement].** Three equal cards, each an icon, a
  heading, a paragraph, a "Learn more". The easiest way to say "we have
  features", and the commonest layout tell. Replace with one primary feature plus
  two secondary, or alternating rows, or anything that is not three identical
  cards.
- **Centred everything. [judgement].** Hero, subhead, button, feature heading,
  testimonial, all dead centre top to bottom. Centre is the safe bet at every
  breakpoint. Left-align almost all body text; reserve centre for true hero
  moments.
- **The icon tile above a heading. [grep] [judgement].** A Lucide icon in a
  rounded-square container larger than the content it introduces. The universal
  feature-card shape. grep for rounded containers wrapping a single icon.
- **The side-tab accent border. [grep].** A thick coloured border on one side of
  a rounded card, fighting the corner radius. grep `border-l-4`, `border-t-4` with
  a colour on a `rounded-*` card.
- **Nested cards (cardocalypse). [judgement].** Cards inside cards inside cards,
  each with its own padding and shadow. The default grouping reflex.
- **Hero eyebrow / pill chip. [grep] [judgement].** A tiny uppercase tracked
  label, or a pill ("Introducing", "New", "Beta"), above an oversized headline.
  grep tiny `uppercase` + `tracking-wide` labels above an H1.
- **Repeated section kicker labels. [judgement].** The same tiny uppercase
  tracked label above every section heading, scaffolding made visible.
- **Numbered section markers used non-sequentially. [judgement].** `01 / 02 / 03`
  as decoration where the sections are not actually a sequence.
- **The hero metric layout. [judgement].** Big number, small label, three
  supporting stats, gradient accent. Used everywhere, trusted nowhere.
- **Sidebar left, chat centre-right. [judgement].** The default AI-tool chrome, a
  direct copy of the OpenAI UX frame.
- **Monotonous spacing. [grep] [judgement].** The same vertical padding
  everywhere, usually 64 to 96px, no rhythm. grep for one repeated spacing token.
  Real products vary it: tight within groups, generous between sections.
- **Modal abuse. [judgement].** Complex settings crammed into a modal that needs
  a scrollbar and three columns. If it needs that, it deserves a page.
- **Default 4px shadcn grid with no rhythm. [grep] [judgement].** Everything on
  multiples of 4px with no variation. Mathematically perfect, emotionally cold.

## Motion

- **Bounce and elastic easing on UI. [grep].** A dialog that springs, a card that
  overshoots. Dated. grep `ease-elastic`, `cubic-bezier` spring curves, `bounce`.
  Use `ease-out-quart` / `quint` / `expo` for interface motion; keep spring for
  genuinely physical elements.
- **Image scale or rotate on hover. [grep].** grep `hover:scale-`, `hover:rotate-`
  on imagery. Let images sit still without a reason to move.
- **Animating layout properties. [grep].** Transitions on `width`, `height`,
  `padding`, `margin` cause layout thrash. grep `transition-all`, `transition:
  width|height|padding|margin`.
- **Lazy-impact decoration. [judgement].** Gradients, sparklines and elastic
  animation deployed to signal quality rather than to communicate anything.

## Copy (overlaps the writing tells)

- **Marketing buzzwords. [grep].** streamline, empower, supercharge, world-class,
  enterprise-grade, unlock, seamless. grep them directly. These also live in
  [tells.md](tells.md); the prose linter catches the same words.
- **More than a couple of em dashes in body copy. [grep].** The written em dash is
  the exact parallel of the visual gradient pill. The prose linter catches these.
- **Aphoristic manufactured contrast. [judgement].** A section landing on a short
  rebuttal: "Not just fast. Extraordinary." The repeated pattern is the tell, the
  same antithesis reflex the writing side calls negative parallelism.
- **Redundant UX writing. [judgement].** Label, sublabel, helper text and hint all
  saying the same thing in slightly different words.

## What intentional design has instead

The distinction is not any single element. It is decisions made for
context-specific reasons. The slop test, from Dan Winer: if the first reaction is
"which AI made this", that is the failure. The aim is "how was this made".

- Asymmetry that directs attention, not randomness.
- Neutrals tinted toward the brand hue, ideally OKLCH.
- Varied spacing: tight within groups, generous between sections, 160 to 200px
  between major bands rather than a flat 64 to 96.
- A deliberate display-and-body font pairing, not a defaulted Inter.
- Motion that marks a state change or guides attention, nothing purely for
  dynamism.
- A colour budget: at most three accents, each appearing at most about three
  times on the page.

## Tool signatures

Useful when the source tool is suspected.

- **v0 (Vercel).** Monochrome, black accents, shadcn default `globals.css`.
  Reverts to black even when overridden.
- **Bolt.new.** Heavier gradients, rigid grids, emoji overuse, repetitive section
  order. Tailwind v3 default.
- **Lovable.** Generic gradient landing pages pre-2026; more configurable after
  its aesthetics update, still defaults to recognisable patterns.
- **Claude Artifacts.** Rounded corners, heavy padding, gradient text, a Material
  You lean when unconstrained.
- **ChatGPT / Canvas.** More conservative, corporate-template feel, less
  gradient-heavy.
- **Gemini.** Material 3 lean, tends to less-complete layouts.

The fonts and colours rotate as each becomes recognised. The structural causes,
training-data convergence and the shadcn monoculture, are durable. Treat those as
the real target, the specific hex codes as the symptom.
