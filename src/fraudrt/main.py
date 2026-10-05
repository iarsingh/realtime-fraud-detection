from fraudrt.ops import router as ops_router
from fastapi import FastAPI, HTTPException
from fraudrt.serve import EVENTS, score
app = FastAPI(title="Real-Time Fraud Detection")
app.include_router(ops_router, prefix="/v1")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/score")
def post_score(body: dict):
    try:
        return score(body, body.get("idempotency_key"))
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

@app.get("/events")
def events():
    return {"count": len(EVENTS), "charged": False}
