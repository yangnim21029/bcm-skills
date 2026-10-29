# BCM Skills — capability-based investment reasoning

Two portable skills for Codex and other Agent Skills hosts. Start with what an organization needs to do, collect related evidence under capability names, then judge which improvements could help a clearly stated outcome.

`bcm-creator` builds the capability map and a sourced investment brief. `ai-opportunity-radar` assesses options, portfolio concentration and readiness. The method is informed by Alexander Hoeppe's Gartner webinar “Accelerate Your AI Journey With Business Capability Maps”; these skills are independent interpretations, not official Gartner templates.

## What the revised method changes

A map organizes knowledge for a decision. Equipment, people, systems and AI proposals link to capabilities; a capability label alone proves neither that the organization has the full capability nor that an investment is worthwhile.

New analyses begin with a short, structured conversation about the decision, scope and materials the user can directly provide. Ask in small rounds, reuse existing answers and let the user explicitly skip. The [intake guide](bcm-creator/references/interactive-intake.md) connects questions to the seven decision lenses and records answers, material scope and unresolved gaps. Both skills include the same portable guide; moving between them does not restart the interview. Prose-only edits reuse the established scope.

Research then begins with a provisional view. Each source reveals a partial perspective; detailed product documentation must not choose the company's investment priority. Seek actual counterexamples to the current boundary, alleged gap or causal claim, then let those findings direct further inquiry and revision. Unknowns can remain open. The final priorities are synthesized from evidence and counterexamples rather than inherited from the initial view. Do not replace this reasoning with an exhaustive information checklist or treat an easy local pilot as the most important business investment.

An AI investment brief addresses seven questions in the actual analysis: can the work execute, who sustains it, how the decision changes with the objective, what to maintain/monitor/innovate, which data makes the task possible, which part really needs improvement, and how human veto/notification should work. These questions shape company-specific investment judgments in connected prose. They do not impose a Why/Example teaching format or generic hypothetical scenarios. Use no tables by default.

Both skills include Traditional Chinese writing and translation rules. The reading page states company facts, proposed actions, mechanisms and validation conditions in clear affirmative sentences. Counterexamples shape the conclusions; research history and production details remain in separate records. The writing rules preserve uncertainty while replacing abstract terms and English sentence patterns with concrete, natural Chinese.

Colors express attention under a selected objective. They do not prescribe budget percentages, equate differentiation with buying AI or exempt commodity capabilities from maintenance. A capability base map, a workflow, an opportunity radar, a value/feasibility matrix and a readiness assessment answer different questions.

Unknown internal information remains unknown. Public disclosures, analyst inferences and proposed goals/roles stay distinguishable. Scores are optional; renderers retain unscored options instead of fabricating coordinates.

## Local use

For Codex, copy or symlink both skill directories into a project `.agents/skills/` or your `~/.agents/skills/`. Codex supports local skill directories and symlinks; see the [official skill documentation](https://learn.chatgpt.com/docs/build-skills). For Claude Code, the same directories can be installed under its configured skill location.

```sh
mkdir -p .agents/skills
cp -R /path/to/bcm-skills/bcm-creator .agents/skills/
cp -R /path/to/bcm-skills/ai-opportunity-radar .agents/skills/
```

Example requests:

- “Use $bcm-creator to map this company and assess where AI could improve the selected business outcome.”
- “Use $ai-opportunity-radar to compare these options; keep unsupported readiness and value scores unknown.”

No private transcript, special sibling writing skill or external subagent is required. An image-generation tool is needed for the primary capability-map PNG. Research real organizations with current primary sources; supplied evidence can support an offline analysis. An independent test should receive the skill, task and necessary raw inputs, without the author's answer or conversation history.

## Outputs and tools

The v3 BCM contract delivers an HTML reading page with its generated capability-map image. Structured models stay under internal `records/model/`; additional Markdown or JSON downloads are created only when explicitly requested. Capabilities have stable IDs; objective-specific overlays remain separate. The [image workflow](bcm-creator/references/capability-map-visuals.md) bundles the user's visual reference, a shared layout and typography specification, and a helper that prepares exact labels and colors. Adapt the actual reference image, inspect the saved result and correct local defects without replacing the whole design. Set `map_image` to its relative path. Mermaid is reserved for useful supplementary diagrams.

```sh
python3 bcm-creator/scripts/prepare_map_image.py bcm.json --output-dir records/map
python3 bcm-creator/scripts/render_bcm_input_html.py bcm.json bcm.html --mermaid-js /path/mermaid.min.js
python3 ai-opportunity-radar/scripts/render_radar.py portfolio.json matrix.html
python3 ai-opportunity-radar/scripts/render_readiness.py portfolio.json readiness.html
```

Python renderers use the standard library. The BCM page embeds a local Mermaid bundle when supplied; otherwise it discloses and uses a CDN. The portfolio pages use inline SVG and work offline. The historical filename `render_radar.py` now explicitly labels its output a value/feasibility matrix; strategic opportunity positioning is a separate categorical diagram.

Small fictional specs in `references/` illustrate the contracts. They replace the previous TSMC answer examples so a TSMC trial need not reuse a completed answer. The schema fixtures require their image to be generated before a CLI render. Existing v2 BCM specs need a generated image and company-analysis paragraphs in place of the Why/Example fields; seven-lens coverage remains, without a mandatory chapter count.

## Validation and provenance

Run `python3 -m unittest discover -s tests` to check meaningful rendering behavior: missing scores remain missing, invalid ranges and dependencies fail, input text is escaped, and outputs preserve the requested structure. Inspect actual diagrams and source support as well; structural validation does not prove the investment judgment.

The references distinguish source claims from interpretation, including the webinar's source-specific autonomy numbering. The instructions are original adaptations; the visual reference was supplied by the user and guides composition only. No new license is implied by this revision.
