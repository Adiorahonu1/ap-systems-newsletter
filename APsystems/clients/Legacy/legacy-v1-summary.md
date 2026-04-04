# Legacy Landing Page — v1 Snapshot

## Design System (KEEP EXACTLY)
- **Fonts:** Cormorant Garamond (serif display) + Outfit (sans body)
- **Colors:** `--navy: #0e1b38` | `--cream: #faf9f6` | `--cream-2: #f3f1ec` | `--red: #C8102E` | `--gold: #b8973d` | `--muted: #7a8096`
- **Easing:** `cubic-bezier(0.25, 0.46, 0.45, 0.94)`
- **Buttons:** pill-shaped (border-radius: 100px), red / navy / outline / gold / outline-white variants
- **Scroll reveal:** `[data-sr]` + IntersectionObserver → `.sr-in` class
- **Section eyebrow:** small red uppercase with left line `::before`

## Page Sections (v1 order)
1. Fixed nav (logo + links + quiz CTA button)
2. Hero — split grid 1fr 1fr. Left: cream bg, headline "We Build Legacies That Last", sub, 2 CTAs, trust stats (1K+, 10+, 5 agents). Right: navy bg, Earnie photo full-height, name badge bottom-left.
3. Trust marquee strip — navy bg, scrolling service names
4. About — split grid, couple photo left (with red frame accent + 98% stat card), story text right, 4 value pillars, CTA button
5. Services — cream-2 bg, 3 service cards in grid (Life Insurance, Financial Planning, Legacy Building), numbered 01/02/03, emoji icons, hover red top-border reveal
6. Stats — navy bg, 4 cells: 1K+ Families / 10+ Years / 98% Satisfaction / 5 Agents (count-up animation)
7. Team strip — full-width photo of team in red varsity jackets, overlay headline "We Are The Winningest Team"
8. Quiz CTA — navy bg, left: headline "What's Your Financial Profile?" + gold button, right: 4 profile preview cards (Protector / Legacy Builder / Freedom Planner / Wealth Creator)
9. How It Works — cream bg, 3 steps horizontal with connector line: Take Quiz → Get Report → Book Call
10. Founders + Book Call — navy bg, couple photo left, text right, gold quiz button + Instagram link
11. Footer — navy bg, 3-col: brand/tagline/social | nav links | contact

## Quiz Overlay (KEEP MECHANIC)
- Slides in from right (`translateX(100%)` → `translateX(0)`)
- Sticky nav bar inside with logo + close button
- Intro screen → 6 questions → generating screen → results → email gate → match bars → book card
- Question types: binary A/B cards with "OR" badge, multi-select chips, range slider
- 4 profiles: The Protector / The Legacy Builder / The Freedom Planner / The Wealth Creator
- Generating screen: red-to-gold gradient progress bar + 5 reveal lines
- Email gate: navy card, name + email inputs, submit reveals match bars + book card

## Sticky Bar + Exit Intent (KEEP)
- Sticky bar: appears after 500px scroll, navy bg, quiz prompt, gold button, dismissible
- Exit intent: triggers on `mouseleave` where `clientY < 10`, cream modal with quiz CTA

## Images
- `Untitled%20design%20(9).png` — Logo (white bg)
- `Untitled%20design%20(10).png` — Team in red varsity jackets
- `Untitled%20design%20(11).png` — Earnie Sears solo (dark bg)
- `Untitled%20design%20(12).png` — Earnie & Sharon couple (dark bg)

## Critique Issues to Fix in v2
1. Page has no emotional narrative arc — restructure flow
2. Quiz CTA buried in section 8 — move to section 3
3. About + Founders are duplicate sections — merge into one
4. "5 Dedicated Agents" stat kills credibility — replace
5. Hero headline is generic — make emotional and personal
6. No social proof / testimonials anywhere
7. Quiz intro screen is flat — add preview/excitement
8. "Book a Call" buttons all go to #founders — give it its own section
9. Services section lacks visual weight — improve contrast
10. Emoji icons in services feel casual — upgrade to SVG/CSS icons
