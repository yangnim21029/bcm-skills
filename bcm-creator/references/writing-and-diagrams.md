# Company analysis and capability images

Write an investment analysis of the named company. Preserve the capability → objective → evidence → gap → option → validation logic, but do not turn that reasoning into a lecture about the method.

## Make the company the subject

Use headings that state a judgment about the company, followed by connected paragraphs. Ground them in the company's actual products, services, systems, disclosed activities and constraints. Explain how those facts affect the investment decision, and distinguish the proposed action from an existing company practice.

Lead with the company and its work in affirmative sentences. Turn counterexamples into the final judgment: an existing tool changes what the proposed investment must improve. Keep the research sequence, abandoned hypotheses and map-production choices in separate records. Captions explain how to read the image; they do not recount how it was made. State missing evidence as a concrete decision condition rather than repeating that the report cannot prove, score or authorize something.

The seven lenses guide analytical coverage; they are not seven mandatory teaching chapters. A section may address several lenses. Do not impose Why/Example labels or two-sentence quotas. Do not add hypothetical machines, parts shortages or imaginary company events to fill a template. Missing internal evidence should become a precise unanswered question or next investigation, not a generic example.

Use full capability names in the reading text. Stable IDs are useful in JSON and source links, but a reader should not need to decode C07 or A1 to understand a conclusion. Keep operational detail only where it changes the decision. Put the capability register behind the main analysis rather than repeating it throughout the report.

## Direct English prose

Draft the report directly in English, including headings, captions, objectives, capability names and diagram labels. A separate translation pass is not part of the default workflow. Explain technical terms through the actual work, preserve certainty and conditions, and use paragraphs or short useful lists without tables by default. Follow an explicitly requested output language when one is supplied.

## Generate the capability-map image

Read [the stable image workflow](capability-map-visuals.md). Use the bundled reference image and shared style specification, then derive exact labels, grouping and colors with `scripts/prepare_map_image.py`. For a reference adaptation, pass the actual image to the tool after viewing it; prose-only descriptions are not equivalent. Keep visual decisions consistent across companies while letting the company model determine the content.

The principal visual is a generated raster image. Use the user's reference for composition, not for copying another company's capabilities. Organize compact rectangular capability cells inside labeled domain panels; distinguish value-realizing and enabling regions when that distinction aids this decision. Favor a landscape canvas, thin borders, aligned spacing, readable labels and a restrained color legend. Match the supplied reference's typography and palette. Do not fill empty space with unsupported capabilities.

Lock the approved capability names, group membership and objective-specific colors before image generation. Supply the image tool with the exact labels and explicit counts. Save its actual output PNG in the project, then inspect every label and assessment against the structured model. Correct missing, duplicated or misspelled labels with the image tool. Keep the prompt and generation provenance with the artifact. Do not use a Mermaid screenshot as a substitute for the generated capability image.

Color expresses assessment under a stated objective; it does not establish maturity, budget or company approval. Include this limit briefly in the caption. Keep the full-size image accessible from the HTML reading page.

## Supplementary diagrams

Mermaid can explain an execution handoff, data dependency, investment sequence or authority boundary beside the relevant company analysis. Label proposed relationships as proposals and known activities as disclosures. Arrows must mean a stated process, dependency or feedback relationship. Do not require a diagram where prose is clearer, and do not replace the primary capability image with a flowchart. Inspect the actual rendered diagrams for clipping, excessive height and readable labels.

## Explain the work before the assessment details

Assume the reader does not know this organization's specialist work. Introduce who does what, the evidenced or suspected obstacle, the proposed change, how that change could improve the outcome, and what would establish its value. Use connected prose, not five repeated labels. Explain unfamiliar capability names through concrete actions and work products. Keep suspected bottlenecks conditional; a disclosed service alone does not establish a failure.

Give the reader enough context to understand the investment judgment before introducing data specifications, role assignments or evaluation formulas. Keep alternatives and constraints that could change the choice visible. Put supporting implementation detail after the explanation or in an expandable block, preserving the full evidence and validation conditions.

Before polishing sentences, read only the headings and opening explanations. Can a reader describe the work, the proposed improvement and why it might be worth funding without opening the technical details? Revise any missing link. Concision alone does not satisfy this check.

For source-backed writing, read [the passage citation and terminology rules](evidence-and-terminology.md) before drafting. Prepare the internal context synthesis, preserve source-specific meanings, and attach citations to the exact claims they support.
