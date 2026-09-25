#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: patch_notification_v2_3_3_restore_integrated_heading.py <edge-monitor-script>")

path = Path(sys.argv[1])
text = path.read_text()

old = '''            _text_block(f"### {title}"),
            _text_block(f"{icon} {scope} · {category}", subtle=True, size="small"),
'''

new = '''            _text_block(f"### {icon} {title}"),
            _text_block(f"{scope} · {category}", subtle=True, size="small"),
'''

count = text.count(old)
if count != 2:
    raise SystemExit(f"TITLE_SCOPE_PATTERN_GATE=FAIL|count={count}")

text = text.replace(old, new)

render_start = text.index("def render_event_payload(")
render_end = text.index("\ndef post_mattermost(", render_start)
render = text[render_start:render_end]

if render.count('f"### {icon} {title}"') != 2:
    raise SystemExit("INTEGRATED_HEADING_GATE=FAIL")

if render.count('f"{scope} · {category}"') != 2:
    raise SystemExit("SCOPE_LINE_GATE=FAIL")

if 'f"{icon} {scope} · {category}"' in render:
    raise SystemExit("INDICATOR_SCOPE_REMOVAL_GATE=FAIL")

if '"type": "column_set"' in render:
    raise SystemExit("MOBILE_LAYOUT_REGRESSION_GATE=FAIL")

path.write_text(text)

print("RESTORE_INTEGRATED_HEADING_V2_3_3_PATCH_GATE=PASS")
