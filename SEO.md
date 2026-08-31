# SEO

What is already built in, what was measured, and the steps only you can do.

## Built in

Every page is generated from one layout, so these hold site-wide and cannot
drift page to page.

| | |
|---|---|
| Unique `<title>` | 26/26, all ≤ 65 chars — build fails on a duplicate or an overlong one |
| Unique meta description | 26/26, all 70–165 chars — same guardrail |
| Canonical URL | 26/26 |
| Open Graph + Twitter card | 26/26, with a 1200×630 image |
| `og:locale`, `author` | 26/26 |
| Exactly one `<h1>` | 26/26 — build fails otherwise |
| No skipped heading levels | 26/26 — build fails otherwise |
| Breadcrumbs + `BreadcrumbList` | 24 pages |
| `Article` schema | 11 (guides + role pages) |
| `FAQPage` schema | 15 |
| `Organization` + `WebSite` | home page — brand entity for sitelinks |
| `SoftwareApplication` | home page |
| Alt text | every content image; decorative logos correctly `alt=""` |
| `width`/`height` on images | every image — this is why CLS is zero |
| Internal links | no broken links, no orphan pages |
| `sitemap.xml` / `robots.txt` | generated on every build |
| 404 | `noindex`, and returns real navigation |

### Measured, in a real browser

| Page | LCP | CLS | Weight | Requests |
|---|---|---|---|---|
| Home | 168 ms | 0.000 | 100 KB | 6 |
| Guide | 116 ms | 0.000 | 45 KB | 5 |
| Calculator | 108 ms | 0.000 | 51 KB | 6 |
| Role page | 140 ms | 0.000 | 88 KB | 6 |
| Pricing | 108 ms | 0.000 | 98 KB | 6 |

Google's thresholds are LCP under 2.5 s and CLS under 0.1. Those numbers are
from localhost so real-world LCP will be higher, but the things that actually
drive it — **six requests, under 100 KB, zero third-party domains, explicit
image dimensions** — are properties of the build, not of the test.

The single biggest reason this is fast is the decision not to load webfonts,
analytics or any CDN. Adding a tag manager later would undo most of it.

## ⚠️ Gate: do this before submitting anything to Google

`$25,000` appears 22 times across 8 pages. Those parameters — the cap, the
2025–2028 years, the net-of-tip-out definition, the 22% illustration — are
still transcribed from the design handoff and **have not been verified against
primary IRS guidance**.

An indexed page carrying a wrong tax figure is much harder to walk back than an
unshipped binary: it gets cached, scraped, and cited. **Verify the four values
in `TAX` (src/build.py) first.** Everything below assumes that is done.

## Step 1 — Verify the domain

Search Console → Add property → **Domain** (`tipfolio.app`), which needs one DNS
TXT record and covers every subdomain and protocol at once. Prefer this over the
URL-prefix method.

If you use the HTML-tag method instead, paste the token into `GSC_TOKEN` in
`src/build.py` and rebuild — it is then emitted on all 26 pages, which keeps
verification alive if you ever change host.

## Step 2 — Submit the sitemap

Search Console → Sitemaps → submit `sitemap.xml`. Same again at
[Bing Webmaster Tools](https://www.bing.com/webmasters) — it also feeds
DuckDuckGo, and takes about two minutes.

## Step 3 — Ask for indexing on the pages that matter

Use **URL Inspection → Request indexing** on these first. Do not bother doing all
26; Google will find the rest through the sitemap and internal links.

1. `/` — the brand and app entity
2. `/guides/no-tax-on-tips/` — highest-intent query on the site
3. `/calculators/real-hourly-rate/` — highest-volume tool
4. `/calculators/tip-out/`
5. `/guides/how-to-track-tips/`

## What to expect

A brand-new domain with no backlinks takes **weeks to months**, not days. A
realistic shape:

- **Week 1–2** — indexed, ranking nowhere, near-zero impressions.
- **Month 1–3** — impressions on long-tail phrases; the calculators usually move
  first because the intent is narrow and the competition is thinner.
- **Month 3–6** — the guides start placing, if they earn any links at all.

The two things that decide whether this works are outside the site: **links**
and **time**. Nothing in the markup substitutes for either.

## Once the app ships

Set `APP_STORE_URL` in `src/build.py` and rebuild. Until then every call to
action is a disabled "Coming soon" chip — deliberately, so there are no dead
links — which also means **the site cannot convert a single visitor yet**. Traffic
that arrives before the listing is live is wasted, so getting indexed early is
useful only because indexing is slow, not because early traffic is valuable.

## What to monitor, and what to ignore

Watch in Search Console: **Pages** (indexed vs excluded, and why), **Queries**
you appear for, and **Core Web Vitals**. Ignore average position as a headline
number — it averages across queries you do not care about.

If a page is excluded as *Crawled – currently not indexed*, that is usually
Google judging it not worth indexing yet, not a technical fault. The fix is
better content and links, not more markup.

## Rules that keep this from rotting

- **Do not add analytics, a tag manager, webfonts or a chat widget.** It would
  cost the performance profile above and contradict the privacy claim the app is
  built on.
- **One `<h1>` per page, no skipped levels.** The build enforces it.
- **Every new page needs a unique title and description in range.** The build
  enforces that too.
- **Link every new page from somewhere.** The build does not check for orphans,
  and an unlinked page will not rank.
