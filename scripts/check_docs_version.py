"""Utilities for checking the published xsnow documentation version.

This script retrieves the documentation homepage and extracts the version
string displayed in the banner (e.g. ``"Version: dev (abcdef)"``).  The value
is printed to stdout so it can be reused by notebooks, CI workflows or other
automation.
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from html import unescape

DEFAULT_DOCS_URL = "https://xsnow.readthedocs.io/en/latest/"
BANNER_PATTERN = re.compile(r"Version:\s*([^<]+)", re.IGNORECASE)


@dataclass
class VersionCheckResult:
    """Structured response for callers that import this module."""

    version: str
    url: str


def fetch_html(url: str, timeout: int = 30) -> str:
    """Fetch *url* and return the decoded HTML as UTF-8 text.

    A small helper that keeps the network logic in one place so the same
    routine can be reused by multiple functions and makes it easier to mock in
    unit tests.
    """

    request = urllib.request.Request(url, headers={"User-Agent": "xsnow-sync/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # type: ignore[arg-type]
        content_type = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(content_type, errors="replace")


def parse_banner_version(html: str) -> str | None:
    """Extract the banner version string from an HTML page.

    The xsnow documentation banner exposes a snippet of text such as
    ``"Version: dev (abcdef)"``.  ``None`` is returned when the pattern is not
    found so callers can decide how to report the missing value.
    """

    match = BANNER_PATTERN.search(html)
    if not match:
        return None
    return unescape(match.group(1)).strip()


def check_docs_version(url: str = DEFAULT_DOCS_URL) -> VersionCheckResult:
    """Fetch ``url`` and return the parsed banner version.

    :raises RuntimeError: if the version banner cannot be located.
    """

    try:
        html = fetch_html(url)
    except urllib.error.URLError as exc:  # pragma: no cover - network failure path
        raise RuntimeError(f"Unable to reach documentation at {url}: {exc}") from exc

    version = parse_banner_version(html)
    if not version:
        raise RuntimeError(
            "Unable to locate a 'Version:' banner in the xsnow documentation page."
        )
    return VersionCheckResult(version=version, url=url)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--url",
        default=DEFAULT_DOCS_URL,
        help="Documentation homepage to inspect (default: %(default)s).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        result = check_docs_version(args.url)
    except RuntimeError as exc:
        parser.error(str(exc))
        return 2

    print(result.version)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
