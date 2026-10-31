---
name: ai-opportunity-radar
description: Assess AI options against a capability map, distinguish portfolio positioning from value/feasibility scoring, and explain readiness gaps, data dependencies and authority. Use for opportunity radars, AI prioritization, value/feasibility matrices and readiness reviews after capabilities and an objective are identified.
---

# AI Opportunity Assessment

Connect each candidate to an objective, capability, specific problem, evidence, implementation needs and a way to check results. If no map exists, establish the relevant capabilities or use `bcm-creator`.

For a new assessment, read [the structured interactive intake](references/interactive-intake.md) before external research or ranking. Reuse the current conversation and any `intake-record.json` from capability work; ask only the unanswered, decision-relevant questions in small rounds. Let the user identify directly available materials or explicitly skip. A skip leaves a provisional scope and gaps to investigate; it does not establish a business priority. Pure prose revisions do not restart this interview.

Check how the objective and scope were selected before ranking candidates. A detailed product source or feasible demo does not establish company-wide priority. For a broad company question, keep the initial model provisional and test its boundary, alleged gaps and causal claims against actual counterexamples and competing business explanations. Let those findings guide additional research; do not immediately fill all unknowns or refine scores inside an unjustified scope. Preserve conditional alternatives when the evidence cannot choose a priority.

Read [the assessment method](references/assessment-method.md) and [the portfolio contract](references/portfolio-contract.md). Both are included here; no hardcoded sibling installation is required.

## Choose the visual for the question

- **Opportunity radar:** Where does the portfolio concentrate effort: front office, back office, products/services or core capabilities, and everyday improvement or a change in competitive position? This is strategic positioning; unlabeled ring distance is not ROI, feasibility or maturity.
- **Value/feasibility matrix:** How valuable and implementable is a candidate for this organization and objective? A point needs two supported scores and their basis. This is not the opportunity radar.
- **Readiness gap:** What must change between current conditions and a justified target? Examine strategy, value, organization, people/culture, governance, engineering and data in context. Unknown is not 0 or 1; the target is not automatically 5.

Provide the relevant visuals. The historical filename `render_radar.py` is retained, but its output is explicitly a value/feasibility matrix. Use Mermaid or a labeled categorical diagram for portfolio positioning; do not fabricate numerical coordinates.

## Assess options

Use supplied scores and evidence. Ask for material missing internal judgments, or continue with qualitative findings and `null` scores when only public evidence is available. Provide illustrative scores only when the user asks for estimates, marking each with its basis. Never label a numeric guess “TBD” and plot it as measured.

For each candidate, establish:

- Objective and capability ID, the actual bottleneck, and a comparable non-AI/process option when relevant.
- Expected contribution and evidence that would establish it, with units, period and uncertainty. Avoid double-counting benefits across dependent projects.
- Data, integration, latency, permissions and operational resources. Show prerequisites explicitly; a supporting data project can precede a higher-scoring application.
- What the system detects, decides, acts on and confirms, and what people or other systems still do. Separate function from authorization and performance.
- Responsibility for data defects, operational exceptions, outcome review and changes, distinguishing proposed roles from confirmed owners.
- A validation step and conditions for advancing, revising or stopping. An upper-right point does not authorize deployment.

Distinguish six agent dimensions: perception, decision, action, autonomy, adaptation and knowledge. Choose functions for the task; do not assume every use case needs an agent or maximum autonomy.

Defend concerns individual-work improvement, Extend team/process change, and Upend a strategic bet on new value or markets. The category does not guarantee ROI, risk, cost or success. A portfolio need not contain all three.

## Write and render

Write directly in English by default, including headings, captions and diagram labels; set `language` to `en`. Use another language or bilingual output only when explicitly requested. State company facts and proposed actions in affirmative, concrete sentences. Preserve uncertainty through explicit conditions. Keep research history, abandoned hypotheses, chart construction and missing-score explanations in separate records; explain the actual work and the information needed to decide in the reader-facing page.

Write company-specific investment judgments in connected prose: actual disclosed activity, evidence, proposed improvement and the information needed to decide. Do not use a mandatory Why/Example teaching format or fill missing evidence with generic hypothetical cases. Preserve the seven analytical lenses while letting the company's decision determine the headings. Use capability names in the narrative and keep IDs in the structured data. Supplementary Mermaid diagrams may clarify actual dependencies, responsibilities or authority; use prose rather than tables.

For a full investment brief, deliver `investment-options.html`, `readiness.html` and `research-opportunities.html`, with shared navigation to each other and `index.html`; unknown scores do not waive these pages. Generate the research page through the preprint process below. Save `portfolio.json` internally under `records/model/` using the contract; do not create additional Markdown deliverables or Markdown/JSON download links unless explicitly requested. `scripts/render_radar.py` plots supported value/feasibility pairs and retains unscored candidates in the page. `scripts/render_readiness.py` displays separate current/target marks, so missing values do not create a fictitious polygon. When all relevant scores are unknown, the renderers show the work and requirements without an empty chart. Optional readiness `title` fields can state concrete conditions. Both render source links and human-readable capability and dependency names while retaining IDs in internal JSON and link anchors.

For the narrative brief and capability map, use `bcm-creator` or the user's existing format. Verify source scope, dependency links, uncertainty, plotted counts, missing-score behavior and actual output. Preserve the raw result when the user requests an independent trial; do not silently polish it before review.

## Make the comparison testable

For each proposed success measure, specify the task, eligible denominator and observation window. State how repeats, unresolved cases, abandonment and justified refusals count when relevant. A correct referral or refusal measures handling quality; it does not establish the user's completed outcome.

Compare AI and process alternatives on the same outcome and population, including human review, rework and recurring data maintenance. Treat an uncontrolled before/after change as provisional evidence and consider changes in demand, staffing or task mix before attributing improvement to AI. Use a bounded comparison appropriate to the decision rather than prescribing a new research project.

Keep pilot order separate from investment priority. For a recommendation, identify the evidence supporting the preference, the missing dependency and the result that would reverse it. Feasibility ratings and capability-map case studies support hypotheses about use; they do not establish realized returns.

## Draft, review and repair the explanations

Before drafting, read [the complete-explanation and revision process](references/explain-and-revise.md). Apply it to each option and readiness condition, including expandable details. After drafting, identify what an unfamiliar reader would have to infer, repair those passages, and review the complete text again before delivery. Keep actual revisions in the internal clarity record.

## Recommended companion skills when available

Check the current skill catalog and prefer using these companions when available:

- **`no-ai-slop`**: Before drafting, read its writing principles to guide the initial prose; this supplies writing context and does not require a user-provided draft. After the first complete draft, apply its editing workflow and evaluation checks. Preserve necessary explanations, factual limits and passage citations while removing abstract wording, tangled sentences and unnecessary material. Treat initial writing guidance and later editing as separate uses.
- **`academic-research-suite`**: When the task involves scholarly literature, research-method review or citation verification, use the matching workflow. Load only the instructions needed for that work.

Read the selected skill's instructions rather than applying its name as a label. Preserve the confirmed task scope and HTML deliverables. If a companion is unavailable, continue with this skill's existing methods without requiring installation. Record which companions were actually applied and their resulting changes in the internal review record.

## Investigate preprint investment leads

For full investment briefs or requested research-opportunity lists, follow [the arXiv discovery and comparison process](references/preprint-opportunities.md). Start from mapped work and examine what a method could improve. Preserve exact queries, search limits, unsuitable papers and evidence gaps. Present the paper inventory as a plain HTML comparison table, with reading leads distinguished from investment recommendations.
