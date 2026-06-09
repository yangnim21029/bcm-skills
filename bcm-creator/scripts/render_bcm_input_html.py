#!/usr/bin/env python3
"""Render a BCM-INPUT BRIEF to a self-contained corporate-briefing HTML file.

This is the "homework" deliverable of bcm-creator. Its content is exactly
what note 1 (the Gartner BCM webinar) says a BCM needs — NOT a generic company
profile, and NOT the BCM picture itself (that is generated as an image):

  - business objectives            (note 1, L96-98: top of the one-pager)
  - a capability inventory, split into value-realizing and value-enabling
    (note 1, L100-102), each row a metadata card (note 1, L256-258):
      public fields:   definition, level, industry-typical KPI, AI pin
      internal fields: owner, supporting systems, data in/out, data readiness 1-5
                       — NOT public; shown as TBD for the org to fill (note 1, L258/262)
  - a short company-context paragraph for orientation

NOTE: pace layer is deliberately NOT in this list. It is a strategic OVERLAY
(note 1, L120-126, base map vs overlay) decided when you draw the MAP — it lives on
the BCM image, not in the capability inventory.

Style = corporate briefing: restrained ink + single accent, ruled
sections, scannable tables. No pastel cards.

Usage:  render_bcm_input_html.py <brief.json> [out.html]

Schema:
{
  "company": str, "tagline": str?, "as_of": str?, "classification": str?,
  "facts": [{"k","v"}]?,                       # optional top fact strip
  "context": str | [str],                      # short company background
  "objectives": [{"name": str, "kpi": str?}],  # business objectives (BCM top row)
  "capabilities": [
    {"name": str, "level": str?, "role": "realizing"|"enabling",
     "ai": bool?, "definition": str, "kpi": str?}
  ],
  "internal_fields_note": str?,                # defaults to the TBD line
  "notes": [str]?,                             # data-notes caveats
  "sources": [str]?
}
"""
import html
import json
import sys
from pathlib import Path

DEFAULT_INTERNAL_NOTE = (
    "Each capability also needs an internal metadata card: owner (single), supporting systems, "
    "data input/output, data readiness (1–5). These four fields are not public — mark them \"TBD\" for the organization to fill (note 1, L256–262)."
)

CSS = """
:root{ --ink:#1a1d21; --muted:#565d66; --faint:#8b929a;
  --rule:#d7dce1; --rule-strong:#1a1d21; --accent:#1f3a5f; --bg:#ffffff; }
*{ box-sizing:border-box; }
body{ margin:0; padding:56px 64px; max-width:960px; background:var(--bg); color:var(--ink);
  font:15px/1.65 "PingFang TC","Microsoft JhengHei","Noto Sans CJK TC","Hiragino Sans GB",
    -apple-system,"Segoe UI",Roboto,sans-serif; }
.doc-head{ border-bottom:2px solid var(--rule-strong); padding-bottom:16px; margin-bottom:4px; position:relative; }
.kicker{ margin:0 0 10px; font-size:11px; font-weight:600; letter-spacing:.18em; text-transform:uppercase; color:var(--accent); }
.doc-head h1{ margin:0; font-size:26px; font-weight:700; letter-spacing:-.01em; }
.doc-meta{ margin:7px 0 0; color:var(--muted); font-size:13px; }
.doc-meta .dot{ margin:0 9px; color:var(--faint); }
.classif{ position:absolute; top:0; right:0; font-size:10.5px; font-weight:700; letter-spacing:.12em;
  text-transform:uppercase; color:var(--faint); border:1px solid var(--rule); padding:3px 8px; }
table.facts{ width:100%; border-collapse:collapse; margin:24px 0 30px; font-size:13.5px; }
table.facts th{ width:118px; text-align:left; vertical-align:top; padding:9px 18px 9px 0;
  color:var(--faint); font-weight:600; border-bottom:1px solid var(--rule); }
table.facts td{ padding:9px 0; border-bottom:1px solid var(--rule); color:var(--ink); font-weight:600; }
section{ margin:0 0 28px; }
section>h2{ display:flex; align-items:baseline; gap:12px; margin:0 0 12px; padding-bottom:7px;
  font-size:16px; font-weight:700; border-bottom:1px solid var(--rule); }
section>h2 .num{ font-size:12px; font-weight:700; color:var(--accent); font-variant-numeric:tabular-nums; }
section>h2 .tag{ margin-left:auto; font-size:11px; font-weight:600; color:var(--faint); letter-spacing:.04em; }
section p{ margin:0 0 9px; color:#2b2f35; }
ul.obj{ margin:0; padding:0; list-style:none; }
ul.obj li{ display:flex; gap:14px; padding:9px 0; border-bottom:1px solid var(--rule); }
ul.obj .o-name{ flex:0 0 230px; font-weight:700; }
ul.obj .o-kpi{ color:var(--muted); font-size:13.5px; }
table.cap{ width:100%; border-collapse:collapse; font-size:13.5px; }
table.cap thead th{ text-align:left; padding:8px 10px; border-bottom:2px solid var(--rule-strong);
  font-size:11.5px; letter-spacing:.04em; color:var(--faint); font-weight:700; }
table.cap td{ padding:9px 10px; border-bottom:1px solid var(--rule); vertical-align:top; }
table.cap td.name{ font-weight:700; white-space:nowrap; }
table.cap td.def{ color:#2b2f35; }
table.cap td.kpi{ color:var(--muted); min-width:180px; }
.aibadge{ display:inline-block; margin-left:6px; background:#111; color:#fff; font-size:9.5px;
  font-weight:800; padding:1px 5px; border-radius:7px; letter-spacing:.5px; vertical-align:middle; }
.intnote{ margin:12px 0 0; padding:10px 13px; background:#f6f8fa; border-left:3px solid var(--accent);
  font-size:12.5px; color:var(--muted); }
.foot{ margin-top:38px; padding-top:12px; border-top:1px solid var(--rule); font-size:11.5px; color:var(--faint); }
.foot b{ color:var(--muted); font-weight:600; }
.foot ul{ margin:5px 0 0; padding-left:18px; } .foot li{ margin:2px 0; }
"""


def esc(v) -> str:
    return html.escape(str(v))


def facts_table(facts):
    if not facts:
        return ""
    rows = "".join(f'<tr><th>{esc(f.get("k",""))}</th><td>{esc(f.get("v",""))}</td></tr>' for f in facts)
    return f'<table class="facts">{rows}</table>'


def context_section(ctx, idx):
    paras = ctx if isinstance(ctx, list) else [ctx]
    body = "".join(f"<p>{esc(p)}</p>" for p in paras)
    return f'<section><h2><span class="num">{idx:02d}</span>Company context</h2>{body}</section>'


def objectives_section(objs, idx):
    items = "".join(
        f'<li><span class="o-name">{esc(o.get("name",""))}</span>'
        f'<span class="o-kpi">{esc(o.get("kpi",""))}</span></li>'
        for o in objs
    )
    return (f'<section><h2><span class="num">{idx:02d}</span>Business Objectives'
            f'<span class="tag">BCM top row</span></h2><ul class="obj">{items}</ul></section>')


def cap_table_section(caps, idx, title, tag, note):
    head = ("<thead><tr><th>Capability</th><th>Level</th>"
            "<th>Definition (what it does)</th><th>Industry-typical KPI</th></tr></thead>")
    rows = []
    for c in caps:
        ai = '<span class="aibadge">AI</span>' if c.get("ai") else ""
        rows.append(
            f'<tr><td class="name">{esc(c["name"])}{ai}</td>'
            f'<td>{esc(c.get("level","L1"))}</td>'
            f'<td class="def">{esc(c.get("definition",""))}</td>'
            f'<td class="kpi">{esc(c.get("kpi","—"))}</td></tr>'
        )
    note_html = f'<p class="intnote">{esc(note)}</p>' if note else ""
    return (f'<section><h2><span class="num">{idx:02d}</span>{esc(title)}'
            f'<span class="tag">{esc(tag)}</span></h2>'
            f'<table class="cap">{head}<tbody>{"".join(rows)}</tbody></table>{note_html}</section>')


def notes_section(notes, idx):
    items = "".join(f'<li><span class="o-kpi">{esc(n)}</span></li>' for n in notes)
    return (f'<section><h2><span class="num">{idx:02d}</span>Data notes</h2>'
            f'<ul class="obj">{items}</ul></section>')


def render(spec):
    company = esc(spec.get("company", "Company"))
    meta_bits = []
    if spec.get("tagline"): meta_bits.append(esc(spec["tagline"]))
    if spec.get("as_of"): meta_bits.append(f'as of {esc(spec["as_of"])}')
    meta_html = ('<p class="doc-meta">' + '<span class="dot">·</span>'.join(meta_bits) + "</p>") if meta_bits else ""
    classif_html = f'<span class="classif">{esc(spec["classification"])}</span>' if spec.get("classification") else ""

    idx = 1
    blocks = []
    if spec.get("context"):
        blocks.append(context_section(spec["context"], idx)); idx += 1
    if spec.get("objectives"):
        blocks.append(objectives_section(spec["objectives"], idx)); idx += 1
    if spec.get("capabilities"):
        caps = spec["capabilities"]
        realizing = [c for c in caps if c.get("role") == "realizing"]
        enabling = [c for c in caps if c.get("role") != "realizing"]
        note = spec.get("internal_fields_note", DEFAULT_INTERNAL_NOTE)
        if realizing:
            blocks.append(cap_table_section(realizing, idx, "Capabilities · value-realizing",
                                            "BCM left side · directly delivers outcome", None)); idx += 1
        if enabling:
            blocks.append(cap_table_section(enabling, idx, "Capabilities · value-enabling",
                                            "BCM base layer · holds others up, don't cut", note)); idx += 1
    if spec.get("notes"):
        blocks.append(notes_section(spec["notes"], idx)); idx += 1

    foot = ""
    if spec.get("sources"):
        items = "".join(f"<li>{esc(s)}</li>" for s in spec["sources"])
        foot = f'<div class="foot"><b>Sources</b><ul>{items}</ul></div>'

    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{company} — BCM Input Brief</title>\n<style>{CSS}</style>\n</head>\n<body>\n"
        f'<div class="doc-head">{classif_html}<p class="kicker">BCM Input Brief · Capability Map Inputs</p>'
        f"<h1>{company}</h1>{meta_html}</div>\n"
        f"{facts_table(spec.get('facts'))}\n{''.join(blocks)}\n{foot}\n"
        "</body>\n</html>\n"
    )


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else spec_path.with_suffix(".html")
    out_path.write_text(render(spec), encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
