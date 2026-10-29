---
name: bcm-creator
description: Build or revise a Business Capability Map and use it to reason about business or AI investment. Organize evidence under capabilities and explain execution, ownership, data needs, scope and autonomy. Use for BCMs, capability models and capability-based investment briefs; not lecture transcription or org charts.
---

# BCM Creator

A capability name gives related knowledge a common home. Bring equipment records, people, working practices, data and proposed tools together under the work the business must perform; then ask which improvement could help the chosen outcome. The map supports that judgment. It does not decide the investment.

Read [the modeling method](references/bcm-method-howto.md) before deriving capabilities. For an investment brief, also read [the seven decision lenses](references/bcm-method-govern.md) and [the writing and diagram guide](references/writing-and-diagrams.md). Before writing or translating Traditional Chinese, read [the native writing and translation rules](references/chinese-writing.md). Use [the output contract](references/output-contract.md) for deliverables. These references are self-contained; no prior conversation, private notes or other writing skill is required.

## Establish the decision

For a new company analysis or investment assessment, begin with [the structured interactive intake](references/interactive-intake.md) before external research. Ask in small rounds about the decision, scope and evidence the user can directly provide, then selectively explore the seven lenses. Reuse existing answers and offer an explicit skip path. If the user skips, record provisional scope and material gaps, then research them through competing explanations and counterexamples. Do not interpret silence as a skip. Pure prose revisions reuse the established scope without restarting intake.

Use the user's company, viewpoint, scope, objective, period and language. Respect an explicitly selected business unit or goal. When only a company is named, begin with a provisional view of its businesses, customers and shared capabilities; keep gaps visible. A detailed product page can support a local case but cannot by itself establish the company's investment priority. Do not settle on a business unit or objective because it is easy to research.

Treat each source as a partial view shaped by its purpose, audience, scope and date. Prefer primary evidence for disclosed facts; use other relevant perspectives to test interpretation. Separate a source's facts from its explanation of causes or claimed importance. Repeated coverage of one announcement is not independent corroboration, and search ranking or source volume is not business significance.

Form tentative explanations, then seek actual counterexamples: a material business omitted from the map, a capability that crosses the proposed boundary, an existing feature that contradicts a supposed gap, or an outcome that does not follow from the proposed improvement. Let these challenges direct the next search. Do not immediately fill every empty field or gather more supporting material for the first plausible story. Read [the counterexample method](references/bcm-method-howto.md#revise-the-model-through-counterexamples) before narrowing a broad company request.

Revise the boundary, causal claim or priority when the evidence warrants it. A hypothetical failure condition is a question to investigate, not an observed counterexample; failing to find a counterexample does not prove the hypothesis. Combine partial evidence into a qualified model without forcing disagreements to disappear. Distinguish what is worth researching, what is feasible to pilot and what deserves business investment. If the evidence cannot choose among objectives, retain conditional alternatives rather than manufacture a winner.

Use supplied internal evidence when available, retaining each document's actual business, time and usage scope. Record URLs, dates, units and denominators; distinguish disclosures, estimates, inference and unknowns. Propose a working objective only after the intake and scope check. Present its company-specific basis and conditional alternatives as direct judgments; label proposed goals as recommendations. Keep the history of choosing and revising them in the research record. After intake, ask targeted follow-ups only when a material ambiguity changes the decision; otherwise deliver the provisional map and bounded judgments.

## Organize evidence by capability

1. Identify the work the organization must perform within the current, explicitly provisional scope. Name capabilities at a comparable level and define what each includes. Keep the model revisable when counterexamples expose omitted work or a poor boundary. A capability may exist, be outsourced, be proposed or remain unverified; having a box does not prove it exists today.
2. Group related capabilities into useful domains. Check for missing work against accessible industry models when relevant. A process taxonomy is a completeness aid, not a ready-made capability map; do not claim to have consulted an unavailable proprietary template.
3. Attach evidence, people, systems and data to stable capability IDs. The same equipment or dataset may support several capabilities. Distinguish outcomes, process steps, organizations and technologies from capabilities.
4. Decompose where it helps answer the decision: differences in outcomes, responsibility, evidence or improvement needs may justify L2/L3 detail. There is no mandatory box count, child count or universal depth limit.
5. Explain which capabilities realize the selected value and which enable others. Enabling work can be essential, but its cost and scope still need justification.

## Apply the investment logic

For a full AI investment brief, use all seven lenses to reach company-specific judgments. They are analytical questions, not a lecture-note template: write the company's actual situation, supporting evidence, investment implication and remaining uncertainty in connected prose. Do not impose Why/Example labels, sentence counts, invented factory stories or seven repetitive teaching chapters. Where evidence is missing, name the exact missing company information rather than filling the gap with a hypothetical example.

- **Can the work execute?** Trace data → usable judgment → workflow handoff → authorized action → outcome. Locate the missing link, not just whether a demo works.
- **Who sustains it?** Establish responsibility for data, operations, outcome review and changes. Distinguish proposed roles from confirmed owners; account for time, authority and recurring cost.
- **What decision changed?** Keep the capability base stable while showing how objectives, measures, period or constraints change evidence and priorities.
- **Maintain, monitor or innovate?** Tie attention to a specific objective and rationale. Commodity still needs maintenance; keep-up needs indicators and responses; differentiating needs an improvement hypothesis and validation. These are not maturity levels, budget percentages or instructions to buy AI.
- **What data makes this task possible?** Specify the judgment, inputs and outcomes, timing, access, linkage, production availability and responsibility. Do not impose universal labeled-data requirements or wait for all enterprise data to be clean.
- **Which part actually needs improvement?** Separate detection, decision, action and confirmation. An alert does not establish end-to-end autonomy. Compare a process or non-AI alternative when it addresses the same bottleneck.
- **How much authority is appropriate?** Separate function, permission and technical performance. Describe human veto and notification arrangements. Use the webinar's numbered levels only when explicitly explaining that source; otherwise describe permission directly.

The lenses are detailed in `bcm-method-govern.md`. Preserve unknowns and conditional recommendations. Do not invent internal readiness scores, cost savings, budget shares or approved autonomy to complete a visual.

## Produce a reviewable result

Deliver an HTML reading page that prominently displays the generated capability-map image. Keep `bcm.json` and other structured authoring data under internal `records/model/`; image files remain page assets. Do not additionally deliver Markdown or JSON downloads, or add their links to navigation, unless explicitly requested. This is an analysis of the named company. Use its actual products, disclosed systems, operating activities and constraints throughout; a paragraph that fits any factory without substantive change needs more research or a narrower claim. Use capability names in prose; keep IDs for internal cross-references and structured data. Do not use tables by default.

Write affirmative, concrete sentences about the company, the work and its consequences. Preserve uncertainty with explicit conditions and proposed actions. Present the conclusions reached through counterexamples; keep the search history, withdrawn hypotheses, map-making decisions and explanations of missing scores in separate records. Explain unfamiliar terms in ordinary language, and keep raw schema fields out of the reading page.

Generate the map with an available image-generation tool after verifying labels, grouping and assessments. Read [the stable image workflow](references/capability-map-visuals.md): it includes the user's reference PNG, a shared style specification and `scripts/prepare_map_image.py` for exact image inputs. View and pass the actual reference when adapting it; retain the fixed visual grammar across companies. Save the actual PNG in the deliverable directory and inspect every label, duplicate, omission and color against the JSON. Use focused image edits to correct defects, and record actual reference use and validation. Do not substitute a Mermaid screenshot for a requested generated image or infer provenance from file size. If generation is unavailable, disclose that limitation rather than calling a different artifact generated.

Use `scripts/render_bcm_input_html.py` with the v3 contract to embed the saved image and render the company analysis. Resolve paths relative to this skill directory. Mermaid remains useful for supplementary workflows, dependencies or authority boundaries when they clarify an actual company decision; it is not the primary capability-map deliverable. A local bundle passed with `--mermaid-js` makes those supplementary diagrams work offline.

The map groups capabilities; arrows belong in supplementary workflows. Colors express an objective-specific assessment, not an assertion that the company has approved the investment or deployed an AI feature. Avoid filling the map with extra generic boxes just to match the density of a reference image.

For portfolio positioning, value/feasibility or readiness, use the companion `ai-opportunity-radar` skill. Do not force numerical charts into an unscored public-data brief.

## Verify

Check why this objective and boundary were chosen before checking objective → capability → evidence → gap → option → validation. Verify that a material counterexample or competing explanation changed or limited the judgment; retain the revision history in the research record. The reader should see the resulting company facts, causal explanation and recommendation, not a narration of the analysis process. Confirm source scope and certainty; proposed owners, scores and targets must not silently become facts. Check all seven lenses on an investment brief, capability IDs, links, Mermaid syntax, visible labels and the actual reading page. Read headings and opening sentences for clarity as well as checking structure.
