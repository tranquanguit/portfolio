"""Generated visuals for the portfolio.

Everything here is drawn as SVG at build time, so the site has imagery even where
no photograph exists yet — and a real file dropped into `assets/img/...` always
takes precedence over the generated fallback.

    monogram()          organisation / client badge when no real logo is present
    cover()             article and project cover art, deterministic per slug
    cert_badge()        certification badge illustration
    award_medal()       award illustration
    illustration()      hand-drawn product illustrations (warehouse, document flow)
    diagram()           technical diagrams, inlined so they follow the colour theme
    tech_icons()        technology logos for a list of tags
"""

from __future__ import annotations

import hashlib
import html
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TECH_DIR = ROOT / "assets" / "img" / "tech"

FONT = "'Be Vietnam Pro', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"


def _e(text) -> str:
    return html.escape(str(text), quote=True)


def _seed(text: str) -> int:
    return int(hashlib.sha1(text.encode("utf-8")).hexdigest()[:8], 16)


def _wrap(text: str, width: int) -> list[str]:
    words, lines, line = str(text).split(), [], ""
    for word in words:
        if len(line) + len(word) + (1 if line else 0) > width:
            if line:
                lines.append(line)
            line = word
        else:
            line = f"{line} {word}" if line else word
    if line:
        lines.append(line)
    return lines


# ---------------------------------------------------------------------------
# Technology logos
# ---------------------------------------------------------------------------

# tag (lower case) -> logo file in assets/img/tech
TECH_ICONS = {
    "sap": "sap", "abap": "sap", "abap oo": "sap", "abap cloud": "sap", "rap": "sap",
    "rap model": "sap", "sap btp": "sap", "s/4hana": "sap", "sap s/4hana": "sap",
    "sap integration suite": "sap", "sap ci-ds": "sap", "sap pi/po": "sap", "sap ibp": "sap",
    "sap ewm": "sap", "sap analytics cloud": "sap", "fiori": "sap", "fiori elements": "sap",
    "sap certification": "sap", "sap generative ai": "sap", "cds views": "sap", "cds": "sap",
    "amdp": "sap", "bapi": "sap", "badi": "sap", "idoc": "sap", "event mesh": "sap",
    "cap": "sap", "master data governance": "sap", "mdg": "sap", "clean core": "sap",
    "private cloud": "sap", "mm": "sap", "wm": "sap", "sd": "sap", "fi": "sap", "co": "sap",
    "pp": "sap", "qm": "sap", "fm": "sap", "alv": "sap", "adobe forms": "sap", "bdc": "sap",
    "power bi": "microsoft-power-bi",
    "ms fabric": "microsoft", "microsoft fabric": "microsoft", "ssis": "microsoft",
    "ssas": "microsoft", "sql server": "microsoft", "lakehouse": "microsoft",
    "dataflow gen2": "microsoft", "t-sql": "microsoft",
    "python": "python", "postgresql": "postgresql", "react": "react",
    "typescript": "typescript", "fastapi": "fastapi", "elasticsearch": "elasticsearch",
    "docker": "docker", "flask": "flask", "salesforce": "salesforce", "mulesoft": "mulesoft",
    "jira automation": "jira", "jira": "jira", "git": "git", "oracle": "oracle",
    "pl/sql": "oracle", "java": "java", "javascript": "javascript", "fastify": "fastify",
    "bootstrap": "bootstrap", "nginx": "nginx", "openai": "openai", "rag": "openai",
    "llm": "openai", "pytorch": "pytorch", "deep learning": "pytorch", "vite": "vite",
    "sqlite": "sqlite", "zalo": "zalo",
}


def tech_icons(tags, limit: int | None = None) -> list[str]:
    """Unique logo names for `tags`, in order of first appearance."""
    seen: list[str] = []
    for tag in tags or []:
        name = TECH_ICONS.get(str(tag).strip().lower())
        if name and name not in seen and (TECH_DIR / f"{name}.svg").exists():
            seen.append(name)
    return seen[:limit] if limit else seen


def tech_icon_for(tag: str) -> str | None:
    name = TECH_ICONS.get(str(tag).strip().lower())
    return name if name and (TECH_DIR / f"{name}.svg").exists() else None


# ---------------------------------------------------------------------------
# Monogram badge
# ---------------------------------------------------------------------------

def monogram(text: str, bg: str = "#2c6baf", fg: str = "#ffffff", accent: str | None = None,
             size: int = 96) -> str:
    """A square badge with initials — a clean stand-in until a real logo is supplied."""
    text = str(text)[:4]
    fs = {1: 46, 2: 40, 3: 31, 4: 24}.get(len(text), 24)
    stripe = ""
    if accent:
        stripe = f'<rect x="0" y="78" width="96" height="18" fill="{_e(accent)}"/>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="{size}" height="{size}" '
        f'role="img" aria-label="{_e(text)}">'
        f'<defs><clipPath id="m{_seed(text + bg) % 99999}"><rect width="96" height="96" rx="20"/></clipPath></defs>'
        f'<g clip-path="url(#m{_seed(text + bg) % 99999})">'
        f'<rect width="96" height="96" fill="{_e(bg)}"/>'
        f'<circle cx="86" cy="10" r="34" fill="#fff" opacity=".08"/>'
        f'{stripe}</g>'
        f'<text x="48" y="{58 if not accent else 52}" text-anchor="middle" font-family="{FONT}" '
        f'font-weight="800" font-size="{fs}" letter-spacing="-1" fill="{_e(fg)}">{_e(text)}</text>'
        f'</svg>'
    )


# ---------------------------------------------------------------------------
# Covers
# ---------------------------------------------------------------------------

PALETTES = {
    "sap":     ("#0b3a6e", "#1c6fc4", "#7cc4ff"),
    "data":    ("#0f3b3a", "#1f7a6c", "#8fe0cf"),
    "ai":      ("#2a1f5c", "#5b45c4", "#c4b6ff"),
    "product": ("#3d2410", "#b0621d", "#ffd59a"),
    "award":   ("#3a2c06", "#a97f22", "#ffe08a"),
    "default": ("#16202b", "#2c6baf", "#9cc8f5"),
}


def palette_for(topic: str) -> tuple[str, str, str]:
    t = str(topic).lower()
    # The first word decides: "SAP & ERP" is an SAP topic even if its tags mention data.
    if "sap" in t or "erp" in t or "integration" in t:
        return PALETTES["sap"]
    if "ai" in t.split() or "ai &" in t or "rag" in t or "search" in t:
        return PALETTES["ai"]
    if "data" in t or "analytics" in t:
        return PALETTES["data"]
    if "product" in t or "business" in t:
        return PALETTES["product"]
    if "award" in t or "recognition" in t:
        return PALETTES["award"]
    return PALETTES["default"]


def cover(title: str, label: str, seed: str, topic: str = "", badge_svg: str = "",
          footer: str = "quangtv.com", width: int = 1200, height: int = 630) -> str:
    """Cover art: gradient, a seeded geometric field, a label and the title."""
    dark, mid, light = palette_for(topic or label)
    rnd = _seed(seed)
    shapes = []
    for i in range(14):
        rnd = (rnd * 1103515245 + 12345) & 0x7FFFFFFF
        x = 560 + (rnd % 640)
        rnd = (rnd * 1103515245 + 12345) & 0x7FFFFFFF
        y = (rnd % height)
        r = 18 + (rnd % 90)
        kind = (rnd >> 7) % 3
        op = 0.06 + ((rnd >> 3) % 10) / 100
        if kind == 0:
            shapes.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{light}" opacity="{op:.2f}"/>')
        elif kind == 1:
            shapes.append(f'<rect x="{x}" y="{y}" width="{r * 1.6:.0f}" height="{r * 1.6:.0f}" rx="{r / 4:.0f}" '
                          f'fill="none" stroke="{light}" stroke-width="2" opacity="{op + .08:.2f}" '
                          f'transform="rotate({(rnd >> 5) % 45} {x} {y})"/>')
        else:
            pts = " ".join(f"{x + r * math.cos(a):.0f},{y + r * math.sin(a):.0f}"
                           for a in (k * math.pi / 3 for k in range(6)))
            shapes.append(f'<polygon points="{pts}" fill="{light}" opacity="{op:.2f}"/>')

    lines = _wrap(title, 26)[:4]
    fs = 58 if len(lines) <= 2 else 48
    lh = fs * 1.18
    y0 = height / 2 - (len(lines) - 1) * lh / 2 - 30
    title_svg = "".join(
        f'<text x="72" y="{y0 + i * lh:.0f}" font-family="{FONT}" font-weight="800" font-size="{fs}" '
        f'fill="#fff" letter-spacing="-1.5">{_e(line)}</text>'
        for i, line in enumerate(lines)
    )
    badge = ""
    if badge_svg:
        badge = f'<g transform="translate({width - 72 - 150},{height - 72 - 150})">' \
                f'<svg x="0" y="0" width="150" height="150" viewBox="0 0 96 96">{_strip_svg(badge_svg)}</svg></g>'
    gid = f"g{_seed(seed) % 99999}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="{_e(title)}" preserveAspectRatio="xMidYMid slice">'
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{dark}"/><stop offset="1" stop-color="{mid}"/></linearGradient></defs>'
        f'<rect width="{width}" height="{height}" fill="url(#{gid})"/>'
        f'{"".join(shapes)}'
        f'<rect x="72" y="70" width="{max(120, 13 * len(label) + 36)}" height="40" rx="20" fill="#fff" opacity=".14"/>'
        f'<text x="90" y="97" font-family="{MONO}" font-size="18" letter-spacing="2" fill="#fff">{_e(label.upper())}</text>'
        f'{title_svg}'
        f'<text x="72" y="{height - 64}" font-family="{MONO}" font-size="18" fill="{light}" opacity=".9">{_e(footer)}</text>'
        f'{badge}'
        f'</svg>'
    )


def _strip_svg(svg: str) -> str:
    """Inner markup of an <svg> element, for nesting inside another drawing."""
    start = svg.find(">") + 1
    end = svg.rfind("</svg>")
    return svg[start:end]


# ---------------------------------------------------------------------------
# Certification badge and award medal
# ---------------------------------------------------------------------------

def cert_badge(title: str, code: str, level: str = "Associate", issuer: str = "SAP",
               date: str = "", size: int = 320) -> str:
    """Badge illustration for a certification (not the official badge image)."""
    pro = level.lower().startswith("pro")
    c1, c2 = ("#0a3a73", "#1f7fd6") if not pro else ("#3b1d6e", "#7b4ad6")
    ring = "#ffd257" if pro else "#9fd2ff"
    lines = _wrap(title, 18)[:3]
    tl = "".join(
        f'<text x="160" y="{176 + i * 24}" text-anchor="middle" font-family="{FONT}" font-weight="700" '
        f'font-size="19" fill="#fff">{_e(line)}</text>' for i, line in enumerate(lines)
    )
    hexpts = " ".join(f"{160 + 150 * math.cos(k * math.pi / 3):.1f},"
                      f"{160 + 150 * math.sin(k * math.pi / 3):.1f}" for k in range(6))
    inner = " ".join(f"{160 + 136 * math.cos(k * math.pi / 3):.1f},"
                     f"{160 + 136 * math.sin(k * math.pi / 3):.1f}" for k in range(6))
    gid = f"cb{_seed(title + code) % 99999}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 320" width="{size}" height="{size}" '
        f'role="img" aria-label="{_e(issuer)} {_e(level)} — {_e(title)}">'
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{c2}"/><stop offset="1" stop-color="{c1}"/></linearGradient></defs>'
        f'<polygon points="{hexpts}" fill="{ring}"/>'
        f'<polygon points="{inner}" fill="url(#{gid})"/>'
        f'<text x="160" y="92" text-anchor="middle" font-family="{FONT}" font-weight="800" font-size="30" '
        f'fill="#fff" letter-spacing="1">{_e(issuer)}</text>'
        f'<text x="160" y="116" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="2" '
        f'fill="{ring}">CERTIFIED {_e(level.upper())}</text>'
        f'<line x1="104" y1="140" x2="216" y2="140" stroke="#fff" stroke-opacity=".35"/>'
        f'{tl}'
        f'<text x="160" y="{176 + len(lines) * 24 + 18}" text-anchor="middle" font-family="{MONO}" '
        f'font-size="14" fill="#fff" opacity=".85">{_e(code)}</text>'
        f'<text x="160" y="252" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#fff" '
        f'opacity=".7">{_e(date)}</text>'
        f'</svg>'
    )


def award_medal(title: str, issuer: str, year: str, glyph: str = "★", size: int = 320) -> str:
    lines = _wrap(title, 20)[:3]
    tl = "".join(
        f'<text x="160" y="{196 + i * 21}" text-anchor="middle" font-family="{FONT}" font-weight="700" '
        f'font-size="17" fill="#3a2c06">{_e(line)}</text>' for i, line in enumerate(lines)
    )
    rays = "".join(
        f'<rect x="157" y="20" width="6" height="26" rx="3" fill="#e9b949" opacity=".55" '
        f'transform="rotate({k * 30} 160 160)"/>' for k in range(12)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 320" width="{size}" height="{size}" '
        f'role="img" aria-label="{_e(title)}">'
        f'{rays}'
        f'<circle cx="160" cy="160" r="112" fill="#f6d77a"/>'
        f'<circle cx="160" cy="160" r="100" fill="#fff6d8" stroke="#e2b23e" stroke-width="3"/>'
        f'<text x="160" y="150" text-anchor="middle" font-family="{FONT}" font-size="58" fill="#c9971f">{_e(glyph)}</text>'
        f'{tl}'
        f'<text x="160" y="{196 + len(lines) * 21 + 6}" text-anchor="middle" font-family="{MONO}" '
        f'font-size="12" fill="#8a6a14">{_e(year)}</text>'
        f'</svg>'
    )


# ---------------------------------------------------------------------------
# Product illustrations
# ---------------------------------------------------------------------------

def _iso(x, y, z):
    """Isometric projection of a grid point."""
    return 600 + (x - y) * 46, 250 + (x + y) * 23 - z * 46


def illustration_warehouse() -> str:
    """Isometric warehouse — racks coloured by occupancy, as the sapwm3d cockpit shows it."""
    status = {0: ("#3f8f5a", "#5fb27a", "#2f6e45"),     # normal
              1: ("#c2872a", "#e3a94a", "#94661c"),     # near capacity
              2: ("#b84a3a", "#d96b5a", "#8a3529"),     # overloaded
              3: ("#6b7885", "#8b98a5", "#4e5a66")}     # blocked
    rnd = 7
    cubes = []
    for row in range(5):
        for col in range(7):
            if col == 3:
                continue  # aisle
            height = 1 + ((row * 7 + col * 3) % 3)
            for level in range(height):
                rnd = (rnd * 1103515245 + 12345) & 0x7FFFFFFF
                s = 0 if rnd % 10 < 6 else (1 if rnd % 10 < 8 else (2 if rnd % 10 < 9 else 3))
                cubes.append((col, row, level, s))
    cubes.sort(key=lambda c: (c[0] + c[1], c[2]))
    faces = []
    for x, y, z, s in cubes:
        top, left, right = status[s]
        a, b = _iso(x, y, z + 1), _iso(x + 1, y, z + 1)
        c, d = _iso(x + 1, y + 1, z + 1), _iso(x, y + 1, z + 1)
        b0, c0, d0 = _iso(x + 1, y, z), _iso(x + 1, y + 1, z), _iso(x, y + 1, z)
        p = lambda *pts: " ".join(f"{u:.0f},{v:.0f}" for u, v in pts)
        faces.append(f'<polygon points="{p(a, b, c, d)}" fill="{left}" stroke="#0d1317" stroke-opacity=".25"/>')
        faces.append(f'<polygon points="{p(d, c, c0, d0)}" fill="{top}" stroke="#0d1317" stroke-opacity=".25"/>')
        faces.append(f'<polygon points="{p(b, c, c0, b0)}" fill="{right}" stroke="#0d1317" stroke-opacity=".25"/>')
    floor = " ".join(f"{u:.0f},{v:.0f}" for u, v in (_iso(-.4, -.4, 0), _iso(7.4, -.4, 0),
                                                       _iso(7.4, 5.4, 0), _iso(-.4, 5.4, 0)))
    legend = ""
    for i, (label, s) in enumerate([("Normal", 0), ("Near capacity", 1), ("Overloaded", 2), ("Blocked", 3)]):
        legend += (f'<rect x="{56 + i * 190}" y="560" width="18" height="18" rx="4" fill="{status[s][1]}"/>'
                   f'<text x="{84 + i * 190}" y="574" font-family="{FONT}" font-size="17" fill="#c9d4de">{label}</text>')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img" '
        'aria-label="Isometric warehouse with storage bins coloured by occupancy">'
        '<defs><linearGradient id="whbg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#0d1a24"/><stop offset="1" stop-color="#16324a"/></linearGradient></defs>'
        '<rect width="1200" height="630" fill="url(#whbg)"/>'
        f'<polygon points="{floor}" fill="#1f3a52" stroke="#3d6a8f" stroke-width="2"/>'
        f'{"".join(faces)}'
        f'<text x="56" y="80" font-family="{MONO}" font-size="18" letter-spacing="3" fill="#7cc4ff">WAREHOUSE COCKPIT</text>'
        f'<text x="56" y="122" font-family="{FONT}" font-weight="800" font-size="36" fill="#fff">Where is the capacity problem?</text>'
        f'{legend}'
        '</svg>'
    )


def illustration_docflow() -> str:
    """One order record feeding four generated documents — the SofaFlow idea."""
    docs = [("Quotation", "Báo giá", "#2c6baf"), ("Contract", "Hợp đồng", "#1f7a6c"),
            ("Handover", "Bàn giao", "#a97f22"), ("Payment", "Thanh toán", "#7b4ad6")]
    out = []
    for i, (en, vi, color) in enumerate(docs):
        x = 520 + i * 160
        out.append(
            f'<g transform="translate({x},190)">'
            f'<path d="M0 0h104l28 28v196H0z" fill="#fff" stroke="{color}" stroke-width="3"/>'
            f'<path d="M104 0v28h28" fill="none" stroke="{color}" stroke-width="3"/>'
            f'<rect x="14" y="20" width="62" height="10" rx="3" fill="{color}"/>'
            + "".join(f'<rect x="14" y="{50 + k * 22}" width="{104 - (k % 3) * 18}" height="7" rx="3" fill="#d9dee4"/>'
                      for k in range(6))
            + f'<text x="66" y="262" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="18" fill="#fff">{en}</text>'
            f'<text x="66" y="286" text-anchor="middle" font-family="{FONT}" font-size="15" fill="#c9d4de">{vi}</text>'
            f'</g>'
        )
        out.append(f'<path d="M330 315 C 420 315, 440 {300 + (i - 1.5) * 4:.0f}, {x - 6} 300" fill="none" '
                   f'stroke="{color}" stroke-width="3" stroke-dasharray="7 6" opacity=".9"/>')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img" '
        'aria-label="One order record generating a quotation, contract, handover note and payment record">'
        '<defs><linearGradient id="dfbg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#2a1a0c"/><stop offset="1" stop-color="#5a3415"/></linearGradient></defs>'
        '<rect width="1200" height="630" fill="url(#dfbg)"/>'
        '<g transform="translate(90,215)">'
        '<rect width="240" height="200" rx="18" fill="#ffd59a"/>'
        f'<text x="24" y="44" font-family="{MONO}" font-size="15" letter-spacing="2" fill="#5a3415">ORDER</text>'
        f'<text x="24" y="82" font-family="{FONT}" font-weight="800" font-size="26" fill="#3d2410">One record</text>'
        + "".join(f'<rect x="24" y="{106 + k * 22}" width="{190 - k * 24}" height="9" rx="4" fill="#c98a3d" opacity=".6"/>'
                  for k in range(4))
        + '</g>'
        + "".join(out)
        + f'<text x="90" y="110" font-family="{MONO}" font-size="18" letter-spacing="3" fill="#ffd59a">SOFAFLOW</text>'
        f'<text x="90" y="152" font-family="{FONT}" font-weight="800" font-size="36" fill="#fff">Enter it once. Every document follows.</text>'
        '</svg>'
    )


ILLUSTRATIONS = {"warehouse": illustration_warehouse, "docflow": illustration_docflow}


def illustration(name: str) -> str | None:
    fn = ILLUSTRATIONS.get(name)
    return fn() if fn else None


# ---------------------------------------------------------------------------
# Technical diagrams — inlined into the page so CSS variables theme them
# ---------------------------------------------------------------------------

def _box(x, y, w, h, title, sub="", kind="box", align="middle"):
    cls = {"box": "dg-box", "accent": "dg-accent", "soft": "dg-soft", "gold": "dg-gold"}[kind]
    tx = x + w / 2 if align == "middle" else x + 16
    on = " on-accent" if kind == "accent" else ""
    out = f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>'
    ty = y + (h / 2 + 6 if not sub else h / 2 - 4)
    out += (f'<text class="dg-title{on}" x="{tx}" y="{ty:.0f}" text-anchor="{"middle" if align == "middle" else "start"}">'
            f'{_e(title)}</text>')
    if sub:
        for i, line in enumerate(_wrap(sub, max(10, int(w / 8.2)))[:2]):
            out += (f'<text class="dg-sub{on}" x="{tx}" y="{ty + 20 + i * 16:.0f}" '
                    f'text-anchor="{"middle" if align == "middle" else "start"}">{_e(line)}</text>')
    return out


def _arrow(x1, y1, x2, y2, label=""):
    out = f'<line class="dg-line" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#dg-arrow)"/>'
    if label:
        out += f'<text class="dg-label" x="{(x1 + x2) / 2:.0f}" y="{(y1 + y2) / 2 - 8:.0f}" text-anchor="middle">{_e(label)}</text>'
    return out


def _frame(w, h, body, label):
    return (
        f'<svg class="diagram" viewBox="0 0 {w} {h}" role="img" aria-label="{_e(label)}" '
        f'xmlns="http://www.w3.org/2000/svg">'
        '<defs><marker id="dg-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path class="dg-head" d="M0 0L10 5L0 10z"/></marker></defs>'
        f'{body}</svg>'
    )


def pipeline(stages, label, width=960, box_h=86, note=""):
    """Left-to-right stages. Each stage: (title, subtitle, kind)."""
    n = len(stages)
    gap = 34
    w = (width - 40 - gap * (n - 1)) / n
    body = ""
    for i, (title, sub, kind) in enumerate(stages):
        x = 20 + i * (w + gap)
        body += _box(x, 30, w, box_h, title, sub, kind)
        if i < n - 1:
            body += _arrow(x + w + 4, 30 + box_h / 2, x + w + gap - 4, 30 + box_h / 2)
    h = 30 + box_h + 30
    if note:
        body += f'<text class="dg-note" x="{width / 2}" y="{h + 2}" text-anchor="middle">{_e(note)}</text>'
        h += 24
    return _frame(width, h, body, label)


def stack(layers, label, width=760, layer_h=74, side=None):
    """Top-to-bottom layers. Each layer: (title, subtitle, kind)."""
    body = ""
    x, w = 20, (width - 40) if not side else (width - 300)
    for i, (title, sub, kind) in enumerate(layers):
        y = 20 + i * (layer_h + 22)
        body += _box(x, y, w, layer_h, title, sub, kind, align="start")
        if i < len(layers) - 1:
            body += _arrow(x + 40, y + layer_h + 2, x + 40, y + layer_h + 20)
    h = 20 + len(layers) * (layer_h + 22)
    if side:
        sx = w + 60
        body += f'<text class="dg-label" x="{sx}" y="34">{_e(side[0])}</text>'
        for i, (title, kind) in enumerate(side[1]):
            y = 50 + i * 62
            body += _box(sx, y, 220, 48, title, "", kind)
            body += f'<path class="dg-line" d="M{sx} {y + 24} H{w + 30}" marker-end="url(#dg-arrow)" fill="none"/>'
    return _frame(width, h, body, label)


def columns(cols, label, width=960, head_h=58, item_h=40):
    """Side-by-side option columns: (title, subtitle, kind, [items])."""
    n = len(cols)
    gap = 22
    w = (width - 40 - gap * (n - 1)) / n
    body, h = "", 0
    for i, (title, sub, kind, items) in enumerate(cols):
        x = 20 + i * (w + gap)
        body += _box(x, 20, w, head_h + 22, title, sub, kind)
        for j, item in enumerate(items):
            y = 20 + head_h + 36 + j * (item_h + 10)
            body += _box(x, y, w, item_h, item, "", "box")
            h = max(h, y + item_h + 20)
    return _frame(width, h, body, label)


DIAGRAMS = {
    "rap-stack": lambda: stack(
        [("CDS data model", "Entities, associations and the shape of the data", "soft"),
         ("Behaviour definition", "What can happen: create, update, actions, validations, determinations, locking", "accent"),
         ("Behaviour implementation", "ABAP classes where that behaviour actually runs", "box"),
         ("Projection & service binding", "A consumer-shaped view, exposed as OData V4", "soft")],
        "The four layers of a RAP business object, and who consumes it",
        side=("One contract, every consumer",
              [("Fiori Elements app", "box"), ("External system via OData", "box"), ("ABAP code via EML", "box")])),
    "medallion": lambda: pipeline(
        [("Sources", "SAP HANA · Oracle · application DB · Excel", "box"),
         ("Bronze", "Raw, as it arrived", "gold"),
         ("Silver", "Conformed and cleansed — the rules live here", "soft"),
         ("Gold", "Modelled for the questions people ask", "accent"),
         ("Power BI", "Governed semantic model", "box")],
        "Medallion architecture from sources to Power BI",
        note="Same idea as staging → cleansed → presentation on SQL Server; on Fabric it runs in a Lakehouse."),
    "integration-landscape": lambda: pipeline(
        [("S/4HANA", "IDoc · OData · RFC", "box"),
         ("SAP Integration Suite", "iFlows · 75 inbound checks · error passthrough", "accent"),
         ("SimpleMDG on SAP BTP", "Governed master data: BP, Product", "soft"),
         ("Event Mesh", "Approved changes published as events", "gold"),
         ("Consumers", "Salesforce via MuleSoft · flat files · DWH", "box")],
        "Master data integration landscape around SimpleMDG",
        note="Validate at the door, govern in one place, publish changes as events."),
    "clean-core": lambda: columns(
        [("In-stack · ABAP Cloud", "Logic that belongs to the business object", "accent",
          ["Released APIs only", "RAP business objects", "Released extension points"]),
         ("Side-by-side · SAP BTP", "Own lifecycle, serves many backends", "soft",
          ["CAP or RAP on BTP", "Own release cadence", "Multi-tenant products"]),
         ("Integration · in between", "Each side owns its part", "gold",
          ["Integration Suite iFlows", "Event Mesh", "APIs and IDocs"])],
        "Three answers to where an extension should live under clean core"),
    "code-pushdown": lambda: columns(
        [("Classic: data to code", "Read everything, loop on the app server", "gold",
          ["SELECT * into internal table", "LOOP … SELECT inside", "Aggregate in ABAP", "Minutes at production volume"]),
         ("HANA: code to data", "Let the database do the work", "accent",
          ["CDS view: joins + aggregation", "AMDP when logic needs SQLScript", "Return only what is shown", "Seconds at production volume"])],
        "Moving work from the application server to the database"),
    "ai-gate": lambda: pipeline(
        [("Scoped task", "Bounded, one object pattern", "box"),
         ("AI coding agent", "Generates objects at scale", "soft"),
         ("ADT REST deploy", "Push and activate", "box"),
         ("Byte comparison", "Git ↔ live system must match exactly", "accent"),
         ("Human review", "Sign-off before any customer system", "gold")],
        "AI-assisted delivery behind a verification gate",
        note="The agent is a fast typist. The gate is the engineering."),
}


def diagram(name: str) -> str | None:
    fn = DIAGRAMS.get(name)
    return fn() if fn else None
