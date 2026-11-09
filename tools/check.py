#!/usr/bin/env python3
"""Sanity checks for the generated site.

Run after `tools/build.py`. Exits non-zero and prints every problem it finds, so
a broken link or a missing deploy file fails CI instead of reaching the domain.

    python3 tools/check.py
"""

from __future__ import annotations

import html.parser
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__", "content", "tools", "_site"}
EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|data:|//)")

# Files GitHub Pages needs for the site to serve correctly.
REQUIRED = ["index.html", "404.html", "robots.txt", "sitemap.xml", ".nojekyll"]


class PageParser(html.parser.HTMLParser):
    """Collects the handful of things the checks below care about."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str]] = []   # (attribute value, tag)
        self.ids: set[str] = set()
        self.title = ""
        self.description = ""
        self.canonical = ""
        self.images_without_alt = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}

        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.refs.append((a["href"], tag))
        if tag in ("img", "script") and "src" in a:
            self.refs.append((a["src"], tag))
        if tag == "link" and "href" in a:
            self.refs.append((a["href"], tag))
            if a.get("rel") == "canonical":
                self.canonical = a["href"]
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name") == "description":
            self.description = a.get("content", "")
        # alt="" is correct for a decorative image; a missing attribute is not.
        if tag == "img" and "alt" not in a:
            self.images_without_alt += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def pages() -> list[Path]:
    found = []
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        found.append(path)
    return sorted(found)


def main() -> int:
    problems: list[str] = []

    site_url = ""
    try:
        site = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))
        domain = str(site.get("customDomain", "")).strip().strip("/")
        site_url = f"https://{domain}" if domain else str(site.get("siteUrl", "")).rstrip("/")
    except (OSError, ValueError) as exc:
        problems.append(f"content/site.json could not be read: {exc}")

    for name in REQUIRED:
        if not (ROOT / name).exists():
            problems.append(f"missing required file: {name}")

    found = pages()
    if not found:
        problems.append("no HTML pages were generated — did tools/build.py run?")

    for page in found:
        rel = page.relative_to(ROOT)
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))

        if not parser.title.strip():
            problems.append(f"{rel}: empty <title>")
        if not parser.description.strip():
            problems.append(f"{rel}: missing meta description")
        if parser.images_without_alt:
            problems.append(f"{rel}: {parser.images_without_alt} <img> without alt text")
        if site_url and parser.canonical and not parser.canonical.startswith(site_url):
            problems.append(f"{rel}: canonical points outside the site — {parser.canonical}")

        for ref, tag in parser.refs:
            if not ref or EXTERNAL.match(ref):
                continue

            if ref.startswith("#"):
                anchor = ref[1:]
                if anchor and anchor not in parser.ids:
                    problems.append(f"{rel}: anchor #{anchor} has no matching id")
                continue

            if ref.startswith("/"):
                # Root-relative: resolve against the site root.
                target = ROOT / urlsplit(ref).path.lstrip("/")
                if urlsplit(ref).path.endswith("/"):
                    target = target / "index.html"
            else:
                target = (page.parent / urlsplit(ref).path).resolve()

            if not target.exists():
                problems.append(f"{rel}: <{tag}> points at a missing file — {ref}")

    if problems:
        print(f"FAILED — {len(problems)} problem(s):\n", file=sys.stderr)
        for p in problems:
            print(f"  • {p}", file=sys.stderr)
        return 1

    print(f"OK — {len(found)} pages, links and metadata all valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
