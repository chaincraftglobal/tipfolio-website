#!/usr/bin/env python3
"""
Tipfolio site generator.

Renders every page of tipfolio.app from one layout so the header, footer,
SEO block and disclaimers cannot drift page to page.

    python3 src/build.py                  # writes ./docs/

Design rules this file enforces:
  * Zero third-party requests. No webfonts, no analytics, no CDNs. The site
    makes the same promise the app does, so it must be able to keep it.
  * Every tax figure comes from TAX below, which mirrors AppConfig.Tax in the
    app. Never hard-code a cap or a year into page copy.
  * Every page that states a tax figure carries the disclaimer. `build` refuses
    to write a page that breaks this rule.
"""

import html
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
# GitHub Pages serves this repo from /docs on the main branch, so the build
# output has to land there. Everything in docs/ is generated except assets/.
OUT = ROOT / "docs"
# The canonical origin. EVERY canonical tag, Open Graph URL, sitemap entry and
# JSON-LD @id is built from it.
#
# www, not the apex: gettipfolio.app 308-redirects to www.gettipfolio.app on
# Vercel, so canonicals pointing at the apex would each aim at a redirect rather
# than at the page that actually serves.
#
# It was "https://tipfolio.app" until Aug 2026. That domain belongs to a
# different company shipping a different product also called TipFolio, so every
# canonical was telling Google the authoritative copy of this content lived on a
# competitor's site. Do not point it back.
SITE = "https://www.gettipfolio.app"
CNAME_HOST = ""  # GitHub Pages only; leave empty while hosting on Vercel.

# --------------------------------------------------------------------------
# Tax parameters — mirror of Tipfolio/Resources/AppConfig.swift `enum Tax`.
# If the app's values change, change them here in the same commit.
# --------------------------------------------------------------------------
TAX = {
    "cap": 25_000,
    "cap_display": "$25,000",
    # The cap is per RETURN, regardless of filing status - two tipped workers
    # filing jointly share one $25,000, not two. Copy must never imply per person.
    "cap_is_per_return": True,
    "years": "2025–2028",
    "year_start": 2025,
    "year_end": 2028,
    "net_of_tipout": True,
    "savings_rate": 0.22,
    # IRC 224 phase-out: the deduction is reduced (but not below zero) by $100
    # for each $1,000 of MAGI above the threshold. On a full $25,000 deduction
    # that reaches zero at $400,000 single / $550,000 joint.
    "phaseout_single": 150_000,
    "phaseout_joint": 300_000,
    "phaseout_increment": 1_000,
    "phaseout_reduction": 100,
    "phaseout_single_display": "$150,000",
    "phaseout_joint_display": "$300,000",
    # The deduction reduces federal INCOME tax only. Payroll taxes are untouched.
    "reduces_payroll_tax": False,
    "occupation_count": 71,
    "citation": "IRS Publication 531 and the final regulations under IRC §224",
    "disclaimer": (
        "Tipfolio helps you keep records. It is not tax advice. Consult a "
        "qualified tax professional and verify current IRS rules before filing."
    ),
}

BRAND = {
    "name": "Tipfolio",
    "entity": "Lacewing Technologies LLC",
    "address": "30 N Gould St, Ste N, Sheridan, WY 82801, United States",
    "email": "support@gettipfolio.app",
    "price_monthly": "$3.99",
    "price_annual": "$29.99",
    "trial": "7-day free trial",
}

# --------------------------------------------------------------------------
# Components
# --------------------------------------------------------------------------

NAV = [
    ("Features", "/features/"),
    ("Guides", "/guides/"),
    ("Calculators", "/calculators/"),
    ("Pricing", "/pricing/"),
    ("Support", "/support/"),
]

FOOTER = [
    ("Product", [
        ("Features", "/features/"),
        ("Pricing", "/pricing/"),
        ("About", "/about/"),
        ("Support", "/support/"),
    ]),
    ("Free tools", [
        ("Tip-out calculator", "/calculators/tip-out/"),
        ("Real hourly rate", "/calculators/real-hourly-rate/"),
        ("Tip tax deduction", "/calculators/tip-tax-deduction/"),
        ("Shift earnings", "/calculators/shift-earnings/"),
    ]),
    ("Guides", [
        ("No Tax on Tips, explained", "/guides/no-tax-on-tips/"),
        ("How to track your tips", "/guides/how-to-track-tips/"),
        ("Reporting cash tips", "/guides/reporting-cash-tips/"),
        ("All guides", "/guides/"),
    ]),
    ("Who it's for", [
        ("Servers", "/for/servers/"),
        ("Bartenders", "/for/bartenders/"),
        ("Baristas", "/for/baristas/"),
        ("Delivery drivers", "/for/delivery-drivers/"),
        ("Hairstylists & barbers", "/for/hairstylists/"),
        ("All jobs", "/for/"),
    ]),
    ("Legal", [
        ("Privacy policy", "/privacy/"),
        ("Terms of service", "/terms/"),
        ("Contact", "mailto:support@gettipfolio.app"),
    ]),
]

LOGO = '<img src="/assets/img/favicon.svg" width="34" height="34" alt="">'


def cta(label="Coming soon to the App Store", cls="btn-primary"):
    """The App Store call to action.

    The listing is not live yet, so this deliberately renders as a non-link.
    When the app ships, set APP_STORE_URL and every page updates at once.
    """
    if APP_STORE_URL:
        return f'<a class="btn {cls}" href="{APP_STORE_URL}" rel="noopener">{label}</a>'
    return f'<span class="btn {cls}" aria-disabled="true">{label}</span>'


APP_STORE_URL = ""  # TODO: paste the App Store listing URL here once live.

# Google Search Console verification token. Paste the content value of the
# meta tag Search Console gives you (the "HTML tag" method) and rebuild; it is
# then emitted on every page, which also verifies the domain if you later move
# host. Leave empty to emit nothing.
GSC_TOKEN = ""


def header(active=""):
    parts = []
    for label, href in NAV:
        cls = ' class="is-active"' if active == href else ""
        parts.append('<a href="%s"%s>%s</a>' % (href, cls, html.escape(label)))
    links = "".join(parts)
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/">{LOGO}<span class="brand-name">Tipfolio</span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
    <nav class="nav" id="site-nav" aria-label="Primary">
      {links}
      {cta("Get the app", "btn-primary")}
    </nav>
  </div>
</header>"""


def footer():
    cols = ""
    for title, links in FOOTER:
        items = "".join(f'<li><a href="{h}">{html.escape(l)}</a></li>' for l, h in links)
        cols += (f'<div><p class="footer-heading" id="foot-{title.lower().replace(" ", "-").replace(chr(39), "")}">'
                 f'{title}</p><ul aria-labelledby="foot-{title.lower().replace(" ", "-").replace(chr(39), "")}">'
                 f'{items}</ul></div>')
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/">{LOGO}<span class="brand-name">Tipfolio</span></a>
        <p class="small">The tip log for people who actually work for tips.
           On your iPhone, with no server for your earnings.</p>
        <p class="small" style="margin-top:12px">{BRAND['entity']}<br>{BRAND['address']}</p>
      </div>
      {cols}
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 {BRAND['entity']}. All rights reserved.</span>
      <span>Tipfolio is not a tax advisor. Not affiliated with the IRS or Apple.</span>
    </div>
  </div>
</footer>"""


def breadcrumbs(trail):
    """trail: [(label, href), ...] ending with the current page (href None)."""
    if not trail:
        return "", ""
    items, ld = [], []
    for i, (label, href) in enumerate(trail, start=1):
        if href:
            items.append(f'<li><a href="{href}">{html.escape(label)}</a></li>')
        else:
            items.append(f'<li aria-current="page">{html.escape(label)}</li>')
        ld.append(
            '{"@type":"ListItem","position":%d,"name":"%s"%s}'
            % (i, html.escape(label), f',"item":"{SITE}{href}"' if href else "")
        )
    nav = f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'
    schema = ('{"@context":"https://schema.org","@type":"BreadcrumbList",'
              '"itemListElement":[%s]}' % ",".join(ld))
    return nav, schema


def disclaimer(extra=""):
    return (f'<div class="disclaimer">{TAX["disclaimer"]}'
            f'{" " + extra if extra else ""}</div>')


def related(links, title="Keep reading"):
    if not links:
        return ""
    items = "".join(
        f'<li><a href="{h}"><strong>{html.escape(t)}</strong>'
        f'<span>{html.escape(d)}</span></a></li>' for t, h, d in links
    )
    return (f'<section class="related"><div class="wrap narrow"><h2>{title}</h2>'
            f'<ul class="related-list">{items}</ul></div></section>')


def app_cta_band(
    heading="Stop reconstructing your year from memory.",
    body="Tipfolio turns ten seconds a night into the daily record your deduction "
         "is built on. Free to log, forever.",
):
    return f"""<section class="cta-band"><div class="wrap">
  <div class="band">
    <div class="band-grid">
      <div>
        <h2>{heading}</h2>
        <p style="margin-top:14px">{body}</p>
      </div>
      <div class="band-cta">{cta("Coming soon to the App Store", "btn-onDark")}
        <p class="small" style="color:rgba(255,255,255,.7);margin-top:14px">
          iPhone · No account required · Your earnings never leave the device</p>
      </div>
    </div>
  </div>
</div></section>"""


# --------------------------------------------------------------------------
# Page rendering
# --------------------------------------------------------------------------

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#F7F4EE">{robots}{verification}
<meta name="author" content="Lacewing Technologies LLC">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Tipfolio">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{site}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/favicon.svg">
<link rel="stylesheet" href="/assets/css/site.css">
{schema}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{header}
<main id="main">
{body}
</main>
{footer}
<script src="/assets/js/site.js" defer></script>{page_js}
</body>
</html>
"""

ORG_SCHEMA = (
    '{"@context":"https://schema.org","@graph":['
    '{"@type":"Organization","@id":"%(site)s/#org","name":"Tipfolio",'
    '"legalName":"Lacewing Technologies LLC","url":"%(site)s/",'
    '"logo":{"@type":"ImageObject","url":"%(site)s/assets/img/og-image.png",'
    '"width":1200,"height":630},'
    '"contactPoint":{"@type":"ContactPoint","contactType":"customer support",'
    '"email":"support@gettipfolio.app"},'
    '"address":{"@type":"PostalAddress","streetAddress":"30 N Gould St, Ste N",'
    '"addressLocality":"Sheridan","addressRegion":"WY","postalCode":"82801",'
    '"addressCountry":"US"}},'
    '{"@type":"WebSite","@id":"%(site)s/#website","url":"%(site)s/",'
    '"name":"Tipfolio","inLanguage":"en-US",'
    '"publisher":{"@id":"%(site)s/#org"}}]}'
) % {"site": SITE}

PAGES = []


class Page:
    def __init__(self, path, title, description, body, *, og_title=None,
                 og_type="website", schema=None, trail=None, noindex=False,
                 page_js="", priority="0.6", nav=""):
        self.path = path
        self.title = title
        self.description = description
        self.body = body
        self.og_title = og_title or title
        self.og_type = og_type
        self.schema = schema or []
        self.trail = trail or []
        self.noindex = noindex
        self.page_js = page_js
        self.priority = priority
        self.nav = nav


def add(page):
    PAGES.append(page)
    return page


def render(page):
    crumb_html, crumb_schema = breadcrumbs(page.trail)
    schemas = list(page.schema)
    if crumb_schema:
        schemas.append(crumb_schema)
    schema_html = "".join(
        f'<script type="application/ld+json">{s}</script>\n' for s in schemas
    )
    canonical = SITE + page.path
    return TEMPLATE.format(
        title=html.escape(page.title),
        description=html.escape(page.description, quote=True),
        canonical=canonical,
        site=SITE,
        robots='\n<meta name="robots" content="noindex">' if page.noindex else "",
        verification=(f'\n<meta name="google-site-verification" content="{GSC_TOKEN}">'
                      if GSC_TOKEN else ""),
        og_type=page.og_type,
        og_title=html.escape(page.og_title),
        schema=schema_html,
        header=header(page.nav),
        body=(crumb_html + "\n" if crumb_html else "") + page.body,
        footer=footer(),
        page_js=page.page_js,
    )


def write_all():
    if not OUT.exists():
        OUT.mkdir(parents=True)

    problems = []
    for page in PAGES:
        markup = render(page)

        # Guardrail: a page whose own body states a tax figure must carry the
        # disclaimer. Scoped to the body, since the shared footer links to
        # "Tip tax deduction" on every page and would otherwise always trip it.
        states_tax = (TAX["cap_display"] in page.body
                      or "deduction" in page.body.lower()
                      or "No Tax on Tips" in page.body)
        if states_tax and "not tax advice" not in page.body:
            problems.append(f"{page.path}: states a tax figure without the disclaimer")

        h1s = re.findall(r"<h1[^>]*>", markup)
        if len(h1s) != 1:
            problems.append(f"{page.path}: {len(h1s)} <h1> elements (want exactly 1)")
        levels = [int(m) for m in re.findall(r"<h([1-6])[^>]*>", markup)]
        prev = 0
        for lv in levels:
            if prev and lv > prev + 1:
                problems.append(f"{page.path}: heading level skips h{prev} -> h{lv}")
                break
            prev = lv

        if len(page.title) > 65:
            problems.append(f"{page.path}: title {len(page.title)} chars (>65)")
        if not (70 <= len(page.description) <= 165):
            problems.append(
                f"{page.path}: description {len(page.description)} chars (want 70-165)")

        target = OUT / page.path.strip("/") / "index.html" if page.path != "/" \
            else OUT / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(markup, encoding="utf-8")

    # Duplicate title / description check — both are ranking-relevant.
    for field in ("title", "description"):
        seen = {}
        for p in PAGES:
            seen.setdefault(getattr(p, field), []).append(p.path)
        for value, paths in seen.items():
            if len(paths) > 1:
                problems.append(f"duplicate {field}: {paths}")

    write_404()
    write_sitemap()
    return problems


def write_404():
    """GitHub Pages serves /404.html for anything it cannot find. It lives at the
    root rather than in a directory, so it is written outside the Page list."""
    body = """
<section class="doc">
  <div class="wrap narrow" style="text-align:center">
    <p class="eyebrow green">404</p>
    <h1>That page isn&#39;t in the log.</h1>
    <p class="lede" style="margin:18px auto 0">
      The link may be old, or we may have moved it. Everything Tipfolio has is a tap away.
    </p>
    <div class="hero-actions" style="justify-content:center">
      <a class="btn btn-primary" href="/">Back to Tipfolio</a>
      <a class="btn btn-ghost" href="/guides/">Read the guides</a>
      <a class="btn btn-ghost" href="/support/">Get support</a>
    </div>
  </div>
</section>"""
    page = Page("/404.html", "Page not found — Tipfolio",
                "That page could not be found. Head back to Tipfolio, the tip log for "
                "people who actually work for tips, or browse the guides.",
                body, noindex=True)
    (OUT / "404.html").write_text(render(page), encoding="utf-8")


def write_sitemap():
    urls = "".join(
        f"  <url><loc>{SITE}{p.path}</loc><lastmod>2026-08-31</lastmod>"
        f"<priority>{p.priority}</priority></url>\n"
        for p in sorted(PAGES, key=lambda x: x.path) if not p.noindex
    )
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    if CNAME_HOST:
        (OUT / "CNAME").write_text(CNAME_HOST + "\n", encoding="utf-8")
    elif (OUT / "CNAME").exists():
        (OUT / "CNAME").unlink()
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    # Run as a script this file is `__main__`, but the content modules do
    # `from build import ...` — which would load a *second* copy with its own
    # empty PAGES list. Import the module properly and drive that instance, so
    # everything registers into one list.
    sys.path.insert(0, str(SRC))
    import build as B
    import content_core, content_guides, content_occupations, content_calculators, content_legal
    for module in (content_core, content_guides, content_occupations,
                   content_calculators, content_legal):
        module.build()
    issues = B.write_all()
    print(f"wrote {len(B.PAGES)} pages to {B.OUT}")
    if issues:
        print("\nISSUES:")
        for i in issues:
            print("  -", i)
        sys.exit(1)
    print("no issues")
