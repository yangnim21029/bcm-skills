# BCM output contract · version 3

One internal UTF-8 JSON holds the capability model and company analysis. Store it under `records/model/`; deliver the HTML reading page and its required image assets. Markdown and JSON downloads are provided only when explicitly requested. Version 3 changes presentation; the investment reasoning remains capability → objective → evidence → gap → option → validation.

For a new analysis, keep the [interactive intake record](interactive-intake.md#問答紀錄與完成條件) beside the research records. Preserve user-specified scope, material usage limits and explicit skips there. The reading page presents the resulting business scope and conditions, not the interview transcript. Rewriting an existing report does not imply that a new intake or scope review occurred.

## Required fields

- `schema_version`: `3`.
- `mode`: `map` or `investment`.
- `company`, `as_of`, `language`, `viewpoint`, `decision_context`.
- `context`: paragraph or list of short paragraphs about the company's business, relevant constraints and the outcome worth improving. Give the final factual basis and conditional alternatives directly. Counterexamples should shape these conclusions; keep the history of discovering them or revising the map in a separate research record. A company-only request must not silently become the best-documented product's investment case. Follow the writing guide for reader-facing language.
- `map_image`: relative PNG/JPEG/WebP path from the HTML output directory; generate this file before rendering. `map_alt`: concise description. `map_caption`: scope and meaning of colors. Optional `map_generation` records tool, prompt file and provenance.
- `objectives`: unique `id`, `name`, `kpi`, `status` and source IDs in `evidence`. Distinguish analyst-proposed goals from approved company targets.
- `capabilities`: unique `id`, `name`, `level`, `domain`, `role` (`realizing` or `enabling`), `definition`, `status`, `evidence`. Optional `kpi`, `owner`, `systems`, `data_inputs`, `data_outputs`, `scope` contain company-specific prose.
- `sources`: unique `id`, `title`, `url`, `date`, `kind`. Optional `perspective`, `scope`, `limitations` and `origin` can record why a claim is partial or shared across sources; they supplement the prose and do not imply independent corroboration.

## Assessments and prose

`overlays`: objects with `capability_id`, `objective_id`, `pace` (`commodity`, `keep_up`, `differentiating`, `unknown`), `reason`, `status`, `evidence`. `map_objective_id` selects the assessment used in the generated image. Missing assessments remain unknown. Image generation must preserve these labels and colors.

If no priority is justified, retain alternative working objectives and omit `map_objective_id` for an unassessed base map. Do not force investment colors or scores to make an unfinished judgment look settled. The provisional map can still support useful conditional analysis.

`analysis`: objects with `id`, `lenses` (a list), `title`, `paragraphs` (nonempty strings), `evidence`. In investment mode the union of `lenses` must cover `execution`, `sustain`, `decision`, `attention`, `data`, `scope`, `autonomy`. This checks analytical coverage without requiring seven chapters. Optional `mermaid` and `diagram_caption` add a supplementary company-specific diagram.

Write actual company facts and judgments in `paragraphs`, not generic examples. Keep unsupported internal conditions explicit. Do not include `why` or `example` fields. Sentence count is determined by the explanation, not a template.

`recommendations`: objects with `title`, `paragraphs`, `evidence`. State the proposed action, its basis and the company information that would change the decision. Optional `notes` records decision-relevant conditions; put generation, tool access and validation details in separate files. Keep IDs and null scores in structured data, and express their business meaning in the reading text.

## Rendering

Generate and inspect the capability PNG first, then run:

```sh
python3 scripts/render_bcm_input_html.py /path/bcm.json /path/index.html --mermaid-js /path/mermaid.min.js
```

The command checks the image path relative to the HTML output and writes only the HTML page by default. Use `--export-sources` only when Markdown and Mermaid authoring exports are explicitly requested. The optional local bundle supports offline supplementary diagrams. Source facts and analysis remain readable without JavaScript.

The fictional JSON fixtures illustrate the schema only; their image path is a placeholder to be generated before a CLI render. They are not company examples to reproduce. A v2 file needs a generated image plus `paragraphs`/`lenses` in place of the lecture-note fields before use with this renderer.
