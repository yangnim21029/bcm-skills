# Portfolio JSON · version 2

This is internal authoring data under `records/model/`. Deliver HTML pages; expose Markdown or JSON downloads only when explicitly requested.

For a full investment brief, render this model into both `investment-options.html` and `readiness.html` beside the main `index.html`. Automatically produce `research-opportunities.html` using [the preprint process](preprint-opportunities.md). Add shared relative navigation labeled **Capability & Investment Analysis**, **Investment Options**, **Execution Readiness** and **Research Opportunities**, marking the current page. The renderers do not add this navigation automatically. Verify all four files and links after assembly. Keep scope, objectives, capability IDs and evidence meanings consistent with the main analysis; connect readiness gaps to affected candidates in the prose. Unknown scores retain these pages with qualitative findings. Standalone requests for a specific assessment keep their requested scope.

Top-level fields: `schema_version: 2`, `company`, `as_of`, `objective`, `score_scale`, `use_cases`, `readiness`, optional `language`, `notes` and `sources`. Set `language` to `en` by default; use another language only when explicitly requested. Describe what 1–5 means in `score_scale` when scores are used; when all scores remain null, explain the business information needed to compare options in plain language.

Reuse the [intake record](interactive-intake.md#問答紀錄與完成條件) from capability analysis, or create it for a new standalone assessment. Keep user intent, source scope and unresolved gaps in that record; avoid repeating the interview in the reading page.

Each `use_cases` item has `id`, `name`, `capability_id`, `capability`, `type` (`defend`, `extend`, `upend` or `unclassified`), `value`, `feasibility`, `score_status` (`user_supplied`, `documented`, `estimated` or `unknown`), and `basis`. Scores must be finite numbers in [1,5] or null. Numeric scores require a non-unknown status and a nonempty basis; estimated values require the user's authorization in the task, not simply a renderer flag.

Also include relevant `dependencies` (IDs of other use cases), `data_requirements`, `execution`, `ownership`, `authority`, `validation`, `alternative`, `assessment` and `evidence`. Text fields are prose strings; `dependencies` and `evidence` are lists. `assessment` connects the company's actual disclosed situation to a proposed investment judgment. Do not include teaching-format `why`/`example` fields or generic hypothetical stories. Any proposed owner or unknown internal condition must be labeled at the point of use. The renderer checks structural validity; it cannot verify consent to estimate or factual support.

Each readiness item has `dim`, `current`, `future` (numbers in [1,5] or null), `score_status`, `basis`, and optional `next_action` and `title`. Use `title` for a concrete, company-relevant heading; `dim` remains the stable analytical category. Use a separate item for each of the seven dimensions. Partial knowledge remains visible: known current or target values can be drawn separately; a missing value is never imputed to close a shape.

`render_radar.py portfolio.json investment-options.html` produces a value/feasibility matrix with numbered, hoverable markers and prose candidate descriptions. Candidates missing either score are retained as unscored; they are not assigned coordinates.

`render_readiness.py portfolio.json readiness.html` produces a current/target dot chart and explanatory paragraphs. It does not require a full polygon or a table. Both scripts omit empty numeric charts when all relevant scores are null. Supported numbers show their status and basis; prose uses capability and dependency names rather than raw IDs or schema values. Both validate ranges and dependencies, and avoid automatic “deploy now” zone recommendations.

Sources may be strings or objects with `id`, `title`, `url`, `date`, `kind`, `scope` and `limitations`. Source objects become readable references with link targets for candidate `evidence` IDs. Keep source scope and certainty explicit.

`references/example-portfolio.json` is a fictional demonstration with explicitly illustrative scores and an unscored candidate. It is not permission to estimate a real organization's internal scores.

## Explain each option before its implementation details

Write `assessment` as a self-contained explanation for a reader unfamiliar with the sector: who performs which task, where an evidenced or suspected obstacle occurs, what the proposed change does, why it could improve the outcome, and how to judge whether it is worth the cost. Explain specialist terms through that work. Keep suspected problems conditional and material alternatives visible. A service description establishes activity; it does not establish a bottleneck. Use connected paragraphs; blank lines may separate paragraphs within the string.

These are authoring fields, not a mandatory reading outline. The renderer leads with `assessment` and places the supporting problem statement, data, execution, responsibilities, authority, full validation plan and alternatives in an expandable block. Preserve formulas, denominators, windows and stopping conditions there. Keep sources, prerequisites and numeric-score provenance accessible outside the block. Older models without `assessment` retain their problem and basis as visible context.

Read each option with the details closed. The reader must understand the task, proposed improvement, potential benefit and decision condition. Fix missing explanations before a style-editing pass; a collapsed checklist cannot supply the main argument.

For source-backed prose, read [the passage citation and terminology rules](evidence-and-terminology.md). Reuse the brief's internal context synthesis, preserve distinct meanings, and use passage-level inline citations for factual claims; do not let simplification widen their scope.

For a full brief, set `passage_reference_page` to `index.html` after confirming that the main page renders the same source passages. Companion inline citations then link to that shared reference section, avoiding duplicate quotations. Keep paper-specific passages on `research-opportunities.html`. Omit this field for a standalone assessment.
