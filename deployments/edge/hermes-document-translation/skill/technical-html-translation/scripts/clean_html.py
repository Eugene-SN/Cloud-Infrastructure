#!/usr/bin/env python3
"""Source-relative extraction, assembly and verification; never calls a model."""
import argparse
from collections import Counter
import hashlib
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re

CJK = re.compile(r'[\u3400-\u9fff]')
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr'}
LEAVES = {'p', 'li', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'figcaption'}
BR = re.compile(r'<br\s*/?>', re.I)
NUMBERS = re.compile(r'\d+(?:[.,]\d+)*')

def load(path):
    return json.loads(Path(path).read_text())

def digest(data):
    return hashlib.sha256(data).hexdigest()

class Source(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.lines = [0]
        self.lines.extend(m.end() for m in re.finditer('\n', text))
        self.stack, self.leaves, self.visible, self.pages = [], [], [], []
        self.events, self.counts = [], Counter()
        self.html_roots = []
        self.page = None

    def absolute_position(self):
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def handle_starttag(self, tag, attrs):
        raw, start = self.get_starttag_text(), self.absolute_position()
        self.events.append(('start', tag, attrs))
        self.counts[tag] += 1
        if tag == 'html':
            self.html_roots.append({'start': start, 'raw': raw, 'attrs': attrs})
        if tag == 'section' and 'docvortex-page' in dict(attrs).get('class', '').split():
            self.page = int(dict(attrs)['data-page-idx']) + 1
            self.pages.append(self.page)
        if tag not in VOID:
            self.stack.append({'tag': tag, 'attrs': attrs, 'start': start,
                               'inner_start': start + len(raw), 'page': self.page})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        self.events.append(('end', tag, []))
        if not self.stack or self.stack[-1]['tag'] != tag:
            raise ValueError('Unbalanced source HTML: ' + tag)
        node = self.stack.pop()
        node['inner_end'] = self.absolute_position()
        if tag in LEAVES and node['page'] is not None:
            raw = self.text[node['inner_start']:node['inner_end']]
            if CJK.search(raw):
                if any(n['tag'] in LEAVES for n in self.stack):
                    return
                node['source_html'] = raw
                self.leaves.append(node)
        if tag == 'section':
            self.page = None

    def handle_data(self, data):
        if self.page is not None and not any(n['tag'] in {'script', 'style'} for n in self.stack):
            self.visible.append((self.absolute_position(), data))

def parse(text):
    p = Source(text)
    p.feed(text)
    p.close()
    if p.stack:
        raise ValueError('Unclosed HTML nodes')
    return p

class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text, self.events = [], []
    def handle_starttag(self, tag, attrs):
        self.events.append(('start', tag, attrs))
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)
    def handle_endtag(self, tag):
        self.events.append(('end', tag, []))
    def handle_data(self, data):
        self.text.append(data)

def fragment(text):
    p = Text()
    p.feed(text)
    p.close()
    return p

def extract(source, manifest, workdir):
    raw = Path(source).read_bytes()
    m = load(manifest)
    if not m.get('source_only') or m.get('prior_targets_provided') or m.get('translation_memory_provided'):
        raise ValueError('Clean translation requires source-only provenance')
    if digest(raw) != m['source_html_sha256']:
        raise ValueError('Source hash differs from manifest')
    doc = parse(raw.decode())
    if doc.pages != m['pages']:
        raise ValueError('Page order differs from manifest')
    units = []
    for i, n in enumerate(sorted(doc.leaves, key=lambda n: n['inner_start'])):
        units.append(dict(n, id=f'page{n["page"]:02d}-block{i:03d}',
                          normalize_prose_wraps=n['tag'] == 'p' and 'docvortex-text' in dict(n['attrs']).get('class', '').split() and bool(BR.search(n['source_html']))))
    uncovered = [pos for pos, text in doc.visible if CJK.search(text) and not any(n['inner_start'] <= pos < n['inner_end'] for n in units)]
    if uncovered:
        raise ValueError('Chinese visible text missing from extracted blocks: ' + str(uncovered))
    w = Path(workdir)
    package = {'source': str(Path(source).resolve()), 'source_sha256': digest(raw),
               'pages': doc.pages, 'counts': dict(doc.counts), 'units': units}
    (w/'extracted.json').write_text(json.dumps(package, ensure_ascii=False, indent=2)+'\n')
    for page in doc.pages:
        page_units = [{k: n[k] for k in ['id', 'page', 'tag', 'source_html', 'normalize_prose_wraps']} for n in units if n['page'] == page]
        (w/f'page-{page:02d}.source.json').write_text(json.dumps(page_units, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'pages': doc.pages, 'blocks': len(units), 'page_blocks': dict(Counter(n['page'] for n in units)), 'prose_wrap_blocks': [n['id'] for n in units if n['normalize_prose_wraps']]}))

def assemble(extracted, translations_dir, output):
    pack = load(extracted)
    raw = Path(pack['source']).read_bytes()
    if digest(raw) != pack['source_sha256']:
        raise ValueError('Source changed')
    source_doc = parse(raw.decode())
    if len(source_doc.html_roots) != 1 or source_doc.html_roots[0]['raw'] != '<html lang="und">':
        raise ValueError('Expected accepted DocVortex source root <html lang="und">')
    root = source_doc.html_roots[0]
    targets = {}
    for page in pack['pages']:
        page_path = Path(translations_dir)/f'page-{page:02d}.en.json'
        try:
            chunk = load(page_path)
        except json.JSONDecodeError as exc:
            raise ValueError('Malformed translation JSON in ' + str(page_path) + ': ' + str(exc)
                             + '. Correct only your current page JSON. '
                             + pack.get('translation_json_recovery_hint', 'Preserve every source block ID and JSON entry delimiter; do not change source, extraction or validator.')) from exc
        if not isinstance(chunk, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in chunk.items()):
            raise ValueError('Each translation must map local block IDs to English HTML strings')
        if targets.keys() & chunk.keys():
            raise ValueError('Duplicate translation IDs')
        targets.update(chunk)
    expected = {n['id'] for n in pack['units']}
    if targets.keys() != expected:
        raise ValueError('Translation coverage differs: missing ' + str(sorted(expected-targets.keys())) + ' extra ' + str(sorted(targets.keys()-expected)))
    issues, quantity_flags, wrap_removals, numeric_equivalences = [], [], [], []
    for n in pack['units']:
        target = targets[n['id']]
        src, dst = fragment(n['source_html']), fragment(target)
        source_events = src.events
        remove_indices = n.get('remove_br_indices', [])
        if n['normalize_prose_wraps']:
            remove_indices = list(range(len(BR.findall(n['source_html']))))
        if remove_indices:
            br_index, source_events = 0, []
            for event in src.events:
                if event[1] == 'br':
                    keep = br_index not in remove_indices
                    br_index += 1
                else:
                    keep = True
                if keep:
                    source_events.append(event)
            wrap_removals.append({'id': n['id'], 'tag': n['tag'],
                                  'removed_br': len(remove_indices), 'removed_br_indices': remove_indices,
                                  'reason': n.get('normalization_reason', 'Continuous prose PDF line wrapping')})
        if source_events != dst.events:
            issues.append({'id': n['id'], 'reason': 'Inline markup/attributes changed, or audited PDF wraps retained',
                           'required_remove_br_indices': remove_indices,
                           'expected_inline_events': source_events, 'actual_inline_events': dst.events,
                           'required_inline_structure': n.get('required_inline_structure'),
                           'source_html': n['source_html'],
                           'diagnostic': n.get('diagnostic', 'Only audited br tags may be removed. Retain every original non-br inline tag and attribute. Correct the English JSON, not source/extraction/helper.'),
                           'normalization_notes': pack.get('normalization_notes')})
        if CJK.search(''.join(dst.text)):
            issues.append({'id': n['id'], 'reason': 'Chinese text remains'})
        src_text, dst_text = ''.join(src.text), ''.join(dst.text)
        if n.get('meaning_review_issue') and re.search(n['meaning_review_issue']['reject_target_pattern'], dst_text, re.I):
            issues.append({'id': n['id'], 'reason': n['meaning_review_issue']['reason'],
                           'operator_update': 'Correct your own English translation against the Chinese source; do not reuse prior targets.'})
        a, b = Counter(NUMBERS.findall(src_text)), Counter(NUMBERS.findall(dst_text))
        for rule in n.get('numeric_source_word_equivalences', []):
            count = src_text.count(rule['source_quote'])
            if count != 1 or NUMBERS.search(rule['source_quote']):
                raise ValueError('Source word-number equivalence lacks unique word evidence')
            a[rule['number']] += count
            numeric_equivalences.append({'id': n['id'], 'source_quote': rule['source_quote'],
                                         'source_number': rule['number'], 'count': count})
        for rule in n.get('numeric_word_equivalences', []):
            if rule['source_quote'] not in src_text:
                raise ValueError('Numeric equivalence lacks source evidence')
            count = len(re.findall(rule['target_pattern'], dst_text, re.I))
            if count:
                b[rule['number']] += count
                numeric_equivalences.append({'id': n['id'], 'source_quote': rule['source_quote'],
                                             'target_pattern': rule['target_pattern'], 'number': rule['number'], 'count': count})
        if '双路' in src_text and re.search(r'\b2[- ]socket\b', dst_text, re.I):
            a['2'] += src_text.count('双路')
        if a != b:
            quantity_flags.append({'id': n['id'], 'source_numbers': dict(a), 'target_numbers': dict(b)})
        if '联想问天' in src_text and 'Lenovo WenTian' not in dst_text:
            issues.append({'id': n['id'], 'reason': 'Required Lenovo WenTian family changed'})
        if '产品指南' in src_text and 'Product Guide' not in dst_text:
            issues.append({'id': n['id'], 'reason': 'Required Product Guide wording changed'})
    if issues:
        raise ValueError(json.dumps(issues, ensure_ascii=False))
    text = raw.decode()
    for n in sorted(pack['units'], key=lambda n: n['inner_start'], reverse=True):
        text = text[:n['inner_start']] + targets[n['id']] + text[n['inner_end']:]
    if text[root['start']:root['start'] + len(root['raw'])] != root['raw']:
        raise ValueError('Source root changed during fragment assembly')
    text = text[:root['start']] + '<html lang="en">' + text[root['start'] + len(root['raw']):]
    doc = parse(text)
    remaining = [{'offset': pos, 'text': data} for pos, data in doc.visible if CJK.search(data)]
    if remaining:
        raise ValueError('Untranslated visible Chinese: ' + str(remaining))
    removals = sum(n['removed_br'] for n in wrap_removals)
    expected_counts = Counter(pack['counts'])
    expected_counts['br'] -= removals
    if doc.counts != expected_counts or doc.pages != pack['pages']:
        raise ValueError('Document structure/counts changed')
    no_br = lambda events: [e for e in events if e[1] != 'br']
    expected_events = [('start', 'html', [('lang', 'en')]) if e == ('start', 'html', [('lang', 'und')]) else e
                       for e in source_doc.events]
    if no_br(expected_events) != no_br(doc.events):
        raise ValueError('Document tags/attributes changed')
    Path(output).write_text(text)
    result = {'pass': not quantity_flags, 'structural_pass': True, 'pages': doc.pages,
              'translated_blocks': len(targets), 'source_sha256': pack['source_sha256'],
              'output_sha256': digest(text.encode()), 'counts': dict(doc.counts),
              'normalized_wrap_blocks': wrap_removals, 'numeric_review_flags': quantity_flags,
              'verified_numeric_word_equivalences': numeric_equivalences,
              'remaining_visible_chinese': remaining,
              'all_bytes_outside_translated_inner_fragments_preserved': False,
              'all_bytes_outside_translated_inner_fragments_preserved_except_declared_metadata': True,
              'metadata_exceptions': [{'type': 'html-language', 'source_tag': root['raw'],
                                       'target_tag': '<html lang="en">',
                                       'source_byte_offset': len(raw.decode()[:root['start']].encode())}],
              'meaning_and_browser_review_required': True,
              'review_input_notice': pack.get('review_input_notice')}
    Path(output).with_suffix('.checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result['pass'] else 1

def check_review(extracted, review):
    pack, report = load(extracted), load(review)
    expected = {n['id'] for n in pack['units']}
    ids = report.get('checked_block_ids', [])
    if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids):
        raise ValueError('checked_block_ids must be an array of local extraction IDs')
    issues = []
    if len(ids) != len(set(ids)):
        issues.append('Duplicate checked IDs')
    if set(ids) != expected:
        issues.append('Missing/extra checked IDs')
    if report.get('checked_pages') != pack['pages']:
        issues.append('Page coverage differs from source manifest')
    result = {'pass': not issues, 'checked_blocks': len(set(ids) & expected),
              'missing_ids': sorted(expected - set(ids)), 'extra_ids': sorted(set(ids) - expected),
              'issues': issues, 'coverage_does_not_approve_meaning': True}
    print(json.dumps(result))
    return 0 if result['pass'] else 1

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='cmd', required=True)
    e = sub.add_parser('extract')
    e.add_argument('source'); e.add_argument('manifest'); e.add_argument('workdir')
    a = sub.add_parser('assemble')
    a.add_argument('extracted'); a.add_argument('translations_dir'); a.add_argument('output')
    r = sub.add_parser('check-review')
    r.add_argument('extracted'); r.add_argument('review')
    args = p.parse_args()
    if args.cmd == 'extract':
        extract(args.source, args.manifest, args.workdir)
    elif args.cmd == 'assemble':
        return assemble(args.extracted, args.translations_dir, args.output)
    else:
        return check_review(args.extracted, args.review)

if __name__ == '__main__':
    raise SystemExit(main())
