#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: patch_notification_v2_offline_harness.py <decoded-helper.sh>")

path = Path(sys.argv[1])
text = path.read_text()

old_first = """ns['post_mattermost'] = lambda payload: posts.append(payload) or True
ns['save_notification_state'] = lambda data: None
update = ns['update_notifications']
"""

new_first = """update = ns['update_notifications']
update.__globals__['post_mattermost'] = lambda payload: posts.append(payload) or True
update.__globals__['save_notification_state'] = lambda data: None
"""

old_second = """ns['post_mattermost'] = lambda payload: suppressed_posts.append(payload) or True
suppressed_durable = {'notification_model': 2, 'incidents': {}}
"""

new_second = """update.__globals__['post_mattermost'] = lambda payload: suppressed_posts.append(payload) or True
suppressed_durable = {'notification_model': 2, 'incidents': {}}
"""

if text.count(old_first) != 1:
    raise SystemExit("FIRST_HARNESS_PATTERN_GATE=FAIL")
if text.count(old_second) != 1:
    raise SystemExit("SECOND_HARNESS_PATTERN_GATE=FAIL")

text = text.replace(old_first, new_first)
text = text.replace(old_second, new_second)

path.write_text(text)

if "ns['post_mattermost'] =" in text:
    raise SystemExit("STALE_NAMESPACE_POST_MOCK_GATE=FAIL")
if "ns['save_notification_state'] =" in text:
    raise SystemExit("STALE_NAMESPACE_STATE_MOCK_GATE=FAIL")

print("OFFLINE_HARNESS_PATCH_GATE=PASS")
