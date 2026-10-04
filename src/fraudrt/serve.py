from functools import lru_cache
from sklearn.ensemble import GradientBoostingClassifier
CACHE = {}
EVENTS = []
FEATURES = ["amount", "foreign", "velocity"]

@lru_cache(maxsize=1)
def clf():
    X = [[12,0,1],[20,0,1],[900,1,8],[40,0,2],[1100,1,9],[15,0,1],[800,1,7],[30,0,1]]
    y = [0,0,1,0,1,0,1,0]
    m = GradientBoostingClassifier(random_state=0)
    m.fit(X, y)
    return m

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
