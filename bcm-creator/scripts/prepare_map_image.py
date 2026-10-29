#!/usr/bin/env python3
"""Prepare exact content and a shared visual prompt; does not generate an image."""
import argparse
import hashlib
import json
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]


def build_content(model, style):
    objectives = {o['id']: o for o in model.get('objectives', [])}
    objective_id = model.get('map_objective_id')
    if objective_id and objective_id not in objectives:
        raise ValueError('map_objective_id must resolve to an objective')
    capabilities = model['capabilities']
    if not capabilities:
        raise ValueError('The map needs at least one capability')
    ids = [c['id'] for c in capabilities]
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate capability IDs')
    overlays = {}
    for overlay in model.get('overlays', []):
        if overlay['capability_id'] not in ids:
            raise ValueError('Overlay refers to a missing capability')
        if overlay['objective_id'] not in objectives:
            raise ValueError('Overlay refers to a missing objective')
        key = (overlay['capability_id'], overlay['objective_id'])
        if key in overlays:
            raise ValueError('Multiple assessments for the same capability and objective')
        if overlay['pace'] not in ('commodity', 'keep_up', 'differentiating', 'unknown'):
            raise ValueError('Unknown pace value')
        overlays[key] = overlay['pace']
    domains = {}
    for cap in capabilities:
        if cap['role'] not in ('realizing', 'enabling'):
            raise ValueError('Capability role must be realizing or enabling')
        for field in ('id', 'name', 'domain'):
            if not isinstance(cap[field], str) or not cap[field].strip():
                raise ValueError(f'Capability {field} must be nonempty text')
        group = domains.setdefault(cap['domain'], {'name': cap['domain'], 'role': cap['role'], 'cells': []})
        if group['role'] != cap['role']:
            raise ValueError('A domain spans two roles; resolve its grouping before drawing')
        pace = overlays.get((cap['id'], objective_id), 'unknown') if objective_id else 'unassessed'
        group['cells'].append({'id': cap['id'], 'label': cap['name'], 'assessment': pace,
                               'fill': style['palette'][pace],
                               'text_color': '#FFFFFF' if pace == 'differentiating' else style['palette']['ink']})
    zh = model.get('language', '').lower().startswith('zh')
    labels = ({'commodity': '維持運作', 'keep_up': '持續監控', 'differentiating': '驗證新做法', 'unknown': '待確認'}
              if zh else {'commodity': 'Maintain', 'keep_up': 'Monitor', 'differentiating': 'Test improvements', 'unknown': 'Unknown'})
    legend = [{'label': labels[p], 'fill': style['palette'][p]} for p in labels] if objective_id else []
    return {'company': model['company'], 'title': model['company'] + ('｜業務能力地圖' if zh else ' | Business Capability Map'),
            'objective': objectives[objective_id]['name'] if objective_id else None,
            'subtitle': (('分析目標：' if zh else 'Working objective: ') + objectives[objective_id]['name']) if objective_id else ('業務範圍與支援能力' if zh else 'Business scope and enabling capabilities'),
            'region_labels': {'realizing': '實現客戶價值' if zh else 'Realize customer value', 'enabling': '支援營運' if zh else 'Enable operations'},
            'capability_count': len(capabilities), 'domain_count': len(domains),
            'domains': list(domains.values()), 'legend': legend}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    style_path = SKILL / 'assets/capability-map-style.json'
    style = json.loads(style_path.read_text())
    reference = style_path.parent / style['reference']
    content = build_content(json.loads(args.input.read_text()), style)
    manifest = {'style_version': style['version'], 'style': style,
                'reference': {'path': str(reference), 'sha256': hashlib.sha256(reference.read_bytes()).hexdigest(), 'role': 'edit target: preserve visual grammar; replace all business content'},
                'model_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(), 'content': content}
    template = (SKILL / 'references/map-image-prompt.txt').read_text()
    prompt = template + 'CONTENT:\n' + json.dumps(content, ensure_ascii=False, indent=2) + '\n'
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'map-content.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (args.output_dir / 'map-prompt.txt').write_text(prompt)
    print(f"Prepared {content['capability_count']} capabilities in {content['domain_count']} domains at {args.output_dir}")


if __name__ == '__main__':
    main()
