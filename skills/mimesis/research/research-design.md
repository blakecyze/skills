# AI/LLM Design Fingerprints: A Practitioner's Guide to the Clichés, Causes, and Countermeasures (2026)

> **Purpose of this document:** A working reference for designers and developers who want to identify, critique, and systematically exclude the aesthetic defaults that signal "made by an AI tool." Covers the root causes, specific patterns, per-tool signatures, and what separates generic from intentional design. Prioritises practitioner sources and community critique over marketing copy.

***

## Table of Contents

1. [Why Every AI Site Looks the Same](#1-why-every-ai-site-looks-the-same)
2. [Aesthetic Clichés: The Obvious Tells](#2-aesthetic-clichés-the-obvious-tells)
3. [Layout and Component Patterns](#3-layout-and-component-patterns)
4. [Colour Defaults That Betray Generation](#4-colour-defaults-that-betray-generation)
5. [Typography and Spacing Signatures](#5-typography-and-spacing-signatures)
6. [Motion, Interaction, and UX Copy Tells](#6-motion-interaction-and-ux-copy-tells)
7. [Tool-by-Tool Signatures](#7-tool-by-tool-signatures)
8. [Distinguishing Intentional from Generated Design](#8-distinguishing-intentional-from-generated-design)
9. [Anti-Slop Reference Checklists](#9-anti-slop-reference-checklists)
10. [The Broader Problem: Homogenisation at Scale](#10-the-broader-problem-homogenisation-at-scale)
11. [Useful Tools and Resources](#11-useful-tools-and-resources)

***

## 1. Why Every AI Site Looks the Same

The root cause is not any single model's aesthetic preference — it is training data convergence. When you ask Claude, Lovable, Cursor, v0, or Bolt to build a landing page, the model draws on a corpus that is shockingly narrow: Tailwind CSS documentation examples, shadcn/ui component libraries, the top ~200 templates on Vercel, public landing pages of YC-backed startups from 2022–2024, and design systems that all reference the same canonical patterns. The output is not variety; it is the *statistical average* of those inputs.[^1]

This convergence is structurally reinforced during training. Human evaluators consistently rate "safe" outputs higher than "interesting" ones. A purple gradient hero passes review; an asymmetric layout with a single accent colour gets flagged as confusing. After thousands of feedback rounds, the model learns to optimise for safety — which is a synonym for "looks like the median landing page." The median landing page in 2024 has a purple gradient, three feature cards, Inter weight 700, and centred everything.[^1]

Switching tools does not help. Lovable, Cursor, Claude Code, v0, and Bolt all produce variations of the same five patterns because they all learned design from variations of the same training corpus. A 2026 academic paper co-published by Microsoft Research ("Interrogating Design Homogenization in Web Vibe Coding," Shin et al., March 2026) confirmed this quantitatively: cross-tool analysis of LLM-generated websites showed statistical clustering around a narrow set of Western design norms in typography, layout, and colour. The paper introduced the term **"frictionless generation"** — the design pipeline that prioritises speed and minimal user effort — as the structural cause of homogenisation.[^2][^3][^1]

***

## 2. Aesthetic Clichés: The Obvious Tells

The following patterns recur so consistently across AI-generated interfaces that they function as fingerprints. Sources: practitioner posts by Paul Bakaus (Google) and Dan Winer (January 2026), the impeccable.style slop catalogue (updated continuously), and community threads on r/UXDesign and Hacker News.[^4][^5][^6][^7][^8]

### 2.1 The Purple Gradient Hero

The single most recognisable tell. A hero section with a gradient background fading from violet (#7C3AED is the literal default in v0's design specification) to indigo, sometimes via pink or cyan. Text is centred and white. The CTA button is also gradient, often reading "Get started" or "Try it free."[^9]

**Why it happens:** Stripe popularised the conic-gradient aesthetic in 2021; Vercel's marketing pages spread it; every Tailwind template repository has at least three "gradient hero" examples. The model learned: *hero = gradient, gradient = modern*. It is no longer modern. It is 2024 Vercel-aesthetic.[^1]

### 2.2 Glassmorphism Everywhere

Blur effects, glass cards, and glow borders used as decoration rather than to solve a real layering problem. This is what impeccable.style categorises as "Lazy Cool." It appears constantly in dark-mode AI interfaces alongside neon/cyan-on-dark accents and monospace fonts deployed for "hacker vibe."[^5][^8]

### 2.3 Cardocalypse

Cards inside cards inside cards — sometimes five levels of nesting, each with its own padding and shadow. This is the LLM's default solution for almost any content-grouping problem. It produces visual noise and excessive depth.[^8]

### 2.4 The Side-Tab Accent Border

A thick coloured border on one side of a rounded card. This single pattern is described by impeccable.style as "the most recognizable tell of AI-generated UIs." The border conflicts with the rounded corners; the combination signals thoughtlessness rather than hierarchy.[^8]

### 2.5 Emoji Bullets

Emoji used as list markers or section icons — particularly the flat sidebar with emoji as navigation icons — is a widely-cited tell in community critique. It reads as substituting decoration for information architecture.[^7]

### 2.6 The Hero Eyebrow / Pill Chip

A tiny uppercase letter-spaced label sitting immediately above an oversized hero headline, or the same shape rendered as a pill chip ("✨ Introducing", "New", "Beta"). Described by impeccable.style as "the default AI SaaS hero." The fix is to drop the eyebrow, fold the kicker into the headline, or run it as a breadcrumb instead.[^8]

### 2.7 The "Most Popular" Gradient Pricing Badge

In pricing sections, the middle plan gets a small pill reading "Most popular" with a gradient background — usually purple-to-pink. Often paired with a gradient stroke on the card border. Described by rottoways.com (May 2026) as "the most visible single tell" because pricing sections are short and the badge is impossible to miss.[^1]

### 2.8 Dark Mode with Glowing Accents

Dark backgrounds with coloured `box-shadow` glows are the default "cool" look of AI-generated UIs. Neon cyan on dark is the second-most recognisable colour tell after purple gradients.[^6][^8]

### 2.9 Gradient Text on Headings

Gradient fills applied to display headline text — especially on metrics and KPI numbers. A common AI tell that impeccable.style flags as purely decorative and meaningless.[^8]

### 2.10 Massive Rounded Lucide Icons

An icon tile stacked above a heading, with the icon in a rounded-square container larger than the content it introduces. This is, in impeccable.style's words, "the universal AI feature-card template — every generator outputs this exact shape." The fix is to try a side-by-side icon and heading, or let the icon sit in flow without its own container.[^8]

***

## 3. Layout and Component Patterns

### 3.1 The Three-Card Feature Row

Three cards, equal width, each containing an icon, a heading, a paragraph, and sometimes a "Learn more" link. They align in a row that breaks to a single column on mobile. The training data has this shape thousands of times; it is the easiest way to express "we have features."[^1]

**What to do instead:** Replace with a primary feature taking 60% of the width and two secondary features sharing the remaining 40%. Or stack features vertically with alternating image alignment. Or use a single hero feature with a tabbed interface. Anything except three identical cards.[^1]

### 3.2 Centred Everything

Centred hero text, centred subhead, centred button, centred feature heading, centred testimonial — the entire page reads top to bottom, dead centre, no asymmetry anywhere. Centre alignment is the LLM's safest bet: it works at every screen size and requires no thinking about visual hierarchy.[^1]

**What to do instead:** Left-align almost all body text. Reserve centre alignment for true hero moments — and even then consider a left-aligned hero with a generous right margin.[^1]

### 3.3 The Hero Metric Layout

Big number, small label, three supporting stats, gradient accent. Used everywhere, trusted nowhere. Impeccable.style classifies this as a named template pattern: "big number, small label, three supporting stats, gradient accent."[^8]

### 3.4 Sidebar Left, Chat Centre-Right

The dominant AI-tool chrome: a sidebar on the left and a chat panel in the centre-right — a direct copy of the OpenAI UX framework, noted by a UX Collective writer in March 2025: "Each time I see AI tools I often see a copy of OpenAI's UX framework — sidebar on the left and chat in the center right."[^10]

### 3.5 Numbered Section Markers (01 / 02 / 03)

Numbered display markers as section labels appear throughout AI-generated editorial content. Impeccable.style notes: "Numbers earn their place only when the section actually is a sequence."[^8]

### 3.6 Repeated Section Kicker Labels

Tiny uppercase tracked labels above *every* section heading — like structural scaffolding made visible. Impeccable.style: "Repeating tiny uppercase tracked labels above section headings turns a brand page into AI editorial scaffolding."[^8]

### 3.7 Monotonous Spacing

The same spacing value used everywhere — no rhythm, no variation. Most AI-generated sites use 64–96px of vertical padding between sections. Practitioners recommend 160–200px, arguing that "the whitespace is what makes the page feel like a real product instead of a template."[^1]

### 3.8 Modal Abuse

Complex settings crammed into a modal — if it needs a scroll bar and three columns, it deserves its own page. Paul Bakaus (January 2026) called this out as a "junior designer rush job" pattern.[^5][^8]

***

## 4. Colour Defaults That Betray Generation

### 4.1 The AI Colour Palette

Purple/violet gradients and cyan-on-dark are the two most recognisable tells of AI-generated UIs, catalogued explicitly by impeccable.style. A LinkedIn post by Jessica Misener (November 2025) made the comparison explicit: "If GPT writing has the em dash, vibe-coded HTML has this gradient purple and those coloured border boxes."[^11][^8]

The AI default palette, as summarised by practitioners:[^6][^7][^5]
- Purple (#7C3AED) to indigo/blue gradient as primary accent[^9]
- Cyan-on-dark for "tech" or "hacker" aesthetics
- Neon glows: green, pink, or cyan on very dark backgrounds
- Cream/beige as the "tasteful off-white" background (now itself a tell)[^8]

### 4.2 Gray Text on Coloured Backgrounds

Muted gray body text sitting on a coloured surface creates low contrast and a washed-out look. The correct approach is using a darker shade of the background colour or white/near-white for contrast.[^5][^8]

### 4.3 Pure Black and White Without Tinting

Using absolute `#000000` and `#FFFFFF` without tinting toward any brand hue. Practitioner guidance (impeccable.style, paddo.dev) recommends tinting neutrals toward the brand hue using OKLCH colour space for perceptually uniform, distinctive palettes.[^12][^6]

### 4.4 The Vercel-Inspired Black Accent

v0 specifically inherits Vercel's native aesthetic: frequent use of black as the primary accent and monochrome palette conforming to Vercel's own brand style. Users in the Vercel community forum (May 2025) reported that even when they specified custom colour palettes, v0 would revert to black accents and Vercel-inspired styling on subsequent interactions.[^13][^14]

***

## 5. Typography and Spacing Signatures

### 5.1 Inter at Weight 700

Display headlines on AI-built sites are almost always **Inter, weight 700, with negative letter-spacing around -0.02em**. Inter became the default because it is free, on Google Fonts, ships with shadcn/ui, and appears in the canonical Vercel and Linear marketing pages that the training data scraped. Weight 700 is the default for display text in those examples, so the model learned: *headline = Inter 700*.[^1]

The fix: use Inter at weight 500 (or even 400) for display headlines and let size do the work; or replace Inter entirely with a serif like Fraunces or a geometric sans like Geist. The visual difference between weight 500 and weight 700 at large sizes is described as "the difference between 'considered' and 'trying'."[^1]

**The emerging rotation of overused faces** (as of 2026): Inter → Geist (itself now overused) → Space Grotesk → Instrument Serif → Fraunces. Each becomes a new cliché as the corpus updates. Impeccable.style: "Each new wave of AI-generated UIs converges on the same handful of faces."[^8]

### 5.2 Single Font for Everything

Only one font family across the entire page: headings, body, labels, buttons. No typographic hierarchy, no personality. Intentional design typically pairs a distinctive display font with a refined body font.[^8]

### 5.3 Flat Type Hierarchy

Font sizes too close together — no clear visual hierarchy. Impeccable.style recommends aiming for at least a 1.25 ratio between type scale steps.[^8]

### 5.4 Crushed Letter Spacing

Letter spacing pulled tighter than the point where characters keep their own shapes — a common AI "design signifier" on display text that costs legibility at body sizes.[^8]

### 5.5 Oversized Hero Headline

A full sentence set at display size, dominating the viewport and leaving no room for anything else above the fold. The model blows up the headline because size is its signal for importance; intentional design uses size sparingly.[^8]

### 5.6 Italic Serif Display Headline

Oversized italic serif as the primary hero headline "reads as taste in isolation but has become the universal AI-startup landing page hero." Context-dependent: editorial registers may legitimately use this; SaaS landing pages using it are signalling generic taste.[^8]

### 5.7 Default shadcn/Tailwind Spacing Grid

The shadcn/ui default `globals.css` uses a base scale of `0.25rem` (4px), with everything in multiples of 4px. AI tools that default to this grid produce "mathematically perfect but emotionally cold" spacing — the same increments used everywhere with no rhythm.[^15][^16]

***

## 6. Motion, Interaction, and UX Copy Tells

### 6.1 Bounce and Elastic Easing

Bounce and elastic easing on interface elements (a dialog that springs in, a card that overshoots) is described by impeccable.style as "dated and tacky." It is the AI's default way to signal "dynamic." The fix: use `ease-out-quart`, `ease-out-quint`, or `ease-out-expo` for interface motion; reserve spring physics for genuinely physical elements.[^6][^8]

### 6.2 Image Hover Transform (Scale/Rotate)

Scaling or rotating an image on hover is a recurring generated-UI signature. Let imagery sit still unless there is a purposeful, contextual reason for the motion.[^8]

### 6.3 "Lazy Impact" Animations

Gradients, sparklines, elastic animations deployed as signals of quality rather than to communicate anything. Paul Bakaus's January 2026 LinkedIn post categorised this as "lazy impact" — the AI's substitute for genuine visual interest.[^5]

### 6.4 Redundant UX Writing

Label, sublabel, helper text, and hint text all saying the same thing in slightly different words. Bakaus (January 2026) called this "Japanese-style UX writing (extreme redundancy)" — a side-effect of the AI optimising for completeness over clarity.[^5][^8]

### 6.5 Marketing Buzzwords

"Streamline," "empower," "supercharge," "world-class," "enterprise-grade" — generic SaaS phrases that appear in AI-generated copy because they are the most common words adjacent to "benefits" in the training data. Impeccable.style classifies these as explicit AI tells in the copy layer.[^8]

### 6.6 Aphoristic-Cadence Copy

Sections landing on a short manufactured-contrast aphorism or rebuttal: "Not just fast. Extraordinary." The repeated pattern is the tell, not the individual instance.[^8]

### 6.7 Em-Dash Overuse

More than a couple of em-dashes in body copy is catalogued as an AI cadence tell. The parallel to text generation is exact: the visual em-dash of AI design is the gradient pill; the written em-dash is the em-dash.[^8]

***

## 7. Tool-by-Tool Signatures

Different platforms have distinct default aesthetics, rooted in their tech stack choices and training/fine-tuning. The following analysis synthesises community reports, forum posts, and practitioner comparisons.

| Tool | Default Stack | Primary Aesthetic Signature | Specific Tells |
|---|---|---|---|
| **v0 (Vercel)** | React + shadcn/ui + Tailwind | Vercel-brand monochrome; black accents, white backgrounds, muted grays | Forces black accent even when overridden[^13][^14]; shadcn default `globals.css` is "responsible for its standard aesthetic"[^17]; purple (#7C3AED) as the named primary in design specs[^9] |
| **Bolt.new** | React/Next.js + Tailwind (v3 + shadcn) | Faster/more "vibrant" than v0; defaults to Tailwind v3 without custom shadcn overrides | Tailwind pre-installed in every project; no global style settings persist across sessions[^18][^19]; "heavy gradients, rigid cookie-cutter grids, overuse of emojis, same repetitive section order" per Bolt's own retrospective (January 2026)[^20] |
| **Lovable** | React + Tailwind (agent mode) | Similar to v0/Bolt base; introduced "aesthetics update" May 2026 to add typography/layout/colour preferences | Pre-update: generic gradient landing pages; Post-May 2026 update: more configurable, but still defaults to recognisable patterns unless overridden[^21][^22]; Agent Mode (default since July 2025) can lock in homogenised patterns across whole projects[^22] |
| **Claude Artifacts** | HTML/React (no fixed framework) | Clean whitespace, soft grays, rounded elements; tendency toward Material Design 3 / "anthropomorphic" style | Overtly rounded corners, excessive padding, gradient text on headings[^4]; without instructions, defaults to "lame attempt at Material You"[^4]; Claude Code (no Artifacts) closer to shadcn aesthetic when using React |
| **ChatGPT / Canvas** | HTML or React | "Structured, uncluttered, enterprise-friendly"[^23]; more conservative than Claude or Lovable | Efficiency-focused, closer to corporate template than SaaS landing page; less gradient-heavy than competitors in LLM showdowns[^23][^24] |
| **Gemini / Google tools** | Variable | Tends to produce less-complete designs; Material You influence | Identified as finishing last in direct comparisons for UI completeness[^25]; Material 3 aesthetic when given latitude[^4] |
| **Figma Make** | Figma components | Polished within Figma conventions | Inherits whatever Figma community kit was scraped; produces high-fidelity but template-matching outputs |
| **Cursor / Claude Code** | Project-determined | Inherits the model's defaults unless constrained by system prompts or skills | Quality highly dependent on whether the developer has loaded anti-slop skill files[^26][^12]; without constraints, converges to the same Inter/purple/card defaults as other tools |

### The Shared Technical Root

All React-based tools converge on the same aesthetic because they share the same dependency tree: **React + Tailwind CSS + shadcn/ui**. The shadcn/ui default `globals.css` uses Inter as the base font and a purple (`oklch(0.205 0 0)` on dark, violet-family on light) as the primary colour. V0 explicitly documents that "the shadcn/ui kit comes with a default one [globals.css] and v0 falls back to that (which is responsible for its standard aesthetic)." Every tool built on this stack produces the same output unless `globals.css` is explicitly overridden with brand-specific tokens.[^17][^27][^15]

***

## 8. Distinguishing Intentional from Generated Design

The core distinction between intentional and AI-generated design is not any single visual element — it is the presence or absence of *decisions made for context-specific reasons*. Dan Winer (LinkedIn, January 2026): "A distinctive interface should make someone ask, 'How was this made?' not 'Which AI made this?'"[^6]

### 8.1 Intentionality Markers

Intentional design exhibits:

- **Asymmetry with a reason**: Breaking the grid is not random — it directs attention or creates tension that resolves visually. AI output uses grids because they are always "safe"; intentional design uses asymmetry because the content calls for it.[^6]
- **Tinted neutrals**: Backgrounds and foregrounds are tinted toward the brand hue rather than using pure black/white or absolute gray.[^12][^6]
- **Visual rhythm through varied spacing**: Sections are not all padded identically; groupings of related items are tight, separations between sections are generous.[^8]
- **Typographic personality**: Display and body fonts are paired deliberately — not defaulted to Inter. The font choice reinforces the brand's voice.
- **Motion that earns its place**: Micro-interactions mark state changes or guide attention; there is no animation purely for dynamism.[^28][^8]
- **A specific colour budget**: Practitioners recommend maximum three accent colours, appearing at most three times each on the page.[^1]

### 8.2 AI Default Markers

AI-generated output exhibits:

- **"Aggressively mediocre" design**: Not broken, but indistinguishable — the visual equivalent of stock photography. Technically competent, instantly forgettable.[^1]
- **Template applications**: The layout is not composed for the content; the content is poured into a template the model recognised as "landing page."
- **Mathematically perfect, emotionally cold spacing**: Everything on a 4px or 8px grid with no variation in rhythm — the same mechanical spacing values reused everywhere.[^16][^15]
- **Context-free decisions**: Rounded corners, gradients, and cards are applied regardless of whether the product warrants them.
- **No "designer's hand"**: The 2026 design counter-movement explicitly valorises visible craft — "hand-drawn cursive," "janky VFX," "asymmetric type" — as signals that a person made aesthetic judgements.[^29]

### 8.3 The "AI Slop Test"

Dan Winer's formulation (LinkedIn, January 2026): "If someone immediately thinks 'AI made this,' it's a problem." The test is whether a viewer's first reaction is attribution to a tool rather than curiosity about a product.[^6]

Fuselab Creative's analysis (2026) adds a practitioner framing: "The tools are good at consistency. They are not good at distinctiveness. That boundary is where the designer's judgment still determines whether the product looks like itself or like everything else."[^30]

***

## 9. Anti-Slop Reference Checklists

These are synthesised from community anti-slop tools — primarily impeccable.style (Paul Bakaus, continuously updated) and the Claude Code frontend-design skill by Anthropic (widely referenced in practitioner discussions).[^26][^31][^8]

### ❌ CLI-Detectable Violations

The following are mechanically detectable in code (via `npx impeccable detect`):[^8]

**Colour**
- `bg-gradient-to-r from-purple-500 to-purple-600` or equivalent[^32]
- `box-shadow` glow on dark backgrounds[^8]
- Gray text on coloured backgrounds (`text-gray-*` on any non-gray `bg-*`)[^8]
- Gradient text on headings (`background-clip: text`)[^8]
- Cream/beige background (#fafaf9 or equivalent) used reflexively[^8]

**Typography**
- Font family: Inter, Roboto, Arial, system fonts as the *only* typeface[^4][^32]
- Overused faces: Geist, Space Grotesk, Instrument Serif used reflexively[^8]
- Single font family for everything — no pairing[^8]
- Flat type hierarchy (< 1.25× ratio between scale steps)[^8]
- Crushed letter spacing (< -0.04em on body text)[^8]
- Oversized full-sentence hero headline[^8]
- All-caps body text[^8]
- Repeated section kicker labels above every H2[^8]
- Hero eyebrow / pill chip above headline[^8]
- Italic serif as primary hero display face[^8]

**Layout / Components**
- Three identical feature cards in a row[^1][^8]
- Icon tile (rounded-square container) stacked above heading[^8]
- Side-tab accent border on rounded card[^8]
- Numbered section markers (01 / 02 / 03) used non-sequentially[^8]
- Nested cards (cards inside cards)[^8]
- Monotonous spacing (same padding/margin value used everywhere)[^8]

**Motion**
- Bounce or elastic easing on interface elements[^8]
- Image scale/rotate on hover[^8]
- Animation of `width`, `height`, `padding`, or `margin` (causes layout thrash)[^8]

**Copy**
- Marketing buzzwords: streamline, empower, supercharge, world-class, enterprise-grade[^8]
- More than two em-dashes in body copy[^8]
- Aphoristic manufactured-contrast endings to sections[^8]

### ❌ LLM-Review Violations (not mechanically detectable)

- Glassmorphism used as decoration rather than for a layering reason[^8]
- Extreme border-radius on cards (24px+ on small cards)[^8]
- Hero metric layout (big number, three supporting stats, gradient accent)[^8]
- Identical card grids across multiple sections[^8]
- Redundant UX writing (label + sublabel + helper text all saying the same thing)[^8]
- Modal used for content that warrants a separate page[^8]

***

## 10. The Broader Problem: Homogenisation at Scale

The individual aesthetic complaints above connect to a documented systemic risk. The Shin et al. paper (March 2026, Microsoft Research / University of Washington) identified a feedback loop: AI tools trained on a narrow Western corpus reproduce those patterns; as vibe-coded sites flood the web, future training data contains even fewer non-standard aesthetics; models then become further homogenised — a process the paper calls "model collapse" at the design layer.[^3][^2]

Survey data from the paper confirmed that professional designers independently observed the same homogeneity observed in automated analysis. The paper's proposed mitigation is "productive friction" — deliberate interactional interventions that break the pattern of reflexive acceptance of AI defaults.[^33][^3]

This manifests at three scales:

1. **Individual creator**: Being forced to articulate cultural context, motifs, or style references before generation begins — instead of typing "landing page" and accepting the output.[^33][^2]
2. **Organisation**: Requiring AI tools to ingest existing brand tokens and design systems before generating anything, and flagging divergences from the established system.[^2]
3. **Ecosystem**: Encoding provenance metadata into generated designs so that future crawlers can prioritise diverse aesthetics in training data.[^2]

The countermeasure community has coalesced around a practical alternative: **operating at the design-system level rather than the prompt level**. The argument (rottoways.com, May 2026; impeccable.style): you cannot fix AI design clichés by rewording prompts, because the clichés are baked into the model's training corpus. You must give the model a different corpus — explicit design tokens, anti-pattern lists, and cultural references that override its defaults.[^1][^8]

***

## 11. Useful Tools and Resources

### Detection and Anti-Slop Enforcement

| Tool | What it does | Source |
|---|---|---|
| **impeccable.style** (`npx impeccable detect`) | CLI + browser extension; deterministic detection of 30+ AI slop patterns; LLM-review commands (`/critique`, `/audit`, `/polish`) | Paul Bakaus (Google), continuously updated[^8][^31] |
| **shadcn-ui-design-validator** (Claude Skills marketplace) | Automatically validates `.tsx` components for generic patterns (Inter fonts, purple gradients, minimal animations); triggers on every component creation | Jan 2026[^32] |
| **skills-slides** (dev.to, March 2026) | Token-based design system for Claude Code that prevents AI-generic slide design; includes anti-slop checklist | nghiahsgs, dev.to[^34] |

### Anti-Pattern System Prompts

The Hacker News community compiled a widely-cited snippet (January 2026) that has been reproduced in dozens of skill files:[^4]

```
NEVER use generic AI-generated aesthetics like overused font families
(Inter, Roboto, Arial, system fonts), clichéd color schemes
(particularly purple gradients on white backgrounds), predictable
layouts and component patterns, and cookie-cutter design that lacks
context-specific character.

Interpret creatively and make unexpected choices that feel genuinely
designed for the context. No design should be the same. Vary between
light and dark themes, different fonts, different aesthetics. NEVER
converge on common choices (Space Grotesk, for example) across
generations.
```

### Design References and Vocabulary Tools

- **impeccable.style** — vocabulary layer for design concepts (OKLCH colour, vertical rhythm, fluid type scale) that developers can pass to AI tools[^12]
- **Anthropic's frontend-design skill** — official Claude Code skill for frontend design; widely referenced as a baseline (277k installs as of March 2026)[^12]
- **rams.ai** — design reference system[^6]
- **TweakCN** (tweakcn.com) — visual tool to customise shadcn/ui colour variables before they become the basis for v0 output[^17]
- **ReactBits / 21st.dev** — curated interactive component libraries as alternatives to default shadcn components[^20]

### Key Practitioner Sources (Chronological)

- UX Collective, "Thinking past the cliché of LLMs AI design patterns" — March 2025[^10]
- Paul Bakaus (Google), "AI slop design tells (design anti-patterns)" — LinkedIn, January 2026[^5]
- Dan Winer, "The AI Slop Test" — LinkedIn, January 2026[^6]
- Hacker News, "Why does LLM-generated websites feel so 'LLM-generated'?" — January 2026[^4]
- rottoways.com, "Why your AI-generated website looks like every other AI-generated website" — May 2026[^1]
- Shin et al. (Microsoft Research / UW), "Interrogating Design Homogenization in Web Vibe Coding" — arXiv, March 2026[^3]
- Bolt.new official blog, "How to create stunning websites in 2026 (without looking like AI)" — January 2026[^20]
- r/UXDesign, "What are the top AI slop design patterns?" — March 2026[^7]
- impeccable.style/slop — continuously updated slop catalogue[^8]

***

*Document compiled June 2026. Patterns evolve rapidly; the specific font and colour tells rotate as each becomes recognisable and practitioners develop countermeasures. The structural causes — training data convergence, frictionless generation, and the shadcn/Tailwind monoculture — are more durable and should be treated as the root issues.*

---

## References

1. [Why your AI generated website looks like every other AI ...](https://rottoways.com/blog/ai-generated-website-looks-generic) - AI generated websites all look the same because every AI was trained on the same Tailwind defaults, ...

2. [[Literature Review] Interrogating Design Homogenization in Web ...](https://www.themoonlight.io/en/review/interrogating-design-homogenization-in-web-vibe-coding) - The paper "Interrogating Design Homogenization in Web Vibe Coding" investigates the risk of design h...

3. [Interrogating Design Homogenization in Web Vibe Coding - Microsoft](https://www.microsoft.com/en-us/research/publication/interrogating-design-homogenization-in-web-vibe-coding/) - Generative AI is known for its tendency to homogenize, often reproducing dominant style conventions ...

4. [Why does LLM generated websites feel so "LLM ... - Hacker News](https://news.ycombinator.com/item?id=46475531)

5. [AI slop design tells (design anti-patterns): The obvious ones:](https://www.linkedin.com/posts/paulbakaus_ai-slop-design-tells-design-anti-patterns-activity-7416272383017164800-10DR) - AI slop design tells (design anti-patterns): The obvious ones: - purple gradients / everything - ove...

6. [The AI Slop Test: If someone immediately thinks "AI made ... - LinkedIn](https://www.linkedin.com/posts/danwiner_the-ai-slop-test-if-someone-immediately-activity-7416821636450127872-NQhr) - A distinctive interface should make someone ask, "How was this made?" not "Which AI made this?" Here...

7. [What are the top AI slop design patterns? : r/UXDesign - Reddit](https://www.reddit.com/r/UXDesign/comments/1s1guo5/what_are_the_top_ai_slop_design_patterns/) - Purple accent color. Glows and gradients everywhere. Bad glassmorphism effects. Some combo of Space ...

8. [Slop - Impeccable](https://impeccable.style/slop) - Purple/violet gradients and cyan-on-dark are the most recognizable tells of AI-generated UIs. Choose...

9. [Design specification – v0 by Vercel](https://v0.dev/chat/design-specification-k5K15EAvkpw) - build this page: with this specs Color Palette: - Primary: Purple (`#7C3AED`) - Used for interactive...

10. [Thinking past the cliche of LLM's AI design patterns - UX Collective](https://uxdesign.cc/thinking-past-the-cliche-of-llms-ai-design-patterns-c9b849fce9e8) - I understand the need to use patterns and normalize design, and I don't know if anyone in 2025 will ...

11. [Why do LLMs favor certain design styles for websites?](https://www.linkedin.com/posts/jessicamisener_why-does-every-vibe-coded-website-have-that-activity-7397289064476893184-yA4L) - Why does every vibe-coded website have "that" look? We talk a lot about the writing styles that Chat...

12. [Impeccable: The Design Vocabulary AI Was Missing](https://paddo.dev/blog/impeccable-design-vocabulary/) - You can't ask for “tinted neutrals” or “vertical rhythm” or “fluid type scale with optical sizing” i...

13. [Persistent Styling Bias in v0 Towards Vercel Design Aesthetic](https://community.vercel.com/t/persistent-styling-bias-in-v0-towards-vercel-design-aesthetic/11125.md)

14. [Persistent Styling Bias in v0 Towards Vercel Design Aesthetic - Help](https://community.vercel.com/t/persistent-styling-bias-in-v0-towards-vercel-design-aesthetic/11125) - Hi Vercel-Team, I want to raise an issue I’ve consistently encountered while working with v0 (paid-v...

15. [Design Guidelines for shadcn/ui with Tailwind v4 - ctxs.ai](https://ctxs.ai/weekly/shadcn-ui-tailwind-v4-7z8p3v) - Explore design principles and implementation guidelines for shadcn/ui using Tailwind v4, ensuring co...

16. [How to Break the AI-Generated UI Curse: Your Guide to Authentic ...](https://dev.to/a_shokn/how-to-break-the-ai-generated-ui-curse-your-guide-to-authentic-professional-design-2en) - Transform your generic AI outputs into stunning, human-centered interfaces that users actually...

17. [Theming in v0 - Discussions - Vercel Community](https://community.vercel.com/t/theming-in-v0/17000) - As v0 uses shadcn/ui for its components, almost all of its styling can be controlled via a single gl...

18. [Setting global system prompt on bolt doesn't work !!!](https://www.reddit.com/r/boltnewbuilders/comments/1lfztda/setting_global_system_prompt_on_bolt_doesnt_work/) - Setting global system prompt on bolt doesn't work !!!

19. [Integrate Tailwind CSS with Bolt.new | Step-by-Step Guide | RapidDev](https://rapidevelopers.com/bolt-ai-integrations/tailwind) - Tailwind CSS is pre-installed and pre-configured in every Bolt.new project — you do not need to inst...

20. [How to create stunning websites in 2026 (without looking ...](https://bolt.new/blog/2026-create-stunning-websites-bolt) - Learn how to build a website that stands out (and doesn't scream 'AI-generated') in this guide to sc...

21. [Introducing the Lovable aesthetics update, a new level of design in ...](https://www.linkedin.com/posts/lovable-dev_introducing-the-lovable-aesthetics-update-activity-7459640329667895296-P-U7) - Introducing the Lovable aesthetics update, a new level of design in vibe coding. Ask for typography,...

22. [Lovable for Designers: The Complete Guide to Building Apps with AI ...](https://muz.li/blog/lovable-for-designers-the-complete-guide-to-building-apps-with-ai-2026/) - Since July 2025, Lovable runs in Agent Mode by default. This is not just a chatbot that writes code....

23. [Claude vs OpenAI vs Gemini on UI Generation using Lovable.dev](https://medium.com/devskills-weekly/i-tried-the-same-prompt-on-lovable-app-with-claude-openai-and-gemini-heres-what-i-learned-8d7debc56f6f) - What It Revealed About Their Design Cognition

24. [I asked Gemini, Claude, and ChatGPT to create a website, and there was one obvious winner](https://vocal.media/education/i-asked-gemini-claude-and-chat-gpt-to-create-a-website-and-there-was-one-obvious-winner) - Testing the "vibe-coding" prowess of today’s top LLMs to see which one truly masters the art of func...

25. [I asked Claude, Gemini, and ChatGPT to design a website... - daily.dev](https://app.daily.dev/posts/i-asked-claude-gemini-and-chatgpt-to-design-a-website-wireframe-and-only-one-looked-like-it-came--tp96wk3o4) - A zero-shot comparison of Claude Sonnet 4.6, ChatGPT, and Gemini 3.1 Pro on a sports betting website...

26. [Georgi K.'s Post - LinkedIn](https://www.linkedin.com/posts/geknz_if-you-use-claude-code-for-frontend-here-activity-7450880214513012736-f9f8) - If you use Claude Code for frontend, here are 9 tools worth keeping close: 1. Impeccable for anti-sl...

27. [ui/tailwind.config.cjs at main · shadcn-ui/ui](https://github.com/shadcn-ui/ui/blob/main/tailwind.config.cjs) - A set of beautifully-designed, accessible components and a code distribution platform. Works with yo...

28. [8 UI design trends we're seeing in 2025 - Pixelmatters](https://www.pixelmatters.com/insights/8-ui-design-trends-2025) - Discover some of our favorite UI design trends for 2025, from dynamic minimalism to functional AI an...

29. [Commence the 2026 design trends content!!! The slop ... - Instagram](https://www.instagram.com/reel/DRvRC-vktYv/) - Is 2026 the year design goes anti-slop? Because look at these rising trends. The child-like linework...

30. [AI-Generated UI Design: What Practitioners Need to Know](https://fuselabcreative.com/ai-generated-ui-design/) - NNGroup's March 2026 research draws a critical distinction between AI-assisted design, where tools h...

31. [Fill Design Gaps with Impeccable Bridges | Paul Bakaus posted on ...](https://www.linkedin.com/posts/paulbakaus_anthropics-frontend-design-skill-for-claude-activity-7415193729671655424--yZa) - Include image references, button styles, code snippets and other components to keep things creative....

32. [shadcn-ui-design-validator - Claude Skills](https://claude-plugins.dev/skills/@hirefrank/hirefrank-marketplace/shadcn-ui-design-validator) - Automatically validates frontend design patterns to prevent generic aesthetics (Inter fonts, purple ...

33. [Interrogating Design Homogenization in Web Vibe Coding | AI ...](https://ai-paper-delta.vercel.app/en/papers/2603.13036)

34. [I built a Claude Code skill that generates 50000+ unique slide designs](https://dev.to/nghiahsgs/i-built-a-claude-code-skill-that-generates-50000-unique-slide-designs-and-killed-the-ai-slop-3g4c) - AI-generated slides look the same: purple gradients, Inter font, identical shadows, flat backgrounds...

