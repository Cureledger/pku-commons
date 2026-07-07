"""Tiny, dependency-free config loader for PKU Commons.

Resolves values in this order (first hit wins):
  1. real process environment (e.g. `export FDC_API_KEY=...`)
  2. a `.env` file at the repo root (KEY=VALUE lines; `#` comments and blanks ignored)
  3. the provided default

No third-party deps (no python-dotenv needed).
"""
import os

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_dotenv(path):
    vals = {}
    if not os.path.exists(path):
        return vals
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            vals[key.strip()] = val.strip().strip('"').strip("'")
    return vals


_DOTENV = _load_dotenv(os.path.join(_REPO_ROOT, ".env"))


def get(name, default=None):
    if name in os.environ and os.environ[name]:
        return os.environ[name]
    if name in _DOTENV and _DOTENV[name]:
        return _DOTENV[name]
    return default


# Convenience accessors
FDC_API_KEY = get("FDC_API_KEY", "DEMO_KEY")
FDC_API_BASE = get("FDC_API_BASE", "https://api.nal.usda.gov/fdc/v1")
