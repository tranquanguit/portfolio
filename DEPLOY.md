# Deploy

The site is plain static HTML. It needs **no server, no Node, no database** —
only a host that serves files. GitHub Pages does this for free, including HTTPS
on your own domain.

---

## 1. Publish on GitHub Pages (current setup)

The generated `.html` files are committed to the repository, so publishing is
just a settings change.

1. GitHub → your repository → **Settings** → **Pages**
2. **Source**: `Deploy from a branch`
3. **Branch**: `main`, folder `/ (root)` → **Save**

Live at `https://tranquanguit.github.io/portfolio/` after a minute or two.

From then on, every `git push` to `main` updates the site automatically.

---

## 2. Point your own domain at it

Still no server. GitHub keeps hosting the files; your domain just points there.

### Step 1 — set the domain in this repo

Edit `content/site.json`:

```json
"customDomain": "quangtran.dev",
```

Then rebuild and push:

```bash
python3 tools/build.py
git add -A && git commit -m "Point site at custom domain" && git push
```

This writes a `CNAME` file (which is how GitHub Pages recognises the domain) and
rewrites the canonical links and `sitemap.xml` to the new address. Leave
`customDomain` empty to go back to the github.io URL — the `CNAME` file is
removed automatically.

### Step 2 — configure DNS at your registrar

Where you bought the domain (Namecheap, GoDaddy, Cloudflare, Porkbun, Mat Bao,
PA Vietnam …), open the DNS records and add:

**If you want the apex domain** (`quangtran.dev`) — four `A` records:

| Type | Host | Value |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |

Optionally add the IPv6 equivalents as `AAAA` records:
`2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`,
`2606:50c0:8003::153`.

**If you want a subdomain** (`portfolio.quangtran.dev` or `www.quangtran.dev`)
— one `CNAME` record instead, which is simpler and more robust:

| Type | Host | Value |
| --- | --- | --- |
| CNAME | `portfolio` | `tranquanguit.github.io.` |

> These IP addresses are GitHub's published Pages addresses. They change very
> rarely, but confirm them against
> <https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site>
> before you type them in.

### Step 3 — tell GitHub

Settings → Pages → **Custom domain** → enter the domain → **Save**.

GitHub checks the DNS. Once it passes, tick **Enforce HTTPS** — the certificate
is issued free by Let's Encrypt and renews itself.

### Step 4 — wait

DNS propagation takes anywhere from a few minutes to a few hours. Check with:

```bash
dig +short quangtran.dev
curl -sI https://quangtran.dev | head -1
```

**Note:** if you use Cloudflare as your DNS, set the records to **DNS only**
(grey cloud), not proxied, until GitHub has issued the certificate. Proxying
before that blocks the validation.

---

## 3. Other hosts

The same files work anywhere. If you ever want to move off GitHub Pages:

| Host | How | Notes |
| --- | --- | --- |
| **Cloudflare Pages** | Connect the repo | Free, fast in Vietnam, free custom domain + HTTPS |
| **Netlify** / **Vercel** | Connect the repo | Free tier, custom domain + HTTPS |
| **Any shared hosting / VPS** | Upload the files by FTP | Point the web root at the repository root |

For the first three, set the build command to `python3 tools/build.py` and the
output directory to `.` — or leave the build command empty, since the HTML is
already committed.

If you move host, update `siteUrl` (or `customDomain`) in `content/site.json`
and rebuild so the canonical links and sitemap stay correct.

---

## Which domain should you buy?

For a professional portfolio, an apex domain with your name reads best:
`quangtran.dev`, `tranvanquang.com`, `quangtran.io`. `.dev` and `.io` are common
for developers; `.com` is the safest for recruiters. Expect roughly USD 10–15
per year — the hosting itself stays free.
