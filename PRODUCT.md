# Product

## Register

product

## Users

Cycling enthusiasts and hobbyists speccing a build they care about. They know bikes
reasonably well — they have opinions about groupsets, wheelsets, and drivetrains — and
they come to compare components, check compatibility, watch the price add up, and share
the result with a like-minded community. Their context is deliberate and exploratory:
they're configuring something, not completing a chore, often across multiple sessions as
a build evolves.

The product has two first-class surfaces that must stay coherent with each other:
- **The builder (primary product surface):** the authenticated workflow — bike-type
  selection, component selection and filtering, the live build with running price, profiles,
  and saved builds. Design here serves the task: clarity, speed, and trustworthy compatibility.
- **The community/landing surface:** the home page, public builds, and shared builds.
  These create the first impression and carry social proof among enthusiasts.

## Product Purpose

BikeBuilder is a dynamic bike configurator: select a component and the build updates in
real time — image, name, price, and compatibility. It exists to make speccing a complete,
compatible bike feel confident and legible instead of like wrangling a spreadsheet or a
parts catalog. Success is a hobbyist arriving with a vague idea, leaving with a complete
build they trust is compatible, priced, and worth sharing — and coming back to refine it.

## Brand Personality

Precise and technical. Confident, spec-forward, engineering-grade — the feel of a tool
built by people who genuinely know bikes. Voice is knowledgeable but not gatekeeping:
exact about compatibility and numbers, warm enough to belong to an enthusiast community
(closer to Strava's shared-passion energy than to corporate tooling). Three words:
**precise, trustworthy, enthusiast-built.** It should evoke the quiet confidence of a
well-machined component — nothing decorative that it can't back up.

## Anti-references

- **Generic SaaS dashboard.** No cream-and-purple AI-template look, no hero-metric cards,
  no endless identical icon-card grids. This is a configurator, not a metrics dashboard.
- **Cluttered parts catalog.** Not Amazon/eBay listing spam — dense, untrustworthy, hard
  to scan. Component data must be scannable and editorial, not a wall of SKUs.
- **Childish gamified toy.** No cartoonish, over-animated, badge-and-confetti energy.
  Motion and feedback should feel mechanical and earned, never undercut technical credibility.
- Also avoid: cold enterprise gray-on-gray with no enthusiast soul.

## Design Principles

- **Compatibility is the product, so make it legible.** Compatibility and price are the
  reasons to trust a build — surface them with precision and clarity at every step, never
  buried or implied.
- **Spec-forward, not spec-spam.** Treat component data as editorial: scannable hierarchy,
  the numbers that matter foremost, restraint over density. Earn the enthusiast's trust by
  respecting their attention.
- **Real-time feedback should feel mechanical.** The live updates (price, image, fit) are
  the magic — motion and state changes should feel precise and engineered, like a component
  clicking into place, not bouncy or decorative.
- **One coherent system across builder and community.** The landing/community surface and
  the authenticated builder share one visual language; the first impression should promise
  exactly what the tool delivers.
- **Confidence without gatekeeping.** Expert-grade precision, but legible to an enthusiast
  who isn't a pro mechanic. Clarity is the form respect takes.

## Accessibility & Inclusion

Target **WCAG 2.1 AA**: body text ≥4.5:1 contrast (≥3:1 for large text), visible keyboard
focus on all interactive elements, full keyboard navigation through the build flow, and a
`prefers-reduced-motion` alternative for every animation (especially the real-time build
feedback). Don't rely on color alone to signal compatibility/incompatibility — pair it with
text or iconography.
