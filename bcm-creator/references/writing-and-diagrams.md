# Company analysis and capability images

Write an investment analysis of the named company. Preserve the capability → objective → evidence → gap → option → validation logic, but do not turn that reasoning into a lecture about the method.

## Make the company the subject

Use headings that state a judgment about the company, followed by connected paragraphs. Ground them in the company's actual products, services, systems, disclosed activities and constraints. Explain how those facts affect the investment decision, and distinguish the proposed action from an existing company practice.

Lead with the company and its work in affirmative sentences. Turn counterexamples into the final judgment: an existing tool changes what the proposed investment must improve. Keep the research sequence, abandoned hypotheses and map-production choices in separate records. Captions explain how to read the image; they do not recount how it was made. State missing evidence as a concrete decision condition rather than repeating that the report cannot prove, score or authorize something.

The seven lenses guide analytical coverage; they are not seven mandatory teaching chapters. A section may address several lenses. Do not impose Why/Example labels or two-sentence quotas. Do not add hypothetical machines, parts shortages or imaginary company events to fill a template. Missing internal evidence should become a precise unanswered question or next investigation, not a generic example.

Use full capability names in the reading text. Stable IDs are useful in JSON and source links, but a reader should not need to decode C07 or A1 to understand a conclusion. Keep operational detail only where it changes the decision. Put the capability register behind the main analysis rather than repeating it throughout the report.

## Natural Traditional Chinese

Read [the native writing and translation rules](chinese-writing.md) before drafting or revising Chinese prose. Apply them to headings, captions, objectives, candidate descriptions and readiness notes as well as the main narrative. Explain technical terms through the actual work, preserve certainty and conditions, and use paragraphs or short useful lists without tables by default.

## Generate the capability-map image

Read [the stable image workflow](capability-map-visuals.md). Use the bundled reference image and shared style specification, then derive exact labels, grouping and colors with `scripts/prepare_map_image.py`. For a reference adaptation, pass the actual image to the tool after viewing it; prose-only descriptions are not equivalent. Keep visual decisions consistent across companies while letting the company model determine the content.

The principal visual is a generated raster image. Use the user's reference for composition, not for copying another company's capabilities. Organize compact rectangular capability cells inside labeled domain panels; distinguish value-realizing and enabling regions when that distinction aids this decision. Favor a landscape canvas, thin borders, aligned spacing, readable labels and a restrained color legend. Match the supplied reference's typography and palette. Do not fill empty space with unsupported capabilities.

Lock the approved capability names, group membership and objective-specific colors before image generation. Supply the image tool with the exact labels and explicit counts. Save its actual output PNG in the project, then inspect every label and assessment against the structured model. Correct missing, duplicated or misspelled labels with the image tool. Keep the prompt and generation provenance with the artifact. Do not use a Mermaid screenshot as a substitute for the generated capability image.

Color expresses assessment under a stated objective; it does not establish maturity, budget or company approval. Include this limit briefly in the caption. Keep the full-size image accessible from the HTML reading page.

## Supplementary diagrams

Mermaid can explain an execution handoff, data dependency, investment sequence or authority boundary beside the relevant company analysis. Label proposed relationships as proposals and known activities as disclosures. Arrows must mean a stated process, dependency or feedback relationship. Do not require a diagram where prose is clearer, and do not replace the primary capability image with a flowchart. Inspect the actual rendered diagrams for clipping, excessive height and readable labels.
