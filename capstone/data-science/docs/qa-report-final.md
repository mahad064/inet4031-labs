# Lab 11 — Draft QA Test Cases

| Test | Expected result | Status |
| --- | --- | --- |
| Run `python3 generate_tickets.py` | Files generated without an exception | PASS (initial local generation) |
| Count rows in `output/tickets.csv` excluding header | At least 10,000 | PASS (10,000) |
| Check date span in `output/data_quality.csv` | At least 90 days | PASS (119 days) |
| Check every ticket has a category | 0 missing categories | PASS (initial local generation) |
| Check closed tickets have resolution timestamps and hours | 0 closed tickets missing either | PASS (initial local generation) |
| Run generator twice and compare outputs | Identical byte-for-byte files | TODO: rerun and compare |
| Query existing course PostgreSQL database | Database responds | NOT RUN — environment needs verification |
| Verify Kubernetes nodes and pods | All expected nodes/services healthy | NOT RUN — environment needs verification |
| Verify Prometheus `up` metric | Expected targets respond | NOT RUN — environment needs verification |
| Restart services and verify persistence | No unexpected data loss | NOT RUN — environment needs verification |

These first five passes reflect the provided Python generator's assertions and file creation, not checks of the course infrastructure. Update test results only after running them yourself on your chosen environment.
