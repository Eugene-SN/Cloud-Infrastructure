#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: patch_notification_v2_3_1_compact_heading.py <edge-monitor-script>")

path = Path(sys.argv[1])
text = path.read_text()

old = '_text_block(f"**{icon} {title}**"),'
new = '_text_block(f"#### {icon} {title}"),'

count = text.count(old)
if count != 2:
    raise SystemExit(f"TITLE_PATTERN_GATE=FAIL|count={count}")

text = text.replace(old, new)

render_start = text.index("def render_event_payload(")
render_end = text.index("\ndef post_mattermost(", render_start)
render = text[render_start:render_end]

if render.count('f"#### {icon} {title}"') != 2:
    raise SystemExit("COMPACT_HEADING_INSERTION_GATE=FAIL")

if 'f"### {icon} {title}"' in render:
    raise SystemExit("OLD_LARGE_HEADING_GATE=FAIL")

if 'f"**{icon} {title}**"' in render:
    raise SystemExit("BOLD_ONLY_TITLE_GATE=FAIL")

path.write_text(text)

print("COMPACT_HEADING_V2_3_1_PATCH_GATE=PASS")
