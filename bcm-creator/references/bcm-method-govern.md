# How to Use a BCM: use-case evaluation, readiness, value streams, and ongoing governance

> The companion reference `bcm-method-howto.md` teaches "how to draw a BCM." This one teaches "how to use it and how to keep it alive once it's drawn" — because a BCM is not a document you draw once and file away, it's an **ongoing governance backbone.** The method comes from note 1 (the source Gartner BCM webinar).

## 0. Drawing it isn't the finish line, it's the starting line

Once it's drawn, all you have is a base map. The value is in using it as "the unit of conversation for company-wide AI governance." The most common way it dies: the BCM gets built once, filed into SharePoint, and nobody looks at it for three years. **A BCM with no cadence is a dead map.**

## 1. The full chain: Capability → Value Stream → Process → IT system

A BCM lists capabilities only — it says nothing about sequence (like a box of Lego: you have the blocks but don't know which comes first). To operationalize it, connect downward:

- **Value Stream (also a kind of map)**: string capabilities into a flow — "to deliver outcome X, pass through A → B → C in order"; each capability on the flow has a KPI, an input, an output, and a dependency. **The BCM is the box; the value stream is the arrow.** You usually start from the BCM's L2–3 (L1 is too abstract to sequence).
- **Process**: on a given value stream, how this capability actually runs.
- **IT system**: the process maps further down to applications, data sources, and integrations.

Each layer aligns to the one above. Building a process model before the BCM is solid = building a house starting from the middle floor.

## 2. Digital Thread: making data governance = business governance

Map the value stream onto the data flow — every capability transition carries a transformation and movement of data. Follow it all the way: the "customer places an order" value stream triggers which table updates, which system calls, which model predictions. **A digital thread makes "data governance" and "business governance" the same thing, not two parallel lines.**

## 3. One metadata card per capability (the real unit of governance)

A BCM is more than boxes. Each capability gets one card beneath it: **definition / responsible owner (single) / data input / data output / supporting systems.** A BCM with no metadata filled in is a decoration; fill it in and it can drive investment decisions, accountability, and cross-team communication.

(These are exactly the four columns marked "TBD" in the bcm-creator input brief — owner / systems / data in-out are non-public and the organization has to fill them in itself. The input brief fills in the public half and leaves the slots ready for the internal data.)

## 4. Data readiness is contextual

Readiness isn't "zero errors in the data," it's "what does each capability need from data, and does our structure support it?" Rated on a 1–5 scale. **The same dataset may be level 5 for capability A and level 2 for capability B.** A company that waits for data to be 100% clean before starting AI investment will never start.

## 5. BCM × use case: pin AI on capabilities (Opportunity Radar)

With a BCM in hand, map your AI use cases onto it (the **AI Opportunity Radar**, four quadrants: core capability / back office / product & services / front office). **Pin on the capability, not on the use case itself** — a use case goes stale in six months, a capability holds for three to five years. You see at a glance where investment is concentrated, what's being ignored, and whether the portfolio is balanced.

## 6. Break every use case into 6 agent dimensions

To evaluate a use case's — or a vendor's — agent, break it into 6 dimensions: **Perception (see / hear / read), Decisioning, Actioning, Agency (degree of autonomy), Adaptability, Knowledge (knowledge access).** Most use cases only need 2–3 of these to be strong. Evaluating against these 6 dimensions is ten times more reliable than listening to a vendor say "we have agentic AI."

## 7. Agency warning: a wrong autonomous decision spreads

Agency is a 5-level spectrum, not an on/off switch. **Level 1 fully autonomous is science fiction in most industries** — an end-to-end value chain is too complex, and any single wrong autonomous decision spreads. A selective process (a single mechanical action) can be Level 1; end-to-end can't. Most enterprises reasonably stop at Level 3–4, and that's not a failure — it's pragmatism.

## 8. For every use case, get clear on: technology + data sources + integration engineering

A use case is never built with "one AI." Before you sign off or evaluate, get clear on: **which AI technologies + which data sources + which integration engineering** it needs. Not every use case calls for Gen AI — picking wrong doesn't just waste money, it injects probabilistic behaviour into a deterministic process and ends up less accurate than the old system. Skip this clarity and the POC runs but production won't.

## 9. AI Readiness (7 dimensions, read the gap not the score)

Before starting, assess readiness across 7 dimensions: **Strategy / Value / Organization / People & Culture / Governance / AI Engineering / AI Data**, each 1–5. **What matters is not the current score, it's the gap between current and future.** Most organizations mistake readiness for just two dimensions — "talent + data" — and overlook Strategy and Governance, which is the main reason they can't scale later. Future state is usually overestimated; it needs a case to back it, not a gut call. If you can't find a single example proving your vision is feasible, that's not a vision, it's a hallucination.

## 10. Tag every use case Defend / Extend / Upend (yes, really)

Yes, you tag the AI business case with one of these three:

- **Defend**: augment existing staff without changing the process structure; ROI is steady and easy to compute (AI writing code / JDs / copy). Low risk, low ceiling.
- **Extend**: rewrite the process, with a vendor-packaged solution and computable ROI (customer-service automation, insurance claims auto-approval). The enterprise main battlefield.
- **Upend**: the frontier, where even whether the value exists is uncertain (drug discovery). High risk, high return, needs patience capital.

A healthy portfolio mixes all three — bet everything on Defend and you have no differentiation in three years; bet everything on Upend and you burn through your cash.

## 11. AI strategy ≠ a subset of IT strategy

AI's impact on the business model and the operating model runs too deep — it needs **independent planning.** A company with no AI strategy loses competitiveness; but a company with a **bad AI strategy gets actively hurt** (compliance, trust, customer experience). The BCM is the base map that carries the AI strategy.

## 12. Bimodal: top-down meets bottom-up (the real reason POCs fail)

- **Top-down (led by leadership)**: BCM, use-case prioritization, readiness assessment — strategic moves.
- **Bottom-up (built hands-on by teams)**: POC, prototype, end-user pilot — operational moves.

Both run at the same time, that's the point. **Many teams' POCs fail not because they couldn't build them, but because they were never connected to the BCM**: the POC goes live and then nobody keeps tracking it, and three months later nobody remembers where the KPI was set — because the KPI was never hung on any capability. The BCM is the pin that fastens the POC to the organization's backbone; top-down alone is PowerPoint governance, bottom-up alone is a headless chicken.

## 13. The workflow for updating a BCM (cadence)

A BCM is an ongoing governance backbone — **put it on the calendar and revisit it every quarter or every six months.** One review runs through these steps:

1. **Re-rate pace** — is each capability's pace against the main objective still right? Was something keep up last year that every competitor has now gone AI on → promote to differentiating?
2. **Use-case status** — has a use case on the radar moved from a calculated risk to a likely win (feasibility has matured)?
3. **Readiness gap** — which capabilities' data / AI readiness improved, and which gaps closed?
4. **Connect the POCs (the most commonly missed step)** — pin each POC that ran back to its corresponding capability + KPI; are the ones that went live still being tracked? Flag the untracked ones red.
5. **Update metadata** — did the owner change? Did the supporting systems change? Did data readiness change?
6. **Add / retire** — has a new business model brought out a new capability? Which capability has become a commodity (and should be outsourced)?
7. **Regenerate the input brief + image** — if the data changed, re-run bcm-creator to update the input brief and the image, tagging the version and date.

AI keeps changing, and a frozen BCM won't survive a year.

## The aha

What a BCM is really doing is pulling AI back from "one PoC in the IT department" to "company-wide strategic governance." A process map is too detailed, a product roadmap too narrow, a project plan too short — only the BCM is at once "abstract enough for the C-level to understand," "concrete enough to attach investment to," and "stable enough to carry a multi-year conversation." It doesn't replace your existing tools; it's the thread that strings them together. Without that thread, AI investment is forever a collection of island POCs; with it, AI investment is the compound growth of organizational capability.
