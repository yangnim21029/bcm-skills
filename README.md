# BCM Skills — a Business Capability Map toolkit for Claude Code

Two [Claude Code](https://claude.com/claude-code) skills that take a company from a blank page to a board-ready **Business Capability Map (BCM)** and the downstream visuals you use to act on it. The method is distilled from a Gartner webinar on BCMs (Alexander Hoeppe) — the core idea: **pin AI investment to durable business capabilities, not to vendor use-cases.**

## The two skills

| Skill | What it does | Outputs |
|---|---|---|
| **`bcm-creator`** | *Make the map.* Clarify the brief → research the company → derive capabilities **bottom-up** → apply pace-layer colours + AI pins. | A **BCM-input brief** (HTML — business objectives + a capability metadata table, split value-realizing / value-enabling) **and the BCM itself as a raster image**. |
| **`ai-opportunity-radar`** | *Use the map.* Score AI use cases and readiness against the BCM. | An **AI Opportunity Radar** (use cases on Value × Feasibility, Defend/Extend/Upend) and a **7-dimension Readiness gap** chart — self-contained HTML + inline SVG. |

The full method is bundled in `bcm-creator/references/`:
- `bcm-method-howto.md` — *how to draw* a BCM (9-step walkthrough; the hard step is unit purity: don't put outcomes/processes/use-cases in capability boxes).
- `bcm-method-govern.md` — *how to use & govern* it (use-case assessment, the 6 agent dimensions, readiness, Capability→Value Stream→Process→IT + Digital Thread, the update cadence). A BCM is an ongoing governance backbone, not a one-off diagram.

## Install

Claude Code auto-discovers skills in `~/.claude/skills/`. Copy the two folders there:

```bash
cp -R bcm-creator ai-opportunity-radar ~/.claude/skills/
```

Then in Claude Code just ask in natural language — the skills trigger on intent:
- "make a BCM for `<company>`" → `bcm-creator`
- "build the AI opportunity radar / readiness for it" → `ai-opportunity-radar`

## Dependencies (all optional — the skills degrade gracefully)

- **`python3`** (stdlib only) — required for the HTML renderers. No matplotlib/numpy needed.
- **OpenAI Codex CLI** (`$imagegen`, gpt-image-2) — for the BCM raster image. **Without it, `bcm-creator` writes a ready-to-paste ChatGPT/DALL·E image prompt instead.**
- Sibling skills the SKILL.md files link with `[[...]]` (`codex-image-gen`, `polish-doc`, `search-cross`, `browser-use`, `gemini-image-gen`) are conveniences, not hard requirements: research falls back to plain web search, and you can skip the prose-polish pass. Those links will be dangling if you don't have those skills — harmless.

## Design principles baked in (the non-obvious ones)

- **Bottom-up, not top-down.** List the real concrete capabilities first, then aggregate into domains/tiers — don't force-fit a 13-category taxonomy (that's ideation, not derivation).
- **Analyst-grade data, not PR.** Pull operational reality (cost structure, unit economics, throughput) from industry/business-analysis sources, not revenue/market-share headlines; tag each figure's grade; leave genuinely-internal fields (`owner`/systems/KPI/readiness) marked TBD (to be filled internally).
- **The HTML is the stable base map; the image is the overlay.** pace-layer colour and AI pins are strategic overlays that live on the *image*, not in the capability list. The image is a real raster (codex), never an HTML screenshot.
- **The hard part is unit purity, not layout.** A pretty map full of outcomes and processes is a wrong map.
- **Fresh/trending lane for fast-moving targets.** A recency pass keeps the *overlays* (objectives, AI pins, pace) current — never the stable capability list. One news cycle ≠ a capability change.

## Examples

Worked example specs ship in each skill's `references/` (`example-bcm-input.json`, `example-bcm.json`, `example-portfolio.json`) — run the renderers on them to see the output formats.

## Credit & licensing

Method distilled from the Gartner webinar *"Accelerate Your AI Journey With Business Capability Maps"* (Alexander Hoeppe, VP Analyst). Reference capability templates (APQC PCF, etc.) are **not** included — obtain your own per their licences. The skills, scripts, and method write-ups here are original work; add a LICENSE of your choice before redistributing.
