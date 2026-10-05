from fraudrt.progression import fraud

def test_fraud_scores_and_caches():
    cache = {}
    a = fraud({"amount": 900, "velocity": 9, "card_id": "c1"}, cache)
    b = fraud({"amount": 10, "velocity": 1, "card_id": "c1"}, cache)
    assert a["label"] in {"fraud", "legitimate"}
    assert b["cache_hits"] == 2
    assert a["applied"] is False

