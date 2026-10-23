#!/usr/bin/env python3
"""Verify the curriculum and restored study workspaces on a running server."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import parse_qs, quote, unquote, urlsplit
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.h1 = ''
        self.in_h1 = False
        self.ids = set()
        self.links = []
        self.topic_links = []
        self.track_cards = 0
        self.html = html
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1':
            self.in_h1 = True
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
            if 'track-card' in attrs.get('class', '').split():
                self.track_cards += 1
            if 'topic-row-link' in attrs.get('class', '').split():
                self.topic_links.append(attrs.get('href'))
    def handle_endtag(self, tag):
        if tag == 'h1':
            self.in_h1 = False
    def handle_data(self, data):
        if self.in_h1:
            self.h1 += data


def check(base):
    def page(path):
        url = base.rstrip('/') + path
        with urlopen(url, timeout=30) as response:
            assert response.status == 200, (path, response.status)
            assert response.url == url, f'{path} redirected to {response.url}'
            return Page(response.read().decode())
    tracks = json.loads((ROOT / 'content/curriculum/tracks.json').read_text())
    topics = [json.loads(p.read_text()) for p in (ROOT / 'content/curriculum').glob('*/*.json')]
    home = page('/')
    workspaces = {
        '/problems': 'Problems & practice',
        '/problems?plan=75': 'Problems & practice',
        '/problems?plan=150': 'Problems & practice',
        '/problems?plan=hw': 'Problems & practice',
        '/concepts': 'DSA concepts',
        '/system-design': 'System design',
        '/ai-ml': 'AI & ML',
        '/companies': 'Companies, pay & roles',
        '/companies?view=pay': 'Companies, pay & roles',
        '/companies/google': 'Google',
        '/cheat-sheets': 'Cheat sheets',
        '/roadmap': 'Study plan',
        '/tracker': 'Review queue',
        '/playground': 'Python playground',
        '/focus': 'Focus sessions',
        '/search?q=RAG': 'Search the workspace',
        '/search?q=zzzznotfound': 'Search the workspace',
        '/ai-ml?saved=1': 'Saved AI / ML lessons',
        '/ai-ml?q=autoregression': 'AI & ML',
        '/library': 'All reference material',
        '/companies/google?view=pay': 'Google',
        '/companies/dassault-sys%C3%A8tmes': 'Dassault Sysètmes',
    }
    for route, heading in workspaces.items():
        assert page(route).h1 == heading, route
    for route in ['/problems', '/concepts', '/system-design', '/ai-ml', '/companies', '/cheat-sheets', '/roadmap', '/playground', '/focus', '/tracker']:
        assert route in home.links, f'Homepage missing {route}'
    for route in ['/legacy/viewer.html', '/legacy/static/vendor/skulpt.min.js', '/runtime/skulpt.min.js', '/python-worker.js']:
        with urlopen(base.rstrip('/') + route, timeout=30) as response:
            assert response.status == 200, route
    ai_home = page('/ai-ml')
    assert ai_home.track_cards == len(tracks), 'Show each learning track exactly once'
    assert '/curriculum' not in home.links, 'Duplicate curriculum entry in navigation'
    assert len(ai_home.topic_links) == len(topics), 'AI hub must retain every lesson in its search disclosure'
    assert len([link for link in ai_home.links if link.startswith('/library/ai-ml/')]) == 5
    for old, target in [('/curriculum', '/ai-ml'), ('/curriculum?saved=1', '/ai-ml?saved=1'), ('/curriculum?q=KV+cache&track=deep-learning', '/ai-ml?q=KV+cache&track=deep-learning'), ('/?saved=1', '/ai-ml?saved=1'), ('/library/companies/google', '/companies/google')]:
        with urlopen(base.rstrip('/') + old, timeout=30) as response:
            actual = urlsplit(response.url)
            expected = urlsplit(base.rstrip('/') + target)
            assert actual.path == expected.path and parse_qs(actual.query) == parse_qs(expected.query), (old, response.url)
    for track in tracks:
        path = '/tracks/' + track['id']
        assert path in ai_home.links, f'AI hub missing {path}'
        result = page(path)
        assert result.h1 == track['title'], (path, result.h1)
        assert result.track_cards == 0, 'Track page must focus on its own lessons'
        expected = {'/topics/' + t['slug'] for t in topics if t['track'] == track['id']}
        assert set(result.topic_links) == expected, f'{path} lists the wrong lessons'
    assert '/topics/not-a-lesson' not in home.links
    titles = set()
    for topic in topics:
        result = page('/topics/' + topic['slug'])
        assert result.h1 == topic['title'], (topic['slug'], result.h1)
        titles.add(result.h1)
        for number in range(1, 7):
            assert f'block-{number}' in result.ids, f'{topic["slug"]}: missing block {number}'
        for section in topic['explanations']:
            assert section['id'] in result.ids, f'{topic["slug"]}: missing {section["id"]}'
        assert '/tracks/' + topic['track'] in result.links
        next_in_track = next((t for t in topics if t['track'] == topic['track'] and t['order'] == topic['order'] + 1), None)
        if next_in_track:
            assert '/topics/' + next_in_track['slug'] in result.links
        else:
            assert 'END OF TRACK' in result.html, topic['slug']
        if topic.get('nextTopic'):
            assert '/topics/' + topic['nextTopic'] in result.links
    assert len(titles) == len(topics), 'Distinct topics rendered duplicate headings'
    for path in ['/topics/not-a-lesson', '/tracks/not-a-track']:
        try:
            page(path)
        except HTTPError as error:
            assert error.code == 404, (path, error.code)
        else:
            raise AssertionError(f'{path} did not return 404')
    print(f'Validated {len(workspaces)} study routes, {len(tracks)} track pages, and {len(topics)} distinct topic pages: headings, assets, lesson anchors, navigation, and 404s.')

def audit_collection(base, output):
    catalog = json.loads((ROOT / 'content/indexes/study-catalog.json').read_text())
    routes = {'/companies/' + p['slug'] for p in catalog['companyProfiles']}
    routes.update('/' + n['id'] if n['id'].startswith('companies/') else '/library/' + n['id'] for n in catalog['notes'])
    routes.update('/source/' + p.relative_to(ROOT / 'content').as_posix() for p in (ROOT / 'content/dsa').rglob('*.py'))
    def inspect(route):
        with urlopen(base.rstrip('/') + quote(route, safe='/?=&'), timeout=45) as response:
            assert response.status == 200, (route, response.status)
            assert unquote(urlsplit(response.url).path) == route, (route, response.url)
            page = Page(response.read().decode())
            assert page.h1.strip(), f'{route}: no page title'
            return {'route': route, 'heading': page.h1, 'status': response.status}
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(inspect, sorted(routes)))
    report = {'collection_pages': len(results), 'company_pages': sum(r['route'].startswith('/companies/') for r in results), 'document_pages': sum(r['route'].startswith('/library/') for r in results), 'python_sources': sum(r['route'].startswith('/source/') for r in results), 'pages': results}
    Path(output).write_text(json.dumps(report, indent=2) + '\n')
    print(f"Audited all {len(results)} collection pages: {report['company_pages']} companies, {report['document_pages']} documents, {report['python_sources']} Python sources. Saved {output}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='http://127.0.0.1:3001')
    parser.add_argument('--all-content', action='store_true', help='Visit every company, reference document, and Python source page')
    parser.add_argument('--report', default='docs/learner-audit-routes.json')
    args = parser.parse_args()
    check(args.base)
    if args.all_content:
        audit_collection(args.base, args.report)
