#!/usr/bin/env python3
"""Turns the psql -At output of export-suburb-stats.sql into suburb-stats.json.

Usage:  psql "$DATABASE_URL" -At -f tools/export-suburb-stats.sql | python3 -I tools/stats-to-json.py > tools/suburb-stats.json
"""
import json
import sys

rows = []
for line in sys.stdin:
    line = line.rstrip("\n")
    if not line.strip():
        continue
    parts = line.split("|")
    # top_categories is itself pipe-joined, so take the ends and rejoin the middle
    if len(parts) < 6:
        sys.stderr.write("skipping malformed row: %r\n" % line)
        continue
    suburb, incidents = parts[0], parts[1]
    centre_lat, centre_lon, most_recent = parts[-3], parts[-2], parts[-1]
    top = [c for c in parts[2:-3] if c]
    rows.append({
        "suburb": suburb,
        "incidents_12mo": int(incidents),
        "top_categories": top,
        "centre": [float(centre_lat), float(centre_lon)],
        "most_recent": most_recent,
    })

rows.sort(key=lambda r: -r["incidents_12mo"])
json.dump({"generated_from": "incident_alerts, last 12 months, >=12 incidents",
           "suburbs": rows}, sys.stdout, indent=2)
sys.stdout.write("\n")
sys.stderr.write("%d suburbs passed the >=12 incident gate\n" % len(rows))
