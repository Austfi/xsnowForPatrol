#!/usr/bin/env python3
"""Utility for fetching the documentation build version for xsnow notebooks.

The script is intentionally lightweight so that it can be executed from within
Jupyter notebooks (including Google Colab) without additional dependencies.

It supports the following resolution order:

1. ``XSNOW_DOCS_VERSION`` environment variable. When set, that value is returned
   directly. This is handy for offline trainings or mirrored documentation
   deployments.
2. ``XSNOW_DOCS_VERSION_URL`` environment variable. When set, the script tries
   to download the value from the provided URL.
3. ``https://raw.githubusercontent.com/Austfi/xsnowForPatrol/main/docs/VERSION``.
   This mirrors the canonical documentation repository layout and allows the
   notebooks to stay in sync with hosted docs.

On success the resolved version string is printed to ``stdout``. On failure an
error message is printed to ``stderr`` and the script exits with a non-zero
status so that callers can surface the problem to the user.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_URL = "https://raw.githubusercontent.com/Austfi/xsnowForPatrol/main/docs/VERSION"


def _download(url: str) -> str:
    with urllib.request.urlopen(url, timeout=10) as response:
        raw = response.read()
        content_type = response.headers.get("Content-Type", "").lower()
    data = raw.decode("utf-8", errors="ignore").strip()
    if "application/json" in content_type:
        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            return data
        for key in ("version", "docs_version", "tag"):
            if key in payload and isinstance(payload[key], str):
                return payload[key].strip()
        # Fallback to the first string value
        for value in payload.values():
            if isinstance(value, str):
                return value.strip()
        return data
    return data


def resolve_docs_version() -> str:
    direct_value = os.environ.get("XSNOW_DOCS_VERSION")
    if direct_value:
        return direct_value.strip()

    url = os.environ.get("XSNOW_DOCS_VERSION_URL", DEFAULT_URL)
    return _download(url)


def main() -> int:
    try:
        version = resolve_docs_version()
    except (OSError, urllib.error.URLError, urllib.error.HTTPError) as exc:
        print(f"Unable to fetch xsnow documentation version: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - defensive programming
        print(f"Unexpected error determining docs version: {exc}", file=sys.stderr)
        return 1

    if not version:
        print("xsnow documentation version could not be determined", file=sys.stderr)
        return 1

    print(version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
