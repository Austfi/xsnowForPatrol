"""Synchronise tutorial assets from the public xsnow documentation.

The script performs the following steps:

* Crawl the tutorial index page to identify individual tutorial URLs.
* Download linked Jupyter notebooks or, if none are available, scrape Python
  code blocks from the tutorial HTML.
* Store the collected artefacts locally and update ``_manifest.yml`` with the
  synchronised metadata.
* Print a brief diff summary that highlights added, updated and removed
  tutorials so CI jobs can display a concise report.

Only the Python standard library is used which keeps the script lightweight and
portable.  The behaviour can be customised with CLI options; run the script
with ``--help`` for details.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import List, Optional, Sequence

DEFAULT_INDEX_URL = "https://xsnow.readthedocs.io/en/latest/tutorials/index.html"
DEFAULT_LINK_PATTERN = "/tutorials/"
DEFAULT_OUTPUT_DIR = "notebooks"
DEFAULT_MANIFEST = "_manifest.yml"
USER_AGENT = "xsnow-sync/1.0"


class TutorialIndexParser(HTMLParser):
    """Collect tutorial links from an index page."""

    def __init__(self, base_url: str, link_pattern: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.link_pattern = link_pattern
        self.links: set[str] = set()

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if not href or href.startswith("#"):
            return
        if self.link_pattern not in href:
            return
        absolute = urllib.parse.urljoin(self.base_url, href)
        self.links.add(absolute)


class TutorialPageParser(HTMLParser):
    """Extract metadata, notebook links and code blocks from a tutorial page."""

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.title: str | None = None
        self._current_data: list[str] = []
        self._capture_title = False
        self.notebook_links: list[str] = []
        self._in_pre = False
        self._in_code = False
        self.code_blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        attr_map = dict(attrs)
        if tag in {"title", "h1"} and self.title is None:
            self._capture_title = True
            self._current_data = []
            return
        if tag == "a":
            href = attr_map.get("href")
            if href and href.endswith(".ipynb"):
                self.notebook_links.append(urllib.parse.urljoin(self.base_url, href))
            return
        if tag == "pre":
            self._in_pre = True
        if tag == "code" and self._in_pre:
            self._in_code = True
            self._current_data = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"title", "h1"} and self._capture_title:
            text = "".join(self._current_data).strip()
            if text:
                self.title = text
            self._capture_title = False
            self._current_data = []
            return
        if tag == "code" and self._in_code:
            block = "".join(self._current_data).strip("\n")
            if block:
                self.code_blocks.append(block)
            self._in_code = False
            self._current_data = []
            return
        if tag == "pre":
            self._in_pre = False

    def handle_data(self, data: str) -> None:
        if self._capture_title or self._in_code:
            self._current_data.append(data)


@dataclasses.dataclass
class TutorialAsset:
    slug: str
    title: str
    source_url: str
    asset_path: pathlib.Path
    source_type: str  # ``notebook`` or ``scraped``


def fetch(url: str, timeout: int = 30) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # type: ignore[arg-type]
        return response.read()


def ensure_directory(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def slug_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path.rstrip("/")
    slug = path.split("/")[-1] or "tutorial"
    if slug.endswith(".html"):
        slug = slug[:-5]
    return slug


def collect_tutorial_links(index_url: str, link_pattern: str) -> list[str]:
    html = fetch(index_url).decode("utf-8", errors="replace")
    parser = TutorialIndexParser(index_url, link_pattern)
    parser.feed(html)
    return sorted(parser.links)


def parse_tutorial_page(url: str) -> TutorialPageParser:
    html = fetch(url)
    parser = TutorialPageParser(url)
    parser.feed(html.decode("utf-8", errors="replace"))
    return parser


def write_if_changed(path: pathlib.Path, data: bytes) -> bool:
    if path.exists() and path.read_bytes() == data:
        return False
    ensure_directory(path.parent)
    path.write_bytes(data)
    return True


def write_text_if_changed(path: pathlib.Path, text: str) -> bool:
    data = text.encode("utf-8")
    return write_if_changed(path, data)


def load_manifest(path: pathlib.Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
    except Exception:  # pragma: no cover - optional dependency
        return _load_manifest_simple(text)
    else:  # pragma: no cover - optional dependency
        data = yaml.safe_load(text) or {}
        items = data.get("tutorials", [])
        if isinstance(items, list):
            return [dict(item) for item in items if isinstance(item, dict)]
        return []


def _load_manifest_simple(text: str) -> list[dict[str, str]]:
    tutorials: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("tutorials:"):
            continue
        if stripped.startswith("-"):
            if current:
                tutorials.append(current)
            current = {}
            remainder = stripped[1:].strip()
            if remainder:
                key, _, value = remainder.partition(":")
                current[key.strip()] = value.strip().strip("\"")
            continue
        if current is None:
            continue
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            current[key.strip()] = value.strip().strip("\"")
    if current:
        tutorials.append(current)
    return tutorials


def dump_manifest(path: pathlib.Path, tutorials: Sequence[dict[str, str]]) -> bool:
    lines = ["tutorials:"]
    for item in tutorials:
        lines.append("  - slug: {}".format(_yaml_escape(item.get("slug", ""))))
        for key in ("title", "source_url", "asset", "source_type"):
            value = item.get(key)
            if value is None:
                continue
            lines.append(f"    {key}: {_yaml_escape(value)}")
    text = "\n".join(lines) + "\n"
    return write_text_if_changed(path, text)


def _yaml_escape(value: str) -> str:
    if not value:
        return "''"
    if any(ch in value for ch in ":#-{}[]\n\"'"):
        escaped = value.replace("\"", "\\\"")
        return f'"{escaped}"'
    return value


def build_asset_from_parser(
    parser: TutorialPageParser,
    url: str,
    output_dir: pathlib.Path,
) -> tuple[TutorialAsset, list[str]]:
    slug = slug_from_url(url)
    title = parser.title or slug.replace("-", " ").title()
    asset_changes: list[str] = []
    if parser.notebook_links:
        notebook_url = parser.notebook_links[0]
        data = fetch(notebook_url)
        asset_path = output_dir / f"{slug}.ipynb"
        if write_if_changed(asset_path, data):
            asset_changes.append(f"updated notebook {asset_path}")
        source_type = "notebook"
    else:
        code = "\n\n".join(parser.code_blocks).strip()
        if not code:
            code = "# No code blocks were detected in the source documentation."
        asset_path = output_dir / f"{slug}.py"
        if write_text_if_changed(asset_path, code + "\n"):
            asset_changes.append(f"updated script {asset_path}")
        source_type = "scraped"
    asset = TutorialAsset(
        slug=slug,
        title=title,
        source_url=url,
        asset_path=asset_path,
        source_type=source_type,
    )
    return asset, asset_changes


def summarise_differences(
    previous: Sequence[dict[str, str]],
    current: Sequence[dict[str, str]],
) -> str:
    prev_map = {item.get("slug"): item for item in previous if item.get("slug")}
    curr_map = {item.get("slug"): item for item in current if item.get("slug")}

    added = sorted(set(curr_map) - set(prev_map))
    removed = sorted(set(prev_map) - set(curr_map))
    changed = sorted(
        slug
        for slug in set(curr_map) & set(prev_map)
        if _hash_dict(prev_map[slug]) != _hash_dict(curr_map[slug])
    )

    lines: list[str] = []
    if added:
        lines.append("Added: " + ", ".join(added))
    if removed:
        lines.append("Removed: " + ", ".join(removed))
    if changed:
        lines.append("Updated: " + ", ".join(changed))
    if not lines:
        return "No manifest changes detected."
    return "; ".join(lines)


def _hash_dict(data: dict[str, str]) -> str:
    digest = hashlib.sha1()
    for key in sorted(data):
        digest.update(key.encode("utf-8"))
        digest.update(b"=")
        digest.update(data[key].encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def sync_tutorials(
    index_url: str,
    link_pattern: str,
    output_dir: pathlib.Path,
    manifest_path: pathlib.Path,
    dry_run: bool = False,
) -> str:
    ensure_directory(output_dir)

    previous_manifest = load_manifest(manifest_path)

    try:
        tutorial_links = collect_tutorial_links(index_url, link_pattern)
    except urllib.error.URLError as exc:  # pragma: no cover - network failure path
        raise RuntimeError(f"Unable to download tutorial index: {exc}") from exc

    assets: list[TutorialAsset] = []
    asset_logs: list[str] = []
    for url in tutorial_links:
        try:
            parser = parse_tutorial_page(url)
        except urllib.error.URLError as exc:  # pragma: no cover - network failure path
            asset_logs.append(f"failed to fetch {url}: {exc}")
            continue
        asset, changes = build_asset_from_parser(parser, url, output_dir)
        assets.append(asset)
        asset_logs.extend(changes)

    manifest_entries = [
        {
            "slug": asset.slug,
            "title": asset.title,
            "source_url": asset.source_url,
            "asset": str(asset.asset_path),
            "source_type": asset.source_type,
        }
        for asset in assets
    ]

    manifest_entries.sort(key=lambda item: item["slug"])

    summary = summarise_differences(previous_manifest, manifest_entries)

    if dry_run:
        if asset_logs:
            summary += "\n" + "\n".join(f"DRY-RUN: {log}" for log in asset_logs)
        return summary

    if dump_manifest(manifest_path, manifest_entries) and summary.startswith("No "):
        summary = "Manifest updated but no semantic changes detected."

    if asset_logs:
        summary += "\n" + "\n".join(asset_logs)
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--index-url",
        default=DEFAULT_INDEX_URL,
        help="Tutorial index URL (default: %(default)s).",
    )
    parser.add_argument(
        "--link-pattern",
        default=DEFAULT_LINK_PATTERN,
        help="Substring that tutorial links must contain (default: %(default)s).",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        type=pathlib.Path,
        help="Directory where tutorials should be written (default: %(default)s).",
    )
    parser.add_argument(
        "--manifest",
        default=DEFAULT_MANIFEST,
        type=pathlib.Path,
        help="Manifest path to update (default: %(default)s).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Crawl and report without writing files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        summary = sync_tutorials(
            index_url=args.index_url,
            link_pattern=args.link_pattern,
            output_dir=args.output_dir,
            manifest_path=args.manifest,
            dry_run=args.dry_run,
        )
    except RuntimeError as exc:
        parser.error(str(exc))
        return 2

    print(summary)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
