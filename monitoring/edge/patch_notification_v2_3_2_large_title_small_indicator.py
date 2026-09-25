#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: patch_notification_v2_3_2_large_title_small_indicator.py <edge-monitor-script>")

path = Path(sys.argv[1])
text = path.read_text()

old = '''            _text_block(f"#### {icon} {title}"),
            _text_block(f"{scope} · {category}", subtle=True, size="small"),
'''

new = '''            _text_block(f"### {title}"),
            _text_block(f"{icon} {scope} · {category}", subtle=True, size="small"),
'''

count = text.count(old)
if count != 2:
    raise SystemExit(f"TITLE_SCOPE_PATTERN_GATE=FAIL|count={count}")

text = text.replace(old, new)

render_start = text.index("def render_event_payload(")
render_end = text.index("\ndef post_mattermost(", render_start)
render = text[render_start:render_end]

if render.count('f"### {title}"') != 2:
    raise SystemExit("LARGE_TITLE_INSERTION_GATE=FAIL")

if render.count('f"{icon} {scope} · {category}"') != 2:
    raise SystemExit("SMALL_INDICATOR_SCOPE_GATE=FAIL")

if 'f"#### {icon} {title}"' in render:
    raise SystemExit("OLD_COMPACT_HEADING_GATE=FAIL")

if '"type": "column_set"' in render:
    raise SystemExit("MOBILE_LAYOUT_REGRESSION_GATE=FAIL")

path.write_text(text)

print("LARGE_TITLE_SMALL_INDICATOR_V2_3_2_PATCH_GATE=PASS")
