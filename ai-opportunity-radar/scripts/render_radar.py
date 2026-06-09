#!/usr/bin/env python3
"""Render an AI OPPORTUNITY RADAR to a self-contained HTML page (inline SVG).

The radar plots AI use cases on Value (y) × Feasibility (x), each dot coloured by
its Defend / Extend / Upend business-case type and pinned to a BCM capability.
Zones (note 1): Likely wins (hi value + hi feasibility) / Calculated risks (hi
value, low feasibility) / Marginal gains (low value). Precise coordinates, so it's
a deterministic SVG chart — not a raster.

Usage:  render_radar.py <portfolio.json> [out.html]

Reads `company`, `as_of`, `use_cases[]`, `notes[]` from the portfolio JSON. Each
use case: {name, capability, value 1-5, feasibility 1-5, type: defend|extend|upend}.
"""
import html
import json
import sys
from pathlib import Path

TYPE = {  # business-case type -> (colour, label)
    "defend": ("#1f3a5f", "Defend（augment、ROI 穩）"),
    "extend": ("#d9701b", "Extend（改流程、有方案）"),
    "upend":  ("#7a3e9d", "Upend（顛覆、高風險高回報）"),
}
X0, X1, Y0, Y1 = 80, 660, 64, 556          # plot box (svg coords)
SVGW, SVGH = 930, 600


def esc(v):
    return html.escape(str(v))


def fx(feas):
    return X0 + (feas - 0.5) / 5.0 * (X1 - X0)


def fy(val):
    return Y1 - (val - 0.5) / 5.0 * (Y1 - Y0)


def svg(spec):
    midx, midy = fx(3.0), fy(3.0)
    out = [f'<svg viewBox="0 0 {SVGW} {SVGH}" width="100%" preserveAspectRatio="xMidYMid meet" font-family="inherit">']
    # zones
    out.append(f'<rect x="{midx:.0f}" y="{Y0}" width="{X1-midx:.0f}" height="{midy-Y0:.0f}" fill="#e8f0e6"/>')   # likely wins
    out.append(f'<rect x="{X0}" y="{Y0}" width="{midx-X0:.0f}" height="{midy-Y0:.0f}" fill="#faf1dd"/>')        # calculated risks
    out.append(f'<rect x="{X0}" y="{midy:.0f}" width="{X1-X0}" height="{Y1-midy:.0f}" fill="#f1f2f4"/>')         # marginal gains
    out.append(f'<text x="{X1-8:.0f}" y="{Y0+18}" text-anchor="end" font-size="12" font-weight="700" fill="#3f7d3a">Likely wins</text>')
    out.append(f'<text x="{X0+8:.0f}" y="{Y0+18}" font-size="12" font-weight="700" fill="#b07d1a">Calculated risks</text>')
    out.append(f'<text x="{X0+8:.0f}" y="{Y1-10:.0f}" font-size="12" font-weight="700" fill="#8b929a">Marginal gains（別分心）</text>')
    # gridlines + ticks
    for n in (1, 2, 3, 4, 5):
        gx, gy = fx(n), fy(n)
        out.append(f'<line x1="{gx:.0f}" y1="{Y0}" x2="{gx:.0f}" y2="{Y1}" stroke="#dfe3e8" stroke-width="1"/>')
        out.append(f'<line x1="{X0}" y1="{gy:.0f}" x2="{X1}" y2="{gy:.0f}" stroke="#dfe3e8" stroke-width="1"/>')
        out.append(f'<text x="{gx:.0f}" y="{Y1+16:.0f}" text-anchor="middle" font-size="11" fill="#8b929a">{n}</text>')
        out.append(f'<text x="{X0-10}" y="{gy+4:.0f}" text-anchor="end" font-size="11" fill="#8b929a">{n}</text>')
    # axes frame + labels
    out.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" fill="none" stroke="#1a1d21" stroke-width="1.5"/>')
    out.append(f'<text x="{(X0+X1)/2:.0f}" y="{Y1+40:.0f}" text-anchor="middle" font-size="12.5" font-weight="700" fill="#1a1d21">Feasibility 可行性（技術 + 內部成熟度）→</text>')
    out.append(f'<text transform="translate({X0-44},{(Y0+Y1)/2:.0f}) rotate(-90)" text-anchor="middle" font-size="12.5" font-weight="700" fill="#1a1d21">Value 價值（對經營目標的貢獻）→</text>')
    # dots
    for uc in spec.get("use_cases", []):
        color = TYPE.get(uc.get("type", "extend"), TYPE["extend"])[0]
        cx, cy = fx(float(uc["feasibility"])), fy(float(uc["value"]))
        title = f'{uc.get("name","")}｜{uc.get("capability","")}｜{uc.get("type","")}'
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="{color}" stroke="#fff" stroke-width="1.5"><title>{esc(title)}</title></circle>')
        out.append(f'<text x="{cx+11:.1f}" y="{cy+4:.1f}" font-size="11.5" fill="#1a1d21">{esc(uc.get("name",""))}</text>')
    # legend (right)
    lx, ly = 700, Y0 + 6
    out.append(f'<text x="{lx}" y="{ly}" font-size="12" font-weight="700" fill="#565d66">Business-case type</text>')
    for i, key in enumerate(("defend", "extend", "upend")):
        c, lab = TYPE[key]
        yy = ly + 22 + i * 22
        out.append(f'<circle cx="{lx+7}" cy="{yy-4}" r="7" fill="{c}"/>')
        out.append(f'<text x="{lx+22}" y="{yy}" font-size="11.5" fill="#2b2f35">{esc(lab)}</text>')
    out.append(f'<text x="{lx}" y="{ly+104}" font-size="12" font-weight="700" fill="#565d66">Zones</text>')
    zones = ["Likely wins → 馬上做", "Calculated risks → 小規模試", "Marginal gains → 別分心"]
    for i, z in enumerate(zones):
        out.append(f'<text x="{lx}" y="{ly+126+i*20}" font-size="11.5" fill="#2b2f35">{esc(z)}</text>')
    out.append(f'<text x="{lx}" y="{ly+210}" font-size="11" fill="#8b929a">釘在 capability，不釘在</text>')
    out.append(f'<text x="{lx}" y="{ly+226}" font-size="11" fill="#8b929a">use case 本身（note 1）</text>')
    out.append("</svg>")
    return "\n".join(out)


CSS = """
*{box-sizing:border-box;} body{margin:0;padding:48px 56px;max-width:1040px;background:#fff;color:#1a1d21;
 font:15px/1.6 "PingFang TC","Microsoft JhengHei","Noto Sans CJK TC",-apple-system,"Segoe UI",sans-serif;}
.kicker{margin:0 0 8px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#1f3a5f;font-weight:700;}
h1{margin:0;font-size:24px;} .meta{margin:6px 0 18px;color:#565d66;font-size:13px;}
.frame{border:1px solid #d7dce1;border-radius:12px;padding:14px;overflow-x:auto;}
svg{max-width:100%;height:auto;display:block;}
@media(max-width:640px){body{padding:22px 14px;}}
.notes{margin-top:18px;padding-top:12px;border-top:1px solid #d7dce1;font-size:12px;color:#8b929a;}
.notes li{margin:3px 0;}
"""


def render(spec):
    company = esc(spec.get("company", "Company"))
    as_of = esc(spec.get("as_of", ""))
    notes = spec.get("notes", [])
    notes_html = ""
    if notes:
        items = "".join(f"<li>{esc(n)}</li>" for n in notes)
        notes_html = f'<div class="notes"><b>資料註記</b><ul>{items}</ul></div>'
    return (
        f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{company} — AI Opportunity Radar</title><style>{CSS}</style></head><body>'
        f'<p class="kicker">AI Opportunity Radar · BCM × use case</p><h1>{company} — AI 機會雷達</h1>'
        f'<p class="meta">Value × Feasibility，dot 顏色＝Defend/Extend/Upend｜{as_of}</p>'
        f'<div class="frame">{svg(spec)}</div>{notes_html}</body></html>'
    )


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    sp = Path(sys.argv[1]); spec = json.loads(sp.read_text(encoding="utf-8"))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else sp.with_name(sp.stem + "-radar.html")
    out.write_text(render(spec), encoding="utf-8"); print(f"Wrote {out}"); return 0


if __name__ == "__main__":
    raise SystemExit(main())
