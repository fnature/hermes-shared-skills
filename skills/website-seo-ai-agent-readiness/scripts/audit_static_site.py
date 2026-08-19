#!/usr/bin/env python3
"""Dependency-free static website readiness audit.

Checks source-level evidence only. It cannot prove live headers, redirects,
performance, colour contrast, keyboard use, or screen-reader behavior.
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


@dataclass
class Finding:
    status: str
    category: str
    code: str
    location: str
    message: str


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.h1_count = 0
        self.main_count = 0
        self.descriptions: list[str] = []
        self.viewports: list[str] = []
        self.canonicals: list[str] = []
        self.markdown_alternates: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.images: list[tuple[str, str | None]] = []
        self.jsonld_parts: list[list[str]] = []
        self.current_jsonld: list[str] | None = None

    @staticmethod
    def attrs_dict(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {k.lower(): (v or "") for k, v in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        a = self.attrs_dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "main":
            self.main_count += 1
        elif tag == "meta":
            name = a.get("name", "").lower()
            if name == "description":
                self.descriptions.append(a.get("content", "").strip())
            elif name == "viewport":
                self.viewports.append(a.get("content", "").strip())
        elif tag == "link":
            rels = {x.lower() for x in a.get("rel", "").split()}
            if "canonical" in rels:
                self.canonicals.append(a.get("href", "").strip())
            if "alternate" in rels and a.get("type", "").lower() == "text/markdown":
                self.markdown_alternates.append(a.get("href", "").strip())
        elif tag == "a":
            self.links.append((a.get("href", "").strip(), a.get("rel", "")))
        elif tag == "img":
            self.images.append((a.get("src", "").strip(), a.get("alt")))
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self.current_jsonld = []
            self.jsonld_parts.append(self.current_jsonld)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag == "script":
            self.current_jsonld = None

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.current_jsonld is not None:
            self.current_jsonld.append(data)

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())

    @property
    def jsonld(self) -> list[str]:
        return ["".join(parts).strip() for parts in self.jsonld_parts]


def add(findings: list[Finding], status: str, category: str, code: str, location: str, message: str) -> None:
    findings.append(Finding(status, category, code, location, message))


def local_target(root: Path, source: Path, href: str) -> tuple[Path | None, str | None]:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc or href.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None, None
    path_text = unquote(parsed.path)
    fragment = unquote(parsed.fragment) or None
    if not path_text:
        return source, fragment
    if path_text.startswith("/"):
        candidate = root / path_text.lstrip("/")
    else:
        candidate = source.parent / path_text
    if path_text.endswith("/"):
        candidate = candidate / "index.html"
    elif not candidate.suffix:
        if (candidate / "index.html").exists():
            candidate = candidate / "index.html"
        elif candidate.with_suffix(".html").exists():
            candidate = candidate.with_suffix(".html")
    return candidate.resolve(), fragment


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser


def audit(root: Path, base_url: str | None, production: bool) -> list[Finding]:
    findings: list[Finding] = []
    html_files = sorted(root.rglob("*.html"))
    if not html_files:
        add(findings, "FAIL", "critical", "no-html", str(root), "No HTML files found in the public root.")
        return findings

    root_resolved = root.resolve()
    pages: dict[Path, PageParser] = {}
    titles: Counter[str] = Counter()
    descriptions: Counter[str] = Counter()

    for path in html_files:
        rel = path.relative_to(root).as_posix()
        try:
            page = parse_page(path)
        except Exception as exc:
            add(findings, "FAIL", "critical", "html-parse", rel, f"Could not parse HTML: {exc}")
            continue
        pages[path.resolve()] = page
        if page.title:
            titles[page.title] += 1
        else:
            add(findings, "FAIL", "seo", "missing-title", rel, "Missing or empty <title>.")
        if len(page.descriptions) != 1 or not page.descriptions[0]:
            add(findings, "FAIL", "seo", "meta-description", rel, "Expected one non-empty meta description.")
        else:
            descriptions[page.descriptions[0]] += 1
        if page.h1_count != 1:
            add(findings, "FAIL", "accessibility", "h1-count", rel, f"Expected one <h1>; found {page.h1_count}.")
        if page.main_count != 1:
            add(findings, "FAIL", "accessibility", "main-count", rel, f"Expected one <main>; found {page.main_count}.")
        if not page.viewports:
            add(findings, "FAIL", "performance", "viewport", rel, "Missing viewport meta tag.")
        if base_url:
            if len(page.canonicals) != 1 or not page.canonicals[0]:
                add(findings, "FAIL" if production else "BLOCKED", "seo", "canonical", rel, "Expected one canonical URL for the confirmed public domain.")
            elif not page.canonicals[0].startswith(base_url.rstrip("/") + "/") and page.canonicals[0] != base_url.rstrip("/"):
                add(findings, "FAIL", "seo", "canonical-host", rel, f"Canonical is outside confirmed base URL: {page.canonicals[0]}")
        elif not page.canonicals:
            add(findings, "BLOCKED", "seo", "canonical-domain", rel, "Canonical URL deferred until the public domain and URL policy are confirmed.")
        elif len(page.canonicals) != 1:
            add(findings, "FAIL", "seo", "canonical-count", rel, f"Expected at most one canonical; found {len(page.canonicals)}.")

        for src, alt in page.images:
            if alt is None:
                add(findings, "FAIL", "accessibility", "missing-alt", rel, f"Image lacks an alt attribute: {src or '(empty src)'}")

        for idx, raw in enumerate(page.jsonld, 1):
            if not raw:
                add(findings, "FAIL", "seo", "empty-jsonld", rel, f"JSON-LD block {idx} is empty.")
                continue
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                add(findings, "FAIL", "seo", "invalid-jsonld", rel, f"JSON-LD block {idx} is invalid: {exc.msg} at line {exc.lineno}.")

        for href in page.markdown_alternates:
            target, _ = local_target(root, path, href)
            if target is not None and not target.exists():
                add(findings, "FAIL", "ai-readiness", "missing-markdown-alternate", rel, f"Markdown alternate does not exist: {href}")

    for title, count in sorted(titles.items()):
        if count > 1:
            locations = [p.relative_to(root).as_posix() for p, page in pages.items() if page.title == title]
            add(findings, "FAIL", "seo", "duplicate-title", ", ".join(locations), f"Duplicate title used {count} times: {title}")

    for description, count in sorted(descriptions.items()):
        if count > 1:
            locations = [
                p.relative_to(root).as_posix()
                for p, page in pages.items()
                if page.descriptions and page.descriptions[0] == description
            ]
            add(findings, "FAIL", "seo", "duplicate-description", ", ".join(locations), f"Duplicate meta description used {count} times.")

    for source, page in pages.items():
        rel = source.relative_to(root_resolved).as_posix()
        for href, _ in page.links:
            if not href or href == "#":
                continue
            target, fragment = local_target(root, source, href)
            if target is None:
                continue
            try:
                target.relative_to(root_resolved)
            except ValueError:
                add(findings, "FAIL", "critical", "link-escapes-root", rel, f"Internal link escapes public root: {href}")
                continue
            if not target.exists():
                add(findings, "FAIL", "critical", "broken-link", rel, f"Broken internal link: {href}")
                continue
            if fragment and target.suffix.lower() in {".html", ".htm"}:
                target_page = pages.get(target)
                if target_page is None:
                    try:
                        target_page = parse_page(target)
                    except Exception:
                        target_page = None
                if target_page and fragment not in target_page.ids:
                    add(findings, "FAIL", "critical", "broken-fragment", rel, f"Missing fragment target in {href}")

    robots = root / "robots.txt"
    sitemap = root / "sitemap.xml"
    if not robots.exists():
        add(findings, "FAIL" if production else "BLOCKED", "seo", "robots", "robots.txt", "Production crawler policy is missing or deferred.")
    else:
        text = robots.read_text(encoding="utf-8", errors="replace")
        if "Sitemap:" not in text:
            add(findings, "FAIL" if production else "BLOCKED", "seo", "robots-sitemap", "robots.txt", "robots.txt does not reference a sitemap.")
    if not sitemap.exists():
        add(findings, "FAIL" if production else "BLOCKED", "seo", "sitemap", "sitemap.xml", "Production sitemap is missing or deferred.")
    else:
        try:
            ET.parse(sitemap)
        except ET.ParseError as exc:
            add(findings, "FAIL", "seo", "invalid-sitemap", "sitemap.xml", f"Invalid XML: {exc}")

    markdown_links = sum(len(p.markdown_alternates) for p in pages.values())
    if markdown_links == 0:
        add(findings, "N/A", "ai-readiness", "markdown-alternates", str(root), "No Markdown alternate system is declared; optional until a synchronized source strategy is chosen.")
    else:
        add(findings, "PASS", "ai-readiness", "markdown-alternates", str(root), f"Found {markdown_links} declared Markdown alternate(s); targets were checked.")

    for filename in ("llms.txt", "llms-full.txt"):
        if (root / filename).exists():
            add(findings, "PASS", "ai-readiness", filename, filename, "File exists; factual/content review remains required.")
        else:
            add(findings, "N/A", "ai-readiness", filename, filename, "Optional file not present; decide from usefulness and maintainability, not checkbox pressure.")

    add(findings, "BLOCKED", "accessibility", "manual-a11y", str(root), "Keyboard, contrast, and representative screen-reader checks require rendered/manual verification.")
    add(findings, "BLOCKED", "performance", "live-performance", str(root), "Production performance and Core Web Vitals require a live or production-equivalent measurement.")
    add(findings, "BLOCKED", "ai-readiness", "live-http", str(root), "Live MIME types, redirects, caching, and content negotiation cannot be proven from static files alone.")

    if not any(f.status == "FAIL" for f in findings):
        add(findings, "PASS", "summary", "source-audit", str(root), f"Source audit completed for {len(html_files)} HTML page(s) with no FAIL findings.")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public_root", type=Path, help="Deployed/public directory to audit")
    parser.add_argument("--base-url", help="Confirmed canonical base URL, e.g. https://example.com")
    parser.add_argument("--production", action="store_true", help="Require production robots, sitemap, and canonicals")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable text")
    args = parser.parse_args()

    root = args.public_root.expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: public root is not a directory: {root}", file=sys.stderr)
        return 2

    findings = audit(root, args.base_url, args.production)
    counts = Counter(f.status for f in findings)
    payload = {
        "public_root": str(root),
        "base_url": args.base_url,
        "production_mode": args.production,
        "summary": {k: counts.get(k, 0) for k in ("PASS", "FAIL", "BLOCKED", "N/A")},
        "findings": [asdict(f) for f in findings],
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"Website readiness audit: {root}")
        print("Summary: " + ", ".join(f"{k}={payload['summary'][k]}" for k in ("PASS", "FAIL", "BLOCKED", "N/A")))
        for finding in findings:
            print(f"[{finding.status}] {finding.category}/{finding.code} — {finding.location}: {finding.message}")
    return 1 if counts.get("FAIL", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
