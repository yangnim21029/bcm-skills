#!/usr/bin/env python3
"""Render v3 company analysis with a generated capability-map image.

Usage: render_bcm_input_html.py input.json output.html [--mermaid-js bundle.js]
Python standard library only. A supplied Mermaid bundle makes HTML offline.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from passage_citations import inline, validate_passages, passage_html, citation_link, references_html, STYLE, SCRIPT

LENSES = {'execution', 'sustain', 'decision', 'attention', 'data', 'scope', 'autonomy'}
PACE = {'commodity', 'keep_up', 'differentiating', 'unknown'}
CSS = '''*{box-sizing:border-box}body{margin:32px auto;padding:36px 46px;max-width:1280px;background:#fff;color:#24333f;font:18px/1.9 -apple-system,"PingFang TC","Microsoft JhengHei",sans-serif}h1{font-size:32px;color:#153a50}h2{margin-top:48px;border-top:1px solid #d7e0e5;padding-top:24px}h3{font-size:21px;color:#193c50}p{margin:14px 0}a{color:#075577;overflow-wrap:anywhere}.meta,.refs{color:#63717c;font-size:15px}.point,.capability{margin:30px 0}.diagram{overflow-x:auto;margin:22px 0}.diagram svg{max-width:100%;height:auto}.map-image{margin:20px 0}.map-image img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:contain;background:#fff}.map-image figcaption{font-size:15px;color:#63717c;margin-top:12px}.caption{font-size:16px;padding:12px 18px;background:#f0f6f8;border-left:3px solid #7cabbc}details{padding:8px 0}summary{cursor:pointer;font-weight:600}pre{white-space:pre-wrap;font:14px/1.6 monospace}.legend{font-size:15px}nav a{margin-right:18px}@media(max-width:720px){body{margin:0;padding:24px 20px;font-size:17px}h1{font-size:27px}}'''


def esc(value):
    return html.escape(str(value), quote=True)


def safe_url(value):
    value = str(value or '')
    return value if urlsplit(value).scheme in ('http', 'https', '') else ''


def index(items, label):
    result = {}
    for item in items:
        key = item.get('id', '')
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', key) or key in result:
            raise ValueError(f'{label}: missing, invalid or duplicate id {key!r}')
        result[key] = item
    return result


def validate(spec):
    validate_passages(spec)
    if spec.get('schema_version') != 3:
        raise ValueError('Use schema_version 3; see references/output-contract.md')
    for key in ('company', 'viewpoint', 'decision_context', 'as_of'):
        if not spec.get(key): raise ValueError(f'Missing {key}')
    image_path = Path(spec.get('map_image', ''))
    if image_path.is_absolute() or '..' in image_path.parts or image_path.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp'):
        raise ValueError('map_image must name a local raster image relative to the output')
    if not spec.get('map_alt') or not spec.get('map_caption'):
        raise ValueError('Provide map_alt and map_caption')
    caps = index(spec.get('capabilities', []), 'capability')
    objectives = index(spec.get('objectives', []), 'objective')
    sources = index(spec.get('sources', []), 'source')
    if not caps or not objectives: raise ValueError('Provide capabilities and objectives')
    for c in caps.values():
        if c.get('role') not in ('realizing', 'enabling') or not all(c.get(k) for k in ('name', 'level', 'domain', 'status', 'definition')):
            raise ValueError(f'Capability {c["id"]} needs name, level, domain, role, status and definition')
    for o in objectives.values():
        if not all(o.get(k) for k in ('name', 'kpi', 'status')):
            raise ValueError('An objective needs name, KPI and status')
    seen = set()
    for o in spec.get('overlays', []):
        pair = (o.get('capability_id'), o.get('objective_id'))
        if pair[0] not in caps or pair[1] not in objectives or pair in seen:
            raise ValueError(f'Invalid or duplicate overlay {pair}')
        if o.get('pace') not in PACE or not o.get('reason'):
            raise ValueError('Overlay needs pace and rationale')
        seen.add(pair)
    if spec.get('map_objective_id') and spec['map_objective_id'] not in objectives:
        raise ValueError('Unknown map_objective_id')
    analyses = spec.get('analysis', [])
    index(analyses, 'analysis')
    if {p['id'] for p in analyses} & {'map', 'objectives', 'recommendations', 'capabilities', 'notes', 'sources'}:
        raise ValueError('Analysis ID conflicts with a document section')
    if spec.get('mode', 'map') not in ('map', 'investment'):
        raise ValueError('Mode must be map or investment')
    covered = set()
    for p in analyses:
        if not isinstance(p.get('lenses', []), list):
            raise ValueError('lenses must be a list')
        covered.update(p.get('lenses', []))
    if spec.get('mode', 'map') == 'investment' and not LENSES <= covered:
        raise ValueError('Investment mode requires all seven decision lenses')
    for p in analyses + spec.get('recommendations', []):
        paragraphs = p.get('paragraphs')
        if not p.get('title') or not isinstance(paragraphs, list) or not paragraphs or not all(isinstance(v,str) and v.strip() for v in paragraphs):
            raise ValueError('Analysis and recommendations need a title and company-specific paragraphs')
        if 'why' in p or 'example' in p:
            raise ValueError('Use company analysis paragraphs, not lecture-note fields')
        if p.get('mermaid') and not p.get('diagram_caption'):
            raise ValueError('Supplementary diagrams need a caption')
    for item in list(caps.values()) + list(objectives.values()) + analyses + spec.get('overlays', []) + spec.get('recommendations', []):
        for source in item.get('evidence', []):
            if source not in sources: raise ValueError(f'Unknown source {source}')
    return spec


def base_map(spec):
    selected = spec.get('map_objective_id')
    overlays = {o['capability_id']: o['pace'] for o in spec.get('overlays', []) if o['objective_id'] == selected}
    groups = {}
    for i, c in enumerate(spec['capabilities']): groups.setdefault(c.get('domain', 'Capabilities'), []).append((i, c))
    lines = ['flowchart LR']
    domains = []
    for i, (name, caps) in enumerate(groups.items()):
        d = f'domain{i}'; domains.append(d)
        lines.extend([f'  subgraph {d}["{esc(name)}"]', '    direction TB'])
        nodes = []
        for n, c in caps:
            node = f'cap{n}'; nodes.append(node)
            lines.append(f'    {node}["{esc(c["name"])}"]')
        if len(nodes) > 1: lines.append('    ' + ' ~~~ '.join(nodes))
        lines.append('  end')
    if len(domains) > 1: lines.append('  ' + ' ~~~ '.join(domains))
    lines.extend(['  classDef commodity fill:#fff,stroke:#8799a5,color:#24333f', '  classDef keep_up fill:#d9eaf3,stroke:#527c94,color:#172e3d', '  classDef differentiating fill:#234e68,stroke:#153a50,color:#fff', '  classDef unknown fill:#f0f0f0,stroke:#999,color:#333', '  classDef enabling stroke-dasharray:5 4'])
    for i, c in enumerate(spec['capabilities']):
        lines.append(f'  class cap{i} {overlays.get(c["id"], "unknown")}')
        if c['role'] == 'enabling': lines.append(f'  class cap{i} enabling')
    return '\n'.join(lines) + '\n'


def render(spec, mermaid_js=None):
    validate(spec)
    zh = spec.get('language', 'en').startswith('zh')
    tr = lambda en, cn: cn if zh else en
    blocks, md, diagrams = [], [], {'map': base_map(spec)}
    title = spec['company'] + tr(' — Capability-based investment brief', '｜能力與投資判斷')
    md.extend([f'# {title}', '', f'{spec["as_of"]} · {spec["viewpoint"]}', '', spec['decision_context'], ''])
    blocks.extend([f'<h1>{esc(title)}</h1>', f'<p class="meta">{esc(spec["as_of"])} · {esc(spec["viewpoint"])}</p>', f'<p>{inline(spec["decision_context"],spec)}</p>'])
    def refs(item):
        ids = item.get('evidence', [])
        return ' '.join(citation_link(i, spec) for i in ids)
    def mdrefs(item):
        return ' '.join(f'[{i}](#source-{i})' for i in item.get('evidence', []))
    def paragraph(value):
        if value: blocks.append(f'<p>{inline(value,spec)}</p>'); md.extend([str(value), ''])
    def heading(value, id):
        blocks.append(f'<h2 id="{id}">{esc(value)}</h2>'); md.extend([f'## {value}', ''])
    def diagram(code, caption):
        blocks.append(f'<div class="diagram"><pre class="mermaid">{esc(code)}</pre></div><p class="caption">{esc(caption)}</p>')
        md.extend(['```mermaid', code.rstrip(), '```', '', caption, ''])
    heading(tr('Capability map', '能力地圖'), 'map')
    img, alt = spec['map_image'], spec['map_alt']
    blocks.append(f'<figure class="map-image"><a href="{esc(img)}" target="_blank" rel="noopener"><img src="{esc(img)}" alt="{esc(alt)}"></a><figcaption>{esc(spec["map_caption"])}</figcaption></figure>')
    md.extend([f'![{alt}]({img})', '', spec['map_caption'], ''])
    context = spec.get('context', [])
    for value in [context] if isinstance(context, str) else context: paragraph(value)
    heading(tr('Decision objectives', '投資需要帶來的改善'), 'objectives')
    for o in spec['objectives']:
        blocks.append(f'<h3>{esc(o["name"])}</h3><p>{inline(o.get("kpi", ""),spec)}</p><p class="meta">{esc(o.get("status", "unknown"))} {refs(o)}</p>')
        md.extend([f'### {o["name"]}', '', o.get('kpi', ''), '', f'{o.get("status", "unknown")} {mdrefs(o)}', ''])
    for point in spec.get('analysis', []):
        heading(point['title'], point['id'])
        for value in point['paragraphs']: paragraph(value)
        if not any('[[' in p for p in point['paragraphs']): blocks.append(f'<p class="refs">{refs(point)}</p>')
        md.extend([mdrefs(point), ''])
        if point.get('mermaid'):
            diagrams[point['id']] = point['mermaid']
            diagram(point['mermaid'], point['diagram_caption'])
    if spec.get('recommendations'):
        heading(tr('Recommended next steps', '下一步如何驗證'), 'recommendations')
        for p in spec['recommendations']:
            blocks.append(f'<h3>{esc(p["title"])}</h3>'); md.extend([f'### {p["title"]}', ''])
            for value in p['paragraphs']: paragraph(value)
            if not any('[[' in value for value in p['paragraphs']): blocks.append(f'<p class="refs">{refs(p)}</p>')
            md.extend([mdrefs(p), ''])
    heading(tr('Capability evidence and boundaries', '能力範圍與證據'), 'capabilities')
    blocks.append('<details><summary>'+tr('Open the capability register', '展開能力範圍與證據')+'</summary>')
    roles={'realizing':tr('Delivers the outcome','直接帶來成果'),'enabling':tr('Enables other capabilities','支援其他能力')}
    paces={'commodity':tr('Maintain reliable service','維持可靠服務'),'keep_up':tr('Monitor and improve','持續監測與修正'),'differentiating':tr('Test an improvement','試驗改善做法'),'unknown':tr('Needs assessment','需要進一步評估')}
    objectives={o['id']:o['name'] for o in spec['objectives']}
    fields = [('scope', 'Scope', '範圍'), ('kpi', 'Measures', '觀察指標'), ('owner', 'Responsibility', '責任'), ('systems', 'Systems', '系統'), ('data_inputs', 'Data inputs', '輸入資料'), ('data_outputs', 'Data outputs', '輸出資料')]
    for c in spec['capabilities']:
        role=roles.get(c['role'],c['role'])
        blocks.append(f'<article class="capability" id="{esc(c["id"])}"><h3>{esc(c["name"])}</h3><p>{inline(c["definition"],spec)}</p><p class="meta">{esc(role)} · {esc(c.get("status", "unknown"))} {refs(c)}</p>')
        md.extend([f'### {c["name"]}', '', c['definition'], '', f'{role} · {c.get("status", "unknown")} {mdrefs(c)}', ''])
        for key, en, cn in fields:
            if c.get(key):
                blocks.append(f'<p><strong>{tr(en,cn)}:</strong> {inline(c[key],spec)}</p>'); md.extend([f'**{tr(en,cn)}:** {c[key]}', ''])
        for o in spec.get('overlays', []):
            if o['capability_id'] == c['id']:
                value = f'{objectives[o["objective_id"]]} · {paces[o["pace"]]}: {o["reason"]}'
                blocks.append(f'<p>{esc(value)} {refs(o)}</p>'); md.extend([value+' '+mdrefs(o), ''])
        blocks.append('</article>')
    blocks.append('</details>')
    if spec.get('notes'):
        heading(tr('Scope and unknowns', '範圍與待確認事項'), 'notes')
        for note in spec['notes']: paragraph(note)
    blocks.append(references_html(spec))
    md.extend([tr('## References', '## 參考資料'), ''])
    for s in spec['sources']:
        url = safe_url(s.get('url'))
        link = f'<a href="{esc(url)}">{esc(s["title"])}</a>' if url else esc(s['title'])
        md.extend([f'<a id="source-{s["id"]}"></a>', f'[{s["id"]}] '+(f'[{s["title"]}]({url})' if url else s['title'])+f' · {s.get("date", "")} · {s.get("kind", "")}', ''])
        for key,en,zh_label in [('scope','Scope','適用範圍'),('limitations','Limits','解讀限制')]:
            if s.get(key):
                md.extend([f'**{tr(en,zh_label)}：** {s[key]}',''])
    if len(diagrams) == 1:
        script = ''
    elif mermaid_js is not None:
        script = '<script>' + mermaid_js.replace('</script', '<\\/script') + '</script>'
    else:
        blocks.append('<p class="meta">'+tr('An internet connection is needed to display the diagrams.', '顯示圖形需要網路連線。')+'</p>')
        script = '<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>'
    if len(diagrams) > 1:
        script += '<script>if(window.mermaid){mermaid.initialize({startOnLoad:true,securityLevel:"strict",theme:"neutral",flowchart:{htmlLabels:false,wrappingWidth:210},themeVariables:{fontFamily:"PingFang TC, Microsoft JhengHei, sans-serif",fontSize:"17px"}});}</script>'
    page = f'<!doctype html><html lang="{esc(spec.get("language","en"))}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{CSS}</style>{STYLE}</head><body>'+''.join(blocks)+script+(SCRIPT if any(s.get('passages') for s in spec['sources']) else '')+'</body></html>'
    return page, '\n'.join(md), diagrams


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('output',type=Path,nargs='?');p.add_argument('--mermaid-js',type=Path)
    p.add_argument('--export-sources',action='store_true',help='Also export Markdown and Mermaid authoring files when explicitly requested')
    args=p.parse_args();spec=json.loads(args.input.read_text())
    out=args.output or args.input.with_suffix('.html');out.parent.mkdir(parents=True,exist_ok=True)
    validate(spec)
    if not (out.parent/spec['map_image']).is_file():
        p.error('Generate and save the capability-map image before rendering: '+spec['map_image'])
    page,md,diagrams=render(spec,args.mermaid_js.read_text() if args.mermaid_js else None)
    out.write_text(page)
    if args.export_sources:
        out.with_suffix('.md').write_text(md)
        for name,code in diagrams.items():out.with_name(out.stem+'-'+name+'.mmd').write_text(code.rstrip()+'\n')
    print(f'Wrote {out}'+(' and requested authoring exports' if args.export_sources else ''))

if __name__=='__main__': main()
