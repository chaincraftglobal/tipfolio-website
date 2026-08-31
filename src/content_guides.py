"""Long-form guides. These are the pages that earn the traffic."""
from build import (Page, add, TAX, BRAND, cta, disclaimer, app_cta_band,
                   related, SITE)

UPDATED = "31 August 2026"


def article_schema(title, description, path):
    return ('{"@context":"https://schema.org","@type":"Article",'
            '"headline":"%s","description":"%s",'
            '"datePublished":"2026-08-31","dateModified":"2026-08-31",'
            '"mainEntityOfPage":{"@type":"WebPage","@id":"%s%s"},'
            '"author":{"@type":"Organization","name":"Lacewing Technologies LLC"},'
            '"publisher":{"@type":"Organization","name":"Tipfolio",'
            '"logo":{"@type":"ImageObject","url":"%s/assets/img/og-image.png"}}}'
            % (title.replace('"', '\\"'), description.replace('"', '\\"'),
               SITE, path, SITE))


def faq_schema(pairs):
    items = ",".join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
        % (q.replace('"', '\\"'), a.replace('"', '\\"')) for q, a in pairs)
    return '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}' % items


def faq_html(pairs, heading="Questions"):
    rows = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in pairs)
    return (f'<h2 style="margin-top:46px">{heading}</h2>'
            f'<div class="faq" style="margin-top:18px">{rows}</div>')


def takeaways(items):
    lis = "".join(
        '<li><span class="tick" style="background:var(--green-tint);color:var(--green)">'
        f'&#10003;</span><span>{i}</span></li>' for i in items)
    return f'<div class="keytakeaways"><h2>In short</h2><ul>{lis}</ul></div>'


def article(kicker, h1, lede, body, *, takeaway=None, faq=None):
    # Every guide touches tax somewhere. Append the disclaimer centrally rather
    # than relying on each body to remember it; build.py refuses to publish a
    # page that states a tax figure without one.
    if "not tax advice" not in body:
        body = body + "\n" + disclaimer()
    return f"""
<section class="article">
  <div class="wrap narrow">
    <div class="article-head">
      <p class="eyebrow green">{kicker}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
      <p class="small" style="margin-top:16px">Last updated {UPDATED} · Written by the Tipfolio team</p>
    </div>
  </div>
</section>
<section style="padding-top:30px">
  <div class="wrap narrow">
    {takeaway or ''}
    <div class="prose" style="margin-top:0">
      {body}
      {faq or ''}
    </div>
  </div>
</section>"""


def build():
    # ==================================================== INDEX
    cards = [
        ("Tax", "No Tax on Tips, explained", "/guides/no-tax-on-tips/",
         f"What the {TAX['cap_display']} deduction actually is, who it helps, who it "
         "quietly doesn't, and the record it depends on."),
        ("Habit", "How to track your tips", "/guides/how-to-track-tips/",
         "The difference between a pile of numbers and a record that holds up — and the "
         "system that survives a double shift."),
        ("Tax", "Reporting cash tips", "/guides/reporting-cash-tips/",
         "What you're required to report, to whom, and why the cash half is where most "
         "people's records fall apart."),
        ("Money", "Tip-outs explained", "/guides/tip-out-explained/",
         "Pools, shares and percent-of-sales — how the money leaves your hand, and what "
         "your house can and can't take."),
        ("Money", "Your real hourly rate", "/guides/real-hourly-rate/",
         "Why the number on the job ad is never the number, and how to work out what a "
         "shift genuinely pays."),
        ("Life admin", "Proof of income for tipped workers", "/guides/proof-of-income-for-tipped-workers/",
         "Apartments, loans and visas, when most of your income arrives as cash and no "
         "one will vouch for it."),
    ]
    grid = "".join(
        f'<a class="link-card" href="{href}"><span class="kicker">{k}</span>'
        f'<h3>{t}</h3><p>{d}</p><span class="more">Read →</span></a>'
        for k, t, href, d in cards)

    index = f"""
<section class="article">
  <div class="wrap">
    <div class="article-head">
      <p class="eyebrow green">Guides</p>
      <h1>Straight answers about tipped work.</h1>
      <p class="lede">The tax rules, the money mechanics and the paperwork — written for
        people who work for tips, without the hedging that makes most of this stuff
        useless.</p>
    </div>
  </div>
</section>
<section style="padding-top:34px">
  <div class="wrap">
    <div class="grid grid-2">{grid}</div>
    {disclaimer()}
  </div>
</section>
{app_cta_band()}
"""
    add(Page("/guides/", "Guides for Tipped Workers — Tax, Tip-Outs & Income",
             "Straight answers on the tip deduction, reporting cash tips, tip-out rules, "
             "your real hourly rate and proving your income when you work for tips.",
             index, trail=[("Home", "/"), ("Guides", None)],
             nav="/guides/", priority="0.9"))

    # ==================================================== 1. NO TAX ON TIPS
    p = "/guides/no-tax-on-tips/"
    faq = [
        ("Are tips actually tax free now?",
         "No. The measure is a deduction against tip income up to an annual cap, not an "
         "exemption. Your tips are still income, still reportable, and still subject to "
         "payroll taxes. What changed is that a portion of tip income may be deductible "
         "when you calculate federal income tax."),
        ("How much can I deduct?",
         f"Up to {TAX['cap_display']} of qualified tips per tax year, for tax years "
         f"{TAX['years']}, subject to the eligibility rules that apply to you. Tips above "
         "the cap do not add to the deduction, though they remain part of your income and "
         "belong in your records."),
        ("Do I still have to report my tips?",
         "Yes. A deduction is applied to income you have reported; it is not permission to "
         "stop reporting. Reporting obligations for cash tips to your employer and on your "
         "return are unchanged."),
        ("Does it help everyone who works for tips?",
         "No, and this is the part most coverage skips. A deduction reduces taxable income, "
         "so its value depends on owing federal income tax in the first place. A large "
         "share of tipped workers already owe little or none, and for them the practical "
         "benefit can be small or zero."),
        ("What records do I need?",
         "A daily record of tips received, kept as you earn them. The IRS has long expected "
         "tipped employees to keep a daily tip record; the value of a contemporaneous log "
         "is that it was made at the time rather than reconstructed later."),
        ("Do mandatory service charges count?",
         "Generally no. An automatic gratuity on a large party is typically treated as a "
         "service charge and as wages rather than as a voluntary tip, and so usually does "
         "not qualify. Log auto-grats separately from voluntary tips."),
    ]
    body = f"""
      <p>If you work for tips you have probably heard some version of "tips aren't taxed
      anymore". That is not what the rule says, and the gap between the headline and the
      actual mechanics is where people get caught out.</p>
      <p>Here is the honest version.</p>

      <h2>What it actually is</h2>
      <p>It is a <strong>deduction</strong>, not an exemption. Tip income is still income:
      you still report it, it still counts for payroll taxes, and it still appears on your
      return. What the measure does is let a portion of qualified tip income be deducted
      when your federal income tax is calculated — up to <strong>{TAX['cap_display']} in a
      tax year</strong>, for tax years <strong>{TAX['years']}</strong>.</p>
      <p>The distinction matters because a deduction only reduces the income you are taxed
      on. It is not a refund, not a credit, and not a cheque.</p>

      <div class="callout">
        <p><strong>The uncomfortable part.</strong> Because it is a deduction against
        federal income tax, its value depends on you owing federal income tax. A great many
        tipped workers — particularly part-time, seasonal, and lower-earning ones — already
        owe little or nothing after the standard deduction. For them, a further deduction
        has little left to reduce. If that is you, the measure may be worth far less than
        the headlines suggest, and possibly nothing at all.</p>
      </div>

      <h2>What counts as a qualified tip</h2>
      <p>Two distinctions do most of the work:</p>
      <table>
        <thead><tr><th></th><th>Typically qualifies</th><th>Typically does not</th></tr></thead>
        <tbody>
          <tr><td><strong>Voluntary vs mandatory</strong></td>
              <td>A tip the customer chose to leave — cash, on the card, or through an app.</td>
              <td>An automatic gratuity or service charge added to the bill. These are generally treated as wages.</td></tr>
          <tr><td><strong>Yours vs passed on</strong></td>
              <td>What you actually kept.</td>
              <td>Money you tipped out to bar, bussers, runners and hosts — that is generally their income, not yours.</td></tr>
        </tbody>
      </table>
      <p>Both distinctions have the same practical consequence: <strong>you need to have
      logged more than one number</strong>. If your record says "made $240 tonight", you
      cannot separate the auto-grat from the voluntary tips, and cannot show what you passed
      on. If it says "$240 in tips, of which $55 was auto-grat, and I tipped out $48", you
      can.</p>

      <h2>The part that decides whether you can claim it</h2>
      <p>Every version of this rule rests on substantiation. Tipped employees have always
      been expected to keep a <em>daily record</em> of tips received. What makes such a
      record credible is that it was <strong>contemporaneous</strong> — written as the money
      came in, not assembled afterwards from memory and bank statements.</p>
      <blockquote><p>A spreadsheet built in March from memory and a log written on the night
      are not the same document, even if the totals match. One is evidence. The other is an
      estimate wearing a suit.</p></blockquote>
      <p>This is the real barrier. The deduction is not hard to understand; the daily record
      is hard to keep. Which is why the whole design of a tip log should be about surviving
      1 AM after a double, not about features.</p>

      <h3>What a defensible record contains</h3>
      <ul>
        <li>The <strong>date</strong> the shift belongs to — not the timestamp you happened to type it at. A New Year's Eve shift logged at 1 AM belongs to the old year.</li>
        <li><strong>Cash and card tips</strong> separately.</li>
        <li><strong>Tip-outs paid</strong>, so gross and net are both derivable.</li>
        <li><strong>Hours worked</strong> and the job it was for.</li>
        <li>The <strong>time the entry was made</strong> — the thing that makes it contemporaneous.</li>
        <li>Any later <strong>amendment, visible as an amendment</strong> rather than silently overwritten.</li>
      </ul>
      <p>That last point is worth dwelling on. A record you can edit invisibly is weaker than
      one that shows its corrections, because an edit history is evidence of good faith
      whereas a suspiciously clean file is not.</p>

      <h2>Working out roughly what it is worth to you</h2>
      <p>Take what you actually kept in voluntary tips across a year, cap it at
      {TAX['cap_display']}, and multiply by your marginal federal rate. That gives you an
      order of magnitude, not an answer — it ignores your filing status, your other income
      and deductions, payroll taxes and your state entirely.</p>
      <p><a href="/calculators/tip-tax-deduction/">Run it through the estimator →</a></p>

      <h2>Before you rely on any of this</h2>
      <p>The cap, the eligible years, the definition of a qualified tip and the treatment of
      tip-outs are the four things everything above rests on. Rules change, and how they
      apply depends on your circumstances. Check the current position against
      <em>{TAX['citation']}</em> and current IRS guidance, and talk to a qualified tax
      professional about your own situation.</p>
      <p>What is not in dispute, and what you can act on today, is the record. Whatever the
      rules turn out to be in April, a year of dated daily entries puts you in a better
      position than a shoebox.</p>
"""
    add(Page(p, f"No Tax on Tips, Explained ({TAX['years']})",
             "What the federal tip deduction actually is: a $25,000 annual deduction, not "
             "an exemption — who it helps, who it doesn't, and the daily record it "
             "depends on.",
             article("Tax", "No Tax on Tips, explained",
                     "It is a deduction, not an exemption — and it rests entirely on a "
                     "record almost nobody keeps. Here is what the rule actually does.",
                     body,
                     takeaway=takeaways([
                         f"A <strong>deduction of up to {TAX['cap_display']} a year</strong> on qualified tips, for tax years {TAX['years']}. Not a blanket exemption.",
                         "Tips remain income. You still report them, and payroll taxes still apply.",
                         "<strong>Voluntary</strong> tips generally qualify; mandatory service charges generally do not.",
                         "If you owe little federal income tax, a deduction has little to reduce — it does not help everyone equally.",
                         "It depends on a <strong>contemporaneous daily record</strong>, which is the part that actually takes effort.",
                     ]),
                     faq=faq_html(faq))
             + related([
                 ("Tip tax deduction estimator", "/calculators/tip-tax-deduction/", "See roughly where your tips land against the cap."),
                 ("How to track your tips", "/guides/how-to-track-tips/", "Building the daily record this all rests on."),
                 ("Reporting cash tips", "/guides/reporting-cash-tips/", "What you must report, and to whom."),
             ])
             + app_cta_band("The rule is simple. The record is the work.",
                            "Ten seconds a night, all year, and the daily log writes "
                            "itself — timestamped, amendable in the open, exportable as "
                            "PDF or CSV."),
             og_type="article",
             trail=[("Home", "/"), ("Guides", "/guides/"), ("No Tax on Tips", None)],
             nav="/guides/", priority="0.9",
             schema=[article_schema("No Tax on Tips, explained",
                                    "What the federal tip deduction is and the record it depends on.", p),
                     faq_schema(faq)]))

    # ==================================================== 2. HOW TO TRACK TIPS
    p = "/guides/how-to-track-tips/"
    faq = [
        ("What is the best way to track tips?",
         "Whatever you will actually do every night. The method matters far less than the "
         "consistency: a scruffy log with an entry for every shift beats an elegant "
         "spreadsheet with three months missing. Record the date, cash and card tips "
         "separately, tip-out paid, and hours worked — on the night."),
        ("Should I track tips in a notebook, a spreadsheet or an app?",
         "A notebook is the most reliable and the least useful later — you cannot total it, "
         "search it or export it. A spreadsheet is powerful and gets abandoned, because "
         "nobody opens a spreadsheet at 1 AM. An app wins only if it is fast enough that "
         "logging is not a decision. Whichever you pick, back it up."),
        ("How long should I keep my tip records?",
         "Keep them for at least as long as the relevant return can be examined, which is "
         "usually several years. Because a tip log is small, the practical answer is to keep "
         "it indefinitely — an old CSV costs nothing to store and is impossible to "
         "reconstruct once thrown away."),
        ("Do I need to track tips if my employer already reports them?",
         "Yes. Your employer reports what was declared through their system, which typically "
         "captures card tips well and cash tips poorly. Your own record is what lets you "
         "check their figure, and it is your position if the two ever disagree."),
        ("What if I forgot to log a few shifts?",
         "Enter them, and let them be visibly late rather than backdating them to look "
         "contemporaneous. A record showing that most entries were same-day and a handful "
         "were caught up a week later is more credible than one where every entry claims to "
         "be perfect."),
    ]
    body = """
      <p>Almost everyone who works for tips starts tracking them at some point. Almost
      everyone stops by about week three. Understanding why is most of the battle.</p>

      <h2>Why tracking fails</h2>
      <p>It is never a motivation problem. It is a friction problem, and it always shows up
      at the same moment: the end of a long shift, when you are tired, your feet hurt, and
      the thing standing between you and the car is a form.</p>
      <p>Any system that asks you to make more than one or two decisions at that moment will
      lose. Which means the design goal is not "capture rich data" — it is
      <strong>capture anything, reliably, in seconds</strong>.</p>
      <blockquote><p>A perfect record of three weeks is worth less than a rough record of
      three years.</p></blockquote>

      <h2>What to record, minimum</h2>
      <p>Five fields do almost all the work. Anything beyond them is optional and should
      never be allowed to slow the entry down.</p>
      <table>
        <thead><tr><th>Field</th><th>Why it matters</th></tr></thead>
        <tbody>
          <tr><td><strong>Business date</strong></td><td>The date the shift belongs to, not when you typed it. A shift that ends at 2 AM belongs to the previous day, and getting this wrong quietly misfiles income across a year boundary.</td></tr>
          <tr><td><strong>Cash tips</strong></td><td>The half no payroll system sees properly. This is the number that is genuinely only yours to record.</td></tr>
          <tr><td><strong>Card tips</strong></td><td>What should reconcile against your employer's figure. Keeping it separate is what makes that check possible.</td></tr>
          <tr><td><strong>Tip-out paid</strong></td><td>Without it you can record gross or net, but not both — and you need both.</td></tr>
          <tr><td><strong>Hours worked</strong></td><td>Actual hours. Without them no rate you calculate means anything.</td></tr>
        </tbody>
      </table>
      <p>Two more are worth having if they cost you nothing: <strong>total sales</strong> (if
      your tip-out runs off sales) and <strong>which job</strong> it was, if you work more
      than one.</p>

      <h2>The thing that makes a record hold up</h2>
      <p>This is the part most guides miss entirely. It is not the totals that make a log
      credible — it is <strong>when the entries were made</strong>.</p>
      <p>A record written on the night is contemporaneous. One assembled in March from
      memory, bank statements and guesswork is a reconstruction. They can contain identical
      numbers and carry very different weight, because the first is evidence of what
      happened and the second is an assertion about it.</p>
      <p>So: log on the night, keep the entry timestamp, and when you correct something,
      correct it <em>visibly</em>. An amendment trail is a strength, not an embarrassment. A
      file with no history is not more convincing — it just has less to show.</p>

      <div class="callout">
        <p><strong>Late is fine. Backdated is not.</strong> If you miss three shifts, enter
        them late and let them read as late. What you should never do is edit the dates to
        make a reconstruction look contemporaneous — that turns a small gap in your records
        into a question about your honesty.</p>
      </div>

      <h2>A system that survives a double</h2>
      <ol>
        <li><strong>Set the defaults once.</strong> Your job, wage and tip-out rule do not
          change nightly. If you are re-entering them every shift, the system is wrong.</li>
        <li><strong>Attach it to something you already do.</strong> The moment you sit down
          in the car, or the moment you count your bank. A trigger you already have beats
          willpower.</li>
        <li><strong>Use a reminder, late.</strong> Around 11:30 PM catches most closing
          shifts. A morning reminder catches you after the details have gone.</li>
        <li><strong>Never let a missing detail block the save.</strong> Tips and hours are
          enough. Sales, notes and the rest can be blank.</li>
        <li><strong>Back it up somewhere you don't control.</strong> A lost phone should not
          cost you a year of records.</li>
        <li><strong>Export once a quarter.</strong> A CSV in your email is the cheapest
          insurance available.</li>
      </ol>

      <h2>What the record buys you</h2>
      <ul>
        <li><strong>The tip deduction.</strong> It rests on a daily record.
          <a href="/guides/no-tax-on-tips/">The explainer →</a></li>
        <li><strong>A check on your W-2.</strong> Employers get tip reporting wrong,
          particularly on cash. You cannot dispute a figure you have nothing to compare
          against.</li>
        <li><strong>Proof of income.</strong> Landlords and lenders want history, not a
          number. <a href="/guides/proof-of-income-for-tipped-workers/">More →</a></li>
        <li><strong>Better decisions.</strong> Once you know your
          <a href="/guides/real-hourly-rate/">real hourly rate</a> by night and by section,
          picking up shifts stops being a guess.</li>
      </ul>
      <p>None of these are available to you retroactively. That is the whole argument for
      starting tonight rather than in January.</p>
"""
    add(Page(p, "How to Track Your Tips (And Actually Keep Doing It)",
             "What to record every shift, why the entry timestamp matters more than the "
             "totals, and how to build a tip log that survives a double shift.",
             article("Habit", "How to track your tips",
                     "Most tip tracking dies in week three. Here is what to record, why "
                     "contemporaneous beats complete, and a system that survives 1 AM.",
                     body,
                     takeaway=takeaways([
                         "Record five things: business date, cash tips, card tips, tip-out paid, hours worked.",
                         "<strong>When you logged it</strong> matters as much as what you logged — contemporaneous beats complete.",
                         "Log late entries as late. Never backdate a reconstruction to look contemporaneous.",
                         "Set job, wage and tip-out rule once; re-entering them nightly is what kills the habit.",
                         "Export and back up quarterly. A lost phone should not cost you a year.",
                     ]),
                     faq=faq_html(faq))
             + related([
                 ("No Tax on Tips, explained", "/guides/no-tax-on-tips/", "The deduction your daily record unlocks."),
                 ("Reporting cash tips", "/guides/reporting-cash-tips/", "The obligations behind the habit."),
                 ("Real hourly rate calculator", "/calculators/real-hourly-rate/", "What one shift actually paid you."),
             ])
             + app_cta_band("Ten seconds. Then the car.",
                            "Tipfolio opens onto a keypad with everything pre-filled, "
                            "nudges you at 11:30 PM, and timestamps every entry as you "
                            "make it."),
             og_type="article",
             trail=[("Home", "/"), ("Guides", "/guides/"), ("How to track your tips", None)],
             nav="/guides/", priority="0.85",
             schema=[article_schema("How to track your tips",
                                    "What to record every shift and how to keep the habit.", p),
                     faq_schema(faq)]))

    # ==================================================== 3. REPORTING CASH TIPS
    p = "/guides/reporting-cash-tips/"
    faq = [
        ("Do I have to report cash tips?",
         "Yes. Cash tips are income and are reportable, in the same way card tips are. The "
         "practical difference is that no system captures them for you, so the obligation "
         "and the record both fall to you."),
        ("What is the $20 rule?",
         "Employees who receive $20 or more in tips in a calendar month at one job are "
         "generally required to report those tips to their employer, in writing, by around "
         "the 10th of the following month. Tips below that monthly threshold at a given job "
         "are still income for your return, even where the reporting-to-employer requirement "
         "does not bite."),
        ("What happens if I under-report my tips?",
         "Under-reporting income can lead to back tax, interest and penalties, and it also "
         "reduces the earnings record that feeds Social Security benefits and anything that "
         "depends on documented income — mortgages, loans, some visas. The cost is rarely "
         "only the tax."),
        ("Does tipping out reduce what I report?",
         "Generally, tips you pass to other employees under a genuine sharing or pooling "
         "arrangement are their income rather than yours, and they report them. That only "
         "works if you can show what you passed on, which means recording gross tips and "
         "tip-out separately."),
        ("How does the IRS know about cash tips?",
         "Through employer reporting, through the relationship between charged tips and "
         "total sales, and through programmes that estimate expected tip rates for an "
         "establishment. The practical point is that a well-kept daily record is your "
         "position if a figure is ever questioned — and there is no substitute available "
         "afterwards."),
    ]
    body = """
      <p>Card tips mostly look after themselves: they run through the point-of-sale, land on
      your payroll, and appear on your W-2 whether you think about them or not. Cash is
      different, and it is where most tipped workers' records quietly fall apart.</p>

      <h2>The obligation, in plain terms</h2>
      <p>Cash tips are income. There is no threshold below which a tip stops being income,
      and no version of the rules in which cash is treated as a gift.</p>
      <p>Separately from that, there is a reporting step to your employer. The general shape
      of it: if you receive <strong>$20 or more in tips in a calendar month</strong> at one
      job, you are required to report those tips to that employer in writing, usually by
      around the 10th of the following month. Your employer then withholds on them and
      includes them in your wage reporting.</p>
      <p>Two things people get wrong about that threshold:</p>
      <ul>
        <li>It is <strong>per employer, per month</strong> — not per shift, and not across
          all your jobs combined.</li>
        <li>Falling under it removes the reporting-to-employer step, <strong>not</strong> the
          fact that the money is income on your return.</li>
      </ul>

      <div class="callout">
        <p><strong>Why this matters beyond tax.</strong> Reported tip income is what builds
        your Social Security and Medicare earnings record, and it is what any lender,
        landlord or immigration process will look for. Under-reporting saves a little tax now
        and costs you the ability to prove you earn what you earn — which tends to become
        expensive at exactly the wrong moment.</p>
      </div>

      <h2>What a daily tip record should contain</h2>
      <p>Tipped employees are expected to keep a daily record of tips received. In practice
      that means, for each shift:</p>
      <ul>
        <li>the <strong>date</strong> of the shift;</li>
        <li><strong>cash tips</strong> received directly from customers;</li>
        <li><strong>card and charged tips</strong>;</li>
        <li><strong>tips paid out</strong> to other employees, and to whom;</li>
        <li>the <strong>name of the employer</strong>, if you work more than one job.</li>
      </ul>
      <p>Keep the record as you go. A log written on the night is worth more than the same
      numbers assembled later, for the same reason a photograph is worth more than a
      description. <a href="/guides/how-to-track-tips/">How to make that a habit →</a></p>

      <h2>Service charges are not tips</h2>
      <p>An automatic gratuity on a party of eight, a mandatory event fee, a delivery charge
      set by the house — these are generally <strong>service charges</strong>, not tips. They
      are typically treated as wages, come to you through payroll, and are handled
      differently for tax purposes.</p>
      <p>They are also frequently muddled together with voluntary tips in people's own
      records, which causes two problems at once: the totals stop reconciling with payroll,
      and the portion that might qualify for the
      <a href="/guides/no-tax-on-tips/">tip deduction</a> becomes impossible to isolate. Log
      them separately.</p>

      <h2>Checking your W-2</h2>
      <p>When your W-2 arrives, compare the tip figure on it against your own log for the
      same year. Three outcomes:</p>
      <table>
        <thead><tr><th>What you see</th><th>What it usually means</th></tr></thead>
        <tbody>
          <tr><td>They broadly agree</td><td>Good. File, and keep the log.</td></tr>
          <tr><td>The W-2 is <strong>lower</strong> than your log</td><td>Something you reported may not have made it through payroll. Ask before you file — the difference is income you still need to report.</td></tr>
          <tr><td>The W-2 is <strong>higher</strong> than your log</td><td>Often service charges being included, or an allocation. Worth understanding rather than accepting silently.</td></tr>
        </tbody>
      </table>
      <p>You can only run this check if you kept your own figures. Without a log there is
      nothing to compare against, and the employer's number simply becomes the truth by
      default.</p>

      <h2>If your records are already patchy</h2>
      <p>Start now rather than trying to fix the past. Reconstruct what you genuinely can
      from bank deposits, schedules and payroll records, mark it clearly as reconstructed,
      and keep it separate from entries made on the night. Then keep a proper daily record
      going forward.</p>
      <p>A record that honestly says "these three months were rebuilt from statements, the
      rest were logged nightly" is far stronger than a uniform file that implies a diligence
      that did not exist.</p>
      <p>If your position is complicated — several years of gaps, a large discrepancy with an
      employer, or a notice you have already received — talk to a tax professional rather
      than working it out from an article.</p>
"""
    add(Page(p, "Do You Have to Report Cash Tips? A Plain Guide",
             "Cash tips are income. Here is the monthly reporting rule, what a daily tip "
             "record should contain, why service charges are different, and how to check "
             "your W-2.",
             article("Tax", "Reporting cash tips",
                     "The card half looks after itself. Cash is where the obligation, the "
                     "record and most people's problems actually live.",
                     body,
                     takeaway=takeaways([
                         "Cash tips are income. There is no threshold below which that stops being true.",
                         "Receive <strong>$20+ in tips in a month at one job</strong> and you generally must report them to that employer in writing.",
                         "That threshold is per employer per month — and being under it does not remove the income from your return.",
                         "<strong>Service charges are not tips.</strong> Log auto-grats separately from voluntary tips.",
                         "Under-reporting shrinks your Social Security record and your ability to prove income to lenders.",
                     ]),
                     faq=faq_html(faq))
             + related([
                 ("How to track your tips", "/guides/how-to-track-tips/", "The daily record this obligation assumes."),
                 ("No Tax on Tips, explained", "/guides/no-tax-on-tips/", "What reporting properly can be worth."),
                 ("Tip-outs explained", "/guides/tip-out-explained/", "Why what you passed on has to be recorded too."),
             ])
             + app_cta_band("Cash is the half nobody records for you.",
                            "Tipfolio keeps cash and card separate on every shift, tracks "
                            "tip-outs alongside them, and reconciles the year against your "
                            "W-2 before you file."),
             og_type="article",
             trail=[("Home", "/"), ("Guides", "/guides/"), ("Reporting cash tips", None)],
             nav="/guides/", priority="0.85",
             schema=[article_schema("Reporting cash tips",
                                    "The obligations around cash tips and the daily record they assume.", p),
                     faq_schema(faq)]))

    # ==================================================== 4. TIP-OUTS EXPLAINED
    p = "/guides/tip-out-explained/"
    faq = [
        ("What is a tip-out?",
         "A tip-out is money you pass to other workers who supported your shift — bar, "
         "bussers, food runners, hosts. It is usually set by house policy as a percentage of "
         "your tips, a percentage of your sales, or a flat amount per shift."),
        ("What is a normal tip-out percentage?",
         "On a percent-of-tips basis, totals across all recipients commonly land somewhere "
         "between 15% and 30% of your tips. On a percent-of-sales basis the number looks "
         "much smaller — often 1% to 5% — because it is taken against total sales rather "
         "than against tips. Your house's written policy is what actually governs you."),
        ("Can my manager take a share of the tip pool?",
         "Rules on this are strict and heavily litigated. Federal law generally prohibits "
         "employers, managers and supervisors from keeping employees' tips, including by "
         "participating in a tip pool, though the details of who counts as a supervisor and "
         "which arrangements are permitted are genuinely complicated. If you think your "
         "employer is taking a cut, that is worth advice from a labour attorney or your "
         "state labour department, not from an app."),
        ("Do I pay tax on tips I tip out?",
         "Generally, tips passed to other employees under a genuine sharing arrangement are "
         "their income rather than yours. But you can only demonstrate that if you recorded "
         "gross tips and tip-out as separate figures — which is the practical reason to log "
         "both."),
        ("Is percent-of-sales tip-out legal?",
         "Sales-based tip-out arrangements are common and are widely used, but they interact "
         "with wage-and-hour rules in ways that vary by state and by the specifics of the "
         "arrangement. The economics are the part you can act on yourself: a sales-based "
         "tip-out shifts the risk of a badly tipping table onto you."),
    ]
    body = """
      <p>Tip-out is the least examined number in tipped work. Most people know their
      percentage, few know what it costs them across a year, and almost nobody can produce
      the figures if asked. That is a shame, because it is usually the second-largest number
      on the shift after the tips themselves.</p>

      <h2>The three shapes</h2>
      <p>Almost every arrangement is one of three, and which one you are on matters more than
      the headline percentage.</p>
      <table>
        <thead><tr><th>Basis</th><th>How it works</th><th>Who carries a bad night</th></tr></thead>
        <tbody>
          <tr><td><strong>Percent of tips</strong></td><td>A share of what you actually made. The most common arrangement.</td><td>Shared. If you make less, you owe less.</td></tr>
          <tr><td><strong>Percent of sales</strong></td><td>A share of your total sales, regardless of what you were tipped.</td><td><strong>You.</strong> A stiffed $400 table still generates tip-out.</td></tr>
          <tr><td><strong>Flat amount</strong></td><td>The same figure every shift.</td><td><strong>You</strong> on slow nights; support staff on busy ones.</td></tr>
        </tbody>
      </table>

      <h3>Why percent-of-sales is the one to watch</h3>
      <p>Work a $1,600 sales night on a 4% sales-based tip-out and you owe $64 — whether you
      were tipped $340 or $150. On a 20%-of-tips basis those same nights would have cost you
      $68 and $30.</p>
      <p>Over one shift, unremarkable. Over a year of shifts, including the slow Tuesdays and
      the big-party-that-didn't-tip nights, the difference is real money. And you can only
      ever see it if you logged sales, tips and tip-out separately.
      <a href="/calculators/tip-out/">Run both bases through the calculator →</a></p>

      <h2>Pools and shares are not the same thing</h2>
      <ul>
        <li><strong>Tip-out</strong> — you keep your tips and pass a defined share to
          specified roles.</li>
        <li><strong>Tip pool</strong> — tips go into a common pot and are redistributed by an
          agreed formula, often weighted by role and hours.</li>
        <li><strong>Tip share</strong> — used loosely for either; ask which one your house
          actually means.</li>
      </ul>
      <p>The distinction matters for your records. In a pool, what you "made" and what you
      "took home" can diverge substantially, and if your log only captures the amount that
      reached your pocket you have lost the ability to show what passed through your hands.</p>

      <div class="callout">
        <p><strong>Who can be in the pool is the part with real legal weight.</strong>
        Federal rules restrict employers, managers and supervisors from keeping employees'
        tips, including through participation in a pool, and states layer their own rules on
        top. If you suspect the pool includes people it should not, that is a question for
        your state labour department or an employment attorney — and a contemporaneous record
        of what you paid in is exactly the evidence such a question needs.</p>
      </div>

      <h2>Record gross and tip-out, never just the net</h2>
      <p>The single most common record-keeping mistake in tipped work is writing down only
      what you walked out with. That number is fine for budgeting and useless for everything
      else:</p>
      <ul>
        <li>You cannot reconcile it against your <a href="/guides/reporting-cash-tips/">W-2</a>,
          which reflects gross tips rather than net.</li>
        <li>You cannot show which portion was passed to other workers — the thing that
          determines whose income it is.</li>
        <li>You cannot show a lender your actual gross earnings.</li>
        <li>You cannot tell whether your arrangement is quietly expensive.</li>
      </ul>
      <p>Two numbers, every night. It costs about three extra seconds and it is the
      difference between a record and a receipt.</p>

      <h2>Sanity checks worth running</h2>
      <ol>
        <li><strong>Does the rule ever exceed your tips?</strong> On a genuinely bad night a
          sales-based or flat tip-out can approach or exceed what you made. If that happens
          regularly, the arrangement deserves a conversation.</li>
        <li><strong>Is the policy written down?</strong> A percentage that lives only in a
          manager's head has a way of drifting upward.</li>
        <li><strong>Do the recipients match the policy?</strong> Roles quietly get added to
          tip-outs.</li>
        <li><strong>What does it total over a year?</strong> Most people have never added it
          up. It is usually a larger number than they expect.</li>
      </ol>
"""
    add(Page(p, "Tip-Outs Explained: Pools, Shares and Percentages",
             "How tip-outs work, the difference between percent of tips and percent of "
             "sales, what a tip pool can legally include, and why gross and tip-out "
             "are two numbers.",
             article("Money", "Tip-outs explained",
                     "The second-biggest number on your shift, and the one almost nobody "
                     "records properly. Here is how the money leaves your hand.",
                     body,
                     takeaway=takeaways([
                         "Three shapes: <strong>percent of tips</strong>, <strong>percent of sales</strong>, <strong>flat</strong>. Which one you are on matters more than the percentage.",
                         "Percent-of-sales shifts the risk of a badly tipping table onto <strong>you</strong>.",
                         "Record <strong>gross tips and tip-out separately</strong> — the net alone is a receipt, not a record.",
                         "Tips you pass on under a genuine arrangement are generally the recipient's income, but only if you can show it.",
                         "Federal rules restrict employers, managers and supervisors from keeping employees' tips. Suspected breaches need a lawyer, not an app.",
                     ]),
                     faq=faq_html(faq))
             + related([
                 ("Tip-out calculator", "/calculators/tip-out/", "Compare what each basis would cost you tonight."),
                 ("Your real hourly rate", "/guides/real-hourly-rate/", "What the shift pays once tip-out is out."),
                 ("How to track your tips", "/guides/how-to-track-tips/", "Capturing both numbers in ten seconds."),
             ])
             + app_cta_band("Set the rule once. Never do the maths again.",
                            "Tipfolio applies your job's tip-out rule to every shift, keeps "
                            "it editable before you save, and stores it alongside your "
                            "gross so both numbers survive."),
             og_type="article",
             trail=[("Home", "/"), ("Guides", "/guides/"), ("Tip-outs explained", None)],
             nav="/guides/", priority="0.85",
             schema=[article_schema("Tip-outs explained",
                                    "How tip-outs, pools and shares work, and what to record.", p),
                     faq_schema(faq)]))

    # ==================================================== 5. REAL HOURLY RATE
    p = "/guides/real-hourly-rate/"
    faq = [
        ("How do I calculate my real hourly rate as a server?",
         "Take your tips, subtract tip-out, add your base wage multiplied by hours worked, "
         "then divide by those hours: (tips - tip-out + wage x hours) / hours. The two "
         "mistakes that inflate the answer are forgetting tip-out and using scheduled hours "
         "instead of actual ones."),
        ("Do servers really make $30 an hour?",
         "Some do, on some shifts. The figure people quote is usually gross tips divided by "
         "scheduled hours on a strong night, which stacks three separate exaggerations. A "
         "blended rate across a few months of shifts is the number that would actually "
         "survive scrutiny, and it is normally meaningfully lower."),
        ("Should I include side work hours?",
         "Yes. Rolling silverware, stocking and cleaning are hours your earnings have to "
         "stretch across, whether or not they generate tips. Excluding them makes the rate "
         "look better and makes it useless for comparing jobs."),
        ("What is a good hourly rate for a tipped job?",
         "The only useful benchmark is your own alternatives: another section, another "
         "shift, another restaurant, or a non-tipped job. A rate is a comparison tool, not a "
         "score — which is why it is worth calculating consistently rather than accurately "
         "once."),
    ]
    body = """
      <p>Ask anyone in a tipped job what they make and you will get a number that sounds
      good. Ask how they got it and you will usually find gross tips, divided by scheduled
      hours, on a night they remember fondly.</p>
      <p>Every one of those three choices pushes the number up.</p>

      <h2>The formula</h2>
      <blockquote><p><strong>real hourly rate = (tips − tip-out + wage × hours) ÷ hours</strong></p></blockquote>
      <p>Four inputs, and three places people go wrong.</p>

      <h3>1. Tip-out comes off first</h3>
      <p>Money you hand to the bar is not money you earned. If your house takes 20% of tips,
      a $300 night is a $240 night. Using gross overstates your rate by exactly the tip-out
      percentage, every single time.</p>

      <h3>2. Hours are actual, not scheduled</h3>
      <p>The forty minutes after close, the pre-shift meeting, the side work — those are
      hours of your life the money has to cover. A shift scheduled 5–10 that ran 4:45–11:15
      is 6.5 hours, not five, and the difference moves the rate by nearly a third.</p>

      <h3>3. Zero hours means no rate at all</h3>
      <p>If you did not record hours, you do not have a rate. Not a big one, not zero —
      none. A figure with no time behind it is arithmetic without meaning, and any tool that
      shows you one is flattering you.</p>

      <h2>Blending, not averaging</h2>
      <p>Here is the subtle one. When you compare a week or a month, do not average your
      per-shift rates.</p>
      <p>A three-hour lunch and a nine-hour Saturday are not equal observations, but an
      average of rates treats them as if they were — and short shifts tend to post higher
      rates, because the dead first hour is a smaller fraction of them. Averaging therefore
      systematically overstates your earnings.</p>
      <p>Blend instead: total all take-home, total all hours, divide once.</p>
      <table>
        <thead><tr><th></th><th>Shift A</th><th>Shift B</th><th>Result</th></tr></thead>
        <tbody>
          <tr><td>Take-home</td><td>$90</td><td>$340</td><td>$430</td></tr>
          <tr><td>Hours</td><td>3</td><td>9</td><td>12</td></tr>
          <tr><td>Rate</td><td>$30.00/hr</td><td>$37.78/hr</td><td><strong>Blended: $35.83/hr</strong></td></tr>
          <tr><td colspan="3">Average of the two rates</td><td>$33.89/hr — wrong</td></tr>
        </tbody>
      </table>
      <p>Here the average understates; with the shift lengths reversed it would overstate.
      Either way it answers a question nobody asked. <a href="/calculators/shift-earnings/">Blend a week properly →</a></p>

      <div class="callout">
        <p><strong>What the number is actually for.</strong> Not self-esteem. It is a
        decision tool: which night to pick up, which section to ask for, whether the
        higher-volume restaurant across town is genuinely better once its tip-out is in, and
        whether a non-tipped offer is really a pay cut.</p>
      </div>

      <h2>One shift tells you almost nothing</h2>
      <p>Rates swing wildly with weather, section, party size, staffing and luck. A single
      shift is a data point; a month is a signal; a year with the seasons in it is knowledge.</p>
      <p>This is why calculating your rate once is far less valuable than logging shifts
      continuously. The patterns worth money — Thursdays running 30% above your average, the
      patio outperforming the bar in summer, one job quietly beating another — only appear
      across dozens of shifts.</p>
      <p><a href="/guides/how-to-track-tips/">Building that log →</a></p>

      <h2>What the rate deliberately excludes</h2>
      <p>The formula gives gross take-home per hour. It does not account for taxes and
      withholding, unpaid commute time, the cost of uniforms and shoes, or the schedule
      volatility that makes a second job hard to hold. Those are real, and they are why two
      jobs at the same rate are not always the same job — but they belong in a separate
      column, not smuggled into the rate.</p>
"""
    add(Page(p, "Your Real Hourly Rate: What a Shift Actually Pays",
             "How to calculate your true hourly rate as a server or bartender — tips minus "
             "tip-out plus wage over actual hours — and why averaging shift rates "
             "misleads you.",
             article("Money", "Your real hourly rate",
                     "The number on the job ad is gross tips over scheduled hours on a good "
                     "night. Here is the honest version, and how to compare shifts fairly.",
                     body,
                     takeaway=takeaways([
                         "<strong>(tips − tip-out + wage × hours) ÷ hours.</strong> All four inputs, or the number is decoration.",
                         "Use <strong>actual</strong> hours, including side work. Scheduled hours flatter the rate.",
                         "No hours means <strong>no rate</strong> — not a big one, and not zero.",
                         "<strong>Blend, don't average.</strong> Total take-home over total hours, divided once.",
                         "One shift is noise. The patterns worth money only show up across months.",
                     ]),
                     faq=faq_html(faq))
             + related([
                 ("Real hourly rate calculator", "/calculators/real-hourly-rate/", "Run one shift through it now."),
                 ("Tip-outs explained", "/guides/tip-out-explained/", "The deduction that comes off before anything else."),
                 ("Shift earnings calculator", "/calculators/shift-earnings/", "Blend a whole week the right way."),
             ])
             + app_cta_band("The rate is easy. The pattern is the point.",
                            "Tipfolio computes it on every shift and shows you the blended "
                            "rate by job and by night of the week — from your own log, on "
                            "your own phone."),
             og_type="article",
             trail=[("Home", "/"), ("Guides", "/guides/"), ("Real hourly rate", None)],
             nav="/guides/", priority="0.85",
             schema=[article_schema("Your real hourly rate",
                                    "Calculating what a tipped shift actually pays.", p),
                     faq_schema(faq)]))

    # ==================================================== 6. PROOF OF INCOME
    p = "/guides/proof-of-income-for-tipped-workers/"
    faq = [
        ("How do I prove my income if I work for tips?",
         "Combine documents that corroborate each other: your tax return and W-2 for the "
         "official figure, recent pay stubs, bank statements showing deposits, and your own "
         "dated shift log to explain the cash portion. No single one of these is usually "
         "enough on its own; together they tell a consistent story."),
        ("Will a landlord accept my own tip records?",
         "Rarely on their own, and they should not be presented as if they were verified. "
         "What your log does is corroborate the official documents and explain a cash "
         "pattern a landlord cannot otherwise see. Offer it as supporting evidence, "
         "alongside a return and statements."),
        ("What if my tax return understates what I really earn?",
         "Then that is the number most processes will use, and there is no way to argue "
         "around it — which is the practical cost of under-reporting. The only fix is "
         "forward-looking: report accurately from now on, and give yourself a documented "
         "history to draw on next year."),
        ("How much income history do lenders want?",
         "Expect to be asked for two years for a mortgage, and less for a rental — often "
         "recent pay stubs plus a return. Variable income is usually averaged over the "
         "period, so a documented low year can weigh on you long after it ends."),
    ]
    body = """
      <p>Applying for an apartment, a car loan, a mortgage or a visa runs into the same wall
      for anyone who works for tips: the systems are built around a steady salary and a
      letter from an employer, and you have neither.</p>
      <p>What you can do is assemble something better than a single document — a set of
      records that corroborate each other.</p>

      <h2>What actually gets accepted</h2>
      <table>
        <thead><tr><th>Document</th><th>Weight</th><th>What it does and doesn't show</th></tr></thead>
        <tbody>
          <tr><td><strong>Tax return</strong></td><td>Highest</td><td>The official figure. Shows reported income only — which is exactly why under-reporting becomes expensive here.</td></tr>
          <tr><td><strong>W-2</strong></td><td>High</td><td>Wages and reported tips from an employer. Usually captures card tips well and cash poorly.</td></tr>
          <tr><td><strong>Pay stubs</strong></td><td>High</td><td>Recent and verifiable. Often shows a small base wage that dramatically understates what you earn.</td></tr>
          <tr><td><strong>Bank statements</strong></td><td>Medium</td><td>Shows money arriving. Cash deposits corroborate a pattern, but do not prove a source.</td></tr>
          <tr><td><strong>Employer letter</strong></td><td>Medium</td><td>Useful for tenure and role; managers are often unwilling to certify tip income.</td></tr>
          <tr><td><strong>Your own shift log</strong></td><td>Supporting</td><td>Explains the cash portion and shows consistency. Not verified, and should never be presented as if it were.</td></tr>
        </tbody>
      </table>

      <h2>The stack that works</h2>
      <ol>
        <li><strong>Lead with the official documents.</strong> Return, W-2, recent stubs.
          These are what the process is designed to read.</li>
        <li><strong>Add bank statements</strong> covering the same period, so deposits and
          reported income visibly agree.</li>
        <li><strong>Then offer your log</strong> as the thing that explains the gap between
          a small base wage and the deposits — a dated, per-shift record covering the same
          months.</li>
        <li><strong>Summarise it in one page.</strong> Total earnings for the period, monthly
          average, shifts worked, hours, and average rate. Nobody reads 200 rows.</li>
      </ol>

      <div class="callout">
        <p><strong>Be straight about what your log is.</strong> It is self-reported and
        unaudited. Label it that way. A record that is honest about its own status reads as
        credible; one dressed up as a certified statement invites exactly the scepticism you
        were trying to avoid — and misrepresenting it can be fraud.</p>
      </div>

      <h2>Why consistency beats size</h2>
      <p>Underwriters and letting agents are not primarily asking "how much?" — they are
      asking "will this continue?". A steady $2,900 a month across fourteen months is a
      stronger application than a spiky average of $3,400 built from three enormous months
      and several thin ones.</p>
      <p>Which means the useful thing is <strong>length of history</strong>, and history is
      the one thing you cannot create retroactively. A log begun today is a strong
      application next spring; a log begun next spring is nothing at all.</p>

      <h2>The under-reporting trap</h2>
      <p>This is where a lot of tipped workers discover the real price of not reporting cash.
      Every serious income process reads your tax return. Income you did not report does not
      exist for a mortgage underwriter, a visa officer or a letting agent — and you cannot
      credibly argue that you actually earn more than you told the government you did.</p>
      <p>People routinely lose an apartment or a rate over income they genuinely earned but
      never documented. <a href="/guides/reporting-cash-tips/">More on reporting cash
      tips →</a></p>

      <h2>Practical notes</h2>
      <ul>
        <li><strong>Ask what they need</strong> before assembling anything. Requirements vary
          enormously.</li>
        <li><strong>Cover a clean period</strong> — full months, matching your statements.</li>
        <li><strong>Explain the seasonality</strong> if your work has any. A resort-town
          winter is not a red flag if you name it first.</li>
        <li><strong>Keep multiple jobs separate and then totalled</strong>, so the sum is
          traceable.</li>
        <li><strong>Send PDFs</strong>, paginated and dated. A screenshot of a spreadsheet
          reads as improvised.</li>
      </ul>
"""
    add(Page(p, "Proof of Income for Tipped Workers: What Works",
             "How to prove your income when most of it is tips: which documents carry "
             "weight, how to present a shift log honestly, and why history beats a big "
             "average.",
             article("Life admin", "Proof of income for tipped workers",
                     "Apartments, loans and visas are built around salaries and employer "
                     "letters. Here is how to build something they will accept instead.",
                     body,
                     takeaway=takeaways([
                         "No single document does it. <strong>Corroboration</strong> is what convinces: return, W-2, stubs, statements, then your log.",
                         "Your own log is <strong>supporting</strong> evidence. Label it self-reported and unaudited — never dress it up.",
                         "Summarise to one page: total, monthly average, shifts, hours, rate.",
                         "Reviewers care about <strong>consistency over time</strong> more than the size of the number.",
                         "Unreported income does not exist for underwriters. That is the real cost of not reporting cash.",
                     ]),
                     faq=faq_html(faq))
             + related([
                 ("Reporting cash tips", "/guides/reporting-cash-tips/", "The reporting decision that shapes every application later."),
                 ("How to track your tips", "/guides/how-to-track-tips/", "Building the history you'll need next spring."),
                 ("Shift earnings calculator", "/calculators/shift-earnings/", "Totalling a period the way a reviewer reads it."),
             ])
             + app_cta_band("History is the one thing you can't backdate.",
                            "Tipfolio turns your log into a clean income statement for any "
                            "period — total earnings, monthly average, hours and rate, "
                            "honestly labelled."),
             og_type="article",
             trail=[("Home", "/"), ("Guides", "/guides/"), ("Proof of income", None)],
             nav="/guides/", priority="0.85",
             schema=[article_schema("Proof of income for tipped workers",
                                    "Documents that work when most of your income is tips.", p),
                     faq_schema(faq)]))
