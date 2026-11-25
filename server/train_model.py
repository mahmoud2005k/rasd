"""Trains the Stacking Ensemble: Random Forest + XGBoost (base learners) and
Logistic Regression (meta-learner), evaluated with Stratified K-Fold cross-validation.

Option 1 (two text files, one URL per line):
    python train_model.py --phish suspicious_links.txt --legit legit_links.txt
Option 2 (a labeled CSV dataset, e.g. Kaggle "Malicious URLs dataset", file malicious_phish.csv):
    python train_model.py --csv data.csv --url-col url --label-col type --phish-labels phishing --legit-labels benign --extra-phish suspicious_links.txt
"""
import argparse
import csv
import json
import random
import sys

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split

try:
    from xgboost import XGBClassifier
except ImportError:
    sys.exit("xgboost is not installed. Run: python -m pip install xgboost")

from features import MODEL_FEATURES as FEATURE_NAMES, extract

ap = argparse.ArgumentParser()
ap.add_argument("--phish")
ap.add_argument("--legit")
ap.add_argument("--csv")
ap.add_argument("--url-col", default="url")
ap.add_argument("--label-col", default="type")
ap.add_argument("--phish-labels", default="phishing")
ap.add_argument("--legit-labels", default="benign")
ap.add_argument("--n", type=int, default=5000, help="links per class")
ap.add_argument("--extra-phish", help="optional: fresh phishing links NOT used in training, to measure real-world detection")
ap.add_argument("--out", default="model.joblib")
args = ap.parse_args()


def read_txt(path):
    with open(path, encoding="utf-8-sig", errors="ignore") as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]


def read_csv(path):
    ph, lg = [], []
    pl = {x.strip().lower() for x in args.phish_labels.split(",")}
    ll = {x.strip().lower() for x in args.legit_labels.split(",")}
    with open(path, encoding="utf-8-sig", errors="ignore", newline="") as f:
        rd = csv.DictReader(f)
        cols = rd.fieldnames or []
        if args.url_col not in cols or args.label_col not in cols:
            sys.exit(f"Columns not found. Your file has: {cols}. Use --url-col and --label-col with the right names.")
        for row in rd:
            u, lab = (row.get(args.url_col) or "").strip(), (row.get(args.label_col) or "").strip().lower()
            if u and lab in pl:
                ph.append(u)
            elif u and lab in ll:
                lg.append(u)
    return ph, lg


if args.csv:
    phish, legit = read_csv(args.csv)
    if args.phish:  # phishing from your own file, legit from the CSV
        phish = read_txt(args.phish)
elif args.phish and args.legit:
    phish, legit = read_txt(args.phish), read_txt(args.legit)
else:
    sys.exit(__doc__)

rnd = random.Random(42)
phish, legit = sorted(set(phish)), sorted(set(legit))
k = min(args.n, len(phish), len(legit))
if k < 100:
    sys.exit(f"Not enough data (phishing={len(phish)}, legit={len(legit)}).")
phish, legit = rnd.sample(phish, k), rnd.sample(legit, k)
urls = phish + legit
y = np.array([1] * k + [0] * k)
X = np.array([[extract(u)[n] for n in FEATURE_NAMES] for u in urls], dtype=float)
print(f"Dataset: {k} phishing + {k} legitimate = {len(y)} links, {len(FEATURE_NAMES)} features")

# --- dataset sanity check: avoid the model learning only 'has a path = phishing'
ip, iq = FEATURE_NAMES.index("path_len"), FEATURE_NAMES.index("query_len")
has_path = lambda M: float(np.mean((M[:, ip] > 1) | (M[:, iq] > 0)))
rp, rl = has_path(X[y == 1]), has_path(X[y == 0])
print(f"Share of links with a path/query: phishing {rp:.0%} | legitimate {rl:.0%}")
sch = lambda L: sum(u.lower().startswith(("http://", "https://")) for u in L) / max(1, len(L))
www = lambda L: sum(u.lower().replace("http://", "").replace("https://", "").startswith("www.") for u in L) / max(1, len(L))
print(f"Share with explicit http(s):// prefix: phishing {sch(phish):.0%} | legitimate {sch(legit):.0%}")
print(f"Share starting with www.:               phishing {www(phish):.0%} | legitimate {www(legit):.0%}")
if abs(sch(phish) - sch(legit)) > 0.3:
    print("NOTE: the classes differ in how links are written (prefix). The scheme and www are ignored by the features for this reason.")
if abs(rp - rl) > 0.4:
    print("WARNING: the two classes differ a lot in path usage. Accuracy will look better than it is.\n"
          "         Use legit links that also have paths (see make_legit_list.py --paths or a labeled CSV).")

rf = lambda: RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
xg = lambda: XGBClassifier(n_estimators=300, max_depth=5, learning_rate=0.1, subsample=0.9, colsample_bytree=0.9,
                           eval_metric="logloss", random_state=42, n_jobs=-1)
stack = lambda: StackingClassifier(estimators=[("rf", rf()), ("xgb", xg())],
                                   final_estimator=LogisticRegression(max_iter=1000),
                                   stack_method="predict_proba", cv=5, n_jobs=1)

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]
metrics = {}
print("\nStratified 5-fold cross-validation (mean +- std):")
for name, make in (("Random Forest", rf), ("XGBoost", xg), ("Stacking (RF+XGB -> LogReg)", stack)):
    cv = cross_validate(make(), X, y, cv=skf, scoring=scoring, n_jobs=1)
    metrics[name] = {m: [float(cv[f"test_{m}"].mean()), float(cv[f"test_{m}"].std())] for m in scoring}
    print(f"  {name:30s} " + "  ".join(f"{m}={metrics[name][m][0]:.4f}+-{metrics[name][m][1]:.4f}" for m in scoring))

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
hold = stack().fit(Xtr, ytr)
pred = hold.predict(Xte)
print("\nHold-out test (20%, stratified) for the stacking model:")
print(classification_report(yte, pred, target_names=["legitimate", "phishing"], digits=4))
print("Confusion matrix [[TN FP] [FN TP]]:\n", confusion_matrix(yte, pred))

final = stack().fit(X, y)
rf_imp = final.named_estimators_["rf"].feature_importances_
bundle = {"model": final, "features": FEATURE_NAMES, "means": X.mean(axis=0).tolist(), "stds": X.std(axis=0).tolist(),
          "importance": rf_imp.tolist(), "metrics": metrics, "n_per_class": k}
if args.extra_phish:
    extra = [u for u in read_txt(args.extra_phish) if u not in set(urls)]
    Xe = np.array([[extract(u)[n] for n in FEATURE_NAMES] for u in extra], dtype=float)
    detected = int((final.predict(Xe) == 1).sum())
    metrics["external_phishing_recall"] = [detected / max(1, len(extra)), len(extra)]
    print(f"\nExternal check on {len(extra)} fresh phishing links never seen in training: "
          f"{detected} detected ({detected / max(1, len(extra)):.1%})")
joblib.dump(bundle, args.out)
with open("model_metrics.json", "w", encoding="utf-8") as f:
    json.dump({"metrics": metrics, "n_per_class": k, "top_features": sorted(
        zip(FEATURE_NAMES, map(float, rf_imp)), key=lambda t: -t[1])[:15]}, f, ensure_ascii=False, indent=2)
print(f"\nTop features (Random Forest importance):")
for n, v in sorted(zip(FEATURE_NAMES, rf_imp), key=lambda t: -t[1])[:10]:
    print(f"  {n:18s} {v:.4f}")
print(f"\nSaved: {args.out} and model_metrics.json")
