"""Occupation landing pages. Written per role — the pay realities genuinely differ,
so these are not one template with the noun swapped."""
from build import (Page, add, TAX, BRAND, cta, disclaimer, app_cta_band,
                   related, SITE)
from content_guides import faq_html, faq_schema, takeaways, article_schema


def role_page(*, path, title, description, kicker, h1, lede, points, body,
              takeaway, faq, crumb, shot="01-home", shot_alt=None, rel=None):
    hero = f"""
<section class="role-hero" style="padding:clamp(44px,5vw,76px) 0">
  <div class="wrap">
    <div>
      <p class="eyebrow green">{kicker}</p>
      <h1>{h1}</h1>
      <p class="lede" style="margin-top:18px">{lede}</p>
      <ul class="privacy-list" style="margin-top:26px">
        {''.join(f'<li><span class="tick">&#10003;</span><span>{p}</span></li>' for p in points)}
      </ul>
      <div class="hero-actions">{cta()}
        <a class="btn btn-ghost" href="/calculators/real-hourly-rate/">Check your real rate</a></div>
    </div>
    <div><div class="phone"><picture>
      <source srcset="/assets/img/{shot}.webp" type="image/webp">
      <img src="/assets/img/{shot}.jpg" width="860" height="1869" loading="lazy"
           alt="{shot_alt or 'The Tipfolio home screen.'}"></picture></div></div>
  </div>
</section>
<section style="padding-top:clamp(44px,5vw,72px)">
  <div class="wrap narrow">
    {takeaways(takeaway)}
    <div class="prose" style="margin-top:0">
      {body}
      {faq_html(faq)}
    </div>
  </div>
</section>"""
    add(Page(path, title, description,
             hero + related(rel or []) + app_cta_band(),
             og_type="article",
             trail=[("Home", "/"), ("Who it's for", "/for/"), (crumb, None)],
             nav="", priority="0.8",
             schema=[article_schema(h1.replace("&amp;", "and"), description, path),
                     faq_schema(faq)]))


def build():
    # ==================================================== HUB
    roles = [
        ("Servers &amp; waitstaff", "/for/servers/",
         "The most complicated tip-out in the building, plus auto-grats, side work "
         "and a section you do not choose."),
        ("Bartenders", "/for/bartenders/",
         "On both sides of the tip-out: cash-heavy, and shifts that cross midnight "
         "into the wrong business date."),
        ("Baristas &amp; café staff", "/for/baristas/",
         "Pooled tips split by hours. Small per shift, substantial per year, and "
         "easy to under-count from memory."),
        ("Delivery drivers", "/for/delivery-drivers/",
         "Tips versus delivery fees versus promotions — three different things the "
         "app screens blur into one total."),
        ("Hairstylists &amp; barbers", "/for/hairstylists/",
         "Commission or chair rent: two genuinely different tax positions wearing "
         "the same job title."),
    ]
    cards = "".join(
        f'<a class="link-card" href="{href}"><h2>{name}</h2><p>{blurb}</p>'
        f'<span class="more">Read →</span></a>' for name, href, blurb in roles)

    hub_body = f"""
<section class="article">
  <div class="wrap">
    <div class="article-head">
      <p class="eyebrow green">Who it's for</p>
      <h1>Different jobs, different money.</h1>
      <p class="lede">A server's tip-out is nothing like a booth renter's chair rent, and a
        delivery fee is not a tip at all. The rules that matter change with the job, so start
        with the one you actually do.</p>
    </div>
  </div>
</section>
<section style="padding-top:34px">
  <div class="wrap">
    <div class="grid grid-3">{cards}</div>
    <p class="lede" style="margin-top:34px">Hotel staff, casino dealers, valets, tattoo
      artists and everyone else — the <a href="/guides/">guides</a> cover the rules that
      apply across tipped work, and the <a href="/calculators/">calculators</a> work whatever
      your job title is.</p>
    {disclaimer()}
  </div>
</section>
{app_cta_band()}
"""
    add(Page("/for/", "Tipfolio by Job — Servers, Bartenders, Baristas & More",
             "Tip tracking for the job you actually do. Servers, bartenders, baristas, "
             "delivery drivers and salon pros each face different tip-out, cash and "
             "tax realities.",
             hub_body, trail=[("Home", "/"), ("Who it's for", None)], priority="0.85"))

    # ==================================================== SERVERS
    role_page(
        path="/for/servers/",
        crumb="Servers",
        title="Tip Tracker for Servers & Waitstaff — Tipfolio",
        description="A tip log built for restaurant servers: log a shift in ten seconds, "
                    "handle tip-outs and auto-grats properly, and see which sections and "
                    "nights actually pay.",
        kicker="For servers & waitstaff",
        h1="A tip log for servers.",
        lede="Your section, your tip-out, your side work, your closing shift. Tipfolio is "
             "built around the ten seconds you have after you cash out — not around a "
             "spreadsheet you will abandon by week three.",
        points=[
            "Tip-out worked out automatically from your house's rule — % of tips, % of sales, or flat.",
            "Cash and card kept separate, because your W-2 only really sees one of them.",
            "Auto-gratuity logged apart from voluntary tips, which matters for the deduction.",
            "Average take-home by night of the week — evidence for which shifts to fight for.",
        ],
        shot="02-insights",
        shot_alt="Insights screen showing average take-home by night of the week.",
        takeaway=[
            "Servers usually carry the most complicated tip-out in the building — record gross and tip-out separately, every night.",
            "<strong>Auto-grat is not a tip.</strong> Log it apart from voluntary tips or you cannot isolate what qualifies.",
            "Side work is hours. Leave it out and your rate is fiction.",
            "Section and night drive earnings more than anything you control — but only a log proves it.",
        ],
        faq=[
            ("How much do servers actually make an hour?",
             "It depends far more on the house, the section and the night than on the "
             "state's tipped minimum. The only figure worth acting on is your own blended "
             "rate across a few months: tips minus tip-out, plus base wage, over actual "
             "hours worked. It is usually lower than the number people quote and higher "
             "than the base wage on the stub."),
            ("Do I have to report cash tips as a server?",
             "Yes. Cash tips are income. Separately, receiving $20 or more in tips in a "
             "month at one job generally triggers a requirement to report them to that "
             "employer in writing. See the guide on reporting cash tips for the detail."),
            ("Does my tip-out reduce my taxable tips?",
             "Generally, tips passed to bussers, bar and runners under a genuine sharing "
             "arrangement are their income rather than yours — but only if you can show "
             "what you passed on, which means recording both numbers."),
            ("What about the automatic gratuity on large parties?",
             "An auto-grat is typically a service charge rather than a voluntary tip, and "
             "is usually treated as wages. Keep it as its own line in your log."),
        ],
        body=f"""
      <h2>Why serving is the hardest tipped job to record</h2>
      <p>A bartender has one tip jar and a bank. A barista has a pooled total handed to them.
      A server has: cash tips, card tips, an auto-grat on the eight-top, a tip-out to the bar
      calculated one way, another to the bussers calculated another way, a comp that changed
      the sales figure, and a closing side-work hour that nobody counts.</p>
      <p>All of which arrives at once, at midnight, when you want to leave. It is not that
      servers are worse at record-keeping — it is that serving generates more to record than
      any other tipped role.</p>

      <h2>The four numbers to protect</h2>
      <ol>
        <li><strong>Gross tips, cash and card separately.</strong> Your employer's system
          sees the card side reasonably well and the cash side barely at all. The cash figure
          is one only you can produce.</li>
        <li><strong>Tip-out paid.</strong> Not the net you walked with —
          <a href="/guides/tip-out-explained/">both numbers</a>. Servers typically have the
          largest tip-out in the building, and it is the difference between what you earned
          and what you kept.</li>
        <li><strong>Auto-grat, separately.</strong> Mandatory service charges are generally
          treated as wages rather than tips, which means lumping them in makes it impossible
          to isolate what might qualify for the
          <a href="/guides/no-tax-on-tips/">tip deduction</a>.</li>
        <li><strong>Actual hours.</strong> Including the pre-shift and the forty minutes of
          side work after close.</li>
      </ol>

      <h2>The question worth answering</h2>
      <p>Not "what do I make" — "which shifts are worth taking". Servers have more leverage
      over their schedule than almost any other tipped role, and almost none of it gets used,
      because nobody has the evidence.</p>
      <p>Once you have a couple of months logged, the patterns are usually stark: one night
      running well above the others, the patio beating the dining room in summer, brunch
      quietly underperforming the hours it eats. That is information you can take to a
      scheduling conversation.</p>

      <div class="callout">
        <p><strong>The sales-based tip-out trap.</strong> If your house tips out on sales
        rather than tips, a badly tipping large party costs you twice — once in the tip that
        did not come, and once in the tip-out you owe on the sales anyway. Over a year that
        asymmetry is real money, and it is invisible unless you logged sales alongside tips.
        <a href="/calculators/tip-out/">Compare the two bases →</a></p>
      </div>

      <h2>What Tipfolio does with it</h2>
      <ul>
        <li>Your job, wage and tip-out rule are set once and pre-filled every shift.</li>
        <li>A nightly nudge at 11:30 PM that opens straight onto the keypad.</li>
        <li>Every entry timestamped as you make it — the thing that makes it a
          contemporaneous record rather than a reconstruction.</li>
        <li>Multiple jobs, each with its own wage and rule, aggregating into one tax year.</li>
        <li>Exports as PDF or CSV, with the entry time on every line.</li>
      </ul>
      {disclaimer()}
""",
        rel=[("Real hourly rate calculator", "/calculators/real-hourly-rate/",
              "What last night actually paid, once tip-out is out."),
             ("Tip-outs explained", "/guides/tip-out-explained/",
              "Pools, shares, and what your house can take."),
             ("Reporting cash tips", "/guides/reporting-cash-tips/",
              "The obligation on the half nobody records for you.")],
    )

    # ==================================================== BARTENDERS
    role_page(
        path="/for/bartenders/",
        crumb="Bartenders",
        title="Tip Tracker for Bartenders — Log Shifts in Ten Seconds",
        description="A tip log built for bartenders: track tips you receive and tip-outs "
                    "you pay, keep cash and card separate, and see what the bar actually "
                    "pays per hour.",
        kicker="For bartenders",
        h1="A tip log for bartenders.",
        lede="You are on both sides of the tip-out — taking a share from the floor and "
             "paying one to the barback. Tipfolio records what came in, what went out, and "
             "what the shift actually paid you per hour.",
        points=[
            "Cash-heavy nights logged as cash, so your own figure is not just the card total.",
            "Long shifts measured properly — an end time before the start means it crossed midnight.",
            "Service bar versus well: log them as separate jobs and compare them honestly.",
            "Your blended rate across a month, not the number from one great Saturday.",
        ],
        shot="01-home",
        shot_alt="Tipfolio home screen showing the night's take-home and hourly rate.",
        takeaway=[
            "Bartenders often <strong>receive</strong> tip-out as well as paying it. Both directions belong in the log.",
            "Bar work is disproportionately cash — the half your employer's system sees worst.",
            "Overnight shifts must be attributed to the right business date or a year's income misfiles.",
            "Comparing service bar to a busy well is only possible if you log them as separate jobs.",
        ],
        faq=[
            ("Do bartenders have to report cash tips?",
             "Yes — cash tips are income regardless of how they arrive. Bar work tends to be "
             "the most cash-heavy tipped role, which makes your own daily record more "
             "important here than almost anywhere else, because payroll captures very little "
             "of it automatically."),
            ("How do I log a shift that ends after midnight?",
             "Attribute it to the date the shift belongs to, not the clock time you typed it "
             "at. A Friday shift ending at 2:15 AM is a Friday shift. Tipfolio handles this "
             "automatically: an end time earlier than the start is read as crossing midnight, "
             "and the business date stays put."),
            ("Should I count the tip-out I receive from servers?",
             "Yes. Money coming to you from the floor is part of what you earned that night, "
             "and leaving it out understates your rate — often substantially on a busy "
             "service-bar shift."),
            ("Is a tip jar split different from a tip pool?",
             "In practice, a jar divided by hours worked behaves like a pool. What matters "
             "for your records is that you log your actual share and, where you can, the "
             "basis it was worked out on."),
        ],
        body=f"""
      <h2>The two-way problem</h2>
      <p>Most tip-tracking advice assumes money flows one way: you get tipped, you tip out, you
      keep the rest. Behind a bar it moves in both directions on the same shift — a share
      coming from the floor on service-bar sales, a barback tip-out going the other way, plus
      whatever landed in the jar directly.</p>
      <p>If your log only captures "what I walked with", all of that collapses into one
      number and you lose the ability to answer the questions that actually matter: whether
      service bar is worth it, whether the barback split is fair, and whether your best nights
      are your busiest ones.</p>

      <h2>Cash is a bigger share of your problem</h2>
      <p>Bar work skews cash — more than the floor, far more than a café. That matters for
      two practical reasons.</p>
      <ul>
        <li>Payroll systems capture card tips well and cash tips only as well as you declare
          them, so <strong>your own record is the only complete one</strong>.</li>
        <li>When you later need to prove earnings — a lease, a car, a mortgage — the cash you
          did not report simply does not exist to the person reading your return.
          <a href="/guides/proof-of-income-for-tipped-workers/">More on that →</a></li>
      </ul>

      <h2>Midnight, and why it matters more than it sounds</h2>
      <p>A bar shift routinely ends after midnight. Log it on the clock and a Friday night's
      money lands on Saturday; do it on New Year's Eve and it lands in the wrong
      <em>tax year</em>.</p>
      <p>That is not pedantry — attribution by business date is what keeps a year's totals
      correct, and it is exactly the kind of thing that is invisible until an annual figure
      is being reconciled against a W-2.</p>

      <div class="callout">
        <p><strong>Log stations as separate jobs.</strong> Service bar on a Saturday and a
        quiet well on a Tuesday are effectively different jobs with different economics.
        Tipfolio lets you keep them separate, each with its own wage and tip-out rule, and
        still aggregates them into one tax year. After a month you will know which one you
        should be asking for.</p>
      </div>

      <h2>What good bar records look like</h2>
      <ol>
        <li>Cash and card tips, separately.</li>
        <li>Tip-out received from the floor, and tip-out paid to barbacks.</li>
        <li>Actual hours, including setup and breakdown.</li>
        <li>The business date, not the clock date.</li>
        <li>Which station or bar it was.</li>
      </ol>
      <p>Five fields, ten seconds, at the point you count your bank. That is the whole
      system. <a href="/guides/how-to-track-tips/">How to make it stick →</a></p>
      {disclaimer()}
""",
        rel=[("Shift earnings calculator", "/calculators/shift-earnings/",
              "Blend a week of bar shifts the right way."),
             ("Tip-outs explained", "/guides/tip-out-explained/",
              "Both directions of the money, properly recorded."),
             ("No Tax on Tips, explained", "/guides/no-tax-on-tips/",
              "The deduction, and the record it rests on.")],
    )

    # ==================================================== BARISTAS
    role_page(
        path="/for/baristas/",
        crumb="Baristas",
        title="Tip Tracker for Baristas — Track Pooled Café Tips",
        description="A tip log for baristas and café staff: record your share of pooled "
                    "tips, keep digital and cash separate, and see what your hourly rate "
                    "really comes to.",
        kicker="For baristas & café staff",
        h1="A tip log for baristas.",
        lede="Café tips arrive pooled, split by hours, and mostly through a screen. That "
             "makes them easy to ignore — and easy to lose track of across a year that "
             "adds up to more than you would guess.",
        points=[
            "Log your share of the pool per shift, not a vague monthly total.",
            "Digital tip-screen prompts and the cash jar recorded separately.",
            "See what tips add to your base wage — the number that decides whether a café job pays.",
            "A year of small numbers, totalled properly, for the deduction and for proof of income.",
        ],
        shot="03-taxes",
        shot_alt="Tax Center showing tips tracked against the annual deduction cap.",
        takeaway=[
            "Café tips are small per shift and substantial per year. The annual total is the one that matters.",
            "Pooled and hour-weighted: log <strong>your share</strong>, on the shift, not a monthly guess.",
            "Digital tip prompts usually run through payroll; the jar usually does not. Keep them apart.",
            "A higher base wage means your rate depends on tips less — which makes the tip figure easier to under-count.",
        ],
        faq=[
            ("Do baristas have to report tips?",
             "Yes. Tips are income whether they arrive through a card reader or a jar. "
             "Digital tips usually flow through payroll and appear on your W-2; the cash jar "
             "generally does not, which makes it the part you have to record yourself."),
            ("How do I track tips that are pooled and split by hours?",
             "Record the share you actually received for that shift. If the split is "
             "published, noting the pool total and your hours alongside it is useful — it "
             "lets you check the arithmetic later and spot a formula that has quietly "
             "drifted."),
            ("Are café tips even worth tracking?",
             "Per shift they look trivial. Across a year of shifts they typically add up to "
             "a meaningful percentage of your earnings — and it is the annual figure that "
             "matters for a deduction, a lease application or a loan. Small and regular is "
             "exactly the pattern people under-count from memory."),
            ("Does the tip screen prompt count as a tip?",
             "A voluntary amount a customer chooses on the screen is generally a tip. A "
             "mandatory service charge or fee set by the café is generally not, and is "
             "usually treated as wages. If your café adds both, keep them separate."),
        ],
        body=f"""
      <h2>Small numbers, large year</h2>
      <p>The reason café tips go unrecorded is not that they are unimportant — it is that any
      single shift's share looks too small to bother writing down. Twelve dollars here,
      twenty-two there.</p>
      <p>Multiply by four or five shifts a week across a year and it stops being small. It is
      also, for many baristas, the difference between a job that works and one that does not
      — which makes it worth knowing precisely rather than approximately.</p>

      <h2>Two streams, and only one of them is recorded for you</h2>
      <table>
        <thead><tr><th>Where it comes from</th><th>Who records it</th></tr></thead>
        <tbody>
          <tr><td><strong>Card / tip-screen prompts</strong></td><td>Usually flows through the POS and payroll, and lands on your W-2. Mostly handled for you.</td></tr>
          <tr><td><strong>Cash jar</strong></td><td>Usually nobody. This is the part that only exists if you write it down.</td></tr>
          <tr><td><strong>Service charges or fees</strong></td><td>Set by the café, generally treated as wages rather than tips. Keep them out of your tip figure.</td></tr>
        </tbody>
      </table>

      <h2>Pooled, hour-weighted, and worth checking</h2>
      <p>Most cafés pool tips and divide by hours worked. That is a reasonable system and it
      has one weakness: almost nobody checks the arithmetic.</p>
      <p>If you log your share per shift alongside your hours, you build the ability to spot
      a split that has drifted, a pool that has quietly gained participants, or a period where
      your share fell without explanation. You do not need to be suspicious for that to be
      worth having — you just need the record.</p>

      <div class="callout">
        <p><strong>The higher base wage cuts both ways.</strong> Café work often pays a real
        hourly wage rather than a tipped minimum, so tips are a smaller share of the total.
        That makes the job steadier — and it makes the tip figure much easier to under-count,
        because you are not depending on it week to week. It still counts as income, and it
        still counts toward what you can prove you earn.</p>
      </div>

      <h2>What it is worth per hour</h2>
      <p>The useful barista number is simple: base wage plus tips, over hours worked. It is
      what tells you whether the busy store across town is actually better, whether opens
      beat closes, and whether a management track is a raise or a lateral move once the tip
      share disappears.</p>
      <p><a href="/calculators/real-hourly-rate/">Work it out for a shift →</a></p>
      {disclaimer()}
""",
        rel=[("Real hourly rate calculator", "/calculators/real-hourly-rate/",
              "Base wage plus tips, over the hours you worked."),
             ("How to track your tips", "/guides/how-to-track-tips/",
              "A ten-second habit that survives a morning rush."),
             ("Proof of income for tipped workers", "/guides/proof-of-income-for-tipped-workers/",
              "Turning a year of small numbers into a lease application.")],
    )

    # ==================================================== DELIVERY DRIVERS
    role_page(
        path="/for/delivery-drivers/",
        crumb="Delivery drivers",
        title="Tip Tracker for Delivery Drivers — Tips, Fees & Miles",
        description="A tip log for delivery drivers: separate real tips from delivery "
                    "fees, track earnings per hour across apps, and keep the record your "
                    "taxes need.",
        kicker="For delivery drivers",
        h1="A tip log for delivery drivers.",
        lede="A delivery fee is not a tip, an hour on the app is not an hour of orders, and "
             "the number the app shows you is not what you took home. Tipfolio records what "
             "actually arrived.",
        points=[
            "Tips logged separately from delivery fees and promotions.",
            "Earnings per hour of actual driving, not per hour logged in.",
            "Multiple platforms tracked as separate jobs, totalled into one year.",
            "A dated record for a role where nobody else is keeping one for you.",
        ],
        shot="05-taxreport",
        shot_alt="Tax report export listing each shift with the time it was entered.",
        takeaway=[
            "<strong>Delivery fees are not tips.</strong> They are platform revenue passed through, and they are treated differently.",
            "Track hours actually driving, not hours logged into an app, or your rate is meaningless.",
            "Many drivers are treated as self-employed — a different tax position, with different records required.",
            "<strong>Vehicle costs are the biggest thing a tip log won't capture.</strong> Track mileage separately.",
        ],
        faq=[
            ("Are delivery fees the same as tips?",
             "No. A delivery fee is charged by the platform or restaurant and passed through "
             "in part or whole; a tip is an amount the customer chose to add for you. They "
             "are usually treated differently for tax, and mixing them in your own records "
             "makes it impossible to separate them later."),
            ("Do I have to report tips from delivery apps?",
             "Yes. Tips are income however they arrive. If you are treated as an independent "
             "contractor you will generally receive a 1099 rather than a W-2, and your tax "
             "position — including self-employment tax and deductible business expenses — is "
             "meaningfully different from an employee's. This is a good area to get "
             "professional advice on."),
            ("Does the tip deduction apply to delivery drivers?",
             f"Eligibility depends on the rules as they apply to your situation and your "
             f"employment status, and the position for independent contractors is not the "
             f"same as for employees. The cap of {TAX['cap_display']} and the tax years "
             f"{TAX['years']} are the parameters to check against current guidance. Take "
             f"advice rather than assuming."),
            ("What about mileage and vehicle costs?",
             "For self-employed drivers these are usually the single largest factor in what "
             "the work actually pays, and they need their own record — a mileage log, kept "
             "contemporaneously. Tipfolio tracks what came in; it does not track what your "
             "car cost you, and you should not treat your take-home figure as profit."),
        ],
        body=f"""
      <h2>Three numbers the apps blur together</h2>
      <p>Open any delivery platform's earnings screen and you will see a total. Underneath it
      are at least three quite different things:</p>
      <ul>
        <li><strong>The tip</strong> — what the customer chose to give you.</li>
        <li><strong>The delivery fee or base pay</strong> — what the platform pays for the
          job. Not a tip, and generally treated differently.</li>
        <li><strong>Promotions and bonuses</strong> — surge, quest completions, referral
          money. Different again.</li>
      </ul>
      <p>Keeping them apart in your own log is the whole game. Collapse them into one figure
      and you cannot isolate the tip portion, cannot compare platforms honestly, and cannot
      tell whether your earnings are coming from customers or from promotions that will end.</p>

      <h2>Logged-in hours are not worked hours</h2>
      <p>An eight-hour session with two dead hours waiting in a car park is not an eight-hour
      shift, and it is not a six-hour one either. Which you count changes your apparent rate
      by a third, so the only rule that matters is <strong>pick one definition and stay with
      it</strong>. Otherwise you cannot compare Tuesday to Friday, let alone one app to
      another.</p>
      <p>Most drivers find hours-on-the-clock (first accept to last drop) the most honest,
      because the waiting is a real cost of the work.</p>

      <div class="callout">
        <p><strong>The thing a tip log cannot tell you.</strong> Fuel, maintenance, tyres,
        insurance and depreciation come out of these numbers, and for a self-employed driver
        they are usually the difference between a decent rate and a poor one. Tipfolio records
        what came in. It does not know what your car cost you — so keep a mileage log
        alongside it and never mistake take-home for profit.</p>
      </div>

      <h2>Employee or contractor changes everything</h2>
      <p>Drivers delivering for a restaurant are often employees, receiving a W-2, with tips
      reported through payroll. Drivers on platforms are commonly treated as independent
      contractors, receiving a 1099, responsible for their own estimated taxes and
      self-employment tax, and able to deduct genuine business expenses.</p>
      <p>Those are materially different tax positions, and the records each one needs are
      different too. If you are not certain which you are, that is worth resolving with a tax
      professional before you file rather than after.</p>

      <h2>Multiple apps, one year</h2>
      <p>Most drivers run more than one platform. Set each one up as its own job so you can
      compare their real rates against each other, while the annual totals still add up into a
      single picture for tax and for proving your income.</p>
      <p><a href="/calculators/shift-earnings/">Compare a week across platforms →</a></p>
      {disclaimer()}
""",
        rel=[("Shift earnings calculator", "/calculators/shift-earnings/",
              "Compare platforms over a week, blended properly."),
             ("Reporting cash tips", "/guides/reporting-cash-tips/",
              "What has to be reported, and to whom."),
             ("Proof of income for tipped workers", "/guides/proof-of-income-for-tipped-workers/",
              "Gig income, and the documents lenders will actually take.")],
    )

    # ==================================================== HAIRSTYLISTS
    role_page(
        path="/for/hairstylists/",
        crumb="Hairstylists & barbers",
        title="Tip Tracker for Hairstylists, Barbers & Nail Techs",
        description="A tip log for salon and barbershop professionals: track client tips "
                    "alongside commission or booth rent, and keep the daily record your "
                    "taxes depend on.",
        kicker="For hairstylists, barbers & nail techs",
        h1="A tip log for salon &amp; barbershop pros.",
        lede="Chair rent or commission, cash tips and card tips, product costs and a "
             "book that varies week to week. Tipfolio handles the tip half properly, which "
             "is the half nobody else is recording.",
        points=[
            "Client tips logged per day, cash and card kept apart.",
            "Works whether you are commission staff or renting a chair.",
            "Daily totals that reconcile against your card processor at month end.",
            "A dated record for a role where self-employment makes records your own responsibility.",
        ],
        shot="06-settings",
        shot_alt="Tipfolio settings screen, footed by: your earnings never leave this iPhone.",
        takeaway=[
            "Booth renters are usually <strong>self-employed</strong> — records are entirely your responsibility, and expenses matter as much as income.",
            "Cash tips in a chair-side environment are the least-captured income in the trade.",
            "Reconcile daily tip totals against your processor monthly; discrepancies are far easier to resolve while recent.",
            "Product and supply costs are not in a tip log. Track them separately or you will overstate what you earn.",
        ],
        faq=[
            ("Do hairstylists have to report cash tips?",
             "Yes. Tips are income, and in a chair-side trade the cash portion is often "
             "substantial. If you are an employee, the usual monthly reporting to your "
             "employer applies. If you rent a chair you are generally self-employed, which "
             "means the reporting, the record-keeping and the estimated tax payments are all "
             "yours to handle."),
            ("Is booth rent different from commission for taxes?",
             "Substantially. Commission stylists are typically employees with a W-2. Booth "
             "renters are typically self-employed, filing a Schedule C, paying "
             "self-employment tax and deducting business expenses including the rent itself. "
             "Which one you are changes almost everything about your filing, so confirm it "
             "rather than assuming."),
            ("Can I deduct product and supply costs?",
             "If you are self-employed, ordinary and necessary business expenses — product, "
             "tools, chair rent, some education — are generally deductible against your "
             "business income. That is a separate record from your tip log, and it needs "
             "receipts. Talk to a tax professional about what qualifies in your case."),
            ("Does the tip deduction apply to barbers and nail techs?",
             "Tipped occupations in personal care are commonly within scope, but eligibility "
             "depends on the rules as applied to your situation and employment status. The "
             "record requirement is the same either way: a contemporaneous daily log of tips "
             "received."),
        ],
        body=f"""
      <h2>Two quite different jobs with the same job title</h2>
      <p>The most consequential fact about your record-keeping is not what you do to hair —
      it is how you are engaged.</p>
      <table>
        <thead><tr><th></th><th>Commission / employed</th><th>Booth or chair rent</th></tr></thead>
        <tbody>
          <tr><td>Tax documents</td><td>W-2 from the salon</td><td>Generally self-employed; Schedule C</td></tr>
          <tr><td>Who withholds</td><td>The salon</td><td>You, through estimated payments</td></tr>
          <tr><td>Tip reporting</td><td>To your employer monthly, then payroll</td><td>Entirely your own record</td></tr>
          <tr><td>Expenses</td><td>Largely not deductible</td><td>Rent, product, tools generally deductible</td></tr>
        </tbody>
      </table>
      <p>If you rent, nobody is producing any record of your income except you. That is a
      significant responsibility and it is also an opportunity: a clean, dated log is what
      makes a mortgage application or a lease possible in a trade where people routinely
      struggle to prove what they earn.</p>

      <h2>The cash problem, chair-side</h2>
      <p>Personal-care work generates a high proportion of cash tips — often handed over
      directly, often at the chair, often unrecorded anywhere at all. It is the least-captured
      income in the trade.</p>
      <p>Log it at the end of the day rather than per client. Trying to record fifteen
      individual tips will fail; recording one honest daily total will not.
      <a href="/guides/how-to-track-tips/">The habit that sticks →</a></p>

      <div class="callout">
        <p><strong>Reconcile monthly.</strong> Compare your logged card tips against your
        processor's statement each month. Discrepancies are ordinary — a batch that settled
        late, a refund, a split payment — and they are trivial to resolve while the month is
        recent and nearly impossible a year later. Ten minutes a month is the whole cost.</p>
      </div>

      <h2>What a tip log does not cover</h2>
      <p>Colour, tools, chair rent, insurance, education, the card processor's fee. If you are
      self-employed these are as important to your actual position as the tips are, and they
      belong in a bookkeeping record with receipts attached, not in a tip log.</p>
      <p>Tipfolio deliberately does one thing: the daily record of tips received. Treat what
      it shows you as revenue, not profit.</p>

      <h2>Why the daily record matters more for you</h2>
      <ul>
        <li>Self-employment means <strong>no employer</strong> is generating a parallel record
          to fall back on.</li>
        <li>Estimated tax payments are easier to size sensibly when you know what you are
          actually taking.</li>
        <li>Proving income for a lease, a loan or a visa is materially harder in this trade —
          and a long, dated history is the strongest thing you can bring.
          <a href="/guides/proof-of-income-for-tipped-workers/">More →</a></li>
        <li>A tip deduction, where it applies, rests on that same daily record.</li>
      </ul>
      {disclaimer()}
""",
        rel=[("Real hourly rate calculator", "/calculators/real-hourly-rate/",
              "What a day in the chair actually pays."),
             ("Proof of income for tipped workers", "/guides/proof-of-income-for-tipped-workers/",
              "Self-employed, and needing to prove it."),
             ("No Tax on Tips, explained", "/guides/no-tax-on-tips/",
              "The deduction, and who it does and doesn't help.")],
    )
