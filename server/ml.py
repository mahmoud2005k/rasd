"""Loads the trained stacking model and explains each prediction (Explainable AI)."""
import os

from features import extract, FEATURE_TEXT

MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.joblib"))
_bundle = None
_tried = False


def load():
    global _bundle, _tried
    if _tried:
        return _bundle
    _tried = True
    if os.getenv("DISABLE_ML"):
        print("[ml] disabled by DISABLE_ML (rules and database still work)")
        return None
    try:
        import joblib
        if os.path.exists(MODEL_PATH):
            _bundle = joblib.load(MODEL_PATH)
            print("[ml] model loaded:", MODEL_PATH)
        else:
            print("[ml] no model file yet. Train one with: python train_model.py ...")
    except Exception as e:  # missing libraries or a broken file
        print("[ml] could not load model:", e)
    return _bundle


def _contribs(b, x):
    """Per-feature push toward 'phishing'. Uses XGBoost's built-in contributions (SHAP-style);
    falls back to an approximation if XGBoost is unavailable."""
    try:
        import numpy as np
        import xgboost as xgb
        est = b["model"].named_estimators_["xgb"]
        c = est.get_booster().predict(xgb.DMatrix(np.array(x)), pred_contribs=True)[0][:-1]
        return [float(v) for v in c]
    except Exception:
        imp, mean, std = b["importance"], b["means"], b["stds"]
        return [imp[i] * ((x[0][i] - mean[i]) / (std[i] or 1.0)) for i in range(len(b["features"]))]


def predict(url):
    b = load()
    if b is None:
        return None
    names = b["features"]
    f = extract(url)
    x = [[float(f[n]) for n in names]]
    p = float(b["model"].predict_proba(x)[0][1])
    contrib = _contribs(b, x)
    order = sorted(range(len(names)), key=lambda i: contrib[i], reverse=True)
    factors = []
    for i in order:
        if contrib[i] <= 0.05 or len(factors) >= 5:
            break
        n, v = names[i], f[names[i]]
        ar, en = FEATURE_TEXT.get(n, (n, n))
        if n == "is_https":
            if v:  # has HTTPS: not a risk factor
                continue
        else:
            val = round(v, 2) if isinstance(v, float) else v
            ar, en = f"{ar}: {val}", f"{en}: {val}"
        factors.append({"feature": n, "impact": round(contrib[i], 3), "ar": ar, "en": en})
    return {"probability": round(p, 4), "factors": factors}
