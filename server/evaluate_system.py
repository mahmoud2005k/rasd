"""Evaluates the WHOLE system offline on links the AI never saw: rules only, AI only, and hybrid (rules + AI).
    python evaluate_system.py --csv malicious_phish.csv --n 2000
Offline = without domain age, DNS, page forms and the links database (these only help the real system)."""
import argparse
import json

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

import evalutil

ap = argparse.ArgumentParser()
ap.add_argument("--csv", required=True)
ap.add_argument("--n", type=int, default=2000, help="links per class")
ap.add_argument("--train-n", type=int, default=5000, help="the --n used when training")
ap.add_argument("--url-col", default="url")
ap.add_argument("--label-col", default="type")
a = ap.parse_args()

urls, y = evalutil.fresh_sample(a.csv, a.n, a.train_n, url_col=a.url_col, label_col=a.label_col)
print(f"Fresh links never used in training: {int(y.sum())} phishing + {int((1 - y).sum())} legitimate")
S = evalutil.score_all(urls)

rows = [("Rules only, alert at >= 20", S["rules"] >= 20, S["rules"]),
        ("Rules only, alert at >= 50", S["rules"] >= 50, S["rules"]),
        ("AI only (probability >= 50%)", S["ml"] >= 50, S["ml"]),
        ("Hybrid, alert at >= 20 (suspicious or worse)", S["hybrid"] >= 20, S["hybrid"]),
        ("Hybrid, alert at >= 50 (dangerous)", S["hybrid"] >= 50, S["hybrid"])]
res = {}
print(f"\n{'System':48s} {'Acc':>6s} {'Prec':>6s} {'Recall':>7s} {'F1':>6s} {'AUC':>6s}")
for name, pred, score in rows:
    m = {"accuracy": accuracy_score(y, pred), "precision": precision_score(y, pred, zero_division=0),
         "recall": recall_score(y, pred), "f1": f1_score(y, pred), "auc": roc_auc_score(y, score)}
    res[name] = m
    print(f"{name:48s} {m['accuracy']:6.3f} {m['precision']:6.3f} {m['recall']:7.3f} {m['f1']:6.3f} {m['auc']:6.3f}")
with open("evaluation.json", "w", encoding="utf-8") as f:
    json.dump({"n_per_class": int((1 - y).sum()), "systems": res}, f, ensure_ascii=False, indent=2)
print("\nSaved evaluation.json. Compare the Hybrid rows with 'AI only' to show what the rules add.")
