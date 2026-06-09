---
name: bcm-creator
description: Build a Business Capability Map (BCM / 業務能力地圖 / business capability model) for a company end-to-end — clarify the brief, research the company, derive its capabilities bottom-up, apply pace-layer colours and AI pins, then ship two artifacts: a BCM-input brief as HTML (the homework — note 1's required inputs: business objectives + a capability metadata table, business-briefing style) AND the BCM itself as a generated raster image (via codex), or a ready-to-paste ChatGPT image prompt when codex CLI isn't installed. Use this whenever the user wants to map what a business does (not how) into a tiered capability picture, asks for a "BCM / capability map / capability model / 能力地圖 / 業務能力地圖", wants to plan where AI investment should go across a company, or wants to turn a strategy into a one-page capability view. Trigger even if they don't say "BCM" but describe wanting to lay out a company's capabilities, decide which to invest AI in, or compare capabilities to competitors. Covers any industry (manufacturing, banking, retail, SaaS, public sector).
---

# bcm-creator

Take a company from a blank page to a finished capability map. A BCM answers "**what does this business do, or should do**" — durable capabilities, not the processes or tools that change every year. The point is to pin AI (and budget) onto stable capabilities instead of vendor use-cases.

Source method: distilled from a Gartner webinar on Business Capability Maps (Alexander Hoeppe). The full method is bundled in this skill's `references/`: `bcm-製作重點.md` (the 9-step *how to draw*) and `bcm-使用與治理.md` (*how to use & govern*). Read them if anything below is unclear.

## The two deliverables (end of the run)

1. **A BCM-input brief, as HTML** — the *homework*, in business-briefing style. Its content is exactly what **note 1** says a BCM needs (NOT a generic company profile): a short company **context**, the **business objectives** (the BCM's top row), and a **capability inventory split into value-realizing / value-enabling** (note 1's two layers, L100–102), each row a metadata card — public fields filled (definition / level / industry-typical KPI / AI pin), internal fields (owner / supporting systems / data in-out / data readiness 1–5) marked **待補** for the org. **pace layer is NOT in this list** — it's a strategic overlay applied on the image. Rendered by `scripts/render_bcm_input_html.py` from a JSON spec.
2. **The BCM, as a picture** — a generated **raster image** via [[codex-image-gen]] (gpt-image-2) when the codex CLI is installed; otherwise a **ready-to-paste ChatGPT image prompt** written to a `.txt`.

**Keep these straight — the HTML is the company background, the BCM is the image.** The BCM is a *picture*, not an HTML page; never render the map as HTML or screenshot a page to make it. The user has corrected this twice — pictures come from a real image generator (codex raster), see [[gen-image-use-codex-not-html]].

## What this skill pulls in

- `AskUserQuestion` — Phase 0 brief.
- Web research for a real company — [[search-cross]] / [[browser-use]] / an `Explore` sub-agent — to fill the BCM-input brief. For a fictional/illustrative company, construct it and say so.
- `Read` — an APQC PCF (apqc.org, free with attribution) or any industry capability-model template you have, to cross-check completeness; plus the bundled method docs in `references/`.
- `scripts/render_bcm_input_html.py` — the HTML path (Phase 2a).
- A [[polish-doc]] sub-agent — Phase 2a prose polish (don't ship the first draft).
- [[codex-image-gen]] — the image path (Phase 2b).

---

## Phase 0 — Clarify the brief first (do not skip)

A BCM goes wrong when you draw before you know whose map it is and what goal it serves. Two outputs (pace-layer colour, AI pins) are **overlays tied to a perspective** — guess the perspective and you colour the whole map wrong, so the investment story it tells is wrong. Ask before building.

Run `AskUserQuestion` (or ask inline if the user is terse). Skip any the conversation already answered; confirm rather than re-ask:

1. **公司、產業、商業模式** — who they are and how they make money. Decides which capabilities exist (a bank has 風控合規; a maker has 供應鏈).
2. **這是誰的地圖（視角）** — the same box means different things from different viewpoints (your own capability vs a supplier's core capability). Pin one viewpoint or boxes drift.
3. **戰略視角 / 經營目標** — e.g. 衝新品 vs 降成本 vs 法遵優先. This decides each box's pace-layer colour. Without it you cannot colour the map.
4. **AI 想在哪裡拉開差距** — which capabilities AI should make a difference in. Becomes the AI pins.
5. **深度** — L1 only (board view, ~10–15 boxes) or L1 + L2.
6. **輸出與語言** — 繁中 or English; both artifacts or just one.

Restate the brief in two lines, then proceed.

---

## Phase 1 — Research the company, then derive the map BOTTOM-UP

### Step 1: research → company context + business objectives

The HTML carries **note 1's BCM inputs, not a generic company profile**. Do NOT pad it with 商業模式 / 目標客群 / 營運模式 sections — note 1 never lists those as what a BCM needs. Collect just two things here (capabilities come in Step 2):

- a **short company context** (2–4 sentences for orientation), and
- the **business objectives** — the strategic targets that sit at the top of the BCM (note 1, L96–98), each with the KPI it's measured by.

For a real company, **research it for real** ([[search-cross]] / [[browser-use]] / a research sub-agent) — specific figures with units, named entities, not generic statements. **Never invent numbers** — cite sources, and drop any contested / 口徑不一 figure into the final 資料註記 instead of silently picking one. For a fictional/illustrative company, say so explicitly. Worked example: `references/example-bcm-input.json`.

**Mind the internal-data wall — but mine the analyst layer first.** owner / supporting systems / data in-out / data readiness (the metadata card, notes line 256) are genuinely private — leave them 待補. But "public" has grades, and **PR/marketing-grade common sense is the shallowest**: revenue, market share, brand campaigns — what everyone already knows. Before settling for that, dig the **industry / business-analysis layer** — equity-research notes, sector studies, capital-markets-day / IR operational disclosures, supply-chain & cost-structure teardowns, operationally-detailed trade press. That layer surfaces the *inner operational reality* per capability (cost structure, throughput/yield, unit economics, inventory turns, capability maturity vs peers) — which is what makes the KPIs real instead of generic "良率／成本". **Tag each data point by grade** — `[財報]` / `[投資人揭露]` / `[分析估計]` / `[PR]` / `[待補-內部]` — so estimates, headlines, and private fields aren't read as equal, and flag low-confidence (e.g. marketing-blog) numbers for first-source re-check. (Verified for Pandora: this turned "world's largest jewelry brand" PR into new-store year-1 EBIT 35–40%, silver = ~67% of materials at ~12bp EBIT per $1/oz, inventory ~281 days — and the non-obvious finding that the cost moat is retail+marketing, not manufacturing.)

### Step 2: derive the capability structure BOTTOM-UP

**This is derivation, not ideation (發想). Build from the bottom up, do not invent a top taxonomy and fill it in.** The Gartner method (notes line 78, 110): a capability is a concrete verb — `assess credit risk`, `execute production`, `操作網路基礎設施`. A grouping like `manage operations` (Level 0) is just the **aggregation** of those concrete Level-1 capabilities. So:

1. **List the concrete capabilities first.** From the context brief, enumerate the real "what this business does or should do" items — verbs, Level-1. Write the actual capabilities the business has, not neat categories you'd like it to have. Starting from top categories force-fits reality and invents capabilities the business doesn't really do — that's the ideation trap the bottom-up order avoids.
2. **Gate every one through the 3 purity tests** (the hard part — most maps rot here; being a "business noun" is not enough):
   - **what ≠ how** — `費用管理` (capability), not `差旅報銷` (a process under it).
   - **capability ≠ outcome** — `敬業與留才管理` (what you do), not `留任` (the result). Pin AI on the capability or you bet AI on a number instead of on the thing that moves it.
   - **same level, same type** — siblings are the same kind and altitude; don't mix capability / process / outcome / use-case in one row.
3. **Cluster upward into domains and tiers.** Let the groupings *emerge* from the clean capabilities — bundle related ones into a domain (L0), then place domains into tiers (策略層 / 核心層 / 支援層, i.e. Strategic / Core / Supporting; name them to fit the company). The shape comes from the capabilities, not the other way round.
4. **Cross-check completeness against APQC / Gartner templates.** Open `apqc-pcf-v7.4-cross-industry.pdf` and the Gartner 10+ industry templates as a *checklist* — did your bottom-up list miss a capability? The cost of skipping this is "你不知道你不知道什麼" (notes line 106). Use the template to catch gaps, not to seed the skeleton.
5. **Drill DOWN to L2 only as the exception** — when one capability serves several outcomes (e.g. `人才管理` touches productivity, innovation, retention), split it so each sub-capability maps to its outcome (notes line 112). Otherwise stop at L1. Only detail-model business-critical capabilities; past ~L3 you're building a process model, not a capability model.

**Record each capability's metadata** (note 1, L256 — this card is the governance unit). Public fields you fill: definition (a tight verb phrase — "what it does", not a noun label), level, role (value-realizing / value-enabling — this splits the list into two sections), industry-typical KPI, AI pin. **Don't assign pace layer here** — pace is an overlay decided when you draw the map (Step 3 / the image), not a property of the inventory. Internal fields you mark 待補: owner, supporting systems, data in-out, data readiness (1–5). These rows ARE the capability list in the HTML; the same capabilities, clustered into tiers/domains and coloured by pace, become the image.

### Step 3: apply the overlays — on the IMAGE, not the list

pace layer and the dashed value-enabling border are **overlays** (note 1, L124, 底圖 vs 疊加層) — they live on the BCM **image** spec, not in the capability list. Decide them when you build the picture (Phase 2b):

- **Pace-layer colour**, from the Phase 0 goal — `differentiating` (重押 AI) / `keep_up` / `commodity`. The same capability can be a different colour under a different objective (notes line 124), which is exactly why it doesn't belong in the inventory.
- **Dashed value-enabling** — flag the capabilities that earn nothing alone but feed others (`enabling: true`); cutting them is the most common BCM governance mistake (notes line 102). In the list these are simply the value-enabling section.
- **AI pins** — pin AI to a *capability*, never to an outcome or use-case. (AI pin shows in both the list and the image.)

### Output of Phase 1: two specs

- A **BCM-input brief JSON** (→ the HTML). Keys: `company / tagline / as_of / classification`, `facts[]`, `context`, `objectives[{name, kpi}]`, `capabilities[{name, level, role: realizing|enabling, ai, definition, kpi}]` (no pace — that's image-only), `notes[]`, `sources[]`. Worked example: `references/example-bcm-input.json`.
- A **BCM image JSON** (→ the picture). `tiers[].domains[].capabilities[{label, pace: differentiating|keep_up|commodity, ai, enabling, l2}]` — the SAME capabilities, clustered into tiers/domains and **coloured by pace here**. Worked example: `references/example-bcm.json`.

---

## Phase 2 — Produce the outputs

### (a) BCM-input brief → HTML (the homework)

Write the BCM-input spec to a `.json`, then render:

```bash
python3 ~/.claude/skills/bcm-creator/scripts/render_bcm_input_html.py /path/to/brief.json /path/to/out.html
```

**Then run a polish pass — don't ship the first draft.** A first-draft brief reads shallow and AI-flavoured: 標題式名詞串、口號句（「樞紐 / 引擎 / 瓶頸」）、翻譯腔、破折號過量, and capability definitions written as noun labels instead of "what it does" verb phrases. Spawn a sub-agent to run [[polish-doc]] on the prose — it uses codex as the external engine plus its own pass over the Chinese dimensions (動詞撐句、砍名詞化/直譯腔、一段 ≤1 個破折號、不湊三軸清單、模糊量詞換具體), editing **only** the prose fields — `context`, `objectives[].name/kpi`, `capabilities[].definition/kpi`, `notes[]` — never the numbers, sources, or the `role`/`level`/`ai`/待補 fields. Have it write a `*.polished.json`; re-render that and `open` it. This step is what turns generated filler into something that reads like a real 匯報 document.

Self-contained HTML, CJK fonts in the stack, no dependencies. Sanity-check the capability/objective counts match the spec.

### (b) BCM → raster image, when codex CLI is installed

Detect first: `command -v codex`. If it prints a path, use [[codex-image-gen]]. Build the image brief from the BCM JSON (layout zones top-to-bottom by tier, short labels, pace-layer colours, AI badges, dashed enabling, language stated). Pipe a CJK brief via stdin per the codex-image-gen skill.

**State the AI-badge count and make it equal the number of `ai:true` capabilities — list them by name.** Never write a contradictory count ("四個…其實三個") — the raster model counts badges from your words; an inconsistent brief makes it guess.

**Guardrail learned the hard way — codex silently fakes a raster on error.** When gpt-image-2 hits an OpenAI server error, codex's agent quietly falls back to writing a PIL/SVG render script and still reports "已完成" — handing you a code-rendered image (`.svg` + small `.png`), not a real raster. So:

- **Forbid the fallback in the brief**, verbatim: 「只能用內建 image_gen（gpt-image-2 raster）；禁止用 SVG / HTML / PIL / matplotlib 或任何寫程式碼畫圖的方式替代；若 image_gen 報錯，把原始錯誤逐字貼出來再停，不要產生替代圖。」
- **Verify which path it took** before calling it done: a real gpt-image-2 raster is ≈ 1 MB+; a PIL render is ≈ 100–250 KB and leaves a `.svg`/`.py` behind. If you see those, it fell back — that's an intermittent server error.
- **On `ServerError`, back off — don't fire rapid back-to-back retries.** It's a known transient codex `image_gen` backend/throttle issue (r/codex, OpenAI error-code docs); per OpenAI's 429 guidance, failed rapid retries count against the limit and *worsen* throttling. Wait 1–2 min between attempts and surface the raw error each time. If `OPENAI_API_KEY` is set, codex can route image_gen through the API lane instead of the throttled ChatGPT-plan OAuth lane — a more reliable escape hatch (needs a paid tier). A clean raster usually lands within a couple of backed-off tries; if it server-errors ~3× in a row, stop and hand over the ChatGPT-prompt fallback (2c) rather than burning more turns.
- Copy the PNG out of `~/.codex/generated_images/...` to the project and `open` it. gpt-image-2 paraphrases long text — keep labels to 2–5 chars/words and eyeball the CJK on the result.

### (c) No codex CLI → ChatGPT image prompt

If `command -v codex` finds nothing, don't fake an image. Write the BCM image brief (without the codex `$imagegen` token and the no-fallback lines) to a `.txt` and tell the user: "Paste this into ChatGPT (GPT-image / DALL·E)." Brief shape:

```
A clean, modern, flat-style Business Capability Map infographic, landscape ~1536x1024.
All text in <language>, rendered crisply. Style like a Gartner consulting slide:
white background, flat rounded boxes, thin grey borders, aligned, generous whitespace.
Three horizontal tiers top to bottom, each labelled on the left: <tier names>.
<Per tier: the domain group boxes; per domain: its capability tiles, colour = pace layer,
 an "AI" badge on the pinned ones, dashed border on value-enabling ones.>
Colour key along the bottom: orange = differentiating / heavy AI bet; gold = keep up;
cream = commodity / buy off-the-shelf; dashed border = value-enabling, don't cut.
Palette: orange #d9701b, gold #f5c266, cream #fbf4e2; near-black text.
AI badge = small black rounded pill, white "AI", top-right of the tile.
```

---

## Phase 3 — use the map as a governance backbone (don't stop at the picture)

The map is the start, not the end — note 1's biggest point. A BCM that's drawn once and filed is a dead picture. Once you have it, it becomes the unit for AI governance, and the workflow continues. Full how-to: [`bcm-使用與治理.md`](~/.claude/skills/bcm-creator/references/bcm-使用與治理.md); the radar + readiness charts auto-generate via the [[ai-opportunity-radar]] skill. In brief:

- **Map use cases onto it (AI Opportunity Radar)** — pin each AI use case to a *capability*, not to itself (use cases age out in months; capabilities last years). Assess each use case on: the **6 agent dimensions** (Perception / Decisioning / Actioning / Agency / Adaptability / Knowledge — most need only 2–3 strong); **which AI techniques + data sources + integration** it needs (not everything wants Gen AI); and a **Defend / Extend / Upend** tag. Heed the agency caution — Level-1 full autonomy is science-fiction for an end-to-end chain (one bad auto-decision propagates).
- **Assess readiness** — 7 dims (Strategy / Value / Organization / People & Culture / Governance / AI Engineering / AI Data); judge the current→future **gap**, not the score. Data readiness is **contextual** (same data is L5 for one capability, L2 for another) — don't wait for 100% clean.
- **Fill the metadata cards** — definition / owner / data in-out / supporting systems per capability (the 待補 fields). Without them the map is decoration, not a governance unit.
- **Operationalize downward** — Capability → Value Stream (the sequence/arrows the BCM lacks) → Process → IT system; the Digital Thread maps the value stream to data flow so data governance and business governance become one thing.
- **Connect bottom-up POCs to the map (bimodal)** — top-down (BCM / prioritization / readiness, leadership) meets bottom-up (POC / pilot, teams). Most POCs fail not because they don't work but because, with no BCM backbone, nobody tracks them post-launch and the KPI is forgotten. Pin every POC to its capability + KPI.
- **Run the update cadence** — re-look quarterly/half-yearly: re-colour pace, advance use cases on the radar, close readiness gaps, re-pin POCs, refresh metadata, regenerate the input brief + image (stamp the version/date).

This is what turns the BCM from "IT's PoC pile" into enterprise-level AI governance — and AI strategy is its own strategy, not a subset of IT strategy.

---

## Gotchas

- **HTML = company homework, BCM = image.** Don't render the BCM as HTML or screenshot a page to make the picture. Separate deliverables, separate paths.
- **Build bottom-up, not top-down.** List the real concrete capabilities, then aggregate into groupings — don't start from a 13-category taxonomy and fill it in. That's the difference between derivation and 發想; templates are a completeness check, not the skeleton.
- **The hard part is purity (the 3 tests), not layout.** A pretty map full of outcomes and processes is a wrong map.
- **codex silently fakes a raster on server error** (Phase 2b). Verify by file size + stray `.svg`/`.py`; never accept a code-render as the raster.
- **Pace-layer colour is an overlay, not an intrinsic property** — re-colouring under a different goal is expected, not a redo. That's why Phase 0 pins the goal.
- **Capability vs product depends on the viewpoint** — no answer until you've pinned whose map it is (Phase 0, Q2). The four reading lenses (視角 / 高度相對 / 底圖vs疊加層 / 單位純度) are in the 01 notes if the user wants the theory.
