"""Writes requirements-deploy.txt with the EXACT library versions installed on your computer, so the hosting server
loads your trained model safely. Also prints the Python version to set on Render.   python make_pins.py"""
import platform
from importlib import metadata

PKGS = ["flask", "flask-cors", "requests", "python-dotenv", "gunicorn", "numpy", "scikit-learn", "xgboost", "joblib",
        "dnspython", "python-whois"]
lines = []
for p in PKGS:
    try:
        lines.append(f"{p}=={metadata.version(p)}")
    except metadata.PackageNotFoundError:
        lines.append(p)
open("requirements-deploy.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
print("\nWrote requirements-deploy.txt")
print("On Render set the environment variable  PYTHON_VERSION =", platform.python_version())
