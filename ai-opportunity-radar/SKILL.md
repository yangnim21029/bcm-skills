---
name: ai-opportunity-radar
description: Auto-generate the two "use the BCM" portfolio visuals from note 1 — an AI Opportunity Radar (AI use cases plotted on Value × Feasibility, coloured by Defend/Extend/Upend, pinned to BCM capabilities, zoned into Likely wins / Calculated risks / Marginal gains) and a 7-dimension AI Readiness gap chart (current vs future on Strategy / Value / Organization / People & Culture / Governance / AI Engineering / AI Data). Use this AFTER a BCM exists (it's the downstream step the [[bcm-creator]] map feeds), or whenever the user wants to prioritise AI use cases, map a use-case portfolio, score AI readiness, see the value/feasibility quadrant, plan where AI investment should go, or turn a capability map into an investment radar. Triggers: "AI opportunity radar", "prioritise use cases", "value feasibility quadrant", "AI readiness assessment", "put use cases on the BCM", "Defend/Extend/Upend", "draw a readiness radar". Renders precise data charts as self-contained HTML+SVG (deterministic), not raster.
---

# ai-opportunity-radar

The downstream half of the BCM method: once you have a capability map ([[bcm-creator]]), this turns it into an **investment radar** and a **readiness gap chart** — the two visuals note 1 uses to decide *where AI goes* and *whether you're ready*. Full method context: `~/.claude/skills/bcm-creator/references/bcm-method-govern.md` (bundled with the bcm-creator skill).

## The two outputs

1. **AI Opportunity Radar** — every AI use case plotted on **Value (y) × Feasibility (x)**, each dot coloured by **Defend / Extend / Upend** and pinned to a BCM capability. Zones: **Likely wins** (hi value + hi feasibility → do now) / **Calculated risks** (hi value, low feasibility → small bets) / **Marginal gains** (low value → don't distract). Rendered by `scripts/render_radar.py`.
2. **AI Readiness gap chart** — a 7-axis spider, **current vs future**, with a gap table. The point is the **gap**, not the score. Rendered by `scripts/render_readiness.py`.

**Format = self-contained HTML + inline SVG (deterministic), NOT a codex raster.** A radar is a scatter at exact (value, feasibility) coordinates and a readiness chart is a spider at exact scores — gpt-image-2 cannot place data points accurately, so a raster would be decorative-but-wrong. This is the same "precise data artifact" lane as the bcm-creator brief HTML, not the illustrative-map lane. (If the user explicitly wants a slide-style raster of these, that's a separate, lossy request — say so.)

## Phase 0 — clarify (the scoring wall)

Most of the input is a **strategic/internal judgement, not web-researchable** (the data wall from [[bcm-creator]]): which use cases the org is weighing, their value/feasibility, the readiness scores. Pin via `AskUserQuestion` (skip what's already given):

1. **Which BCM / company** — and is there a bcm-creator brief to pull capabilities from?
2. **Use cases** — does the user supply them (+ rough value/feasibility), or should I **propose candidates** per capability from the BCM + industry-typical AI use cases?
3. **Who scores** — the user/org gives value/feasibility & readiness, or I put down **estimates marked TBD** for them to adjust? (Never present estimates as the org's real scores.)

## Phase 1 — assemble the portfolio (apply the assessment lenses)

Build one `portfolio.json`:
- `use_cases[]`: `{name, capability (a BCM L1 box), value 1-5, feasibility 1-5, type: defend|extend|upend}`. When proposing/sizing each, apply note 1's lenses (documented in `bcm-method-govern.md`):
  - **value** = contribution to a business objective; **feasibility** = technical maturity + internal readiness.
  - **Defend / Extend / Upend** tag — augment-with-stable-ROI / process-transformation-with-packaged-solutions / frontier-high-uncertainty.
  - sanity-check with the **6 agent dimensions** (Perception / Decisioning / Actioning / Agency / Adaptability / Knowledge — most need 2–3) and **agency caution**: a use case demanding end-to-end Level-1 autonomy is a Calculated risk at best (one bad auto-decision propagates), so its feasibility is low. Also note **which techniques + data sources + integration** it needs — thin integration ⇒ lower feasibility.
- `readiness[]`: the 7 dims `{dim, current 1-5, future 1-5}`. Judge the **gap**; data readiness is contextual (don't require 100% clean).
- `notes[]`: flag every estimate (`TBD`), the scoring wall, and the type-inference basis. Worked example: `references/example-portfolio.json`.

## Phase 2 — render

```bash
python3 ~/.claude/skills/ai-opportunity-radar/scripts/render_radar.py /path/portfolio.json /path/radar.html
python3 ~/.claude/skills/ai-opportunity-radar/scripts/render_readiness.py /path/portfolio.json /path/readiness.html
open /path/radar.html /path/readiness.html
```

Sanity-check: radar dot count = use-case count; readiness axes = 7 (or however many dims given). Both are pure-stdlib (no matplotlib/numpy needed).

## Gotchas

- **Don't present estimated scores as the org's real numbers.** value/feasibility/readiness are internal strategic judgements; pre-fill as `TBD` estimates and say so. A radar full of made-up scores is worse than an empty one.
- **The radar is a prioritisation aid, not truth** — it sorts the conversation, it doesn't make the decision. Two people can score the same use case differently; that disagreement IS the useful output.
- **Pin use cases to a capability, not to themselves** — same as the BCM rule; a use case with no capability to pin to is a smell (it's probably an outcome or a tool).
- **Readiness: gap, not score** — a high current score with no future ambition isn't readiness, it's complacency; a big gap on Strategy/Governance (the oft-ignored dims) is the real blocker.
- **HTML+SVG, not raster** (see above) — these are data charts; deterministic render is the correct tool, not a faked picture.
- This skill is the *use* step; making the map itself is [[bcm-creator]], and the connecting method is `~/.claude/skills/bcm-creator/references/bcm-method-govern.md`.
