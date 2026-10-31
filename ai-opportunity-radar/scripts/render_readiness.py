#!/usr/bin/env python3
"""Render readiness current/target marks without imputing missing scores.
Usage: render_readiness.py portfolio.json [readiness.html]
"""
import json
import sys
from pathlib import Path
from report_utils import esc,page,validate,tr,dimension,score_status,inline,paragraphs


def chart(rows,spec=None):
    spec=spec or {}
    height=100+75*len(rows);x=lambda v:310+(v-1)*100
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 770 {height}" role="img" aria-label="{tr(spec,"Readiness current and target scores","目前條件與目標評分")}">']
    for n in range(1,6):out.append(f'<text x="{x(n)}" y="28" text-anchor="middle">{n}</text>')
    for i,d in enumerate(rows):
        y=65+i*75
        out.append(f'<text x="10" y="{y+5}" font-size="15">{esc(dimension(spec,d["dim"]))}</text><line x1="310" y1="{y}" x2="710" y2="{y}" stroke="#d7e0e5"/>')
        c,f=d.get('current'),d.get('future')
        if c is not None and f is not None:out.append(f'<line x1="{x(c)}" y1="{y}" x2="{x(f)}" y2="{y}" stroke="#7cabbc" stroke-width="4"/>')
        if c is not None:out.append(f'<circle class="current" cx="{x(c)}" cy="{y}" r="7" fill="#365a70"/>')
        if f is not None:out.append(f'<circle class="target" cx="{x(f)}" cy="{y}" r="10" fill="none" stroke="#ad7935" stroke-width="2"/>')
        missing=[]
        if c is None:missing.append(tr(spec,'current unknown','目前條件待評估'))
        if f is None:missing.append(tr(spec,'target unknown','目標待確認'))
        if missing:out.append(f'<text x="310" y="{y+25}" font-size="12" fill="#63717c">{esc("; ".join(missing))}</text>')
    out.append(f'<text x="10" y="{height-12}" font-size="13">{tr(spec,"Filled: current · Outline: target · Missing scores stay unknown","實心：目前評分；空心：目標評分")}</text></svg>')
    return ''.join(out)


def render(spec):
    validate(spec);rows=spec.get('readiness',[])
    parts=[]
    if any(d.get(k) is not None for d in rows for k in ('current','future')):
        parts.append(f'<div class="frame">{chart(rows,spec)}</div>')
    for d in rows:
        c,f=d.get('current'),d.get('future')
        parts.append(f'<article><h2>{esc(d.get("title") or dimension(spec,d["dim"]))}</h2>')
        scores=[]
        if c is not None:scores.append(f'{tr(spec,"Current","目前")}: {c}')
        if f is not None:scores.append(f'{tr(spec,"Target","目標")}: {f}')
        if c is not None and f is not None:scores.append(f'{tr(spec,"Gap","差距")}: {f-c:+g}')
        if scores:parts.append(f'<p class="meta">{esc(" · ".join(scores))} · {esc(score_status(spec,d.get("score_status","unknown")))}</p>')
        parts.append(paragraphs(d.get('basis',''),spec)+paragraphs(d.get('next_action',''),spec)+'</article>')
    return page(spec,tr(spec,'Readiness requirements','讓方案持續運作的條件'),''.join(parts))


def main():
    if len(sys.argv)<2:print(__doc__);return 2
    src=Path(sys.argv[1]);out=Path(sys.argv[2]) if len(sys.argv)>2 else src.with_name(src.stem+'-readiness.html')
    out.write_text(render(json.loads(src.read_text())));print(f'Wrote {out}');return 0
if __name__=='__main__':raise SystemExit(main())
