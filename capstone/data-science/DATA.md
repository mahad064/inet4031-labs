# Lab 11 — Synthetic Incident Data Plan

## Purpose
Harborlight Logistics' fictional Support Desk has six agents. This project will explore incident volume, incident categories, and resolution time to support a later staffing recommendation. **All tickets are synthetic; no real customer or employee information is used.**

## Generation method
`generate_tickets.py` creates 10,000 records across a 120-day window beginning July 1, 2026, with a fixed random seed (4031). It writes `output/tickets.csv` and `output/data_quality.csv`. Each row includes an ID, title, fictional description, category, status, creation time, and — only for closed tickets — resolution timestamp and duration.

The five categories are scanners/handhelds, dispatch application, printers/labels, logins/access, and network. Titles correspond to those categories. The generator deliberately models higher weekday and work-hour volume and slight growth, so those trends are **assumptions built into the fake data**, not discoveries about real Harborlight operations. Resolution durations are skewed, with different typical durations across categories. Recent tickets are more likely to remain unresolved.

## Data location and limits
For the fastest initial setup, the Week 11 dataset is generated and analyzed **from a local CSV**, without altering the existing PostgreSQL database or Kubernetes cluster. This is permitted by the track's Local VM guidance when the approach is documented. It does not replace the required environment checkpoint or later pipeline work.

Because the data is invented, it **cannot prove that Harborlight needs more staff**. Any later staffing recommendation must state assumed agent handling time and distinguish ticket resolution time from human working time. The script uses only Python's standard library and writes no secrets.

## Run
From the folder containing this file:

```bash
python3 generate_tickets.py
```

## Week 11 evidence
- `output/tickets.csv`: the source dataset
- `output/data_quality.csv`: totals, missing-value counts, minimum and maximum creation timestamps, date span
- `docs/qa-report-final.md`: initial test cases

**Still to complete using the actual course VM/repository:** environment-checkpoint output (web, database, Kubernetes, Prometheus), tool-version evidence, GitHub branch/pull-request and backlog where required. Do not claim these checks passed until they have been run.
