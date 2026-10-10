#!/usr/bin/env python3
"""Explain native repeated-unit locations without weakening verify-html."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re

from html_workflow import PAGES, document, fragment, load, one, selected

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr'}


def whitespace(value):
    return re.sub(r'\s+', ' ', value).strip()


class OutsideText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.page, self.stack, self.nodes = 0, [], []

    def handle_starttag(self, tag, attrs):
        if tag == 'section':
            self.page = int(dict(attrs)['data-page-idx']) + 1
        if tag not in VOID:
            self.stack.append((tag, *self.getpos()))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_data(self, data):
        if (self.page not in PAGES and data.strip() and self.stack
                and not any(t in {'style', 'script'} for t, _, _ in self.stack)):
            self.nodes.append((self.page, tuple(self.stack), data.strip()))


def audit(source, target, snapshot):
    source_bytes, a = document(source)
    target_bytes, b = document(target)
    structural_equal = a.events == b.events
    css_equal = a.style_script == b.style_script
    if not structural_equal or not css_equal:
        raise ValueError('Structural events or CSS/scripts changed')
    x, y = OutsideText(), OutsideText()
    x.feed(source_bytes.decode('utf-8')); x.close()
    y.feed(target_bytes.decode('utf-8')); y.close()
    if len(x.nodes) != len(y.nodes):
        raise ValueError('Outside text-node count changed')
    units = selected(snapshot)
    expected, unexpected, spacing = [], [], 0
    for (page, stack, before), (dst_page, dst_stack, after) in zip(x.nodes, y.nodes):
        if page != dst_page or [s[0] for s in stack] != [s[0] for s in dst_stack]:
            raise ValueError('Outside text-node alignment changed')
        if whitespace(before) == whitespace(after):
            spacing += before != after
            continue
        matches = []
        for unit in units:
            src = fragment(one(unit['source']))
            dst = fragment(one(unit['target']))
            # Only complete plain-text units are classified automatically.
            if (src.events or dst.events or whitespace(''.join(src.text)) != whitespace(before)
                    or whitespace(''.join(dst.text)) != whitespace(after)):
                continue
            locations = re.findall(r'([\w.]+):(\d+)-(\d+)(?:,|$)', unit.get('location', ''))
            for tag, line, column in reversed(stack):
                if any(path.split('.')[-1] == tag and int(ln) == line and int(col) == column + 1
                       for path, ln, col in locations):
                    matches.append((unit, tag, line, column + 1))
                    break
        if len(matches) == 1:
            unit, tag, line, column = matches[0]
            expected.append({'page': page, 'id': unit['id'], 'source': before,
                             'target': after, 'tag': tag, 'line': line,
                             'native_column': column, 'native_location_exact': True})
        else:
            unexpected.append({'page': page, 'source': before, 'target': after,
                               'matched_units': len(matches)})
    return {'pass': not unexpected, 'structural_events_equal': structural_equal,
            'css_script_equal': css_equal, 'outside_text_nodes_checked': len(x.nodes),
            'serialization_whitespace_changes': spacing,
            'expected_native_repeated_units': expected,
            'unexpected_outside_changes': unexpected,
            'strict_six_page_only_check': dict(a.text) == dict(b.text),
            'note': 'Native baseline audit only; does not authorize new outside changes.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source'); p.add_argument('target'); p.add_argument('snapshot')
    args = p.parse_args()
    result = audit(args.source, args.target, load(args.snapshot))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
