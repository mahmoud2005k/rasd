"""Makes the figures for your report (PNG files in report_figures/): ROC curves, confusion matrices,
feature importance and score distribution. Needs matplotlib:  python -m pip install matplotlib
    python report_figures.py --csv malicious_phish.csv --n 2000"""
import argparse
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from sklearn.metrics import ConfusionMatrixDisplay, auc, roc_curve  # noqa: E402

import evalutil  # noqa: E402
import ml  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--csv", required=True)
ap.add_argument("--n", type=int, default=2000)
ap.add_argument("--train-n", type=int, default=5000)
ap.add_argument("--out", default="report_figures")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)

urls, y = evalutil.fresh_sample(a.csv, a.n, a.train_n)
S = evalutil.score_all(urls)

plt.figure(figsize=(6, 5))
for key, label in (("rules", "Rules only"), ("ml", "AI model only"), ("hybrid", "Hybrid (rules + AI)")):
    fpr, tpr, _ = roc_curve(y, S[key])
    plt.plot(fpr, tpr, label=f"{label} (AUC = {auc(fpr, tpr):.3f})")
plt.plot([0, 1], [0, 1], "k--", lw=0.8)
plt.xlabel("False positive rate"); plt.ylabel("True positive rate"); plt.title("ROC curves on fresh links")
plt.legend(loc="lower right"); plt.tight_layout(); plt.savefig(f"{a.out}/roc.png", dpi=160); plt.close()

for key, thr, title in (("ml", 50, "AI model only (>= 50%)"), ("hybrid", 20, "Hybrid (score >= 20)")):
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    ConfusionMatrixDisplay.from_predictions(y, S[key] >= thr, display_labels=["legitimate", "phishing"], ax=ax, colorbar=False, cmap="Blues")
    ax.set_title(title); plt.tight_layout(); plt.savefig(f"{a.out}/confusion_{key}.png", dpi=160); plt.close()

b = ml.load()
imp = sorted(zip(b["features"], b["importance"]), key=lambda t: -t[1])[:15][::-1]
plt.figure(figsize=(6.5, 5))
plt.barh([n for n, _ in imp], [v for _, v in imp], color="#20D9A5")
plt.xlabel("Random Forest importance"); plt.title("Top features"); plt.tight_layout()
plt.savefig(f"{a.out}/feature_importance.png", dpi=160); plt.close()

plt.figure(figsize=(6.5, 4))
plt.hist(S["hybrid"][y == 0], bins=20, alpha=0.7, label="legitimate", color="#35a8ff")
plt.hist(S["hybrid"][y == 1], bins=20, alpha=0.7, label="phishing", color="#ff5470")
plt.axvline(20, color="k", ls="--", lw=0.8); plt.axvline(50, color="k", ls=":", lw=0.8)
plt.xlabel("Hybrid risk score"); plt.ylabel("Links"); plt.title("Score distribution"); plt.legend(); plt.tight_layout()
plt.savefig(f"{a.out}/score_distribution.png", dpi=160); plt.close()
print("Saved to", a.out + "/:", ", ".join(sorted(os.listdir(a.out))))
