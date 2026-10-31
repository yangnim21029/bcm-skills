"""Shared validation and prose output for portfolio charts."""
import html
import math
import re
from passage_citations import inline, validate_passages, passage_html, citation_link, references_html, STYLE, SCRIPT

CSS='''*{box-sizing:border-box}body{max-width:1000px;margin:32px auto;padding:30px;color:#24333f;font:17px/1.85 -apple-system,"PingFang TC",sans-serif}h1,h2,h3{color:#193c50}h2{margin-top:36px}article{border-top:1px solid #d7e0e5;padding:18px 0}.frame{overflow-x:auto}svg{width:100%;min-width:640px;height:auto}p{overflow-wrap:anywhere}.meta{color:#63717c;font-size:15px}details{margin:20px 0;padding:12px 16px;border:1px solid #d7e0e5;border-radius:4px}summary{cursor:pointer;color:#193c50;font-weight:600}summary:focus-visible{outline:2px solid #365a70;outline-offset:4px}@media(max-width:640px){body{margin:0;padding:20px}}'''
COLORS={'defend':'#365a70','extend':'#ad7935','upend':'#765493','unclassified':'#777'}
STATUSES={'user_supplied','documented','estimated','unknown'}


def esc(v): return html.escape(str(v),quote=True)


def paragraphs(value,spec):
    return ''.join(f'<p>{inline(p.strip(),spec)}</p>' for p in re.split(r'\n\s*\n',value) if p.strip())


def tr(spec,en,zh):
    return zh if spec.get('language','en').startswith('zh') else en


def score_status(spec,value):
    labels={'user_supplied':('User supplied','使用者提供'),'documented':('Documented','有文件依據'),'estimated':('Estimate','估計'),'unknown':('Needs assessment','待評估')}
    return tr(spec,*labels.get(value,(value,value)))


def dimension(spec,value):
    labels={'Strategy':'策略','Value':'價值','Organization':'組織','People and culture':'人才與文化','Governance':'治理','Engineering':'工程整合','Data':'資料'}
    return tr(spec,value,labels.get(value,value))


def score(value):
    if value is None:return None
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not 1<=value<=5:
        raise ValueError('Scores must be finite numbers in [1,5], or null')
    return value


def provenance(item,fields):
    values=[score(item.get(k)) for k in fields]
    state=item.get('score_status','unknown')
    if state not in STATUSES:raise ValueError('Invalid score_status')
    if any(v is not None for v in values) and (state=='unknown' or not item.get('basis')):
        raise ValueError('Numeric scores need explicit provenance and basis')


def validate(spec):
    validate_passages(spec)
    if spec.get('schema_version')!=2:raise ValueError('Use portfolio schema_version 2')
    items=spec.get('use_cases',[]); ids=set()
    for u in items:
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',u.get('id','')) or u['id'] in ids:raise ValueError('Invalid/duplicate use-case ID')
        ids.add(u['id'])
        if not u.get('capability_id'):raise ValueError('A use case needs a capability_id')
        if u.get('type','unclassified') not in COLORS:raise ValueError('Invalid business-case type')
        provenance(u,['value','feasibility'])
    graph={u['id']:u.get('dependencies',[]) for u in items}
    done=set()
    def visit(key,active):
        if key not in graph:raise ValueError('Unknown dependency '+key)
        if key in active:raise ValueError('Cyclic prerequisites')
        if key in done:return
        for dep in graph[key]:visit(dep,active|{key})
        done.add(key)
    for key in graph:visit(key,set())
    dims=set()
    for d in spec.get('readiness',[]):
        if not d.get('dim') or d['dim'] in dims:raise ValueError('Missing/duplicate readiness dimension')
        dims.add(d['dim']);provenance(d,['current','future'])
    return spec


def cards(items,spec=None):
    spec=spec or {}
    names={u['id']:u.get('name',u['id']) for u in items}
    labels={
        'problem':('What to check in current work','要確認哪些工作問題'),
        'data_requirements':('Which documents and permissions are needed','需要的資料與使用權限'),
        'execution':('What the people and the tool would do','人與工具分別會做什麼'),
        'ownership':('Who would do each job','各項工作由誰負責'),
        'authority':('Who can make decisions','誰能作出決定'),
        'validation':('How to test whether the change helps','如何確認改善是否有幫助'),
        'alternative':('What to compare with','可以比較的做法'),
    }
    out=[]
    for i,u in enumerate(items,1):
        out.append(f'<article id="{esc(u["id"])}"><h2>{i}. {esc(u.get("name",u["id"]))}</h2>')
        if u.get('assessment'):
            out.append(paragraphs(u['assessment'],spec))
        elif u.get('problem'):
            out.append(paragraphs(u['problem'],spec))
        if u.get('capability'):out.append(f'<p class="meta">{tr(spec,"Capability: ","相關能力：")}{esc(u["capability"])}</p>')
        values=[]
        for key,en,zh in [('value','Value','價值'),('feasibility','Feasibility','可行性')]:
            if u.get(key) is not None:values.append(f'{tr(spec,en,zh)}: {u[key]}')
        if values:out.append(f'<p class="meta">{esc(" · ".join(values))} · {esc(score_status(spec,u.get("score_status","unknown")))}</p>')
        if u.get('basis') and (values or not u.get('assessment')):out.append(f'<p>{inline(u["basis"],spec)}</p>')
        if u.get('dependencies'):out.append('<p>'+tr(spec,'Prerequisites: ','先完成：')+', '.join(f'<a href="#{esc(d)}">{esc(names[d])}</a>' for d in u['dependencies'])+'</p>')
        detail=[]
        for k,label in labels.items():
            if k=='problem' and not u.get('assessment'):continue
            if u.get(k):
                separator=tr(spec,':','：')
                chunks=[p.strip() for p in re.split(r'\n\s*\n',u[k]) if p.strip()]
                if not chunks:continue
                detail.append(f'<p><strong>{esc(tr(spec,*label))}{separator}</strong> {inline(chunks[0],spec)}</p>')
                detail.extend(f'<p>{inline(chunk,spec)}</p>' for chunk in chunks[1:])
        if detail:
            summary=tr(spec,'How to run and check the trial','如何執行與檢查試驗')
            out.append(f'<details><summary>{esc(summary)}</summary>'+''.join(detail)+'</details>')
        if u.get('evidence'):
            source_ids={s.get('id') for s in spec.get('sources',[]) if isinstance(s,dict)}
            refs=' '.join(citation_link(s,spec) if s in source_ids else esc(s) for s in u['evidence'])
            out.append('<p class="meta">'+tr(spec,'Sources: ','來源：')+refs+'</p>')
        out.append('</article>')
    return ''.join(out)


def page(spec,title,body):
    notes=''.join(f'<p>{inline(n,spec)}</p>' for n in spec.get('notes',[]))
    sources=references_html(spec)
    scale=f'<p>{esc(spec["score_scale"])}</p>' if spec.get('score_scale') else ''
    script=SCRIPT if any(isinstance(s,dict) and s.get('passages') for s in spec.get('sources',[])) else ''
    return f'<!doctype html><html lang="{esc(spec.get("language","en"))}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(spec.get("company",""))} — {esc(title)}</title><style>{CSS}</style>{STYLE}</head><body><h1>{esc(spec.get("company",""))} — {esc(title)}</h1><p class="meta">{esc(spec.get("as_of",""))}</p><p>{inline(spec.get("objective",""),spec)}</p>{scale}{body}{notes}{sources}{script}</body></html>'
