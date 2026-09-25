#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: patch_notification_v2_3_mobile_vertical.py <edge-monitor-script>")

path = Path(sys.argv[1])
text = path.read_text()

old_recovery = '''        columns = [
            _metric_column("DURATION", duration),
            _metric_column("RECOVERED", _fmt_time(ended_at or iso_now())),
        ]
        body = [
            _text_block(f"### {icon} {title}\\n**{scope} · {category}**"),
            _text_block(impact),
            {"type": "column_set", "gap": "medium", "columns": columns},
        ]
'''

new_recovery = '''        body = [
            _text_block(f"**{icon} {title}**"),
            _text_block(f"{scope} · {category}", subtle=True, size="small"),
            _text_block(impact),
            {"type": "divider"},
            _text_block("DURATION", subtle=True, size="small"),
            _text_block(duration),
            _text_block("RECOVERED", subtle=True, size="small"),
            _text_block(_fmt_time(ended_at or iso_now())),
        ]
'''

old_incident = '''        columns = [
            _metric_column("STARTED", _fmt_time(started_at or iso_now())),
        ]
        if confirmation:
            columns.append(
                _metric_column("CONFIRMED", confirmation)
            )
        body = [
            _text_block(f"### {icon} {title}\\n**{scope} · {category}**"),
            _text_block(impact),
            {"type": "divider"},
            _text_block(f"**Cause**\\n{incident.get('cause') or 'Unknown cause'}"),
            {"type": "column_set", "gap": "medium", "columns": columns},
        ]
'''

new_incident = '''        body = [
            _text_block(f"**{icon} {title}**"),
            _text_block(f"{scope} · {category}", subtle=True, size="small"),
            _text_block(impact),
            {"type": "divider"},
            _text_block("CAUSE", subtle=True, size="small"),
            _text_block(incident.get("cause") or "Unknown cause"),
            {"type": "divider"},
            _text_block("STARTED", subtle=True, size="small"),
            _text_block(_fmt_time(started_at or iso_now())),
        ]
        if confirmation:
            body.extend(
                [
                    _text_block("CONFIRMED", subtle=True, size="small"),
                    _text_block(confirmation),
                ]
            )
'''

if text.count(old_recovery) != 1:
    raise SystemExit("RECOVERY_LAYOUT_PATTERN_GATE=FAIL")

if text.count(old_incident) != 1:
    raise SystemExit("INCIDENT_LAYOUT_PATTERN_GATE=FAIL")

text = text.replace(old_recovery, new_recovery, 1)
text = text.replace(old_incident, new_incident, 1)

render_start = text.index("def render_event_payload(")
render_end = text.index("\ndef post_mattermost(", render_start)
render = text[render_start:render_end]

if '"type": "column_set"' in render:
    raise SystemExit("PRODUCTION_COLUMN_SET_REMOVAL_GATE=FAIL")

if 'f"### {icon} {title}' in render:
    raise SystemExit("HEADING_TITLE_REMOVAL_GATE=FAIL")

path.write_text(text)

print("MOBILE_VERTICAL_V2_3_PATCH_GATE=PASS")
