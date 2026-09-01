# tipfolio.app

The marketing and support site for the Tipfolio iPhone app. Static HTML, no build
dependencies beyond Python 3, deployed to GitHub Pages.

```
src/          source — edit here
  build.py    generator: layout, nav, footer, SEO block, sitemap, guardrails
  content_*.py  page content
  content/    raw HTML bodies for the long legal pages
docs/         GENERATED OUTPUT — GitHub Pages serves the site from here
  assets/     css, js, images (hand-maintained, not regenerated)
```

## Build

```sh
python3 src/build.py
```

Writes 24 pages plus `404.html`, `sitemap.xml`, `robots.txt`, `CNAME` and
`.nojekyll` into `docs/`. It exits non-zero if anything is wrong.

**Never edit files in `docs/` directly** — the next build overwrites them.
The one exception is `docs/assets/`, which the generator does not touch.

Preview locally (absolute asset paths mean `file://` will not work):

```sh
cd docs && python3 -m http.server 8000    # then open http://localhost:8000
```

## Deploy to GitHub Pages

This repo is already initialised with a first commit. To publish it:

```sh
cd "~/Claude Projects/Tip-Folio/tipfolio-website"
gh repo create tipfolio-website --public --source=. --push
```

(Or create the repo on github.com and
`git remote add origin git@github.com:<you>/tipfolio-website.git && git push -u origin main`.)

Then in the repo: **Settings → Pages → Source: Deploy from a branch → `main` / `/docs`**.

The repo must be **public** for GitHub Pages on a free account.

## Deploy to Vercel

`vercel.json` at the repo root already points Vercel at `docs/`. Without it you
get `404: NOT_FOUND`, because Vercel serves the repo root and there is no
`index.html` there — the site is generated into `docs/`.

If a project already exists and still 404s, the dashboard setting overrides the
file: **Project → Settings → Build & Deployment → Root Directory → `docs`**, or
leave Root Directory empty and let `outputDirectory` in `vercel.json` do it.
Redeploy after changing it.

⚠️ `trailingSlash: true` in `vercel.json` is load-bearing. The app ships
`/terms/` and `/privacy/` **with** trailing slashes, and every canonical URL
matches. Do not turn it off.

`CNAME` and `.nojekyll` are GitHub Pages artefacts. Vercel ignores both, so they
are harmless if you host here instead.

DNS for `tipfolio.app`:

| Type | Name | Value |
|---|---|---|
| A | `@` | `185.199.108.153`, `.109.153`, `.110.153`, `.111.153` |
| CNAME | `www` | `<you>.github.io` |

`CNAME` is already in the output. Once DNS resolves, tick **Enforce HTTPS**.

⚠️ The app ships `https://tipfolio.app/terms/` and `https://tipfolio.app/privacy/`
with trailing slashes (`LegalLinks` in `PaywallView.swift`). Both resolve as
directories here, so the URLs work with no redirect — keep it that way. A
redirect through a plain `http://` hop is an App Review problem.

SEO — what's built in, what was measured, and the Search Console steps — is in
[SEO.md](SEO.md).

## Things to change before launch

1. **`APP_STORE_URL` in `src/build.py` is empty**, so every call to action renders as
   a disabled "Coming soon" chip rather than a dead link. Paste the listing URL
   there once the app is live and rebuild — every page updates at once.
2. **`support@tipfolio.app` must actually receive mail.** It is on every page, in
   both legal documents, and is what Apple will use.
3. **`GSC_TOKEN` in `src/build.py` is empty** — paste the Search Console
   verification token there if you use the HTML-tag method. See [SEO.md](SEO.md).
4. **Verify the tax parameters.** `TAX` in `src/build.py` mirrors `AppConfig.Tax` in
   the app — the $25,000 cap, the 2025–2028 years, the net-of-tip-out definition
   and the 22% illustration. These are still unverified against primary IRS
   guidance (see `Marketing/APPLE-POLICY-AUDIT.md`). They are now published on a
   public website, which raises the stakes: **verify before submitting the
   sitemap to Google Search Console.**
5. **Have the two legal pages reviewed.** They are the operator's own terms, not
   advice from counsel.

## House rules the generator enforces

`src/build.py` fails the build rather than publishing a page that breaks these:

- **A page whose body states a tax figure must carry the disclaimer.** Checked
  against the body, not the footer.
- **Titles ≤ 65 characters; descriptions 70–165 characters.**
- **No duplicate titles or descriptions** across the site.
- **Exactly one `<h1>` per page, and no skipped heading levels.**

And two rules it keeps by construction:

- **Zero third-party requests.** No webfonts, no analytics, no CDNs, no
  trackers. The site makes the same promise the app does, so it has to be able
  to keep it. Apple devices — the whole audience, since Tipfolio is iPhone-only —
  render SF Pro Rounded, the exact face the app uses.
- **Tax constants live in one place.** `TAX` in `src/build.py`, mirroring
  `AppConfig.Tax`. Never hard-code a cap or a year into page copy.

## Calculators

`docs/assets/js/calc.js` is a port of `TipCalculator.swift` and
`TaxEngine.swift`. It keeps money in integer cents and carries across the app's
honesty rules deliberately:

- a tip-out never exceeds the tips earned, nor goes negative;
- a percent-of-sales rule with no sales figure yields **zero**, not a guess;
- net tips never go below zero;
- a rate with zero hours is **not shown at all**.

If the app's maths changes, change it here in the same commit.

## Adding a page

```python
# in the right src/content_*.py
add(Page(
    "/guides/my-new-guide/",
    "Title under 65 characters",
    "Description between 70 and 165 characters.",
    body_html,
    og_type="article",
    trail=[("Home", "/"), ("Guides", "/guides/"), ("My new guide", None)],
    nav="/guides/",
    priority="0.85",
))
```

It is picked up by the sitemap automatically. Link to it from somewhere — the
build does not check for orphans, but an unlinked page will not rank.
