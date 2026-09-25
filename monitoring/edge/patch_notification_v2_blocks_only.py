#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: patch_notification_v2_blocks_only.py <edge-monitor-script>")

path = Path(sys.argv[1])
text = path.read_text()

old_event = '''    payload = {
        "text": fallback,
        "props": {
            "mm_blocks": [
'''

new_event = '''    payload = {
        "props": {
            "mm_blocks": [
'''

if text.count(old_event) != 1:
    raise SystemExit("EVENT_PAYLOAD_PATTERN_GATE=FAIL")

text = text.replace(old_event, new_event, 1)

if '"text": fallback,' in text:
    raise SystemExit("EVENT_TOP_LEVEL_TEXT_REMOVAL_GATE=FAIL")

path.write_text(text)

print("BLOCKS_ONLY_EVENT_PAYLOAD_PATCH_GATE=PASS")
