#!/usr/bin/env python3
"""Deterministic local planning and preservation checks; no network or publication."""
import argparse
from collections import Counter, defaultdict
import hashlib
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

POSITIONS = set(range(3, 70)) | set(range(170, 211))
PAGES = {1, 2, 3, 9, 10, 11}
COUNTS = {'section': 64, 'img': 55, 'table': 51, 'tr': 359, 'td': 1457}
SOURCE_SHA256 = '28c83bd6bb8afb9a056f1f6182f9fa4b93fab2d5935e9f3d09f8a3f5490082e7'
CJK = re.compile(r'[\u3400-\u9fff]')
BR = re.compile(r'<br\s*/?>', re.I)
NUMBERS = re.compile(r'(\d+(?:[.,]\d+)*)(?:\s*(%|GHz|MHz|GB|TB|W)(?![A-Za-z]))?', re.I)
PROSE = {'p', 'li', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def one(value):
    if isinstance(value, list):
        if len(value) != 1:
            raise ValueError('Pilot supports single-form HTML units only')
        return value[0]
    if not isinstance(value, str):
        raise ValueError('Expected a string or single-form Weblate array')
    return value


class Fragment(HTMLParser):
    def __init__(self, wrapped=False):
        super().__init__(convert_charrefs=True)
        self.events, self.text = [], []
        self.wrapped = wrapped

    def handle_starttag(self, tag, attrs):
        if tag == 'br' and self.wrapped:
            self.text.append('\n')
        else:
            self.events.append(('start', tag, sorted(attrs)))
            if tag == 'br':
                self.text.append('\n')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag != 'br':
            self.events.append(('end', tag))

    def handle_endtag(self, tag):
        self.events.append(('end', tag))

    def handle_data(self, data):
        self.text.append(data)


def fragment(text, wrapped=False):
    p = Fragment(wrapped)
    p.feed(text)
    p.close()
    return p


def normalized(text):
    text = unescape(text)
    text = re.sub(r'(?<=[\u3400-\u9fff])\s+|\s+(?=[\u3400-\u9fff])', '', text)
    return re.sub(r'\s+', ' ', text).strip()


def key(unit):
    p = fragment(one(unit['source']), unit.get('wrapped_prose', False))
    return json.dumps([p.events, normalized(''.join(p.text))], ensure_ascii=False)


def selected(snapshot):
    if snapshot.get('translation_id') != 10 or snapshot.get('language') != 'en':
        raise ValueError('Wrong translation/language for the accepted pilot')
    if snapshot.get('component') != 'lp2468-wr6220-g5-html':
        raise ValueError('Wrong component')
    units = [u for u in snapshot['units'] if u['position'] in POSITIONS]
    if len(units) != 108 or len({u['id'] for u in units}) != 108:
        raise ValueError('Expected exactly 108 unique pilot units')
    if {u['position'] for u in units} != POSITIONS:
        raise ValueError('Pilot position set is incomplete or duplicated')
    return units


def plan(previous, current):
    old, new = selected(previous), selected(current)
    matches = defaultdict(list)
    for u in old:
        if one(u['target']).strip() and (u['state'] == 20 or u.get('verified') is True):
            matches[key(u)].append(u)
    reuse, pending, review = [], [], []
    for u in new:
        candidates = matches.get(key(u), [])
        # Multiple translations for one exact source are not an automatic match.
        targets = {one(c['target']) for c in candidates}
        common = {'id': u['id'], 'position': u['position'], 'source': one(u['source']),
                  'location': u.get('location', ''),
                  'wrapped_prose': u.get('wrapped_prose', False)}
        if len(targets) == 1:
            c = next((c for c in candidates if c['id'] == u['id']), candidates[0])
            reuse.append(dict(common, target=one(c['target']), previous_id=c['id'],
                              state=c['state'], verified=c.get('verified', False)))
        elif len(targets) > 1:
            review.append(dict(common, reason='Conflicting exact-match translations'))
        else:
            pending.append(common)
    return {'translation_id': 10, 'language': 'en', 'component': current['component'],
            'reuse': reuse, 'translate': pending, 'review': review,
            'translation_candidates': len(pending),
            'translation_requests': 0,
            'note': 'This planner makes no model calls; state-20 reuse remains draft.'}


def check_blocks(work, translations):
    expected = {str(u['id']): u for u in work['translate']}
    if set(translations) != set(expected):
        raise ValueError('Translations must cover exactly the changed blocks')
    issues = []
    for uid, u in expected.items():
        source, target = u['source'], one(translations[uid])
        wrapped = u.get('wrapped_prose', False)
        src, dst = fragment(source, wrapped), fragment(target, wrapped)
        if not target.strip() or CJK.search(''.join(dst.text)):
            issues.append([uid, 'Empty English target or Chinese text remains'])
        if src.events != dst.events:
            issues.append([uid, 'Tags/attributes/order changed'])
        if wrapped and BR.search(target):
            issues.append([uid, 'Obsolete prose wrapping was reintroduced'])
        src_numbers = Counter((n, suffix.lower()) for n, suffix in NUMBERS.findall(''.join(src.text)))
        dst_numbers = Counter((n, suffix.lower()) for n, suffix in NUMBERS.findall(''.join(dst.text)))
        if src_numbers != dst_numbers:
            issues.append([uid, 'Numbers or numeric units changed'])
        for zh, en in [('联想问天', 'Lenovo WenTian'), ('产品指南', 'Product Guide')]:
            if zh in normalized(''.join(src.text)) and en not in normalized(''.join(dst.text)):
                issues.append([uid, 'Required terminology missing: ' + en])
        if '联想问天' in source and 'ThinkSystem' in target:
            issues.append([uid, 'Server family substituted'])
    return {'pass': not issues, 'checked_blocks': len(expected), 'issues': issues,
            'semantic_review_required': True}


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.events, self.counts = [], Counter()
        self.page = 0
        self.text = defaultdict(list)
        self.style_script = []
        self.selected_text = []
        self.raw = None
        self.paragraph = None
        self.paragraph_index = Counter()
        self.breaks = Counter()

    def handle_starttag(self, tag, attrs):
        self.counts[tag] += 1
        if tag == 'section':
            value = dict(attrs).get('data-page-idx')
            if value is None:
                raise ValueError('Missing page identity')
            self.page = int(value) + 1
        if tag == 'p':
            self.paragraph_index[self.page] += 1
            self.paragraph = (self.page, self.paragraph_index[self.page])
        if tag == 'br':
            self.breaks[self.paragraph or (self.page, 'outside-p')] += 1
        else:
            self.events.append(('start', tag, attrs))
        if tag in {'style', 'script'}:
            self.raw = tag
        if self.page not in PAGES:
            self.text[self.page].append(('start', self.get_starttag_text()))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        self.events.append(('end', tag))
        if self.page not in PAGES:
            self.text[self.page].append(('end', tag))
        if tag in {'style', 'script'}:
            self.raw = None
        if tag == 'p':
            self.paragraph = None

    def handle_data(self, data):
        if self.raw:
            self.style_script.append((self.raw, data))
        if self.page not in PAGES:
            self.text[self.page].append(('text', data))
        elif not self.raw:
            self.selected_text.append(data)

    def handle_entityref(self, name):
        self.handle_data('&' + name + ';')

    def handle_charref(self, name):
        self.handle_data('&#' + name + ';')

    def handle_comment(self, data):
        self.events.append(('comment', data))


def document(path):
    data = Path(path).read_bytes()
    p = Document()
    p.feed(data.decode('utf-8'))
    p.close()
    return data, p


def verify_html(source, target, pilot=True):
    source_bytes, a = document(source)
    target_bytes, b = document(target)
    issues = []
    if a.events != b.events:
        issues.append('Non-br HTML tags/attributes/comments changed')
    if a.style_script != b.style_script:
        issues.append('CSS or scripts changed')
    if dict(a.text) != dict(b.text):
        issues.append('Content outside selected pages changed')
    delta = {str(k): a.breaks[k] - b.breaks[k] for k in a.breaks.keys() | b.breaks.keys()
             if a.breaks[k] != b.breaks[k]}
    if pilot:
        if hashlib.sha256(source_bytes).hexdigest() != SOURCE_SHA256:
            issues.append('Source hash does not match the accepted lp2468 original')
        for tag, count in COUNTS.items():
            if a.counts[tag] != count or b.counts[tag] != count:
                issues.append('Unexpected count: ' + tag)
        if (a.counts['br'], b.counts['br']) != (226, 219):
            issues.append('Unexpected br count')
        if len(delta) != 1 or not any(k.startswith('(1, ') and v == 7 for k, v in delta.items()):
            issues.append('Break removal is not confined to one page-1 paragraph')
        if CJK.search(unescape(''.join(b.selected_text))):
            issues.append('Chinese text remains on selected pages')
    return {'pass': not issues, 'issues': issues,
            'source_sha256': hashlib.sha256(source_bytes).hexdigest(),
            'target_sha256': hashlib.sha256(target_bytes).hexdigest(),
            'counts': {tag: b.counts[tag] for tag in (*COUNTS, 'br')},
            'break_delta': delta, 'visual_and_meaning_review_required': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('plan')
    p.add_argument('previous'); p.add_argument('current'); p.add_argument('--out', required=True)
    p = sub.add_parser('check-blocks')
    p.add_argument('plan'); p.add_argument('translations')
    p = sub.add_parser('verify-html')
    p.add_argument('source'); p.add_argument('target')
    args = parser.parse_args()
    if args.cmd == 'plan':
        result = plan(load(args.previous), load(args.current))
        Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({k: len(result[k]) for k in ['reuse', 'translate', 'review']}))
    else:
        result = (check_blocks(load(args.plan), load(args.translations)) if args.cmd == 'check-blocks'
                  else verify_html(args.source, args.target))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['pass'] else 1
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({'pass': False, 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
