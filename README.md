# Real-Time Fraud Detection System

Phase 2

Skills: sklearn, FastAPI, in-memory Redis stand-in, event log

Transaction → features → model → risk score → fraud/legitimate. Cache lookups; no card is charged.

```bash
pip install -r requirements.txt
pytest -q
```

Laptop proof. No hosted model. Cluster apply stays false until a human approves.
