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
        self.model = json.loads((ROOT / 'bcm-creator/references/example-bcm-input.json').read_text())
        self.portfolio = json.loads((ROOT / 'ai-opportunity-radar/references/example-portfolio.json').read_text())

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


if __name__ == '__main__': unittest.main()
