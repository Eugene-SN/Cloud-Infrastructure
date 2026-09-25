#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: patch_notification_v2_2_event_columns.py <edge-monitor-script>")

path = Path(sys.argv[1])
text = path.read_text()

old_recovery = '''        columns = [
            _metric_column("DURATION", duration),
            _metric_column("RECOVERED", _fmt_time(ended_at or iso_now())),
            _metric_column("STATUS", event_class),
        ]
'''

new_recovery = '''        columns = [
            _metric_column("DURATION", duration),
            _metric_column("RECOVERED", _fmt_time(ended_at or iso_now())),
        ]
'''

old_incident = '''        confirmation = incident.get("confirmation") or "transition confirmed"
        fallback = (
            f"{icon} **{title}**\\n"
            f"{scope} · {category}\\n"
            f"{impact}\\n"
            f"Cause: {incident.get('cause') or 'unknown'}\\n"
            f"Started: {_fmt_time(started_at or iso_now())}"
        )
        columns = [
            _metric_column("STARTED", _fmt_time(started_at or iso_now())),
            _metric_column("STATUS", event_class),
            _metric_column("CONFIRMED", confirmation),
        ]
'''

new_incident = '''        confirmation = incident.get("confirmation")
        fallback = (
            f"{icon} **{title}**\\n"
            f"{scope} · {category}\\n"
            f"{impact}\\n"
            f"Cause: {incident.get('cause') or 'unknown'}\\n"
            f"Started: {_fmt_time(started_at or iso_now())}"
        )
        columns = [
            _metric_column("STARTED", _fmt_time(started_at or iso_now())),
        ]
        if confirmation:
            columns.append(
                _metric_column("CONFIRMED", confirmation)
            )
'''

if text.count(old_recovery) != 1:
    raise SystemExit("RECOVERY_COLUMNS_PATTERN_GATE=FAIL")

if text.count(old_incident) != 1:
    raise SystemExit("INCIDENT_COLUMNS_PATTERN_GATE=FAIL")

text = text.replace(old_recovery, new_recovery, 1)
text = text.replace(old_incident, new_incident, 1)

if '_metric_column("STATUS", event_class)' in text:
    raise SystemExit("STATUS_COLUMN_REMOVAL_GATE=FAIL")

if 'or "transition confirmed"' in text:
    raise SystemExit("GENERIC_CONFIRMATION_REMOVAL_GATE=FAIL")

path.write_text(text)

print("EVENT_COLUMNS_V2_2_PATCH_GATE=PASS")
