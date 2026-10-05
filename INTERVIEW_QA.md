# realtime-fraud-detection — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does realtime-fraud-detection address, and what can you demonstrate?

Transaction → features → model → risk score → fraud/legitimate. Cache lookups; no card is charged.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/fraudrt/main.py`](src/fraudrt/main.py): Implementation or supporting configuration.
- [`src/fraudrt/serve.py`](src/fraudrt/serve.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`tests/test_fraud.py`](tests/test_fraud.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `score` and explain the decision it makes?

The main walkthrough here is `score(tx, idempotency_key=None)` in [`src/fraudrt/serve.py`](src/fraudrt/serve.py#L15).

```python
def score(tx, idempotency_key=None):
    if idempotency_key and idempotency_key in CACHE:
        return {**CACHE[idempotency_key], "cached": True}
    for f in FEATURES:
        if not isinstance(tx.get(f), (int, float)) or isinstance(tx.get(f), bool):
            raise ValueError(f"{f} must be a number")
    proba = float(clf().predict_proba([[tx[f] for f in FEATURES]])[0][1])
    result = {"probability": round(proba, 4), "label": "fraud" if proba >= 0.5 else "legitimate", "charged": False, "cached": False}
    EVENTS.append(result)
    if idempotency_key:
        CACHE[idempotency_key] = result
    return result
```

The implementation calls `EVENTS.append`, `ValueError`, `clf`, `clf().predict_proba`, `float`, `isinstance`, `round`, `tx.get`. In an interview, trace those calls in execution order using a fixture input.

## 4. What responsibility does `clf` have?

`clf()` is defined in [`src/fraudrt/serve.py`](src/fraudrt/serve.py#L8).

Its return expressions include:

- `m`

It uses `GradientBoostingClassifier`, `lru_cache`, `m.fit`. This is the code path I would compare against the caller to explain responsibility boundaries.

## 5. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `HTTPException(422, str(exc))` in [`src/fraudrt/main.py`](src/fraudrt/main.py#L14).
- `ValueError(f'{f} must be a number')` in [`src/fraudrt/serve.py`](src/fraudrt/serve.py#L20).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 6. Which test would you use to demonstrate correctness?

[`tests/test_fraud.py`](tests/test_fraud.py#L9) contains `test_flags_risky_and_caches`:

```python
def test_flags_risky_and_caches():
    risky = {"amount": 1000, "foreign": 1, "velocity": 8, "idempotency_key": "k1"}
    a = client.post("/score", json=risky).json()
    b = client.post("/score", json=risky).json()
    safe = client.post("/score", json={"amount": 12, "foreign": 0, "velocity": 1}).json()
    assert a["label"] == "fraud" and a["charged"] is False
    assert b["cached"] is True
    assert safe["label"] == "legitimate"
    assert client.post("/score", json={"amount": 1}).status_code == 422
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 7. What HTTP interface does the code expose?

- `GET /healthz` → `healthz` in [`src/fraudrt/main.py`](src/fraudrt/main.py#L6).
- `POST /score` → `post_score` in [`src/fraudrt/main.py`](src/fraudrt/main.py#L10).
- `GET /events` → `events` in [`src/fraudrt/main.py`](src/fraudrt/main.py#L17).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 8. Where does state live, and what happens with multiple workers?

Module-level containers include `CACHE`, `EVENTS`, `FEATURES` in [`src/fraudrt/serve.py`](src/fraudrt/serve.py).

These containers belong to a Python process. Inspect which are constant fixtures and which are mutated. Mutable process state needs an explicit shared-storage or synchronization strategy before multiple workers can provide consistent behavior.

## 9. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 10. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 11. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 12. What is the input-to-output contract of `score`?

In [`src/fraudrt/serve.py`](src/fraudrt/serve.py#L15), `score(tx, idempotency_key=None)` receives the inputs. The function computes these intermediate values:

- `proba = float(clf().predict_proba([[tx[f] for f in FEATURES]])[0][1])`
- `result = {'probability': round(proba, 4), 'label': 'fraud' if proba >= 0.5 else 'legitimate', 'charged': False, 'cached': False}`

Its result is defined by:

- `result`
- `{**CACHE[idempotency_key], 'cached': True}`

## 13. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/fraudrt/serve.py`](src/fraudrt/serve.py#L15) branches on:

- `idempotency_key and idempotency_key in CACHE`
- `idempotency_key`
- `not isinstance(tx.get(f), (int, float)) or isinstance(tx.get(f), bool)`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
