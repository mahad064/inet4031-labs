#!/usr/bin/env python3
"""Generate reproducible, entirely synthetic Harborlight support tickets and quality metrics."""
import csv
import random
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output'
OUT.mkdir(exist_ok=True)
RANDOM_SEED = 4031
TOTAL = 10_000
START = datetime(2026, 7, 1, 8, 0)
DAYS = 120
rng = random.Random(RANDOM_SEED)
CATEGORIES = {
    'Scanners and handhelds': ['Scanner will not connect', 'Handheld battery failure', 'Barcode scan error'],
    'Dispatch application': ['Dispatch app unavailable', 'Dispatch data not syncing', 'Assignment screen frozen'],
    'Printers and labels': ['Label printer jam', 'Shipping label unreadable', 'Printer offline'],
    'Logins and access': ['Account locked', 'Password reset needed', 'Access permission denied'],
    'Network': ['Depot Wi-Fi outage', 'Slow network', 'VPN connection dropped'],
}
rows = []
for i in range(TOTAL):
    # More weekday tickets and modest growth over time: intentionally modeled patterns.
    while True:
        day = rng.randrange(DAYS)
        date = START + timedelta(days=day)
        weekday_factor = 1.5 if date.weekday() < 5 else 0.5
        growth_factor = 0.75 + 0.5 * day / (DAYS - 1)
        if rng.random() < (weekday_factor * growth_factor) / 2.0:
            break
    hour = rng.choices([8, 10, 13, 15, 19, 23], weights=[18, 25, 26, 18, 9, 4])[0]
    created = date.replace(hour=hour, minute=rng.randrange(60), second=rng.randrange(60))
    category = rng.choices(list(CATEGORIES), weights=[27, 24, 19, 18, 12])[0]
    age_days = (START + timedelta(days=DAYS) - created).total_seconds() / 86400
    status = rng.choices(['closed', 'in_progress', 'open'], weights=[90, 6, 4] if age_days > 7 else [58, 22, 20])[0]
    if status == 'closed':
        category_scale = {'Scanners and handhelds': 3.0, 'Dispatch application': 5.5,
                          'Printers and labels': 2.0, 'Logins and access': 1.2, 'Network': 7.0}[category]
        resolution_hours = round(max(0.1, rng.lognormvariate(0.0, 0.85) * category_scale), 2)
        resolved_at = created + timedelta(hours=resolution_hours)
        # Resolve before the end of the synthetic observation window.
        if resolved_at >= START + timedelta(days=DAYS):
            status = 'in_progress'
            resolved_at_text = ''
            resolution_text = ''
        else:
            resolved_at_text = resolved_at.isoformat(timespec='seconds')
            resolution_text = str(resolution_hours)
    else:
        resolved_at_text = ''
        resolution_text = ''
    rows.append({'id': i + 1, 'title': rng.choice(CATEGORIES[category]),
                 'description': 'Synthetic incident for an example logistics support desk',
                 'category': category, 'status': status,
                 'created_at': created.isoformat(timespec='seconds'),
                 'resolved_at': resolved_at_text, 'resolution_hours': resolution_text})
rows.sort(key=lambda r: (r['created_at'], r['id']))
fields = ['id','title','description','category','status','created_at','resolved_at','resolution_hours']
with (OUT / 'tickets.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

missing = {field: sum(not r[field] and r[field] != 0 for r in rows) for field in fields}
closed = [r for r in rows if r['status'] == 'closed']
assert len(rows) >= 10000
assert (datetime.fromisoformat(max(r['created_at'] for r in rows)) - datetime.fromisoformat(min(r['created_at'] for r in rows))).days >= 90
assert all(r['category'] for r in rows)
assert all(r['resolved_at'] and r['resolution_hours'] for r in closed)
metrics = [('total_rows', len(rows)), ('closed_rows', len(closed)),
           ('open_rows', sum(r['status'] == 'open' for r in rows)),
           ('in_progress_rows', sum(r['status'] == 'in_progress' for r in rows)),
           ('earliest_created_at', min(r['created_at'] for r in rows)),
           ('latest_created_at', max(r['created_at'] for r in rows)),
           ('date_span_days', (datetime.fromisoformat(max(r['created_at'] for r in rows)) - datetime.fromisoformat(min(r['created_at'] for r in rows))).days)]
metrics.extend((f'missing_{field}', count) for field, count in missing.items())
with (OUT / 'data_quality.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['metric', 'value'])
    writer.writerows(metrics)
print(f"Created {len(rows):,} synthetic tickets in {OUT / 'tickets.csv'}")
print(f"Closed tickets: {len(closed):,}; date span: {dict(metrics)['date_span_days']} days")
print(f"Data-quality report: {OUT / 'data_quality.csv'}")
