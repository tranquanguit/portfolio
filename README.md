# Portfolio — Tran Van Quang

Static portfolio site for an SAP Technical Consultant. No frameworks, no CDN
dependencies, no build tooling beyond Python 3.

Live: <https://tranquanguit.github.io/portfolio>

## How it works

All content lives in `content/`. A single script turns it into the HTML pages
at the repository root.

```
content/site.json          profile, contact, stats, education, certifications, organizations
content/experience/*.md    one file per role      → /experience/<slug>.html
content/projects/*.md      one file per project   → /projects/<slug>.html
content/skills/*.md        one file per skill     → /skills/<slug>.html
content/awards/*.md        one file per award     → /awards/<slug>.html
```

Every entry gets its own page, so each project can be told as a story and each
skill written up as a piece of sharing. The home page is assembled from the same
files — write once, and it appears in both places.

## Build

```bash
python3 tools/build.py
```

That regenerates `index.html`, the four listing pages, every detail page,
`sitemap.xml` and `robots.txt`. Commit the generated HTML — GitHub Pages serves
it directly.

**Do not edit the generated `.html` files by hand** — the next build overwrites
them. Edit the markdown in `content/` instead.

## Adding a project

Create `content/projects/my-project.md`:

```markdown
---
title: SAP S/4HANA Implementation — Client Name
slug: my-project
org: fis                      # must match an id in site.json → organizations
client: Client Name
period: 01/2026 – 06/2026
start: 2026-01                # drives ordering (newest first)
end: 2026-06
role: ABAP Developer
image: assets/img/client.jpg  # optional
link: https://example.com     # optional external link
linkLabel: Read the announcement
summary: One or two sentences shown on the card.
tags: [S/4HANA, MM, ABAP OO]
highlights:
  - Bullet shown in the "What I delivered" box.
  - Another bullet.
---

## Context

The story goes here, in markdown.
```

Then run the build. The project appears on the home page under its organization
group, in the projects listing, in the filter counts, and as its own page.

### Adding a new organization group

Add an entry to `organizations` in `content/site.json`:

```json
{ "id": "neworg", "name": "Full Name", "short": "SHORT", "kind": "Company",
  "period": "2026 – Present", "blurb": "One line about the work there." }
```

Any entry with `org: neworg` is then grouped under it. Groups appear in the
order they are listed in `site.json`.

## Frontmatter reference

| Field | Applies to | Notes |
| --- | --- | --- |
| `title` | all | Page and card heading |
| `slug` | all | Output filename; defaults to the file name |
| `summary` | all | Card description and page lede |
| `tags` | all | Inline list: `[a, b, c]` |
| `highlights` | all | Indented `- ` list; renders as the highlight box |
| `period`, `start`, `end` | all | `start` drives sort order |
| `org` | projects, experience, awards | Organization id from `site.json` |
| `current: true` | projects, experience | Shows the "Ongoing" / "Current" pill |
| `image`, `imageAlt` | projects | Card and article hero image |
| `link`, `linkLabel` | projects | External reference button |
| `client`, `role` | projects | Shown in the fact bar |
| `company`, `location` | experience | Shown in the fact bar |
| `category`, `icon`, `short`, `level`, `years` | skills | `level` (0–100) drives the meter |
| `featured: true` + `short` | skills | Included in the radar chart (top 6 by level) |
| `type` | awards | `award`, `certification`, `achievement` — drives the filter |
| `issuer`, `date`, `code` | awards | Shown in the fact bar |

## Markdown supported in the body

Headings (`##`, `###`), paragraphs, bullet and numbered lists, **bold**,
*italic*, `code`, fenced code blocks, links, images, blockquotes, horizontal
rules, and pipe tables. That is the full set the renderer handles — anything
else is passed through as plain text.

## Layout

```
assets/css/style.css   design tokens and all styling (light + dark)
assets/js/main.js      theme toggle, nav, scroll reveal, filters
assets/img/            images
tools/build.py         the generator
```

Colours, spacing and typography are all CSS custom properties at the top of
`style.css`. Dark mode is derived from the same tokens and follows the system
setting until the visitor uses the toggle.
