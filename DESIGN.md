---
name: BikeBuilder
description: A monochrome, spec-forward configurator — near-black ink on crisp white panels over a light-gray canvas, where price and compatibility read with engineering clarity.
colors:
  bg: "#f5f5f6"
  surface: "#ffffff"
  surface-2: "#fafafa"
  surface-hover: "#f1f1f2"
  border: "#e6e6e9"
  border-strong: "#cdcdd2"
  text: "#0a0a0b"
  text-secondary: "#56565c"
  text-muted: "#97979e"
  accent: "#111113"
  accent-hover: "#2c2c30"
  accent-bg: "rgba(17, 17, 19, 0.05)"
  accent-ring: "rgba(17, 17, 19, 0.16)"
  on-accent: "#ffffff"
  green: "#1aae39"
  green-bg: "rgba(26, 174, 57, 0.08)"
  green-ink: "#178a2e"
  warning: "#dd5b00"
  warning-bg: "rgba(221, 91, 0, 0.08)"
  error: "#f87171"
  error-bg: "rgba(248, 113, 113, 0.08)"
  error-ink: "#b42318"
typography:
  heading-page:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  heading-section:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "1.05rem"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0.06em"
  body:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "-0.005em"
  body-strong:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "0.875rem"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "-0.005em"
  label:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "0.7rem"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0.04em"
rounded:
  sm: "6px"
  md: "8px"
  lg: "12px"
  pill: "999px"
  circle: "50%"
spacing:
  xs: "8px"
  sm: "12px"
  md: "16px"
  lg: "20px"
  xl: "28px"
  page-x: "64px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.on-accent}"
    rounded: "{rounded.sm}"
    padding: "7px 16px"
    typography: "{typography.label}"
  button-primary-hover:
    backgroundColor: "{colors.accent-hover}"
    textColor: "{colors.on-accent}"
    rounded: "{rounded.sm}"
    padding: "7px 16px"
  button-ghost:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-secondary}"
    rounded: "{rounded.sm}"
    padding: "7px 16px"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
    padding: "20px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.sm}"
    padding: "8px 12px"
---

# Design System: BikeBuilder

## 1. Overview

**Creative North Star: "The Machined Component"**

BikeBuilder looks the way a well-made bike part feels in the hand: precise, monochrome,
and quietly confident. The system is built almost entirely from neutral grays and a single
near-black ink (`#111113`) laid onto crisp white panels (`#ffffff`) that float on a light
neutral-gray canvas (`#f5f5f6`). There is no decorative color, no brand purple, no gradient
flourish — restraint is the statement. Color enters only where it carries meaning: green for
compatible, amber for caution, red for error. Everything else earns its place by being
legible, scannable, and exact, the way a torque spec or a gear ratio is exact.

This system explicitly rejects the **generic SaaS dashboard** (no cream-and-purple template
look, no hero-metric cards, no endless identical icon-card grids), the **cluttered parts
catalog** (no listing-spam density; component data is editorial and scannable), and the
**childish gamified toy** (no cartoon energy, no confetti). Where motion appears it is
restrained — content fades up a few pixels into place on load so a screen never reads as static,
a hover ring tightens — but it is always subtle and one-shot. Nothing loops, floats, or draws
attention to itself after it has settled. The feel is closer to Linear's calm precision and a
workshop spec sheet than to a marketing page.

**Key Characteristics:**
- Monochrome by doctrine: one near-black ink, a neutral gray ramp, color reserved for meaning.
- Crisp white surfaces over a light-gray canvas, separated by hairline borders and soft neutral shadows.
- Inter everywhere, tuned with negative tracking on body and wide tracking on labels.
- Tight radii (6–12px) and restrained padding — engineered, not soft.
- Restrained entrance motion that settles into place; subtle, never elastic, never perpetual.

## 2. Colors

A true-neutral grayscale carrying a single near-black accent, with three semantic hues used
sparingly to signal build state (compatibility, caution, error).

### Primary
- **Machined Ink** (`#111113`): The lone accent. Primary buttons, active nav state, focus
  intent, the brand mark. On hover it lifts to **Graphite** (`#2c2c30`). Used on a small
  fraction of any screen — its rarity is what gives it weight.

### Neutral
- **Panel White** (`#ffffff`): Every card, navbar block, dropdown, and input surface.
- **Canvas Gray** (`#f5f5f6`): The page background the white panels rest on.
- **Whisper Gray** (`#fafafa`): Secondary surfaces and subtle zebra fills.
- **Hover Gray** (`#f1f1f2`): Surface hover state and the cohesive navbar block.
- **Hairline** (`#e6e6e9`): Default 1px borders and dividers.
- **Hairline Strong** (`#cdcdd2`): Border on hover/emphasis, separators.
- **Ink** (`#0a0a0b`): Primary text — near-black, ~19:1 on white.
- **Slate** (`#56565c`): Secondary text, labels, nav links — ~7:1 on white.
- **Stone** (`#97979e`): Muted text, placeholders, empty/loading states.

### Tertiary (semantic — state only)
- **Compatible Green** (`#1aae39`, bg `rgba(26,174,57,0.08)`, text `#178a2e`): Compatibility-pass signals.
- **Caution Amber** (`#dd5b00`, bg `rgba(221,91,0,0.08)`): Warnings, partial compatibility.
- **Error Red** (`#f87171`, bg `rgba(248,113,113,0.08)`, text `#b42318`): Validation and failure states.

The base semantic hues (`green` / `error`) are too light for body text on white. Each carries
an **`-ink`** shade (`green-ink` `#178a2e`, `error-ink` `#b42318`) for text and small icons, both
≥4.5:1 on white and on their own `-bg` tint. Use the base hue for fills/dots, the `-ink` for text.

### Named Rules
**The One Ink Rule.** There is exactly one accent — Machined Ink. No second brand color is
ever introduced for decoration. If a screen needs visual interest, it comes from hierarchy,
spacing, and the component image, not from a new hue.

**The Color-Means-Something Rule.** Green, amber, and red are reserved for build state
(compatible / caution / error). They are never used decoratively. Never signal state with
color alone — pair it with text or an icon (WCAG AA, color-blind safe).

## 3. Typography

**Display / Body / Label Font:** Inter (with `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`)

**Character:** One family, worked across weights 400–700. A single neutral grotesque keeps
the system disciplined and technical; hierarchy comes from weight, size, and tracking — not
from a second typeface. Body runs slightly tight (`-0.005em`); labels open up with positive
tracking for a spec-sheet cadence.

### Hierarchy
- **Page Heading** (600, 1.5rem, 1.2): Page titles ("Components", profile names).
- **Section Heading / Brand** (700, 1.05rem, +0.06em, often UPPERCASE): The BikeBuilder mark
  and section eyebrows — the one place tracking goes wide.
- **Body** (400, 15px, 1.5, -0.005em): Default reading text. Cap measure at 65–75ch.
- **Body Strong** (600, 0.875rem): Component names, card titles, the price figure.
- **Label** (600, 0.7rem, +0.04em): Chips, metadata, small UI labels and badges.

### Named Rules
**The One Family Rule.** Inter carries everything. Never pair it with a second sans (the
similar-but-not-identical trap). Contrast is made with weight and size, not with a new font.

**The Tracking-Tells-Role Rule.** Negative tracking = reading text. Positive tracking =
labels, brand, eyebrows. The letter-spacing itself signals what kind of text you're looking at.

## 4. Elevation

A hybrid: surfaces are defined primarily by hairline borders and the white-on-gray tonal
step, with soft, neutral, low-contrast shadows added to de-flatten interactive and floating
elements. Shadows are tinted with the ink's own near-black (`rgba(10,10,15,…)`), never pure
black, so they read as ambient depth rather than hard drop-shadows.

### Shadow Vocabulary
- **Resting** (`box-shadow: 0 1px 2px rgba(10,10,15,0.06), 0 1px 3px rgba(10,10,15,0.05)`):
  Cards and rows at rest.
- **Raised** (`box-shadow: 0 4px 10px rgba(10,10,15,0.08), 0 2px 4px rgba(10,10,15,0.05)`):
  Hovered cards, lifted surfaces.
- **Floating** (`box-shadow: 0 16px 34px rgba(10,10,15,0.14), 0 4px 10px rgba(10,10,15,0.07)`):
  Dropdowns, popovers, modals.
- **Accent Lift** (`box-shadow: 0 8px 20px rgba(10,10,15,0.22)`): The hover/active state of
  the primary (ink) button — a tighter, darker lift that reads as a press.

### Named Rules
**The Border-First Rule.** Structure comes from the 1px hairline and the tonal step first;
shadow is the second layer, used to lift on interaction. A flat card with a hairline is
correct; a heavy resting shadow is wrong.

## 5. Components

### Buttons
- **Shape:** Tight, engineered corners (6px radius).
- **Primary:** Machined Ink fill (`#111113`), white text, 1px ink border, label-scale type
  (0.8rem / 600), `7px 16px` padding. Hover → Graphite (`#2c2c30`) with the Accent Lift shadow;
  active settles back to the resting shadow. Disabled drops to `opacity: 0.5`, no shadow.
- **Ghost / Secondary:** Transparent on white, 1px hairline border, secondary-gray text.
  Hover darkens text to ink and strengthens the border to `#cdcdd2`. The quieter default for
  non-primary actions.

### Chips / Tags
- **Style:** Transparent or whisper-gray fill, 1px hairline border, 6px radius, label type
  (0.7rem / 600). Filter and metadata roles.
- **State:** Selected chips take the ink treatment (ink border/text or ink fill); unselected
  stay neutral-gray. Selection is shown by ink, never by a colored fill.

### Cards / Containers
- **Corner Style:** Generous for the system — 12px radius on content cards (component cards,
  panels), 8px on smaller surfaces (dropdowns).
- **Background:** Panel White (`#ffffff`) on the gray canvas.
- **Border:** 1px Hairline (`#e6e6e9`) always; strengthens toward `#cdcdd2` on hover.
- **Shadow Strategy:** Resting shadow at rest, Raised on hover (see Elevation).
- **Internal Padding:** 20–28px for content cards; the build/spec rows run tighter.

### Inputs / Fields
- **Style:** White fill, 1px hairline border, 6px radius, comfortable `8px 12px` padding.
- **Focus:** Border shifts to ink (`#111113`) and a 3px ink ring appears
  (`box-shadow: 0 0 0 3px rgba(17,17,19,0.16)`) — the same ring used for keyboard focus
  everywhere, so focus reads consistently across the app.

### Navigation
- **Style:** A horizontal bar on the hover-gray block (`#f1f1f2`), with a distinctive angled
  tab strip (`clip-path` diagonal slash) revealing the white surface beneath — the system's
  one piece of mechanical geometry. Brand mark is uppercase, 700, wide-tracked.
- **Links:** Muted gray at rest; an ink underline grows from `scaleX(0)` on hover (to 0.5)
  and fills (to 1) on the active route, where the link also goes ink + 600. Dropdowns use the
  Floating shadow and a fade-up entrance.

### Signature Component — The Live Build Row
The configurator's heart: a component row showing image, name, price, and compatibility
state. It updates in real time as selections change. Price is set in Body Strong so the
running total stays the most legible number on screen; compatibility uses the semantic green/
amber/red with an accompanying label, never color alone. The update should feel mechanical —
a fade-up settle (`fadeInUp`, `--ease-out` `cubic-bezier(0.16,1,0.3,1)`, ~220ms), like a part
clicking into place.

## 6. Do's and Don'ts

### Do:
- **Do** keep the palette monochrome. Build interest from hierarchy, spacing, weight, and the
  component imagery — not from a new hue (**The One Ink Rule**).
- **Do** reserve green/amber/red strictly for build state, and always pair them with text or
  an icon — never signal compatibility by color alone (WCAG AA, color-blind safe).
- **Do** structure surfaces with the 1px hairline and the white-on-gray tonal step first;
  add shadow only to lift on interaction (**The Border-First Rule**).
- **Do** make the running price and compatibility the most legible elements on any build
  screen — clarity is how this product earns trust.
- **Do** drive hierarchy with Inter's weights and tracking; negative tracking for reading,
  positive tracking for labels and the brand mark.
- **Do** use the restrained motion vocabulary — `fadeInUp` / `fadeIn` on the ease-out curve
  `cubic-bezier(0.16,1,0.3,1)`, 140–220ms, with a small `translateY` (~10px) — so content
  loads in and settles into place instead of appearing static. Stagger list/grid items with a
  small per-item delay (~70ms) rather than animating each one differently.

### Don't:
- **Don't** ship the **generic SaaS dashboard**: no cream-and-purple template palette, no
  hero-metric cards (big number / small label / gradient accent), no endless identical
  icon-card grids.
- **Don't** ship the **cluttered parts catalog**: no Amazon/eBay listing-spam density.
  Component data stays editorial and scannable.
- **Don't** ship the **childish gamified toy**: no cartoon energy, no confetti, no badges,
  no bouncy/elastic motion.
- **Don't** use perpetual or looping motion — no infinite float/pulse/bob on hero images or
  any element. Motion is one-shot: it plays on load or on interaction, then stops. An element
  still moving after the page has settled is wrong.
- **Don't** introduce a second brand color or a gradient for decoration. One ink, period.
- **Don't** use gradient text (`background-clip: text`), glassmorphism, or a >1px colored
  side-stripe border on cards or rows.
- **Don't** re-introduce a global motion kill-switch in `index.css` (`animation: none
  !important; transition: none !important;`). It was removed so the restrained entrance motion
  can run; the `prefers-reduced-motion` block already present in `index.css` is the correct,
  accessible way to suppress motion for users who ask for it.
