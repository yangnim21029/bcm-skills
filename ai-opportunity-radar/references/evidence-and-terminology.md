# Preserve context in claims, citations and terminology

Read this before drafting or revising a source-backed brief. Simple language must preserve the subject, task, population, time, qualifiers and surrounding argument.

## Establish passage-level evidence

Read the relevant original paragraph and its surrounding section, including qualifications, linked definitions and figure or table notes when material. Search snippets and another author's summary are discovery aids. Preserve a retrieved snapshot and date.

Attach a citation immediately to the clause it supports. Split a sentence when its claims have different support. Distinguish disclosed practice, attributed claims, cross-source inference and proposed action in the wording. Several adjacent citations do not establish agreement or support a new causal claim. Keep a recommendation separate from the source-backed fact that motivates it.

For each cited passage record its source, heading and paragraph/list/table locator, a short exact excerpt, original-language wording, context, interpretation boundary, original URL and retrieval date. Use a stable section link or text fragment when available; retain a locator and snapshot when deep links are unreliable. A local paragraph number must be identified as snapshot-local. Respect quotation limits; linking to a full paragraph does not require reproducing it. Mark translations and never pass a paraphrase off as a quotation.

The existing source-level evidence lists remain useful for navigation. Add `sources[].passages` entries and place `[[S03:P1]]` directly in supported prose. Each entry has `id`, `locator`, `excerpt`, `context`, `limits`, `url`, `retrieved_at`, and optional `language` and `snapshot`. The renderers expose the passage behind an inline link. Software verifies references and escaping; the author must verify semantic support.

## Synthesize meanings after collecting context

Before final drafting, write a short internal `records/context-synthesis.md`; update it when new evidence changes a meaning or boundary. Reuse it across the report and reread it after a context handoff. Keep it separate from reader deliverables.

Organize by contested concepts and consequential relationships, not one summary per source. For each ambiguous term retain a preferred report label, variants, source-specific meanings and passage IDs, scope and time, distinctions that must remain separate, and unresolved conflicts. Distinguish equivalence from broader/narrower or merely related senses. Record which definitions are local analytical choices. Name what evidence would change them.

This is working terminology control, not a new external authority. It cannot overwrite source language, suppress disagreement or turn frequent wording into a consensus. Reopen source passages when the synthesis is insufficient; do not cite the synthesis as primary evidence.

## Check before delivery

Read each claim with its cited passage and context. Check that simplification has not enlarged the population, changed the actor, converted a plan into completion, promoted availability to performance, or merged distinct meanings of validation, access, outcome or value. Inspect the rendered inline link and original-passage route. Preserve substantive qualifiers in visible prose; footnotes cannot repair a misleading sentence.

## Compact reference presentation

Use small superscript document numbers in prose and a compact numbered reference list at the end. Keep source order consistent across the report. Retain stable source and passage IDs internally. Clicking a citation must reveal its original excerpt, locator, context, limits and original URL; collapse this detail by default. A shared document number must preserve every cited passage. Keep exact quotations unchanged, including punctuation. Citation size is a presentation choice, not permission to remove evidence or shorten necessary explanations.
