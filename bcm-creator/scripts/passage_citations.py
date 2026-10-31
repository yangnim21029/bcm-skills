"""Passage-level citations shared by the standalone BCM skills."""
import html
import re
from urllib.parse import urlsplit

TOKEN = re.compile(r'\[\[([A-Za-z][A-Za-z0-9_-]*):([A-Za-z][A-Za-z0-9_-]*)\]\]')
IDENT = re.compile(r'[A-Za-z][A-Za-z0-9_-]*')

def escape(value):
    return html.escape(str(value), quote=True)

def safe_url(value):
    if not isinstance(value, str):
        return ''
    return value if urlsplit(value).scheme.lower() in ('http', 'https') else ''

def passage_index(spec):
    return {(s['id'], p['id']): (s, p)
            for s in spec.get('sources', []) if isinstance(s, dict)
            for p in s.get('passages', [])}

def source_numbers(spec):
    return {s['id']: i for i, s in enumerate(spec.get('sources', []), 1) if isinstance(s, dict)}

def citation_link(sid, spec, pids=()):
    number = source_numbers(spec).get(sid)
    if number is None:
        return escape(sid)
    source = next(s for s in spec['sources'] if isinstance(s, dict) and s['id'] == sid)
    title = source.get('title', sid)
    targets = ['source-' + sid + '-' + pid for pid in dict.fromkeys(pids)]
    if targets:
        index = passage_index(spec)
        title += ' — ' + '; '.join(index[(sid, pid)][1]['locator'] for pid in dict.fromkeys(pids))
    page = spec.get('passage_reference_page', '')
    # Carry all selected passages across a page navigation as well as local clicks.
    query = '?passages=' + ','.join(targets) if page and len(targets) > 1 else ''
    href = page + query + '#' + (targets[0] if targets else 'source-' + sid)
    extra = ' data-passage-targets="' + escape(' '.join(targets)) + '"' if len(targets) > 1 else ''
    kind = 'inline-citation' if targets else 'source-citation'
    return ('<sup class="citation"><a class="' + kind + '" href="' + escape(href)
            + '" aria-label="' + escape(title) + '" title="' + escape(title) + '"' + extra
            + '>[' + str(number) + ']</a></sup>')

def validate_passages(spec):
    target = spec.get('passage_reference_page', '')
    if target and not re.fullmatch(r'[A-Za-z0-9_-]+\.html', target):
        raise ValueError('passage_reference_page must be a relative HTML filename')
    keys = set()
    for source in spec.get('sources', []):
        if not isinstance(source, dict):
            continue
        for passage in source.get('passages', []):
            pid = passage.get('id', '')
            key = (source.get('id'), pid)
            if not IDENT.fullmatch(pid) or key in keys:
                raise ValueError('Invalid or duplicate source passage')
            keys.add(key)
            for field in ('locator', 'excerpt', 'context', 'limits', 'url', 'retrieved_at'):
                if not isinstance(passage.get(field), str) or not passage[field].strip():
                    raise ValueError('Source passage needs ' + field)
            if not safe_url(passage['url']):
                raise ValueError('Source passage needs an HTTP(S) URL')
    def walk(value):
        if isinstance(value, str):
            for key in TOKEN.findall(value):
                if key not in keys:
                    raise ValueError('Unknown source passage ' + ':'.join(key))
        elif isinstance(value, list):
            for child in value:
                walk(child)
        elif isinstance(value, dict):
            for child in value.values():
                walk(child)
    walk(spec)

def inline(value, spec):
    text = str(value)
    index = passage_index(spec)
    parts = []
    cursor = 0
    matches = list(TOKEN.finditer(text))
    i = 0
    while i < len(matches):
        match = matches[i]
        parts.append(escape(text[cursor:match.start()]))
        sid, pid = match.groups()
        if (sid, pid) not in index:
            raise ValueError('Unknown source passage ' + sid + ':' + pid)
        pids = [pid]
        end = match.end()
        while i + 1 < len(matches) and matches[i + 1][1] == sid and not text[end:matches[i + 1].start()].strip():
            i += 1
            following = matches[i]
            if following.groups() not in index:
                raise ValueError('Unknown source passage ' + ':'.join(following.groups()))
            pids.append(following[2]); end = following.end()
        parts.append(citation_link(sid, spec, pids))
        cursor = end
        i += 1
    parts.append(escape(text[cursor:]))
    return ''.join(parts)

def passage_html(source, zh=False):
    blocks = []
    for number, p in enumerate(source.get('passages', []), 1):
        key = source['id'] + '-' + p['id']
        context = '原文脈絡' if zh else 'In context'
        limits = '解讀界線' if zh else 'Interpretation boundary'
        link = '開啟原始段落' if zh else 'Open original passage'
        lang = p.get('language', 'en')
        blocks.append('<details class="source-passage" id="source-' + escape(key)
                      + '"><summary>' + escape(str(number) + '. ' + p['locator'])
                      + '</summary><blockquote lang="' + escape(lang) + '">' + escape(p['excerpt'])
                      + '</blockquote><p><strong>' + context + ':</strong> ' + escape(p['context'])
                      + '</p><p><strong>' + limits + ':</strong> ' + escape(p['limits'])
                      + '</p><p><a href="' + escape(safe_url(p['url'])) + '" target="_blank" rel="noopener">'
                      + link + '</a> · ' + escape(p['retrieved_at']) + '</p></details>')
    return ''.join(blocks)

def references_html(spec):
    if not spec.get('sources'):
        return ''
    zh = spec.get('language', 'en').startswith('zh')
    tr = lambda en, cn: cn if zh else en
    rows = []
    for source in spec['sources']:
        if not isinstance(source, dict):
            rows.append('<li>' + escape(source) + '</li>'); continue
        sid = source['id']; title = escape(source.get('title', sid))
        url = safe_url(source.get('url'))
        link = '<a href="' + escape(url) + '" target="_blank" rel="noopener">' + title + '</a>' if url else title
        metadata = '. '.join(escape(source[k]) for k in ('author', 'publisher', 'date') if source.get(k))
        context = []
        for key, label in [('scope', tr('Scope', '適用範圍')), ('limitations', tr('Limits', '解讀界線'))]:
            if source.get(key): context.append('<p>' + label + ': ' + escape(source[key]) + '</p>')
        if spec.get('passage_reference_page') and source.get('passages'):
            context.append('<p><a href="' + escape(spec['passage_reference_page']) + '#source-' + escape(sid) + '">'
                           + tr('Read original passages and context', '查看原文段落與脈絡') + '</a></p>')
        else:
            context.append(passage_html(source, zh))
        details = ('<details class="reference-details"><summary>' + tr('Quoted passages and source context', '原文段落與來源脈絡')
                   + '</summary>' + ''.join(context) + '</details>') if any(context) else ''
        rows.append('<li id="source-' + escape(sid) + '">' + link + ('. ' + metadata if metadata else '') + '.' + details + '</li>')
    return ('<section class="references"><h2 id="sources">' + tr('References', '參考資料')
            + '</h2><ol class="reference-list">' + ''.join(rows) + '</ol></section>')

STYLE = '''<style>
sup.citation{font-size:11px;line-height:0;vertical-align:super;font-weight:400;margin:0 1px}
sup.citation a{font-size:inherit;text-decoration:none;white-space:nowrap}
.references{margin-top:42px;padding-top:16px;border-top:1px solid #d7e0e5}
.references h2{font-size:18px;margin:0 0 12px}
.reference-list{font-size:13px;line-height:1.55;padding-left:2em;margin:0}
.reference-list>li{margin:0 0 9px;scroll-margin-top:24px}
.reference-details{font-size:13px;margin:2px 0;padding:0;border:0;border-radius:0;background:none}
.reference-details>summary{font-size:12px;font-weight:400;color:#617482;cursor:pointer}
.references .source-passage{font-size:13px;line-height:1.6;margin:10px 0;padding:8px 12px;border:0;border-left:2px solid #cad6dc;border-radius:0;scroll-margin-top:24px}
.references .source-passage summary{font-size:13px;font-weight:400;cursor:pointer;overflow-wrap:anywhere}
.references p,.references blockquote{font-size:13px;line-height:1.6;margin:8px 0}
.references blockquote{padding:0 10px;border-left:2px solid #7cabbc}
.references .source-passage:target{background:#f5f8fa;border-left-color:#087e9f}
summary:focus-visible{outline:2px solid #087e9f;outline-offset:3px}
@media print{.reference-details{display:none}sup.citation a{color:inherit}}
</style>'''
SCRIPT = """<script>
(function(){
 function openTarget(id){
  const el=document.getElementById(id);if(!el)return;
  if(el.classList.contains('source-passage')){
   let node=el;while(node){if(node.tagName==='DETAILS')node.open=true;node=node.parentElement;}
  }else if(el.matches('.reference-list>li')){
   el.querySelectorAll('details').forEach(node=>node.open=true);
  }
 }
 function reveal(){
  const id=decodeURIComponent(location.hash.slice(1));
  const el=document.getElementById(id);
  if(!el||!id.startsWith('source-'))return;
  const selected=(new URLSearchParams(location.search).get('passages')||'').split(',');
  if(selected[0]===id)selected.forEach(openTarget);
  openTarget(id);
  el.scrollIntoView({block:'start'});
 }
 addEventListener('hashchange',reveal);addEventListener('load',reveal);
 document.addEventListener('click',function(e){
  const a=e.target.closest&&e.target.closest('a.inline-citation,a.source-citation');
  if(a){
   if(a.dataset.passageTargets)a.dataset.passageTargets.split(' ').forEach(openTarget);
   setTimeout(reveal,0);
  }
 });
})();
</script>"""
