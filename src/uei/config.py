"""Configuration loading. Secrets come only from environment variables."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"


def _load_dotenv() -> None:
    """Minimal .env reader (no dependency). Existing env vars take priority."""
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


@lru_cache(maxsize=1)
def settings() -> dict:
    _load_dotenv()
    path = CONFIG_DIR / "settings.yaml"
    if not path.exists():
        path = CONFIG_DIR / "settings.example.yaml"
    with open(path) as f:
        cfg = yaml.safe_load(f)
    cfg["_config_file"] = str(path)
    return cfg


@lru_cache(maxsize=1)
def races_2026() -> dict:
    with open(CONFIG_DIR / "races_2026.yaml") as f:
        return yaml.safe_load(f)


def data_dir() -> Path:
    d = ROOT / settings()["paths"]["data_dir"]
    d.mkdir(parents=True, exist_ok=True)
    return d


def db_path() -> Path:
    override = os.environ.get("UEI_DB_PATH")
    p = Path(override) if override else ROOT / settings()["paths"]["database"]
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def secret(name: str, default: str | None = None) -> str | None:
    _load_dotenv()
    val = os.environ.get(name, "").strip()
    return val or default


def user_agent() -> str:
    ua = settings()["http"]["user_agent"]
    contact = secret("UEI_CONTACT")
    return f"{ua} contact:{contact}" if contact else ua
