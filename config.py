"""Shared paths and seed for every notebook in this repo."""
from pathlib import Path

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs"               # result CSVs (tracked)
INTERMEDIATE_DIR = OUT_DIR / "intermediate"  # household-level / model inputs (git-ignored)
FIG_DIR = ROOT / "images"
SEED = 42

for _d in (OUT_DIR, INTERMEDIATE_DIR, FIG_DIR):
    _d.mkdir(parents=True, exist_ok=True)
