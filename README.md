# Real-Time Fraud Detection System

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/fraudrt/main.py`](src/fraudrt/main.py) | HTTP handlers: `GET /healthz`, `POST /score`, `GET /events` |
| [`src/fraudrt/serve.py`](src/fraudrt/serve.py) | Functions: `clf`, `score` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`tests/test_fraud.py`](tests/test_fraud.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

To serve the FastAPI application locally, install the server separately if it is not already available:

```bash
python -m pip install uvicorn
PYTHONPATH=src python -m uvicorn fraudrt.main:app --reload
```

<!-- project-guide:end -->

Phase 2

Skills: sklearn, FastAPI, in-memory Redis stand-in, event log

Transaction → features → model → risk score → fraud/legitimate. Cache lookups; no card is charged.

```bash
pip install -r requirements.txt
pytest -q
```

Laptop proof. No hosted model. Cluster apply stays false until a human approves.
