#!/usr/bin/env python3
"""Render a VALUE/FEASIBILITY MATRIX, not a strategic opportunity radar.
Usage: render_radar.py portfolio.json [matrix.html]
Unscored candidates remain visible without fabricated coordinates.
"""
import json
import sys
from pathlib import Path
from report_utils import COLORS,cards,esc,page,validate,tr,score_status


def svg(spec):
    x=lambda v:90+(v-1)*145
    y=lambda v:520-(v-1)*110
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 600" role="img" aria-label="{tr(spec,"Value and feasibility matrix","價值與可行性比較")}">']
    for n in range(1,6):
        out.extend([f'<line x1="{x(n)}" y1="80" x2="{x(n)}" y2="520" stroke="#d7e0e5"/>',f'<line x1="90" y1="{y(n)}" x2="670" y2="{y(n)}" stroke="#d7e0e5"/>',f'<text x="{x(n)}" y="545" text-anchor="middle">{n}</text>',f'<text x="65" y="{y(n)+5}">{n}</text>'])
    out.append(f'<text x="380" y="580" text-anchor="middle">{tr(spec,"Feasibility","可行性")} →</text><text transform="translate(25,300) rotate(-90)" text-anchor="middle">{tr(spec,"Value","價值")} →</text>')
    positions={}
    for i,u in enumerate(spec.get('use_cases',[]),1):
        if u.get('value') is None or u.get('feasibility') is None:continue
        positions.setdefault((u['feasibility'],u['value']),[]).append((i,u))
    for (f,v),group in positions.items():
        labels=', '.join(str(i) for i,_ in group)
        tip='; '.join(f'{i}. {u["name"]} ({score_status(spec,u["score_status"])})' for i,u in group)
        color=COLORS[group[0][1].get('type','unclassified')] if len(group)==1 else '#333'
        out.append(f'<g class="scored-point"><circle cx="{x(f)}" cy="{y(v)}" r="9" fill="{color}"><title>{esc(tip)}</title></circle><text x="{x(f)+14}" y="{y(v)+5}">{esc(labels)}</text></g>')
    out.append('</svg>')
    return ''.join(out)


def render(spec):
    validate(spec)
    scored=sum(u.get('value') is not None and u.get('feasibility') is not None for u in spec.get('use_cases',[]))
    body=''
    if scored:
        unscored=len(spec.get('use_cases',[]))-scored
        count=tr(spec,f'{scored} scored candidates; {unscored} remain unscored.',f'{scored} 項方案已有評分，{unscored} 項仍需評估。')
        legend=tr(spec,'Blue: individual work · Brown: team/process change · Purple: new value/markets. Shared coordinates list all candidate numbers.','藍色：個人工作改善；棕色：團隊與流程改善；紫色：新價值或市場。同一位置列出所有方案編號。')
        body=f'<p>{count}</p><div class="frame">{svg(spec)}</div><p class="meta">{legend}</p>'
    body+=cards(spec.get('use_cases',[]),spec)
    title=tr(spec,'Value / Feasibility Matrix','投資方案與驗證條件') if scored else tr(spec,'Investment options and validation','投資方案與驗證條件')
    return page(spec,title,body)


def main():
    if len(sys.argv)<2:print(__doc__);return 2
    src=Path(sys.argv[1]);out=Path(sys.argv[2]) if len(sys.argv)>2 else src.with_name(src.stem+'-matrix.html')
    out.write_text(render(json.loads(src.read_text())));print(f'Wrote {out}');return 0
if __name__=='__main__':raise SystemExit(main())
