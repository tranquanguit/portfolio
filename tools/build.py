#!/usr/bin/env python3
"""Static site generator for the portfolio.

Reads everything from `content/` and writes plain HTML to the repository root.
No third-party dependencies — `python3 tools/build.py` is the whole build.

    content/site.json          profile, contact details, organizations
    content/experience/*.md    one file per role
    content/projects/*.md      one file per project
    content/skills/*.md        one file per skill
    content/awards/*.md        one file per award / certification / achievement

Each markdown file carries a small frontmatter block between `---` fences and a
markdown body that becomes the story on the detail page.
"""

from __future__ import annotations

import html
import json
import math
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
# Public location of the site. Both are set from content/site.json at build
# time — `siteUrl` drives canonical links and the sitemap, `ROOT_PATH` is the
# path the site is served under ("/" on a custom domain, "/portfolio/" on a
# github.io project page).
SITE_URL = "https://tranquanguit.github.io/portfolio"
ROOT_PATH = "/portfolio/"

SECTIONS = {
    "projects": {"title": "Projects", "blurb": "Client work, grouped by where it was delivered."},
    "experience": {"title": "Experience", "blurb": "Roles, and what each one actually involved."},
    "skills": {"title": "Skills", "blurb": "What I work with, and what I have learned using it."},
    "awards": {"title": "Recognition", "blurb": "Awards, certifications and achievements."},
}


# ---------------------------------------------------------------------------
# Frontmatter + markdown
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split a `---` fenced frontmatter block from the markdown body."""
    if not text.startswith("---"):
        return {}, text

    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    raw = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")

    meta: dict = {}
    key = None
    for line in raw.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        if line.startswith((" ", "\t")) and line.lstrip().startswith("- ") and key:
            # `key:` followed by indented `- item` lines becomes a list. The key
            # was seeded with "" when its value was blank, so promote it here.
            if not isinstance(meta.get(key), list):
                meta[key] = []
            meta[key].append(_scalar(line.lstrip()[2:].strip()))
            continue

        if ":" not in line:
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()

        if value == "":
            meta[key] = ""
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            meta[key] = [_scalar(v.strip()) for v in inner.split(",") if v.strip()] if inner else []
        else:
            meta[key] = _scalar(value)

    return meta, body


def _scalar(value: str):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1].replace('\\"', '"')
    low = value.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    return value


INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def inline_md(text: str, base: str = "") -> str:
    out = html.escape(text, quote=False)

    codes: list[str] = []

    def stash(match: re.Match) -> str:
        codes.append(match.group(1))
        return f"\x00CODE{len(codes) - 1}\x00"

    out = INLINE_CODE.sub(stash, out)

    out = IMAGE.sub(
        lambda m: f'<img src="{rebase(m.group(2), base)}" alt="{html.escape(m.group(1), quote=True)}" loading="lazy">',
        out,
    )
    out = LINK.sub(lambda m: _link(m.group(1), m.group(2), base), out)
    out = BOLD.sub(r"<strong>\1</strong>", out)
    out = ITALIC.sub(r"<em>\1</em>", out)

    for i, code in enumerate(codes):
        out = out.replace(f"\x00CODE{i}\x00", f"<code>{html.escape(code, quote=False)}</code>")

    return out


def _link(label: str, url: str, base: str) -> str:
    href = rebase(url, base)
    external = url.startswith("http")
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ""
    return f'<a href="{html.escape(href, quote=True)}"{attrs}>{label}</a>'


def rebase(url: str, base: str) -> str:
    """Rewrite root-relative content paths for pages nested one level deep."""
    if base and not url.startswith(("http", "#", "mailto:", "tel:", "/")):
        return base + url
    return url


def render_md(text: str, base: str = "") -> str:
    """Render the markdown subset used across the content files."""
    lines = text.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Fenced code block
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            block: list[str] = []
            while i < n and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            cls = f' class="language-{html.escape(lang, quote=True)}"' if lang else ""
            out.append(f'<pre><code{cls}>{html.escape(chr(10).join(block), quote=False)}</code></pre>')
            continue

        # Horizontal rule
        if re.fullmatch(r"-{3,}|\*{3,}", stripped):
            out.append("<hr>")
            i += 1
            continue

        # Heading
        heading = re.match(r"^(#{2,4})\s+(.*)$", stripped)
        if heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline_md(heading.group(2), base)}</h{level}>")
            i += 1
            continue

        # Table
        if stripped.startswith("|") and i + 1 < n and re.fullmatch(r"\|[\s:|-]+\|", lines[i + 1].strip()):
            header = _row(stripped)
            i += 2
            body: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                body.append(_row(lines[i].strip()))
                i += 1
            head_html = "".join(f"<th>{inline_md(c, base)}</th>" for c in header)
            rows_html = "".join(
                "<tr>" + "".join(f"<td>{inline_md(c, base)}</td>" for c in row) + "</tr>" for row in body
            )
            out.append(
                '<div class="table-scroll"><table><thead><tr>'
                f"{head_html}</tr></thead><tbody>{rows_html}</tbody></table></div>"
            )
            continue

        # Blockquote
        if stripped.startswith(">"):
            block = []
            while i < n and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            inner = " ".join(part for part in block if part)
            out.append(f"<blockquote><p>{inline_md(inner, base)}</p></blockquote>")
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline_md(it, base)}</li>" for it in items) + "</ol>")
            continue

        # Unordered list
        if stripped.startswith("- "):
            items = []
            while i < n and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline_md(it, base)}</li>" for it in items) + "</ul>")
            continue

        # Paragraph
        para = []
        while i < n and lines[i].strip() and not _breaks_paragraph(lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline_md(' '.join(para), base)}</p>")

    return "\n".join(out)


def _breaks_paragraph(line: str) -> bool:
    return (
        line.startswith(("#", ">", "- ", "|", "```"))
        or bool(re.match(r"^\d+\.\s+", line))
        or bool(re.fullmatch(r"-{3,}|\*{3,}", line))
    )


def _row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


# ---------------------------------------------------------------------------
# Content model
# ---------------------------------------------------------------------------

@dataclass
class Entry:
    section: str
    slug: str
    meta: dict
    body: str
    tags: list = field(default_factory=list)
    highlights: list = field(default_factory=list)

    def get(self, key, default=""):
        value = self.meta.get(key, default)
        return default if value in (None, "") else value

    @property
    def title(self) -> str:
        return str(self.meta.get("title", self.slug))

    @property
    def summary(self) -> str:
        return str(self.meta.get("summary", ""))

    @property
    def url(self) -> str:
        return f"{self.section}/{self.slug}.html"

    @property
    def sort_key(self) -> str:
        return str(self.meta.get("start") or self.meta.get("date") or "0000-00")

    @property
    def reading_time(self) -> int:
        return max(1, round(len(self.body.split()) / 190))


def load_entries(section: str) -> list[Entry]:
    directory = CONTENT / section
    if not directory.is_dir():
        return []

    entries = []
    for path in sorted(directory.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        slug = str(meta.get("slug") or path.stem)
        entries.append(
            Entry(
                section=section,
                slug=slug,
                meta=meta,
                body=body,
                tags=[str(t) for t in meta.get("tags", []) if str(t).strip()],
                highlights=[str(h) for h in meta.get("highlights", []) if str(h).strip()],
            )
        )
    return entries


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------

def e(value) -> str:
    return html.escape(str(value), quote=True)


ICONS = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "back": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9h4v12H3V9Zm7 0h3.8v1.7h.05a4.2 4.2 0 0 1 3.75-2c4 0 4.75 2.6 4.75 6V21h-4v-5.5c0-1.3 0-3-1.85-3s-2.15 1.45-2.15 2.9V21h-4V9Z"/></svg>',
    "sun": '<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "moon": '<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
}

HOME_NAV = [
    ("#about", "About"),
    ("#experience", "Experience"),
    ("#skills", "Skills"),
    ("#projects", "Projects"),
    ("#awards", "Recognition"),
    ("#contact", "Contact"),
]

SUB_NAV = [
    ("index.html", "Home"),
    ("experience/index.html", "Experience"),
    ("skills/index.html", "Skills"),
    ("projects/index.html", "Projects"),
    ("awards/index.html", "Recognition"),
]


def nav_html(site: dict, base: str, home: bool) -> str:
    links = HOME_NAV if home else [(base + href, label) for href, label in SUB_NAV]
    desktop = "".join(f'<a href="{e(href)}">{e(label)}</a>' for href, label in links)
    drawer = "".join(f'<a href="{e(href)}">{e(label)}</a>' for href, label in links)
    initials = "".join(part[0] for part in str(site["name"]).split()[:2]).upper()

    return f"""<header class="nav">
  <div class="wrap nav__inner">
    <a class="brand" href="{e(base)}index.html">
      <span class="brand__mark" aria-hidden="true">{e(initials)}</span>
      <span class="brand__text">
        <span class="brand__name">{e(site['name'])}</span>
        <span class="brand__role">{e(site['role'])}</span>
      </span>
    </a>
    <nav class="nav__links" aria-label="Main">{desktop}</nav>
    <div class="nav__tools">
      <button class="icon-btn theme-toggle" type="button" aria-label="Toggle colour theme">{ICONS['sun']}{ICONS['moon']}</button>
      <button class="icon-btn nav__burger" type="button" aria-label="Open menu" aria-expanded="false">{ICONS['menu']}</button>
    </div>
  </div>
  <div class="nav__drawer"><div class="wrap">{drawer}</div></div>
</header>"""


def footer_html(site: dict, base: str) -> str:
    links = "".join(f'<a href="{e(base + href)}">{e(label)}</a>' for href, label in SUB_NAV[1:])
    return f"""<footer class="footer">
  <div class="wrap footer__inner">
    <p class="footer__copy">&copy; <span data-year>{date.today().year}</span> {e(site['name'])} &middot; {e(site['role'])}</p>
    <nav class="footer__links" aria-label="Footer">
      {links}
      <a href="mailto:{e(site['email'])}">Email</a>
      <a href="{e(site['linkedin'])}" target="_blank" rel="noopener noreferrer">LinkedIn</a>
    </nav>
  </div>
</footer>"""


def page(site: dict, *, title: str, description: str, body: str, base: str = "",
         home: bool = False, canonical: str = "") -> str:
    canonical_tag = (
        f'\n  <link rel="canonical" href="{e(SITE_URL)}/{e(public_url(canonical))}">' if canonical else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <meta name="author" content="{e(site['name'])}">
  <meta name="theme-color" content="#faf9f6">{canonical_tag}
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{e(base)}assets/css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='22' fill='%232c6baf'/><text x='50' y='68' font-family='sans-serif' font-size='46' font-weight='700' fill='white' text-anchor='middle'>Q</text></svg>">
  <script>
    (function () {{
      try {{
        document.documentElement.classList.add('js');
        var t = localStorage.getItem('tvq-theme');
        if (!t) t = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', t);
      }} catch (e) {{ document.documentElement.setAttribute('data-theme', 'light'); }}
    }})();
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  {nav_html(site, base, home)}
  <main id="main">
{body}
  </main>
  {footer_html(site, base)}
  <script src="{e(base)}assets/js/main.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Shared fragments
# ---------------------------------------------------------------------------

def tag_list(tags: list, limit: int | None = None, cls: str = "tag") -> str:
    shown = tags[:limit] if limit else tags
    chips = "".join(f'<span class="{cls}">{e(t)}</span>' for t in shown)
    if limit and len(tags) > limit:
        chips += f'<span class="tag">+{len(tags) - limit}</span>'
    return f'<div class="tags">{chips}</div>' if chips else ""


def project_card(entry: Entry, orgs: dict, base: str = "") -> str:
    org = orgs.get(str(entry.get("org")), {})
    image = entry.get("image")
    if image:
        media = (
            f'<div class="card__media"><img src="{e(rebase(str(image), base))}" '
            f'alt="{e(entry.get("imageAlt", entry.title))}" loading="lazy" width="640" height="360"></div>'
        )
    else:
        media = f'<div class="card__media card__media--blank"><span class="card__glyph" aria-hidden="true">◆</span></div>'

    live = '<span class="pill pill--live">Ongoing</span>' if entry.get("current") else ""

    return f"""<a class="card reveal" href="{e(base + entry.url)}" data-filter-target="projects" data-key="{e(entry.get('org'))}">
  {media}
  <div class="card__body">
    <div class="card__meta">
      <span>{e(org.get('short', ''))}</span><span class="dot">&middot;</span><span>{e(entry.get('period'))}</span>
      {live}
    </div>
    <h3 class="card__title">{e(entry.title)}</h3>
    <p class="card__desc">{e(entry.summary)}</p>
    {tag_list(entry.tags, 4)}
    <div class="card__foot"><span class="card__cue">Read the story {ICONS['arrow']}</span></div>
  </div>
</a>"""


def skill_card(entry: Entry, base: str = "") -> str:
    level = int(entry.get("level", 0) or 0)
    meter = ""
    if level:
        meter = f"""<div class="meter"><div class="meter__fill" data-level="{level}"></div></div>
      <div class="meter__label"><span>{e(entry.get('years', ''))} yrs hands-on</span><span>{level}%</span></div>"""

    return f"""<a class="skill-card reveal" href="{e(base + entry.url)}">
  <span class="skill-card__icon" aria-hidden="true">{e(entry.get('icon', '◆'))}</span>
  <span style="flex:1;min-width:0">
    <span class="skill-card__title" style="display:block">{e(entry.title)}</span>
    <span class="skill-card__desc" style="display:block">{e(entry.summary)}</span>
    {meter}
  </span>
</a>"""


AWARD_TYPE_LABEL = {
    "award": "Award",
    "certification": "Certification",
    "achievement": "Achievement",
    "publication": "Publication",
}


def award_card(entry: Entry, base: str = "") -> str:
    kind = str(entry.get("type", "award"))
    return f"""<a class="award-card reveal" href="{e(base + entry.url)}" data-filter-target="awards" data-key="{e(kind)}">
  <span class="award-card__icon" aria-hidden="true">{e(entry.get('icon', '🏅'))}</span>
  <span class="tag tag--gold">{e(AWARD_TYPE_LABEL.get(kind, kind.title()))}</span>
  <span class="award-card__title">{e(entry.title)}</span>
  <span class="award-card__issuer">{e(entry.get('issuer'))}</span>
  <p class="award-card__desc">{e(entry.summary)}</p>
  <span class="award-card__foot">
    <span class="tag">{e(entry.get('period', entry.get('date')))}</span>
    <span class="card__cue">Details {ICONS['arrow']}</span>
  </span>
</a>"""


def timeline_item(entry: Entry, base: str = "") -> str:
    points = "".join(f"<li>{inline_md(h, base)}</li>" for h in entry.highlights[:3])
    live = '<span class="pill pill--live">Current</span>' if entry.get("current") else ""
    return f"""<div class="tl-item {'tl-item--current' if entry.get('current') else ''} reveal">
  <a class="tl-card" href="{e(base + entry.url)}">
    <div class="tl-top">
      <span class="tl-role">{e(entry.title)}</span>
      <span class="tl-company">{e(entry.get('company'))}</span>
      {live}
      <span class="tl-period">{e(entry.get('period'))}</span>
    </div>
    <p class="tl-summary">{e(entry.summary)}</p>
    <ul class="tl-points">{points}</ul>
    {tag_list(entry.tags, 5)}
    <span class="card__cue" style="margin-top:.9rem">Read more {ICONS['arrow']}</span>
  </a>
</div>"""


def radar_svg(skills: list[Entry]) -> str:
    """Inline SVG radar of headline proficiencies — no charting library needed."""
    axes = [(str(s.get("short") or s.title), int(s.get("level", 0) or 0)) for s in skills]
    if len(axes) < 3:
        return ""

    # Extra horizontal room in the viewBox so the outer axis labels are not clipped.
    width, height, cx, cy, r = 360, 300, 180, 148, 100
    count = len(axes)
    parts = [f'<svg class="radar" viewBox="0 0 {width} {height}" role="img" aria-label="Proficiency overview">']

    for ring in (0.25, 0.5, 0.75, 1.0):
        pts = " ".join(
            f"{cx + r * ring * math.cos(2 * math.pi * i / count - math.pi / 2):.1f},"
            f"{cy + r * ring * math.sin(2 * math.pi * i / count - math.pi / 2):.1f}"
            for i in range(count)
        )
        parts.append(f'<polygon class="grid-ring" points="{pts}"/>')

    for i in range(count):
        angle = 2 * math.pi * i / count - math.pi / 2
        parts.append(
            f'<line class="axis-line" x1="{cx}" y1="{cy}" '
            f'x2="{cx + r * math.cos(angle):.1f}" y2="{cy + r * math.sin(angle):.1f}"/>'
        )

    shape = []
    dots = []
    for i, (_, level) in enumerate(axes):
        angle = 2 * math.pi * i / count - math.pi / 2
        radius = r * (level / 100)
        x, y = cx + radius * math.cos(angle), cy + radius * math.sin(angle)
        shape.append(f"{x:.1f},{y:.1f}")
        dots.append(f'<circle class="point" cx="{x:.1f}" cy="{y:.1f}" r="3"/>')
    parts.append(f'<polygon class="shape" points="{" ".join(shape)}"/>')
    parts.extend(dots)

    for i, (label, _) in enumerate(axes):
        angle = 2 * math.pi * i / count - math.pi / 2
        lx, ly = cx + (r + 14) * math.cos(angle), cy + (r + 14) * math.sin(angle)
        anchor = "middle" if abs(math.cos(angle)) < 0.3 else ("start" if math.cos(angle) > 0 else "end")
        parts.append(
            f'<text class="axis-label" x="{lx:.1f}" y="{ly + 3:.1f}" text-anchor="{anchor}">{e(label)}</text>'
        )

    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------

def build_home(site: dict, data: dict, orgs: dict) -> str:
    experience = sorted(data["experience"], key=lambda x: x.sort_key, reverse=True)
    projects = sorted(data["projects"], key=lambda x: x.sort_key, reverse=True)
    skills = data["skills"]
    awards = sorted(data["awards"], key=lambda x: str(x.get("date")), reverse=True)

    stats = "".join(
        f'<div class="stat"><div class="stat__value">{e(s["value"])}</div>'
        f'<div class="stat__label">{e(s["label"])}</div></div>'
        for s in site["stats"]
    )

    hero = f"""<section class="hero">
  <div class="wrap">
    <div class="hero__grid">
      <div>
        <p class="hero__role">{e(site['roleLong'])}</p>
        <h1 class="hero__name">{e(site['name'])}</h1>
        <p class="hero__tagline">{e(site['tagline'])}</p>
        <div class="hero__actions">
          <a class="btn btn--primary" href="#projects">Browse projects {ICONS['arrow']}</a>
          <a class="btn btn--ghost" href="mailto:{e(site['email'])}">{ICONS['mail']} Get in touch</a>
        </div>
        <div class="hero__meta">
          <span>{ICONS['pin']} {e(site['location'])}</span>
          <span><a href="mailto:{e(site['email'])}">{e(site['email'])}</a></span>
          <span><a href="{e(site['linkedin'])}" target="_blank" rel="noopener noreferrer">{e(site['linkedinLabel'])}</a></span>
        </div>
      </div>
      <div class="hero__portrait">
        <img src="{e(site['photo'])}" alt="Portrait of {e(site['name'])}" width="1600" height="1067" fetchpriority="high">
      </div>
    </div>
    <div class="stats reveal" style="margin-top:56px">{stats}</div>
  </div>
</section>"""

    summary_paras = "".join(f"<p>{e(p)}</p>" for p in site["summary"])
    certs = "".join(
        f"""<div class="cert-item">
      <span class="cert-item__seal" aria-hidden="true">✦</span>
      <span>
        <span class="cert-item__name">{e(c['name'])}</span>
        <span class="cert-item__meta">{e(c['code'])} &middot; {e(c['issuer'])} &middot; {e(c['date'])}</span>
      </span>
    </div>"""
        for c in site["certifications"]
    )
    langs = "".join(
        f'<div class="deflist__row"><span class="deflist__k">{e(l["name"])}</span>'
        f'<span class="deflist__v">{e(l["level"])}</span></div>'
        for l in site["languages"]
    )
    edu = site["education"]

    about = f"""<section class="section" id="about">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">About</p>
      <h2>Two disciplines, one delivery path</h2>
    </div>
    <div class="grid grid--2" style="align-items:start;gap:32px">
      <div class="reveal">{summary_paras}</div>
      <div class="stack reveal">
        <div class="panel">
          <p class="panel__title">Education</p>
          <div class="deflist">
            <div class="deflist__row"><span class="deflist__k">Degree</span><span class="deflist__v">{e(edu['degree'])}</span></div>
            <div class="deflist__row"><span class="deflist__k">University</span><span class="deflist__v">{e(edu['school'])}</span></div>
            <div class="deflist__row"><span class="deflist__k">Period</span><span class="deflist__v">{e(edu['period'])}</span></div>
            <div class="deflist__row"><span class="deflist__k">Focus</span><span class="deflist__v">{e(edu['focus'])}</span></div>
          </div>
        </div>
        <div class="panel">
          <p class="panel__title">SAP Certifications</p>
          {certs}
        </div>
        <div class="panel">
          <p class="panel__title">Languages</p>
          <div class="deflist">{langs}</div>
        </div>
      </div>
    </div>
  </div>
</section>"""

    exp_items = "".join(timeline_item(x) for x in experience)
    exp = f"""<section class="section section--alt" id="experience">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Experience</p>
      <h2>{e(SECTIONS['experience']['title'])}</h2>
      <p>{e(SECTIONS['experience']['blurb'])} Every role opens into a full page.</p>
    </div>
    <div class="timeline">{exp_items}</div>
  </div>
</section>"""

    # Skills, grouped by category
    categories: dict[str, list[Entry]] = {}
    for s in skills:
        categories.setdefault(str(s.get("category", "Other")), []).append(s)
    order = ["SAP Development", "Integration & Data", "Working & Leading"]
    ordered = [c for c in order if c in categories] + [c for c in categories if c not in order]

    groups = ""
    for cat in ordered:
        cards = "".join(skill_card(s) for s in sorted(categories[cat], key=lambda x: -int(x.get("level", 0) or 0)))
        groups += f"""<div class="skill-group">
      <h3 class="skill-group__title">{e(cat)}</h3>
      <div class="grid grid--2">{cards}</div>
    </div>"""

    radar_skills = sorted(
        [s for s in skills if s.get("featured") and s.get("short")],
        key=lambda x: -int(x.get("level", 0) or 0),
    )[:6]
    radar = radar_svg(radar_skills)
    radar_panel = f"""<div class="radar-panel reveal">
        <h3 class="radar-panel__title">Proficiency at a glance</h3>
        <p class="radar-panel__note">Self-assessed against what the role actually demands day to day.</p>
        {radar}
      </div>""" if radar else ""

    skills_section = f"""<section class="section" id="skills">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Skills</p>
      <h2>{e(SECTIONS['skills']['title'])}</h2>
      <p>{e(SECTIONS['skills']['blurb'])} Each one links to a page where I write about how I use it.</p>
    </div>
    <div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,320px);gap:40px;align-items:start" class="skills-layout">
      <div>{groups}</div>
      {radar_panel}
    </div>
  </div>
</section>"""

    # Projects grouped by organization
    filters = '<button class="filter is-active" data-value="all" aria-pressed="true">All<span class="filter__n">' \
              + str(len(projects)) + "</span></button>"
    org_blocks = ""
    for org_id, org in orgs.items():
        items = [p for p in projects if str(p.get("org")) == org_id]
        if not items:
            continue
        filters += (
            f'<button class="filter" data-value="{e(org_id)}" aria-pressed="false">{e(org["short"])}'
            f'<span class="filter__n">{len(items)}</span></button>'
        )
        cards = "".join(project_card(p, orgs) for p in items)
        org_blocks += f"""<div class="org" data-filter-section="projects">
      <div class="org__head">
        <span class="org__badge">{e(org['short'])}</span>
        <span class="org__title">
          <span class="org__name">{e(org['name'])}</span>
          <span class="org__kind">{e(org['kind'])} &middot; {e(org['period'])}</span>
        </span>
        <span class="org__count">{len(items)} project{'s' if len(items) != 1 else ''}</span>
        <p class="org__blurb">{e(org['blurb'])}</p>
      </div>
      <div class="grid grid--3">{cards}</div>
    </div>"""

    projects_section = f"""<section class="section section--alt" id="projects">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Projects</p>
      <h2>{e(SECTIONS['projects']['title'])}</h2>
      <p>{e(SECTIONS['projects']['blurb'])} Open any card for the full story — context, decisions and what I would do differently.</p>
    </div>
    <div class="filters" data-filter-group="projects">{filters}</div>
    {org_blocks}
  </div>
</section>"""

    pub = site["publication"]
    award_cards = "".join(award_card(a) for a in awards)
    awards_section = f"""<section class="section" id="awards">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Recognition</p>
      <h2>Awards, certifications &amp; achievements</h2>
    </div>
    <div class="grid grid--3">{award_cards}</div>
    <div class="pub reveal" style="margin-top:32px">
      <div>
        <p class="eyebrow" style="margin-bottom:.25rem">Publication</p>
        <h3 class="pub__title">{e(pub['title'])}</h3>
        <p class="pub__meta">{e(pub['journal'])} &middot; {e(pub['volume'])} &middot; {e(pub['year'])}</p>
        <p class="pub__authors">{e(pub['authors'])}</p>
      </div>
      <a class="btn btn--ghost" href="{e(pub['url'])}" target="_blank" rel="noopener noreferrer">Read the paper {ICONS['arrow']}</a>
    </div>
  </div>
</section>"""

    contact = f"""<section class="section section--alt" id="contact">
  <div class="wrap">
    <div class="section-head section-head--center">
      <p class="eyebrow">Contact</p>
      <h2>Let's talk</h2>
      <p>Open to SAP technical consulting, ABAP and RAP development, and data integration work. The fastest way to reach me is email.</p>
    </div>
    <div style="display:flex;justify-content:center;margin-bottom:32px">
      <a class="btn btn--primary" href="mailto:{e(site['email'])}">{ICONS['mail']} Send an email</a>
    </div>
    <div class="grid grid--4">
      <a class="contact-card reveal" href="mailto:{e(site['email'])}">
        <span class="contact-card__icon">{ICONS['mail']}</span>
        <span style="min-width:0"><span class="contact-card__k" style="display:block">Email</span><span class="contact-card__v">{e(site['email'])}</span></span>
      </a>
      <a class="contact-card reveal" href="tel:{e(site['phoneHref'])}">
        <span class="contact-card__icon">{ICONS['phone']}</span>
        <span style="min-width:0"><span class="contact-card__k" style="display:block">Phone</span><span class="contact-card__v">{e(site['phone'])}</span></span>
      </a>
      <a class="contact-card reveal" href="{e(site['linkedin'])}" target="_blank" rel="noopener noreferrer">
        <span class="contact-card__icon">{ICONS['linkedin']}</span>
        <span style="min-width:0"><span class="contact-card__k" style="display:block">LinkedIn</span><span class="contact-card__v">{e(site['linkedinLabel'])}</span></span>
      </a>
      <div class="contact-card reveal">
        <span class="contact-card__icon">{ICONS['pin']}</span>
        <span style="min-width:0"><span class="contact-card__k" style="display:block">Location</span><span class="contact-card__v">{e(site['location'])}</span></span>
      </div>
    </div>
  </div>
</section>"""

    style_fix = """<style>
  @media (max-width: 980px) { .skills-layout { grid-template-columns: 1fr !important; } }
</style>"""

    body = style_fix + hero + about + exp + skills_section + projects_section + awards_section + contact
    return page(
        site,
        title=f"{site['name']} — {site['role']}",
        description=site["tagline"],
        body=body,
        home=True,
        canonical="index.html",
    )


# ---------------------------------------------------------------------------
# Listing pages
# ---------------------------------------------------------------------------

def build_listing(site: dict, section: str, entries: list[Entry], orgs: dict) -> str:
    base = "../"
    meta = SECTIONS[section]

    head = f"""<section class="listing-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">
      <a href="{base}index.html">Home</a><span class="sep">/</span><span>{e(meta['title'])}</span>
    </nav>
    <h1>{e(meta['title'])}</h1>
    <p class="section-head__lede text-muted" style="margin-top:.75rem;max-width:62ch">{e(meta['blurb'])}</p>
  </div>
</section>"""

    if section == "projects":
        ordered = sorted(entries, key=lambda x: x.sort_key, reverse=True)
        filters = f'<button class="filter is-active" data-value="all" aria-pressed="true">All<span class="filter__n">{len(ordered)}</span></button>'
        blocks = ""
        for org_id, org in orgs.items():
            items = [p for p in ordered if str(p.get("org")) == org_id]
            if not items:
                continue
            filters += (
                f'<button class="filter" data-value="{e(org_id)}" aria-pressed="false">{e(org["short"])}'
                f'<span class="filter__n">{len(items)}</span></button>'
            )
            cards = "".join(project_card(p, orgs, base) for p in items)
            blocks += f"""<div class="org" data-filter-section="projects">
      <div class="org__head">
        <span class="org__badge">{e(org['short'])}</span>
        <span class="org__title">
          <span class="org__name">{e(org['name'])}</span>
          <span class="org__kind">{e(org['kind'])} &middot; {e(org['period'])}</span>
        </span>
        <span class="org__count">{len(items)} project{'s' if len(items) != 1 else ''}</span>
        <p class="org__blurb">{e(org['blurb'])}</p>
      </div>
      <div class="grid grid--3">{cards}</div>
    </div>"""
        content = f'<div class="filters" data-filter-group="projects">{filters}</div>{blocks}'

    elif section == "experience":
        ordered = sorted(entries, key=lambda x: x.sort_key, reverse=True)
        content = '<div class="timeline">' + "".join(timeline_item(x, base) for x in ordered) + "</div>"

    elif section == "skills":
        categories: dict[str, list[Entry]] = {}
        for s in entries:
            categories.setdefault(str(s.get("category", "Other")), []).append(s)
        order = ["SAP Development", "Integration & Data", "Working & Leading"]
        ordered_cats = [c for c in order if c in categories] + [c for c in categories if c not in order]
        content = ""
        for cat in ordered_cats:
            cards = "".join(
                skill_card(s, base) for s in sorted(categories[cat], key=lambda x: -int(x.get("level", 0) or 0))
            )
            content += f'<div class="skill-group"><h2 class="skill-group__title">{e(cat)}</h2><div class="grid grid--2">{cards}</div></div>'

    else:  # awards
        ordered = sorted(entries, key=lambda x: str(x.get("date")), reverse=True)
        kinds: dict[str, int] = {}
        for a in ordered:
            kinds[str(a.get("type", "award"))] = kinds.get(str(a.get("type", "award")), 0) + 1
        filters = f'<button class="filter is-active" data-value="all" aria-pressed="true">All<span class="filter__n">{len(ordered)}</span></button>'
        for kind, count in kinds.items():
            filters += (
                f'<button class="filter" data-value="{e(kind)}" aria-pressed="false">'
                f'{e(AWARD_TYPE_LABEL.get(kind, kind.title()))}<span class="filter__n">{count}</span></button>'
            )
        cards = "".join(award_card(a, base) for a in ordered)
        content = f'<div class="filters" data-filter-group="awards">{filters}</div><div class="grid grid--3">{cards}</div>'

    body = head + f'<section class="section section--tight"><div class="wrap">{content}</div></section>'
    return page(
        site,
        title=f"{meta['title']} — {site['name']}",
        description=meta["blurb"],
        body=body,
        base=base,
        canonical=f"{section}/index.html",
    )


# ---------------------------------------------------------------------------
# Detail pages
# ---------------------------------------------------------------------------

def build_detail(site: dict, entry: Entry, siblings: list[Entry], orgs: dict) -> str:
    base = "../"
    section = entry.section
    meta = SECTIONS[section]
    org = orgs.get(str(entry.get("org")), {})

    facts: list[tuple[str, str]] = []
    if section == "projects":
        facts = [
            ("Client", str(entry.get("client", org.get("name", "—")))),
            ("Organization", str(org.get("name", "—"))),
            ("Role", str(entry.get("role", "—"))),
            ("Period", str(entry.get("period", "—"))),
        ]
    elif section == "experience":
        facts = [
            ("Company", str(entry.get("company", "—"))),
            ("Role", str(entry.title)),
            ("Period", str(entry.get("period", "—"))),
            ("Location", str(entry.get("location", "—"))),
        ]
    elif section == "skills":
        facts = [
            ("Category", str(entry.get("category", "—"))),
            ("Hands-on", f"{entry.get('years', '—')} years"),
            ("Proficiency", f"{entry.get('level', '—')}%"),
            ("Read", f"{entry.reading_time} min"),
        ]
    else:
        facts = [
            ("Type", AWARD_TYPE_LABEL.get(str(entry.get("type", "award")), "Award")),
            ("Issued by", str(entry.get("issuer", "—"))),
            ("Date", str(entry.get("date", "—"))),
            ("Read", f"{entry.reading_time} min"),
        ]

    factbar = '<div class="factbar">' + "".join(
        f'<div class="fact"><div class="fact__k">{e(k)}</div><div class="fact__v">{e(v)}</div></div>'
        for k, v in facts
    ) + "</div>"

    image = entry.get("image")
    hero_img = ""
    if image:
        hero_img = (
            f'<div class="article-hero reveal"><img src="{e(rebase(str(image), base))}" '
            f'alt="{e(entry.get("imageAlt", entry.title))}" width="1200" height="514"></div>'
        )

    external = ""
    if entry.get("link"):
        external = (
            f'<a class="btn btn--ghost" href="{e(entry.get("link"))}" target="_blank" rel="noopener noreferrer">'
            f'{e(entry.get("linkLabel", "External link"))} {ICONS["arrow"]}</a>'
        )

    highlights = ""
    if entry.highlights:
        items = "".join(f"<li>{inline_md(h, base)}</li>" for h in entry.highlights)
        label = "Responsibilities" if section == "experience" else "What I delivered"
        highlights = f'<div class="highlights reveal"><p class="highlights__title">{label}</p><ul>{items}</ul></div>'

    crumb_org = ""
    if org:
        crumb_org = f'<span class="sep">/</span><span>{e(org["short"])}</span>'

    ordered = sorted(siblings, key=lambda x: x.sort_key, reverse=True)
    try:
        index = next(i for i, s in enumerate(ordered) if s.slug == entry.slug)
    except StopIteration:
        index = 0
    prev_entry = ordered[index - 1] if index > 0 else None
    next_entry = ordered[index + 1] if index + 1 < len(ordered) else None

    def pager_link(target: Entry | None, direction: str) -> str:
        if not target:
            return '<span class="pager__spacer"></span>'
        cls = "pager__link pager__link--next" if direction == "next" else "pager__link"
        label = "Next" if direction == "next" else "Previous"
        return (
            f'<a class="{cls}" href="{e(base + target.url)}">'
            f'<span class="pager__k">{label}</span><span class="pager__t">{e(target.title)}</span></a>'
        )

    pager = f'<div class="pager">{pager_link(prev_entry, "prev")}{pager_link(next_entry, "next")}</div>'

    live = '<span class="pill pill--live">Ongoing</span>' if entry.get("current") else ""

    body = f"""<article>
  <header class="article-head">
    <div class="wrap wrap--narrow">
      <nav class="crumbs" aria-label="Breadcrumb">
        <a href="{base}index.html">Home</a><span class="sep">/</span>
        <a href="{base}{section}/index.html">{e(meta['title'])}</a>{crumb_org}
      </nav>
      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-bottom:.9rem">
        <span class="tag tag--accent">{e(entry.get('period', entry.get('date', '')))}</span>
        {live}
      </div>
      <h1>{e(entry.title)}</h1>
      <p class="article-head__lede">{e(entry.summary)}</p>
      <div class="article-head__tags">{tag_list(entry.tags)}</div>
      {factbar}
      {'<div style="margin-top:22px">' + external + '</div>' if external else ''}
    </div>
  </header>

  <div class="section section--tight">
    <div class="wrap wrap--narrow">
      {hero_img}
      {highlights}
      <div class="prose reveal">
{render_md(entry.body, base)}
      </div>

      <div class="cta-strip reveal">
        <div>
          <p class="cta-strip__title">Want the detail behind this?</p>
          <p class="cta-strip__sub">Happy to walk through the technical decisions in a conversation.</p>
        </div>
        <a class="btn btn--primary" href="mailto:{e(site['email'])}">{ICONS['mail']} Email me</a>
      </div>

      {pager}

      <p style="margin-top:28px">
        <a class="btn btn--quiet" href="{base}{section}/index.html">{ICONS['back']} All {e(meta['title'].lower())}</a>
      </p>
    </div>
  </div>
</article>"""

    return page(
        site,
        title=f"{entry.title} — {site['name']}",
        description=entry.summary or meta["blurb"],
        body=body,
        base=base,
        canonical=entry.url,
    )


# ---------------------------------------------------------------------------
# 404 + sitemap
# ---------------------------------------------------------------------------

def build_404(site: dict) -> str:
    body = f"""<section class="section" style="min-height:60vh;display:grid;place-items:center;text-align:center">
  <div class="wrap wrap--narrow">
    <p class="eyebrow" style="justify-content:center">Error 404</p>
    <h1>This page does not exist</h1>
    <p class="text-muted" style="margin:1rem 0 2rem">The link may be out of date, or the story has not been published yet.</p>
    <a class="btn btn--primary" href="{ROOT_PATH}">Back to the portfolio {ICONS['arrow']}</a>
  </div>
</section>"""
    return page(site, title=f"Not found — {site['name']}", description="Page not found.", body=body)


def public_url(path: str) -> str:
    """Canonical form of a page path — `a/index.html` is advertised as `a/`."""
    if path == "index.html":
        return ""
    if path.endswith("/index.html"):
        return path[: -len("index.html")]
    return path


def build_sitemap(urls: list[str]) -> str:
    today = date.today().isoformat()
    items = "".join(
        f"  <url><loc>{SITE_URL}/{public_url(u)}</loc><lastmod>{today}</lastmod></url>\n" for u in urls
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n'


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    global SITE_URL, ROOT_PATH

    site = json.loads((CONTENT / "site.json").read_text(encoding="utf-8"))
    orgs = {o["id"]: o for o in site["organizations"]}

    domain = str(site.get("customDomain", "")).strip().strip("/")
    SITE_URL = f"https://{domain}" if domain else str(site.get("siteUrl", SITE_URL)).rstrip("/")
    path = urlsplit(SITE_URL).path.rstrip("/")
    ROOT_PATH = f"{path}/" if path else "/"

    data = {section: load_entries(section) for section in SECTIONS}

    missing = [s for s, items in data.items() if not items]
    if missing:
        print(f"warning: no content found for {', '.join(missing)}", file=sys.stderr)

    written: list[str] = []

    def write(path: str, content: str) -> None:
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written.append(path)

    write("index.html", build_home(site, data, orgs))

    for section, entries in data.items():
        if not entries:
            continue
        write(f"{section}/index.html", build_listing(site, section, entries, orgs))
        for entry in entries:
            write(entry.url, build_detail(site, entry, entries, orgs))

    write("404.html", build_404(site))
    write("sitemap.xml", build_sitemap([p for p in written if p.endswith(".html") and p != "404.html"]))
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")

    # GitHub Pages reads CNAME to serve the site from a custom domain. Keeping it
    # generated means the domain lives in site.json rather than only in settings.
    if domain:
        write("CNAME", domain + "\n")
    elif (ROOT / "CNAME").exists():
        (ROOT / "CNAME").unlink()

    (ROOT / ".nojekyll").touch()

    print(f"Built {len(written)} files:")
    for section, entries in data.items():
        print(f"  {section:<12} {len(entries)} entr{'y' if len(entries) == 1 else 'ies'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
