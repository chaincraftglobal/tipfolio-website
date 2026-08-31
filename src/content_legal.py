"""Legal, support and error pages."""
import pathlib
from build import Page, add, SITE, BRAND, TAX

C = pathlib.Path(__file__).resolve().parent / "content"


def frag(name):
    return (C / name).read_text(encoding="utf-8")


def build():
    add(Page(
        "/privacy/",
        "Privacy Policy — Tipfolio",
        "How Tipfolio handles your information: your shifts, tips and tax totals "
        "stay on your iPhone. No server, no analytics, no third-party SDKs.",
        frag("privacy.html"),
        og_title="Privacy Policy — Tipfolio",
        og_type="article",
        trail=[("Home", "/"), ("Privacy policy", None)],
        priority="0.4",
    ))

    add(Page(
        "/terms/",
        "Terms of Service — Tipfolio",
        "The terms you agree to when you use Tipfolio, including subscription "
        "and auto-renewal terms and the record-keeping disclaimer.",
        frag("terms.html"),
        og_title="Terms of Service — Tipfolio",
        og_type="article",
        trail=[("Home", "/"), ("Terms of service", None)],
        priority="0.4",
    ))

    add(Page(
        "/support/",
        "Support — Tipfolio for iPhone",
        "Help with Tipfolio: logging shifts, exporting your tax report, "
        "cancelling Pro, encrypted backups, receipt scanning and deleting data.",
        frag("support.html"),
        og_title="Support — Tipfolio",
        trail=[("Home", "/"), ("Support", None)],
        nav="/support/",
        priority="0.7",
        schema=['{"@context":"https://schema.org","@type":"FAQPage",'
                '"mainEntity":[{"@type":"Question","name":"Does Tipfolio work offline?",'
                '"acceptedAnswer":{"@type":"Answer","text":"Yes \\u2014 everything is stored on your '
                'phone. You can log shifts with zero signal; nothing needs a server."}},'
                '{"@type":"Question","name":"How do I cancel Tipfolio Pro?",'
                '"acceptedAnswer":{"@type":"Answer","text":"Settings \\u2192 Subscription \\u2192 Change '
                'or cancel plan, which links straight to Apple\\u2019s subscription settings. Pro stays '
                'active until the end of the period you have paid for, and your log is untouched."}},'
                '{"@type":"Question","name":"How do I delete everything?",'
                '"acceptedAnswer":{"@type":"Answer","text":"Settings \\u2192 Data & privacy \\u2192 Delete '
                'all data, three taps from settings. It offers a free export first, then erases the local '
                'store, scan images, reminders, the iCloud archive and the encryption key."}}]}'],
    ))
