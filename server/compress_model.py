"""Shrinks model.joblib (usually 3-5x) so it fits on GitHub (100 MB limit) and on free hosting. No retraining.
    python compress_model.py"""
import os
import shutil
import sys

import joblib

src = sys.argv[1] if len(sys.argv) > 1 else "model.joblib"
before = os.path.getsize(src)
bundle = joblib.load(src)
shutil.copy(src, src + ".backup")
joblib.dump(bundle, src, compress=("zlib", 9))
joblib.load(src)  # proves the compressed file loads
print(f"{src}: {before / 1e6:.1f} MB -> {os.path.getsize(src) / 1e6:.1f} MB (backup kept as {src}.backup)")
