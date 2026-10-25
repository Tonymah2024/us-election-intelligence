"""Polite HTTP client: descriptive User-Agent, per-host rate limit, on-disk cache."""
from __future__ import annotations

import hashlib
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

from .. import config

_last_call: dict[str, float] = {}


class SourceUnavailable(RuntimeError):
    pass


def _cache_file(url: str, params: dict | None, subdir: str, suffix: str) -> Path:
    key = hashlib.sha1((url + repr(sorted((params or {}).items()))).encode()).hexdigest()[:16]
    d = config.data_dir() / "raw" / subdir
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{key}{suffix}"


def fetch(url: str, params: dict | None = None, subdir: str = "misc", suffix: str = ".bin",
          max_age_hours: float | None = None, force: bool = False) -> Path:
    """Download `url` to the raw cache and return the local path.

    Re-uses a cached copy younger than `max_age_hours` unless `force`.
    Secrets passed in params (e.g. api_key) are excluded from the cache key.
    """
    cfg = config.settings()["http"]
    max_age = cfg["cache_hours"] if max_age_hours is None else max_age_hours
    safe_params = {k: v for k, v in (params or {}).items() if "key" not in k.lower()}
    path = _cache_file(url, safe_params, subdir, suffix)
    if path.exists() and not force and (time.time() - path.stat().st_mtime) < max_age * 3600:
        return path

    host = urlparse(url).netloc
    min_gap = cfg.get("host_min_seconds", {}).get(host, cfg["min_seconds_between_requests"])
    r = None
    for attempt in range(cfg.get("max_retries", 4) + 1):
        wait = min_gap - (time.time() - _last_call.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        try:
            r = requests.get(url, params=params, timeout=cfg["timeout_seconds"],
                             headers={"User-Agent": config.user_agent()}, allow_redirects=True)
        except requests.RequestException as e:
            raise SourceUnavailable(f"{url}: {e}") from e
        finally:
            _last_call[host] = time.time()
        if r.status_code not in (429, 503):
            break
        # Rate limited: honour Retry-After, else back off exponentially (5, 10, 20, 40 s).
        ra = r.headers.get("Retry-After", "")
        time.sleep(min(float(ra), 120) if ra.isdigit() else 5 * 2 ** attempt)
    if r.status_code != 200:
        raise SourceUnavailable(f"{url}: HTTP {r.status_code}")
    # A redirect to a different site (e.g. discontinued 538 URLs -> abcnews) is not data.
    if urlparse(r.url).netloc != host and "dataverse" not in host:
        raise SourceUnavailable(f"{url}: redirected to {r.url}")
    path.write_bytes(r.content)
    return path


def fetch_json(url: str, params: dict | None = None, subdir: str = "misc", **kw) -> dict:
    import json
    p = fetch(url, params=params, subdir=subdir, suffix=".json", **kw)
    return json.loads(p.read_text())
