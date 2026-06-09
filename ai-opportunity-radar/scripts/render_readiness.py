#!/usr/bin/env python3
"""Render an AI READINESS gap chart to a self-contained HTML page (inline SVG spider).

7 dimensions (note 1): Strategy / Value / Organization / People & Culture /
Governance / AI Engineering / AI Data. Two polygons — current (solid) vs future
(dashed) — on a 1–5 spider; the gap between them is the work to do. The point is
the GAP, not the score. Deterministic SVG, not a raster.

Usage:  render_readiness.py <portfolio.json> [out.html]

Reads `company`, `as_of`, `readiness[]`, `notes[]`. Each readiness item:
{dim, current 1-5, future 1-5}.
"""
import html
import json
import math
import sys
from pathlib import Path

CX, CY, R = 310, 330, 205
NAVY, ORANGE = "#1f3a5f", "#d9701b"


def esc(v):
    return html.escape(str(v))


def pt(score, i, n):
    a = -math.pi / 2 + i * 2 * math.pi / n
    rr = (score / 5.0) * R
    return CX + rr * math.cos(a), CY + rr * math.sin(a)


def poly(scores, n):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(s, i, n) for i, s in enumerate(scores)))


def spider(rd):
    n = len(rd)
    cur = [float(d["current"]) for d in rd]
    fut = [float(d["future"]) for d in rd]
    out = [f'<svg viewBox="0 0 640 660" width="100%" preserveAspectRatio="xMidYMid meet" font-family="inherit">']
    # rings
    for ring in (1, 2, 3, 4, 5):
        out.append(f'<polygon points="{poly([ring]*n, n)}" fill="none" stroke="#e3e7ec" stroke-width="1"/>')
    # axes + labels
    for i, d in enumerate(rd):
        ex, ey = pt(5, i, n)
        out.append(f'<line x1="{CX}" y1="{CY}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#dfe3e8" stroke-width="1"/>')
        lx, ly = pt(5.62, i, n)
        anchor = "middle" if abs(lx - CX) < 30 else ("start" if lx > CX else "end")
        gap = fut[i] - cur[i]
        out.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-size="12" font-weight="700" fill="#1a1d21">{esc(d["dim"])}</text>')
        out.append(f'<text x="{lx:.1f}" y="{ly+15:.1f}" text-anchor="{anchor}" font-size="10.5" fill="#8b929a">{cur[i]:g}→{fut[i]:g}（gap {gap:+g}）</text>')
    # future (dashed) then current (filled) so current sits on top
    out.append(f'<polygon points="{poly(fut, n)}" fill="{ORANGE}" fill-opacity="0.10" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="7 5"/>')
    out.append(f'<polygon points="{poly(cur, n)}" fill="{NAVY}" fill-opacity="0.18" stroke="{NAVY}" stroke-width="2"/>')
    # dots
    for i in range(n):
        cx2, cy2 = pt(cur[i], i, n); fx2, fy2 = pt(fut[i], i, n)
        out.append(f'<circle cx="{cx2:.1f}" cy="{cy2:.1f}" r="3.5" fill="{NAVY}"/>')
        out.append(f'<circle cx="{fx2:.1f}" cy="{fy2:.1f}" r="3.5" fill="{ORANGE}"/>')
    # legend
    out.append(f'<rect x="40" y="612" width="16" height="10" fill="{NAVY}" fill-opacity="0.18" stroke="{NAVY}" stroke-width="2"/>')
    out.append(f'<text x="62" y="621" font-size="12" fill="#2b2f35">current 現況</text>')
    out.append(f'<rect x="190" y="612" width="16" height="10" fill="{ORANGE}" fill-opacity="0.10" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="5 4"/>')
    out.append(f'<text x="212" y="621" font-size="12" fill="#2b2f35">future 目標</text>')
    out.append(f'<text x="350" y="621" font-size="12" font-weight="700" fill="#8b929a">看 gap，不看分數</text>')
    out.append("</svg>")
    return "\n".join(out)


def gap_table(rd):
    rows = ""
    for d in sorted(rd, key=lambda x: float(x["future"]) - float(x["current"]), reverse=True):
        gap = float(d["future"]) - float(d["current"])
        bar = "█" * int(round(gap))
        rows += (f'<tr><td>{esc(d["dim"])}</td><td style="text-align:center">{float(d["current"]):g}</td>'
                 f'<td style="text-align:center">{float(d["future"]):g}</td>'
                 f'<td style="color:#d9701b;font-weight:700">+{gap:g} {bar}</td></tr>')
    return ('<table class="gap"><thead><tr><th>維度</th><th>現況</th><th>目標</th><th>gap（要補的功）</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>')


CSS = """
*{box-sizing:border-box;} body{margin:0;padding:48px 56px;max-width:1040px;background:#fff;color:#1a1d21;
 font:15px/1.6 "PingFang TC","Microsoft JhengHei","Noto Sans CJK TC",-apple-system,"Segoe UI",sans-serif;}
.kicker{margin:0 0 8px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#1f3a5f;font-weight:700;}
h1{margin:0;font-size:24px;} .meta{margin:6px 0 18px;color:#565d66;font-size:13px;}
.wrap{display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap;}
.frame{border:1px solid #d7dce1;border-radius:12px;padding:10px;min-width:0;flex:1 1 360px;}
svg{max-width:100%;height:auto;display:block;}
@media(max-width:640px){body{padding:22px 14px;} .wrap{gap:14px;}}
table.gap{border-collapse:collapse;font-size:13.5px;min-width:300px;} table.gap th{text-align:left;color:#8b929a;font-size:11.5px;
 border-bottom:2px solid #1a1d21;padding:7px 12px 7px 0;} table.gap td{border-bottom:1px solid #e3e7ec;padding:8px 12px 8px 0;}
.notes{margin-top:18px;padding-top:12px;border-top:1px solid #d7dce1;font-size:12px;color:#8b929a;} .notes li{margin:3px 0;}
"""


def render(spec):
    company = esc(spec.get("company", "Company"))
    rd = spec.get("readiness", [])
    as_of = esc(spec.get("as_of", ""))
    notes = spec.get("notes", [])
    notes_html = ""
    if notes:
        items = "".join(f"<li>{esc(n)}</li>" for n in notes)
        notes_html = f'<div class="notes"><b>資料註記</b><ul>{items}</ul></div>'
    return (
        f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{company} — AI Readiness</title><style>{CSS}</style></head><body>'
        f'<p class="kicker">AI Readiness · 7 維 current vs future</p><h1>{company} — AI 就緒度（看 gap）</h1>'
        f'<p class="meta">重點是 current→future 的 gap，不是當前分數｜{as_of}</p>'
        f'<div class="wrap"><div class="frame">{spider(rd)}</div><div>{gap_table(rd)}</div></div>{notes_html}</body></html>'
    )


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    sp = Path(sys.argv[1]); spec = json.loads(sp.read_text(encoding="utf-8"))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else sp.with_name(sp.stem + "-readiness.html")
    out.write_text(render(spec), encoding="utf-8"); print(f"Wrote {out}"); return 0


if __name__ == "__main__":
    raise SystemExit(main())
