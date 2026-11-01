import copy
import importlib.util
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'ai-opportunity-radar/scripts'))


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


bcm = module('bcm_renderer', 'bcm-creator/scripts/render_bcm_input_html.py')
matrix = module('matrix_renderer', 'ai-opportunity-radar/scripts/render_radar.py')
readiness = module('readiness_renderer', 'ai-opportunity-radar/scripts/render_readiness.py')


class RenderingBehavior(unittest.TestCase):
    def setUp(self):
        # Minimal synthetic inputs belong to the tests, not the skill resources.
        self.model = {
            'schema_version': 3, 'mode': 'map', 'company': 'Test repair service',
            'as_of': 'Test fixture', 'language': 'en', 'viewpoint': 'Service operator',
            'decision_context': 'Evaluate repeat visits.', 'context': 'Synthetic test data.',
            'objectives': [{'id': 'O1', 'name': 'Reduce repeat visits',
                            'kpi': 'Repeat-visit rate', 'status': 'proposed', 'evidence': ['S1']}],
            'capabilities': [
                {'id': 'C1', 'name': 'Repair equipment', 'level': 'L1',
                 'domain': 'Service delivery', 'role': 'realizing',
                 'definition': 'Diagnose and repair equipment.',
                 'status': 'hypothetical', 'evidence': ['S1']},
                {'id': 'C2', 'name': 'Manage repair records', 'level': 'L1',
                 'domain': 'Service information', 'role': 'enabling',
                 'definition': 'Maintain repair records.',
                 'status': 'hypothetical', 'evidence': ['S1']},
            ],
            'overlays': [], 'analysis': [], 'recommendations': [],
            'sources': [{'id': 'S1', 'title': 'Synthetic test source', 'url': '',
                         'date': 'undated', 'kind': 'hypothetical'}],
            'map_image': 'generated-capability-map.png',
            'map_alt': 'Fictional repair-company capability map',
            'map_caption': 'Synthetic renderer test image.',
        }
        self.portfolio = {
            'schema_version': 2, 'company': 'Test repair service', 'as_of': 'Test fixture',
            'objective': 'Reduce repeat visits', 'score_scale': 'Synthetic 1–5 test values.',
            'use_cases': [
                {'id': 'U1', 'name': 'Find relevant repair history',
                 'capability_id': 'C1', 'capability': 'Repair equipment', 'type': 'defend',
                 'value': 3, 'feasibility': 4, 'score_status': 'estimated',
                 'basis': 'Synthetic score for renderer testing.', 'dependencies': []},
                {'id': 'U2', 'name': 'Suggest replacement parts',
                 'capability_id': 'C1', 'capability': 'Repair equipment', 'type': 'extend',
                 'value': None, 'feasibility': None, 'score_status': 'unknown',
                 'basis': 'No evidence supplied.', 'dependencies': ['U1']},
            ],
            'readiness': [
                {'dim': name, 'current': 2 if i == 0 else None,
                 'future': 3 if i == 0 else None,
                 'score_status': 'estimated' if i == 0 else 'unknown',
                 'basis': 'Synthetic assessment.' if i == 0 else 'No assessment supplied.'}
                for i, name in enumerate(['Strategy', 'Value', 'Organization',
                                          'People and culture', 'Governance', 'Engineering', 'Data'])
            ],
        }

    def test_unknown_candidate_is_visible_without_coordinates(self):
        result = matrix.render(self.portfolio)
        self.assertIn('Suggest replacement parts', result)
        self.assertIn('1 scored candidates; 1 remain unscored', result)
        self.assertEqual(result.count('class="scored-point"'), 1)
        self.assertNotIn('AI Opportunity Radar', result)
        self.assertNotIn('<table', result)

    def test_invalid_or_unexplained_scores_fail(self):
        for value in (0, 6, float('nan'), float('inf'), True, '3'):
            p = copy.deepcopy(self.portfolio)
            p['use_cases'][0]['value'] = value
            with self.assertRaises(ValueError): matrix.render(p)
        p = copy.deepcopy(self.portfolio)
        p['use_cases'][0]['basis'] = ''
        with self.assertRaises(ValueError): matrix.render(p)
        p = copy.deepcopy(self.portfolio)
        p['use_cases'][0]['score_status'] = 'unknown'
        with self.assertRaises(ValueError): matrix.render(p)

    def test_partial_readiness_does_not_impute_missing_targets(self):
        self.portfolio['readiness'][0]['future'] = None
        result = readiness.render(self.portfolio)
        self.assertEqual(result.count('class="current"'), 1)
        self.assertEqual(result.count('class="target"'), 0)
        self.assertIn('target unknown', result)
        self.assertNotIn('<polygon', result)
        self.assertNotIn('<table', result)

    def test_unscored_chinese_report_explains_work_without_empty_charts(self):
        self.portfolio['language'] = 'zh-TW'
        self.portfolio['use_cases'][0]['data_requirements'] = '取得已授權的維修紀錄。'
        for u in self.portfolio['use_cases']:
            u.update(value=None,feasibility=None,score_status='unknown')
        for d in self.portfolio['readiness']:
            d.update(current=None,future=None,score_status='unknown')
        for result in (matrix.render(self.portfolio),readiness.render(self.portfolio)):
            self.assertNotIn('<svg',result)
            self.assertNotIn('unknown',result)
            self.assertNotIn('remain unscored',result)
        self.assertIn('需要的資料',matrix.render(self.portfolio))
        self.assertIn(self.portfolio['readiness'][0]['basis'],readiness.render(self.portfolio))

    def test_portfolio_sources_and_dependencies_use_navigable_names(self):
        self.portfolio['sources']=[{'id':'S1','title':'A source','url':'https://example.com/report','scope':'Disclosed functions','limitations':'Not measured benefit'}]
        self.portfolio['use_cases'][1]['evidence']=['S1']
        result=matrix.render(self.portfolio)
        self.assertIn('id="source-S1"',result)
        self.assertIn('href="#source-S1"',result)
        self.assertIn('href="#U1">'+self.portfolio['use_cases'][0]['name']+'</a>',result)
        self.assertIn('Not measured benefit',result)
        self.assertNotIn('&amp;#',result)
        self.portfolio['sources'][0]['url']='javascript:alert(1)'
        self.assertNotIn('href="javascript:',matrix.render(self.portfolio))

    def test_prerequisites_must_resolve_without_cycles(self):
        p = copy.deepcopy(self.portfolio)
        p['use_cases'][0]['dependencies'] = ['missing']
        with self.assertRaises(ValueError): matrix.render(p)
        p['use_cases'][0]['dependencies'] = ['U2']
        with self.assertRaises(ValueError): matrix.render(p)

    def test_base_map_unknowns_do_not_become_commodity(self):
        page, markdown, diagrams = bcm.render(self.model)
        self.assertIn('class cap0 unknown', diagrams['map'])
        self.assertNotIn('class cap0 commodity', diagrams['map'])
        self.assertNotIn('<table', page)
        self.assertIn('![Fictional repair-company capability map]', markdown)
        self.assertIn('<img src="generated-capability-map.png"', page)
        self.assertNotIn('<pre class="mermaid">', page)

    def test_overlay_is_bound_to_objective(self):
        self.model['overlays'] = [{'capability_id':'C1','objective_id':'O1','pace':'differentiating','reason':'Illustrative proposal','status':'proposed','evidence':['S1']}]
        self.assertIn('class cap0 unknown', bcm.render(self.model)[2]['map'])
        self.model['map_objective_id'] = 'O1'
        self.assertIn('class cap0 differentiating', bcm.render(self.model)[2]['map'])
        self.model['overlays'][0]['objective_id'] = 'missing'
        with self.assertRaises(ValueError): bcm.render(self.model)

    def test_missing_sources_and_lenses_are_not_hidden(self):
        self.model['capabilities'][0]['evidence'] = ['missing']
        with self.assertRaises(ValueError): bcm.render(self.model)
        self.model['capabilities'][0]['evidence'] = ['S1']
        self.model['mode'] = 'investment'
        with self.assertRaises(ValueError): bcm.render(self.model)

    def test_input_text_is_escaped_and_unsafe_urls_not_linked(self):
        self.model['context'] = '<script>alert(1)</script>'
        self.model['sources'][0]['url'] = 'javascript:alert(1)'
        page, _, _ = bcm.render(self.model)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', page)
        self.assertNotIn('href="javascript:', page)

    def test_company_judgment_can_cover_multiple_lenses_without_a_teaching_template(self):
        self.model['mode'] = 'investment'
        self.model['analysis'] = [{'id':'judgment', 'title':'A company-specific decision',
            'lenses':sorted(bcm.LENSES), 'paragraphs':['Observed company facts and a conditional investment judgment.'], 'evidence':['S1']}]
        page, markdown, diagrams = bcm.render(self.model)
        self.assertIn('Observed company facts', page)
        self.assertNotIn('<strong>Why', page)
        self.assertNotIn('<strong>Example', page)
        self.assertEqual(set(diagrams), {'map'})
        self.model['analysis'][0]['example'] = 'A generic invented factory story'
        with self.assertRaises(ValueError): bcm.render(self.model)

    def test_cli_does_not_deliver_a_page_without_its_map_image(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)/'bcm.json'
            out = Path(directory)/'index.html'
            source.write_text(json.dumps(self.model))
            result = subprocess.run([sys.executable,str(ROOT/'bcm-creator/scripts/render_bcm_input_html.py'),str(source),str(out)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('Generate and save the capability-map image',result.stderr)
            self.assertFalse(out.exists())

    def source_with_passage(self):
        return {'id':'S1','title':'Scoped service description','url':'https://example.com/service',
                'passages':[{'id':'P1','locator':'Service scope, paragraph 2',
                'excerpt':'Selected groups can apply.','context':'A service for selected groups.',
                'limits':'No measured benefit is reported.','url':'https://example.com/service#scope',
                'retrieved_at':'2026-10-31'}]}

    def test_inline_passages_preserve_source_context_across_pages(self):
        source=self.source_with_passage()
        self.model['sources']=[source]
        self.model['decision_context']='Selected groups can apply. [[S1:P1]] A trial is proposed.'
        self.portfolio['sources']=[source]
        self.portfolio['use_cases'][0]['assessment']='Selected groups can apply. [[S1:P1]]\n\nA trial is proposed.'
        self.portfolio['readiness'][0]['basis']='Selected groups can apply. [[S1:P1]]'
        outputs=[bcm.render(self.model)[0],matrix.render(self.portfolio),readiness.render(self.portfolio)]
        for result in outputs:
            self.assertIn('href="#source-S1-P1"',result)
            self.assertIn('id="source-S1-P1"',result)
            self.assertIn('A service for selected groups.',result)
            self.assertIn('No measured benefit is reported.',result)
            self.assertIn('https://example.com/service#scope',result)
            self.assertNotIn('[[S1:P1]]',result)

    def test_unknown_or_unsafe_passage_citations_fail(self):
        self.model['sources']=[self.source_with_passage()]
        for marker in ('[[S2:P1]]','[[S1:P2]]'):
            self.model['decision_context']='A claim. '+marker
            with self.assertRaises(ValueError):bcm.render(self.model)
        self.model['decision_context']='A claim. [[S1:P1]]'
        self.model['sources'][0]['passages'][0]['url']='javascript:alert(1)'
        with self.assertRaises(ValueError):bcm.render(self.model)

    def test_cited_prose_and_original_excerpt_are_escaped(self):
        source=self.source_with_passage()
        source['passages'][0]['excerpt']='<script>untrusted()</script>'
        self.portfolio['sources']=[source]
        self.portfolio['use_cases'][0]['assessment']='<img src=x onerror=untrusted()> [[S1:P1]]'
        result=matrix.render(self.portfolio)
        self.assertIn('&lt;script&gt;untrusted()&lt;/script&gt;',result)
        self.assertIn('&lt;img src=x onerror=untrusted()&gt;',result)
        self.assertNotIn('<script>untrusted()',result)
        self.assertNotIn('<img src=x',result)

    def test_document_number_preserves_multiple_passage_destinations(self):
        from passage_citations import inline
        source=self.source_with_passage()
        second=copy.deepcopy(source['passages'][0])
        second.update(id='P2',locator='Exceptions, paragraph 3',excerpt='Some applications require review.',url='https://example.com/service#exceptions')
        source['passages'].append(second)
        spec={'sources':[{'id':'S9','title':'Earlier reference'},source]}
        result=inline('A qualified claim. [[S1:P1]] [[S1:P2]]',spec)
        self.assertEqual(result.count('class="inline-citation"'),1)
        self.assertIn('>[2]</a>',result)
        self.assertIn('href="#source-S1-P1"',result)
        self.assertIn('data-passage-targets="source-S1-P1 source-S1-P2"',result)
        separate=inline('First claim. [[S1:P1]] Different claim. [[S1:P2]]',spec)
        self.assertEqual(separate.count('class="inline-citation"'),2)
        spec['passage_reference_page']='index.html'
        shared=inline('A qualified claim. [[S1:P1]] [[S1:P2]]',spec)
        self.assertIn('href="index.html?passages=source-S1-P1,source-S1-P2#source-S1-P1"',shared)

    def test_compact_references_keep_exact_excerpts_and_all_context(self):
        from passage_citations import references_html
        source=self.source_with_passage()
        source['passages'][0]['excerpt']='原文：保留限定條件。 <original>'
        result=references_html({'sources':[source]})
        self.assertIn('class="reference-list"',result)
        self.assertIn('id="source-S1"',result)
        self.assertIn('id="source-S1-P1"',result)
        self.assertIn('原文：保留限定條件。 &lt;original&gt;',result)
        self.assertIn('A service for selected groups.',result)
        self.assertIn('No measured benefit is reported.',result)
        self.assertNotIn('<details open',result)
        shared=references_html({'sources':[source],'passage_reference_page':'index.html'})
        self.assertIn('href="index.html#source-S1"',shared)
        self.assertNotIn('id="source-S1-P1"',shared)

    def test_implementation_and_readiness_preserve_paragraphs_and_citations(self):
        self.portfolio['sources']=[self.source_with_passage()]
        self.portfolio['use_cases'][0]['validation']='Keep all cases. [[S1:P1]]\n\nCount unresolved work separately.'
        self.portfolio['readiness'][0]['next_action']='Confirm the applicable document.\n\nAsk the office to resolve an exception. [[S1:P1]]'
        options=matrix.render(self.portfolio)
        ready=readiness.render(self.portfolio)
        self.assertIn('<p>Count unresolved work separately.</p>',options)
        self.assertIn('<p>Confirm the applicable document.</p>',ready)
        self.assertIn('<p>Ask the office to resolve an exception.',ready)
        for result in [options,ready]:self.assertIn('href="#source-S1-P1"',result)

    def test_standalone_citation_helpers_remain_identical(self):
        self.assertEqual((ROOT/'bcm-creator/scripts/passage_citations.py').read_bytes(),
                         (ROOT/'ai-opportunity-radar/scripts/passage_citations.py').read_bytes())


if __name__ == '__main__': unittest.main()
