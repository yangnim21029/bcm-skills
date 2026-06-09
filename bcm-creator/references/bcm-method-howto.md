# How to Draw a BCM — Walked Through With an Appliance Maker

> The method comes from note 1 (the source Gartner BCM webinar, by Alexander Hoeppe). The worked example is a fictional own-brand appliance manufacturer, "Dingdian" (designs in-house, outsources production, sells under its own brand). Each step draws one real frame and puts the wrong version right next to the correct one.
> Throughout, keep on the four "reading lenses" from note 1's glossary: **perspective, relative altitude, base map vs overlay, and unit purity.** That last one is the heart of this doc — it's where most people (including my own first draft) come undone.

---

## Step 0: First decide which map you're drawing

Dingdian's IT lead hands you two things: a "procurement process diagram" with 14 boxes (requisition → approval → quote request → bid comparison → order → goods receipt → reconciliation → payment), and a "procurement capability" that is a single box: **Procurement Management.**

A BCM wants the latter. The test, in one line: **will "requisition → approval → quote request" change next year?** Yes — bring in AI for quote requests and the bid-comparison step disappears. But "does Dingdian need to procure?" doesn't change in ten years. **The process changes; the capability doesn't,** and a BCM draws the layer that doesn't change.

## Step 1: Pin down "whose map is this"

Before you draw a line, answer one question: **whose** capability map is this? The answer is Dingdian's own. Why pin it first? Because the same box changes identity depending on where you stand — `Contract Manufacturing` seen from Dingdian is "a capability we outsource," but seen from the contract factory it's "its core capability." **Leave the perspective undefined and the boxes drift:** one moment you want to draw the contract factory's internals in, the next you don't. Pin "Dingdian's own perspective" and the answers to which boxes to include and how detailed they should be become fixed.

## Step 2: Open an APQC PCF as your menu — don't draw from scratch

Open an APQC PCF (cross-industry version). Its 13 top-level categories spread across the first page. Dingdian orders from it like this:
- **Keep**: 2.0 Develop Products (the lifeline), 3.0 Marketing & Sales, 4.0 Supply Chain (life or death for a contract-manufacturing model), 6.0 Customer Service, 7.0–13.0 all the support categories.
- **Rename**: 2.0 "Develop Products" becomes what Dingdian actually calls it — "Product Development."
- **Cut**: 5.0 "Deliver Services" — Dingdian has no service delivery, so delete it.
- **Add**: "After-Sales & Warranty Service Management," which APQC doesn't have — it's specific to appliances, so add it yourself.

Draw from scratch and you'll always miss something; delete and tweak from a template and your coverage is far higher. **The template also clears the next step's three purity tests for you** — every APQC line is already vetted, same-level, clean capability.

## Step 3: Run every box through the 3 purity tests (the key: this is where dirt sneaks in)

To decide whether a box is a **clean capability**, run it through three tests. My first-draft Dingdian failed all three — which makes it the clearest possible counter-example:

| What I wrongly put in (first draft) | Which test it fails | Renamed to a clean capability |
|---|---|---|
| `Retention` | It's an **outcome**, not a capability | **Engagement & Retention Management** |
| `Travel Expense Reimbursement` | It's a **process** (a transaction flow), not a capability | **Expense Management** |
| `Predictive Maintenance` | It's a **use case**, not a capability | **Equipment Maintenance Management** |
| `Recruiting` (just a bare verb) | Leans toward **how / action** | **Talent Acquisition** |

The three tests in plain language:
1. **What, not how**: state "what it does," not "what it uses to do it." `Expense Management` is a capability; `Travel Expense Reimbursement` is a process beneath it.
2. **Capability, not outcome**: `Engagement & Retention Management` is something you do; `Retention` is the result you get when you do it right. Make the outcome a box and you'll later pin AI on the outcome instead of on the capability that produces it (you'll hit this in Step 7).
3. **Same level, no mixed types**: a sibling set of sub-boxes must be the same type and the same altitude — don't mix capability, process, outcome, and use case in one row.

**Why this test is the hardest**: on the surface, `Retention`, `Travel Expense Reimbursement`, and `Predictive Maintenance` are all "business nouns" and all look like capabilities. **Being a business noun ≠ being a clean capability.** Judging which kind each box is takes human judgment; the template (APQC) clears about eighty percent for you, and inventing box names yourself is where you're most likely to slip.

## Step 4: One owner — this is where the argument happens

Draw `Customer Data Management` and the marketing director says "that's mine, I own the CRM," while the customer-service director says "the complaint data lives with me." Both want it → this is the BCM's most painful and most valuable moment: **it forces a decision nobody wants to make — who actually owns this capability.** Don't settle it now and the later AI investment (who pays to build the customer 360 view) becomes a game of hot potato. One owner, non-overlapping boundaries — that's the fourth, real-world test on top of the three purity tests.

## Step 5: Decompose further only when "one box carries multiple objectives"

Dingdian's Level 1 has about 12 boxes, and at that point you can already take it to the board. **The only signal that you should decompose to Level 2: a single box drives several business objectives at once.**

Example: `Talent Management` carries three things at once — production yield (retaining the master technicians), new-product speed (competing for R&D talent), and headcount cost (cutting turnover). One box, three objectives, and you can't tell where to push → decompose to L2: **Talent Acquisition / Learning & Development / Engagement & Retention Management / Compensation Management.** Only after decomposing can you see that "retain the master technicians" maps to `Engagement & Retention Management`, not `Talent Acquisition`. Stop at L2–3; go any deeper and it turns into process.

## Step 6: One page, and mark the "value-enabling" boxes

Boxes play two roles, and your drawing has to tell them apart:
- **Makes money directly (value-realizing)**: `Equipment Maintenance Management` — keeping the line from going down saves money directly, and the boss gets it at a glance.
- **Value-enabling (the foundation, don't cut)**: `Data Governance` — it makes no money on its own, but without it the equipment-maintenance AI model has no clean data to feed on.

Every budget season, `Data Governance` loses to the boxes with visible ROI. **Cut it, and six months later the maintenance model drifts off because the data is dirty.** So mark the enabling boxes right on the map, and shield them when you prioritize: these few can't be cut — they hold up the foundation for everyone else.

## Step 7: Apply the pace-layer 3 colours + pin AI on capabilities

By now the boxes are all correct, but it's still a "plain map." Add the final layer — paint each box one strategic colour. **Remember: the colours and the AI pins are an overlay, not an innate property of the box** (the base-map-vs-overlay lens); change the business objective and the same box changes colour.

Dingdian (taking the "push new products" perspective):
- **Deep orange (differentiating, heavy AI bet ~70%)**: `Product Development`, `Industrial Design`, `Demand Forecasting`, `Engagement & Retention Management`, `Equipment Maintenance Management`.
- **Mid yellow (keep up)**: `Quality Management`, `Supply Chain Management`, `Financial Accounting`.
- **Off-white (commodity, buy off the shelf)**: `Compensation Management`, `Expense Management`.

Pin the AI use cases on — **pin them on the capability, not on the outcome or the process** (this is the payoff from Step 3):
- AI attrition prediction → pin on **`Engagement & Retention Management`** (not on the "retention" outcome).
- AI equipment-anomaly detection → pin on **`Equipment Maintenance Management`** (not on the "predictive maintenance" use case).
- AI invoice recognition → pin on **`Expense Management`** (off-white = commodity, buy it, don't build it).

Once painted and pinned, how to split the AI budget is obvious at a glance: deep orange takes the lion's share, off-white gets not a cent — buy it off the shelf. **This is the step that turns the BCM from an "org chart" into an "investment map."**

## Step 8: Schedule a six-month review

A BCM is not a document you draw once and file away. **Put it on the calendar and revisit it every six months**: which box changed colour (last year Quality Management was keep up; this year every competitor has gone AI, so it's promoted to differentiating)? Which AI project went from a "bet" to a "sure thing"? AI keeps changing, and a frozen BCM won't survive a year.

---

## Condensed to one line

Pin the perspective → open an APQC PCF to grab the skeleton → **run every box through the 3 purity tests (don't let outcome / process / use case in)** → settle the owner → decompose to L2 only for multi-objective boxes → mark the value-enabling boxes → apply the 3 colours + pin AI on capabilities → review in six months.

**The hardest part is not the layout and not the colouring — it's Step 3, unit purity** — confirming that every box is a true capability, at the same level. Fail this test and everything after is built on sand: you'll bet AI on an outcome like `Retention` instead of on the `Engagement & Retention Management` that produces it. That's exactly how my first draft went wrong.

---

## Try another company: Xinda Digital Bank (the second example)

> Why do a second company: Dingdian is manufacturing — it sells appliances you can see. Pick a company as far from it as possible and you find out whether these 9 steps are manufacturing-only or genuinely general. Xinda Digital Bank, a fictional digital bank, is far enough away — it sells financial services, has no physical branches, and is heavily regulated.

**About Xinda Digital Bank**: a fictional branchless internet-only bank where everything runs in the app, serving individual depositors plus micro and small businesses. It wants to use AI to pull ahead on three things — approve credit faster and more accurately, make wealth advisory affordable for everyone, and block fraud in real time.

Move the same 9 steps onto a bank, and here's what changes and what doesn't:

- **The entire core tier gets swapped out** (Step 2, ordering from the APQC menu): Dingdian's core is "Product Development / Supply Chain"; the bank's becomes "Funding & Credit / Deposits, Transfers & Payments / Wealth & Channels." The skeleton holds — the money-making capabilities sit in the middle — but the contents are entirely different.
- **A whole new block appears: "Risk & Compliance"**: KYC, anti-money-laundering (AML), fraud detection. Manufacturing doesn't have this; the bank does, forced out by the regulator. Without this block the bank can't open its doors.
- **Same-named capability, flipped strategic standing** (Step 7's colouring, echoing the base-map-vs-overlay lens): Dingdian can paint "Compensation Management" off-white and buy it. The bank's "Regulatory Compliance" can never be painted off-white — regulation is the lifeline, so at minimum keep up. Change the industry, and what colour a given box should be changes with it.
- **AI still pins on the capability, not the outcome** (Step 3's payoff): pin AI on the four capability boxes `Credit Underwriting`, `Wealth Advisory`, `Digital Channels`, and `Fraud Detection` (deep orange, heavy bet), not on an outcome like "lower bad-debt ratio."
- **The value-enabling boxes still get marked** (Step 6): draw `Data Governance` as a dashed box — it makes no money on its own, but the AI models for both underwriting and fraud detection rely on it to feed clean data, so shield it from cuts at budget time.

Not one of the 9 steps was dropped and the order didn't change, yet you can still draw a bank's BCM. All that changes is "which items you order off the menu and what colours you paint" — the method itself holds up, and that's the proof that it isn't manufacturing-only.

> The generated example image: a gpt-image-2 raster render — crisp Traditional Chinese, with all four AI badges in place.
