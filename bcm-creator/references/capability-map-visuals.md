# Stable capability-map images

Read this guide when producing or revising the main map. The bundled [reference image](../assets/capability-map-reference.png) is the user's latest supplied visual example, saved on 2026-10-29. Its nested rectangles and restrained palette guide the composition; its company, title, domain names, capability names and assessments are not evidence about the subject company. The [style specification](../assets/capability-map-style.json) preserves its compact architecture-map design at a readable resolution.

Keep the reference's compact heading, restrained orange accent, small legend, thin domain borders and individual capability rectangles. Apply the user's current layout preference: a 16:9 landscape canvas, with capability rows stacked vertically inside EVERY domain on BOTH sides. Each row contains one capability; text remains horizontal. Value-realizing domain panels form a compact grid on the left, and value-enabling domain panels stack on the right. Put both region labels above their panels. This updated layout takes precedence over the reference image's horizontal rows on the right. Keep the actual company grouping and assessments, readable labels and modest row heights; a sparse map uses balanced spacing instead of invented capabilities.

## Lock content and appearance separately

Finish the company model and objective assessment first. Then run:

```sh
python3 scripts/prepare_map_image.py /path/bcm.json --output-dir /path/output/records/map
```

The helper creates `map-content.json` and `map-prompt.txt`. It derives every capability, group and cell color from the JSON, and checks duplicate IDs, ambiguous group roles and conflicting assessments. A base map without `map_objective_id` has a neutral palette and no investment legend. Unknown assessments under a selected objective remain visibly unknown. The helper prepares inputs; it does not generate or verify an image.

Use the same style specification for every company in a comparable series. It fixes a 16:9 landscape aspect ratio, title and label hierarchy, two labeled regions, panel treatment, spacing and color meanings. Group and capability counts follow the company model. For a sparse map, use fewer columns; for a genuinely dense map, increase the canvas proportionally before reducing text size. Record any layout adjustment. Do not add capabilities to fill a template or shorten a capability into a different meaning.

## Adapt the actual reference image

Inspect the bundled PNG with the available image viewer. When adapting this reference into a company's map, give the actual local image to the image tool as the edit target, together with `map-prompt.txt`; preserve its visual grammar while replacing all business content. For the built-in tool, use `referenced_image_paths` after viewing the local file. Do not claim that a reference was supplied when it was only described in prose. Follow the actual tool's current interface; never invent seed, size or fidelity arguments. The dimensions in the prompt are requested design dimensions, not a guarantee about the saved file.

If the user requests a fresh design without a reference, use generation mode and its supported arguments instead. If a tool cannot accept the local reference, record that limitation and do not describe the result as a direct reference adaptation. Do not silently replace the user's requested generated PNG with HTML or a Mermaid screenshot.

When replacing an unwanted visual style, use the new reference alone as the image input and take exact company content from the JSON. An old company map can be checked separately, but including its rejected layout as another visual input can pull the result back toward that style. The reusable [prompt template](map-image-prompt.txt) follows this reference-only adaptation.

Retain the reference and style specification with the skill, so a new agent has the same visual input without reading prior conversations. For later corrections, edit the generated company map itself and state the exact labels, colors or spacing to change. Preserve the verified regions. Avoid generating a wholly new layout to fix a local typo.

## Inspect the saved result

Compare the image against `map-content.json`: every capability appears exactly once in its own separately bordered cell within the assigned domain, all text is readable, cell colors match the selected objective, and the title and legend are correct. Check the actual full-size image and its embedded reading-page view. Check that both regions use one capability per row, stacked vertically within each domain, and that the whole image is 16:9. Check the reference for restrained typography, borders and colors; its older horizontal cell layout is superseded. A reference improves consistency; it does not eliminate text or layout errors.

Use focused image edits for material errors, then inspect the full result again. After two unsuccessful correction attempts for the same defect, keep the last output marked as needing review in the delivery record and explain the specific limitation. Do not claim a verified map while known errors remain, silently change the JSON to match a mistaken image, or switch production methods without the user's agreement.

Keep `generation-record.json` beside the prompt with the tool name, actual mode and reference arguments, reference and content hashes, returned image path, copied project path, actual dimensions, iterations, validation findings and remaining issues. Record only actions that occurred. Production details stay in these records; the reader-facing caption explains the business scope and color meanings.
