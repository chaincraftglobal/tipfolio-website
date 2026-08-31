"""The four free calculators, plus their index."""
from build import (Page, add, TAX, BRAND, cta, disclaimer, app_cta_band,
                   related, SITE)

CALC_JS = '\n<script src="/assets/js/calc.js" defer></script>'

NOSCRIPT = ('<noscript><p class="noscript-note">This calculator runs entirely in your '
            'browser, so it needs JavaScript switched on. Nothing you type is sent '
            'anywhere either way.</p></noscript>')

PRIVACY_NOTE = ('<p class="calc-note">Everything above is worked out in your browser. '
                'Nothing you type is uploaded, stored or logged — there is no server '
                'behind this page.</p>')


def faq_schema(pairs):
    items = ",".join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
        % (q.replace('"', '\\"'), a.replace('"', '\\"')) for q, a in pairs
    )
    return ('{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}' % items)


def faq_html(pairs):
    rows = "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in pairs)
    return f'<div class="faq" style="margin-top:26px">{rows}</div>'


def build():
    # ================================================== INDEX
    index = f"""
<section class="article">
  <div class="wrap">
    <div class="article-head">
      <p class="eyebrow green">Free tools</p>
      <h1>Calculators for tipped workers.</h1>
      <p class="lede">Four tools built on the same maths as the Tipfolio app — the tip-out
        rules, the rate formula, the deduction cap. No sign-up, no download, and nothing you
        type leaves your browser.</p>
    </div>
  </div>
</section>

<section style="padding-top:34px">
  <div class="wrap">
    <div class="grid grid-2">
      <a class="link-card" href="/calculators/real-hourly-rate/">
        <span class="kicker">Most popular</span>
        <h2>Real hourly rate calculator</h2>
        <p>Tips minus tip-outs, plus your base wage, divided by the hours you actually
           worked. The one honest number about a shift — and usually not the one on the
           job ad.</p>
        <span class="more">Calculate →</span></a>
      <a class="link-card" href="/calculators/tip-out/">
        <span class="kicker">Every night</span>
        <h2>Tip-out calculator</h2>
        <p>Percent of tips, percent of sales, or a flat amount. Work out what goes to the
           bar, the busser and the runner — and what you actually keep.</p>
        <span class="more">Calculate →</span></a>
      <a class="link-card" href="/calculators/tip-tax-deduction/">
        <span class="kicker">Tax season</span>
        <h2>Tip tax deduction estimator</h2>
        <p>See where your qualified tips land against the {TAX['cap_display']} annual cap
           for {TAX['years']}, and what that could be worth at your marginal rate.</p>
        <span class="more">Estimate →</span></a>
      <a class="link-card" href="/calculators/shift-earnings/">
        <span class="kicker">Week at a glance</span>
        <h2>Shift earnings calculator</h2>
        <p>Add up a week of shifts with base wage and tip-outs handled properly, and see
           the blended rate across all of them.</p>
        <span class="more">Calculate →</span></a>
    </div>
    {disclaimer()}
  </div>
</section>

{app_cta_band("These four numbers, every night, automatically.",
              "The calculators do one shift at a time. Tipfolio keeps the whole year — "
              "and turns it into the record your deduction depends on.")}
"""
    add(Page("/calculators/", "Free Calculators for Tipped Workers — Tipfolio",
             "Four free calculators for servers and bartenders: real hourly rate, "
             "tip-out, shift earnings and the tip tax deduction. Nothing you type "
             "leaves your browser.",
             index, trail=[("Home", "/"), ("Calculators", None)],
             nav="/calculators/", priority="0.9"))

    # ================================================== TIP-OUT
    to_faq = [
        ("What is a normal tip-out percentage?",
         "It varies by house and by role. Percent-of-tips arrangements commonly land "
         "somewhere between 15% and 30% of your tips split across bar, busser, runner and "
         "host. Percent-of-sales arrangements are usually a much smaller number — often 1% "
         "to 5% — because they are taken against total sales rather than against your tips. "
         "Your employer's written policy is the only figure that actually governs you."),
        ("Is tip-out taken from my tips before or after tax?",
         "Tip-out is a transfer of money you received to other workers, and it happens "
         "before any tax question arises. What matters for your records is that you log both "
         "the gross tips you took and the tip-out you paid, so your net is derived rather "
         "than estimated. Tipfolio always stores both."),
        ("Does tip-out reduce the tips I have to report?",
         "Generally, tips you pass on to other employees under a tip-sharing or tip-pooling "
         "arrangement are not part of your own tip income, and the workers who receive them "
         "report them instead. The precise treatment depends on your arrangement, so keep "
         "the record of both figures and confirm the treatment with a tax professional."),
        ("Can a tip-out be more than my tips?",
         "It should not be, and this calculator will not let it: a tip-out is capped at the "
         "tips earned, exactly as the Tipfolio app caps it. If your house's rule produces a "
         "number larger than what you made on a slow night, that is worth raising — it "
         "usually means the rule is percent-of-sales and the night went badly."),
    ]
    tipout = f"""
<section class="article">
  <div class="wrap">
    <div class="article-head">
      <p class="eyebrow green">Free calculator</p>
      <h1>Tip-out calculator</h1>
      <p class="lede">Work out what you owe the bar, the busser and the runner tonight —
        and what you actually walk with. Handles percent of tips, percent of sales and flat
        amounts.</p>
    </div>
  </div>
</section>

<section style="padding-top:30px">
  <div class="wrap">
    <div class="calc" id="calc-tipout">
      <form class="calc-form" onsubmit="return false">
        {NOSCRIPT}
        <div class="field">
          <label for="to-tips">Tips you took tonight <span class="hint">Cash and card together, before tip-out.</span></label>
          <input type="number" id="to-tips" inputmode="decimal" min="0" step="0.01" value="240" placeholder="0.00">
        </div>
        <div class="field">
          <label>How is your tip-out worked out?</label>
          <div class="segmented" role="radiogroup" aria-label="Tip-out basis">
            <label><input type="radio" name="basis" value="tips" checked><span>% of tips</span></label>
            <label><input type="radio" name="basis" value="sales"><span>% of sales</span></label>
            <label><input type="radio" name="basis" value="flat"><span>Flat</span></label>
          </div>
        </div>
        <div class="field" id="to-sales-field" hidden>
          <label for="to-sales">Your total sales tonight <span class="hint">Needed for a percent-of-sales rule.</span></label>
          <input type="number" id="to-sales" inputmode="decimal" min="0" step="0.01" value="1800" placeholder="0.00">
        </div>
        <div class="field">
          <label for="to-rate"><span id="to-rate-label">Percent of your tips</span>
            <span class="hint">Enter <span id="to-rate-unit">%</span>.</span></label>
          <input type="number" id="to-rate" inputmode="decimal" min="0" step="0.1" value="20">
        </div>
      </form>

      <div class="calc-result" aria-live="polite">
        <p class="eyebrow">You keep</p>
        <p class="headline" id="to-kept">$0.00</p>
        <p class="headline-sub" id="to-share">—</p>
        <ul class="calc-lines">
          <li><span>Tips taken</span><b id="to-gross">$0.00</b></li>
          <li><span>Tip-out paid</span><b id="to-out">$0.00</b></li>
        </ul>
        <p class="calc-warn" id="to-warn-sales" hidden>Enter your total sales — a
          percent-of-sales rule yields zero without one, rather than guessing.</p>
        <p class="calc-warn" id="to-warn-cap" hidden>That rule would take everything you
          made. A tip-out is capped at your tips here, as it is in the app.</p>
        {PRIVACY_NOTE}
      </div>
    </div>
  </div>
</section>

<section style="padding-top:44px">
  <div class="wrap narrow">
    <div class="prose" style="margin-top:0">
      <h2>The three ways houses do this</h2>
      <p>Almost every tip-out arrangement is one of three shapes, and which one you are on
        changes your risk profile far more than the percentage does.</p>
      <table>
        <thead><tr><th>Basis</th><th>How it's worked out</th><th>Who carries the risk of a bad night</th></tr></thead>
        <tbody>
          <tr><td><strong>% of tips</strong></td><td>A cut of what you made. The most common arrangement.</td><td>Shared. A slow night costs you both proportionally.</td></tr>
          <tr><td><strong>% of sales</strong></td><td>A cut of your total sales, regardless of what you were tipped.</td><td><strong>You.</strong> Get stiffed on a $400 table and you still owe on it.</td></tr>
          <tr><td><strong>Flat amount</strong></td><td>The same dollar figure every shift.</td><td><strong>You</strong> on slow nights; the support staff on busy ones.</td></tr>
        </tbody>
      </table>
      <div class="callout">
        <p><strong>Why percent-of-sales stings.</strong> On a $1,800 sales night at 4%, you
          owe $72 whether you were tipped $400 or $180. That is the arrangement worth
          tracking most carefully — over a year, the difference between what you'd owe on a
          tips basis and what you actually paid is real money, and you can only see it if
          you logged both figures.</p>
      </div>

      <h2>The formula</h2>
      <p>This calculator uses exactly the maths the Tipfolio app uses:</p>
      <ul>
        <li><strong>Percent of tips</strong> — <code>tip-out = gross tips × rate ÷ 100</code></li>
        <li><strong>Percent of sales</strong> — <code>tip-out = total sales × rate ÷ 100</code>, and <strong>zero</strong> if you have not entered a sales figure. It will not guess.</li>
        <li><strong>Flat</strong> — the amount you entered.</li>
        <li>In every case the result is clamped: <code>0 ≤ tip-out ≤ gross tips</code>.</li>
        <li><strong>What you keep</strong> — <code>net = gross tips − tip-out</code>, never below zero.</li>
      </ul>

      <h2>Log both numbers, not just the net</h2>
      <p>The single most common record-keeping mistake tipped workers make is writing down
        only what they walked with. That number is fine for your own budgeting and useless
        for everything else: you cannot check a W-2 against it, cannot show a lender your
        gross, and cannot tell whether your tip-out arrangement is quietly costing you.</p>
      <p>Keep the gross and the tip-out separately, every night.
        <a href="/guides/tip-out-explained/">More on how tip-outs work →</a></p>
      {disclaimer()}
      <h2>Questions</h2>
    </div>
    {faq_html(to_faq)}
  </div>
</section>

{related([
  ("Real hourly rate calculator", "/calculators/real-hourly-rate/", "What the shift actually paid, once tip-out and wage are in."),
  ("Tip-outs explained", "/guides/tip-out-explained/", "Pools, shares and what your house can legally take."),
  ("How to track your tips", "/guides/how-to-track-tips/", "The habit that makes the record hold up."),
])}

{app_cta_band("Your tip-out rule, applied automatically.",
              "Set it once per job and Tipfolio works it out on every shift — editable "
              "before you save, and stored alongside your gross so nothing is lost.")}
"""
    add(Page("/calculators/tip-out/", "Tip-Out Calculator — What You Owe the Bar Tonight",
             "Free tip-out calculator for servers and bartenders. Percent of tips, percent "
             "of sales or flat amount — see what you owe and what you actually keep.",
             tipout, og_type="article", page_js=CALC_JS,
             trail=[("Home", "/"), ("Calculators", "/calculators/"), ("Tip-out", None)],
             nav="/calculators/", priority="0.8", schema=[faq_schema(to_faq)]))

    # ================================================== REAL HOURLY RATE
    hr_faq = [
        ("How do you calculate a server's real hourly rate?",
         "Take your tips, subtract the tip-out you paid, add your base wage multiplied by "
         "the hours you worked, then divide the whole thing by those hours. In short: "
         "(net tips + base wage x hours) / hours. Most people skip the tip-out and use "
         "scheduled hours instead of actual, and both mistakes inflate the answer."),
        ("Should I use scheduled hours or the hours I actually worked?",
         "Actual. Side work, a late cut, and the forty minutes rolling silverware after "
         "close are all hours your earnings have to stretch across. Using scheduled hours "
         "flatters the number and makes it useless for comparing one job to another."),
        ("Is my real hourly rate what I should tell a landlord?",
         "It is a useful number, but a landlord or lender usually wants total earnings over "
         "a period rather than a rate. What they will not accept is a figure with nothing "
         "behind it, which is why a dated log matters more than any single number."),
        ("Why is my real rate lower than I expected?",
         "Usually one of three things: tip-out was not subtracted, unpaid or unrecorded "
         "hours were left out, or a couple of strong nights were quietly standing in for a "
         "typical one. A blended rate across many shifts is the honest version."),
    ]
    hourly = f"""
<section class="article">
  <div class="wrap">
    <div class="article-head">
      <p class="eyebrow green">Free calculator</p>
      <h1>Real hourly rate calculator</h1>
      <p class="lede">Tips, minus tip-outs, plus your base wage, divided by the hours you
        actually worked. It is the only number that lets you compare one shift, one job, or
        one night of the week against another.</p>
    </div>
  </div>
</section>

<section style="padding-top:30px">
  <div class="wrap">
    <div class="calc" id="calc-rate">
      <form class="calc-form" onsubmit="return false">
        {NOSCRIPT}
        <div class="field-row">
          <div class="field">
            <label for="hr-tips">Tips <span class="hint">Before tip-out.</span></label>
            <input type="number" id="hr-tips" inputmode="decimal" min="0" step="0.01" value="240">
          </div>
          <div class="field">
            <label for="hr-hours">Hours worked <span class="hint">Actual, not scheduled.</span></label>
            <input type="number" id="hr-hours" inputmode="decimal" min="0" step="0.25" value="7.5">
          </div>
        </div>
        <div class="field">
          <label for="hr-wage">Base hourly wage <span class="hint">Your cash wage before tips. Enter 0 if you have none.</span></label>
          <input type="number" id="hr-wage" inputmode="decimal" min="0" step="0.01" value="7.25">
        </div>
        <div class="field">
          <label>Tip-out basis</label>
          <div class="segmented" role="radiogroup" aria-label="Tip-out basis">
            <label><input type="radio" name="basis" value="tips" checked><span>% of tips</span></label>
            <label><input type="radio" name="basis" value="sales"><span>% of sales</span></label>
            <label><input type="radio" name="basis" value="flat"><span>Flat</span></label>
          </div>
        </div>
        <div class="field" id="hr-sales-field" hidden>
          <label for="hr-sales">Total sales</label>
          <input type="number" id="hr-sales" inputmode="decimal" min="0" step="0.01" value="1800">
        </div>
        <div class="field">
          <label for="hr-rate"><span id="hr-rate-label">Tip-out, percent of tips</span>
            <span class="hint">Enter <span id="hr-rate-unit">%</span>. Use 0 if you don't tip out.</span></label>
          <input type="number" id="hr-rate" inputmode="decimal" min="0" step="0.1" value="20">
        </div>
      </form>

      <div class="calc-result" aria-live="polite">
        <p class="eyebrow">Your real rate</p>
        <p class="headline" id="hr-headline">—</p>
        <p class="headline-sub" id="hr-sub">Enter your hours to see a rate</p>
        <ul class="calc-lines" id="hr-lines">
          <li><span>Gross tips</span><b id="hr-gross">$0.00</b></li>
          <li><span>Tip-out</span><b id="hr-out">$0.00</b></li>
          <li><span>Tips kept</span><b id="hr-net">$0.00</b></li>
          <li><span>Base wage earned</span><b id="hr-wage-earned">$0.00</b></li>
          <li class="total"><span>Total take-home</span><b id="hr-take">$0.00</b></li>
        </ul>
        <p class="calc-warn" id="hr-nohours" hidden>With zero hours there is no rate to
          show. This tool leaves it blank rather than inventing one.</p>
        {PRIVACY_NOTE}
      </div>
    </div>
  </div>
</section>

<section style="padding-top:44px">
  <div class="wrap narrow">
    <div class="prose" style="margin-top:0">
      <h2>Why the number on the job ad is never the number</h2>
      <p>"$35 an hour on a good night" is doing a lot of work in that sentence. It usually
        means gross tips divided by scheduled hours on the best Friday of the month — which
        is three separate exaggerations stacked on top of each other.</p>
      <p>The honest version subtracts what you tipped out, counts the hours you were actually
        there, and looks at a normal night rather than a memorable one.</p>

      <h3>The formula</h3>
      <blockquote><p><strong>real hourly rate = (tips − tip-out + wage × hours) ÷ hours</strong></p></blockquote>
      <p>Three details matter, and this calculator gets all three right because the app does:</p>
      <ul>
        <li><strong>Tip-out comes off first.</strong> Money you hand to the bar is not money
          you earned.</li>
        <li><strong>Hours are actual.</strong> Including the side work and the forty minutes
          after close.</li>
        <li><strong>Zero hours means no rate.</strong> Not a huge number, not zero — nothing.
          A rate with no time behind it is meaningless.</li>
      </ul>

      <h2>Averaging across shifts: do it the right way</h2>
      <p>When you compare weeks or jobs, do not average your per-shift rates. A three-hour
        lunch and a nine-hour Saturday are not equal votes, but averaging their rates treats
        them as if they were, and it will flatter whichever shift was shortest.</p>
      <p>Instead, blend: add up <em>all</em> the take-home, add up <em>all</em> the hours,
        and divide once. That is what Tipfolio does, and it is why the app's number sometimes
        looks lower than the one people carry in their heads.</p>

      <div class="callout">
        <p><strong>The comparison that actually pays.</strong> Once you have a few weeks of
          honest rates, the useful question stops being "what do I make?" and becomes "which
          night is worth picking up?". A Thursday that reliably runs 30% above your average
          is worth more than a raise you have to ask for.</p>
      </div>

      <h2>What to do with the number</h2>
      <ul>
        <li><strong>Compare sections and stations</strong> — patio versus bar, lunch versus dinner.</li>
        <li><strong>Compare jobs</strong> — the higher-volume place is not automatically the better one once its tip-out is in.</li>
        <li><strong>Price your own time</strong> — decide whether a pickup shift beats the alternative.</li>
        <li><strong>Sanity-check a new role</strong> before you leave a known quantity for it.</li>
      </ul>
      <p><a href="/guides/real-hourly-rate/">The full guide to your real hourly rate →</a></p>
      {disclaimer()}
      <h2>Questions</h2>
    </div>
    {faq_html(hr_faq)}
  </div>
</section>

{related([
  ("Tip-out calculator", "/calculators/tip-out/", "Work out what you owe the bar before you work out your rate."),
  ("Shift earnings calculator", "/calculators/shift-earnings/", "Blend a whole week properly, not by averaging averages."),
  ("How to track your tips", "/guides/how-to-track-tips/", "One shift is a data point. A year is evidence."),
])}

{app_cta_band("One shift tells you very little.",
              "Tipfolio computes this on every shift automatically, then shows you the "
              "blended rate by job and by night of the week — from your own log, on your "
              "own phone.")}
"""
    add(Page("/calculators/real-hourly-rate/",
             "Real Hourly Rate Calculator for Tipped Workers",
             "Free calculator for servers and bartenders: tips minus tip-out, plus base "
             "wage, over the hours you actually worked. See what a shift really paid.",
             hourly, og_type="article", page_js=CALC_JS,
             trail=[("Home", "/"), ("Calculators", "/calculators/"), ("Real hourly rate", None)],
             nav="/calculators/", priority="0.8", schema=[faq_schema(hr_faq)]))

    # ================================================== TIP TAX DEDUCTION
    td_faq = [
        ("Is the tip deduction the same as tips being tax free?",
         "No, and the popular name for it is misleading. It is a deduction against tip "
         "income up to an annual cap, not an exemption. If you owe little or no federal "
         "income tax to begin with, a deduction has little or nothing to reduce — which is "
         "why a large share of tipped workers see no benefit from it at all."),
        ("Do mandatory service charges count?",
         "Generally no. An automatic gratuity added to a large party's bill is typically "
         "treated as a service charge and as wages, not as a voluntary tip, so it usually "
         "does not qualify. This is one of the clearest reasons to log your tips and your "
         "auto-grat separately rather than as one number."),
        ("Does my tip-out reduce the tips I can deduct?",
         "Under the approach this estimator uses, yes: what you count is what you actually "
         "kept, after tip-outs paid to other workers. That is why the calculator asks for "
         "both figures. Confirm the treatment for your own arrangement with a tax "
         "professional before you rely on it."),
        ("What records do I need to claim it?",
         "A daily record of your tips, kept as you earn them. The value of a "
         "contemporaneous log is that it was written at the time rather than reconstructed "
         "afterwards, which is precisely what makes it credible. A spreadsheet built in "
         "March from memory is worth far less than a dated entry made on the night."),
        ("Is this estimate reliable?",
         "It is arithmetic on figures you typed, using parameters that are stated on this "
         "page. It is not a tax calculation, does not know your filing status, income, "
         "other deductions or state taxes, and is not advice. Treat it as a way to see the "
         "shape of the thing, then talk to a professional."),
    ]
    deduction = f"""
<section class="article">
  <div class="wrap">
    <div class="article-head">
      <p class="eyebrow green">Free estimator</p>
      <h1>Tip tax deduction estimator</h1>
      <p class="lede">See roughly where your qualified tips land against the
        {TAX['cap_display']} annual cap for {TAX['years']} — and what that could be worth at
        your marginal rate. An illustration from your own numbers, not a tax calculation.</p>
    </div>
  </div>
</section>

<section style="padding-top:30px">
  <div class="wrap">
    <div class="calc" id="calc-deduction" data-cap="{TAX['cap']}"
         data-phaseout-single="{TAX['phaseout_single']}"
         data-phaseout-joint="{TAX['phaseout_joint']}"
         data-phaseout-increment="{TAX['phaseout_increment']}"
         data-phaseout-reduction="{TAX['phaseout_reduction']}">
      <form class="calc-form" onsubmit="return false">
        {NOSCRIPT}
        <div class="field">
          <label>What are you entering?</label>
          <div class="segmented" role="radiogroup" aria-label="Period">
            <label><input type="radio" name="period" value="week" checked><span>Per week</span></label>
            <label><input type="radio" name="period" value="month"><span>Per month</span></label>
            <label><input type="radio" name="period" value="year"><span>Whole year</span></label>
          </div>
        </div>
        <div class="field">
          <label for="td-tips">Tips for that period <span class="hint">Voluntary tips only — leave out mandatory service charges.</span></label>
          <input type="number" id="td-tips" inputmode="decimal" min="0" step="0.01" value="600">
        </div>
        <div class="field">
          <label for="td-tipout">Tip-out you paid, same period <span class="hint">Money passed to bar, bussers and runners.</span></label>
          <input type="number" id="td-tipout" inputmode="decimal" min="0" step="0.01" value="120">
        </div>
        <div class="field" id="td-shifts-field" hidden>
          <label for="td-shifts">Shifts per year</label>
          <input type="number" id="td-shifts" inputmode="decimal" min="0" step="1" value="200">
        </div>
        <div class="field">
          <label>How do you file?</label>
          <div class="segmented" role="radiogroup" aria-label="Filing status">
            <label><input type="radio" name="filing" value="single" checked><span>Single</span></label>
            <label><input type="radio" name="filing" value="joint"><span>Married, jointly</span></label>
          </div>
        </div>
        <div class="field">
          <label for="td-magi">Household income for the year
            <span class="hint">Modified adjusted gross income — everything, not just tips.
              The deduction starts shrinking above {TAX['phaseout_single_display']}
              ({TAX['phaseout_joint_display']} filing jointly). Leave 0 if you are well under.</span></label>
          <input type="number" id="td-magi" inputmode="decimal" min="0" step="1000" value="0">
        </div>
        <div class="field">
          <label for="td-rate">Your marginal federal income tax rate
            <span class="hint">A labelled assumption, not a lookup. If you don't know it, {int(TAX['savings_rate']*100)}% is a common bracket.</span></label>
          <input type="number" id="td-rate" inputmode="decimal" min="0" max="50" step="1" value="{int(TAX['savings_rate']*100)}">
        </div>
      </form>

      <div class="calc-result" aria-live="polite">
        <p class="eyebrow">Potentially deductible</p>
        <p class="headline" id="td-headline">$0</p>
        <p class="headline-sub" id="td-sub">Deductible, based on what you entered.</p>
        <ul class="calc-lines">
          <li><span>Tips for the year</span><b id="td-gross">$0</b></li>
          <li><span>Tip-out paid</span><b id="td-out">$0</b></li>
          <li><span>Qualified tips</span><b id="td-qualified">$0</b></li>
          <li><span>Annual cap (per return)</span><b id="td-cap">$0</b></li>
          <li id="td-phaseout-row" hidden><span>Income phase-out</span><b id="td-phaseout">$0</b></li>
          <li class="total"><span>Illustrative federal income tax saving at <span id="td-rate-echo">22%</span></span><b id="td-saving">$0</b></li>
        </ul>
        <p class="calc-warn" id="td-warn-cap" hidden>You are above the cap. Tips beyond it
          do not add to the deduction — but they still belong in your log.</p>
        <p class="calc-warn" id="td-warn-phaseout" hidden>Your income is above the phase-out
          threshold, so part of the deduction is taken back — $100 for every $1,000 over.</p>
        {PRIVACY_NOTE}
      </div>
    </div>
    {disclaimer("The saving line is an illustration at a rate you chose. It is not a "
                "prediction of your refund, and it ignores your other deductions, "
                "payroll tax and state tax entirely.")}
  </div>
</section>

<section style="padding-top:34px">
  <div class="wrap narrow">
    <div class="keytakeaways">
      <h2>In short</h2>
      <ul>
        <li><span class="tick" style="background:var(--green-tint);color:var(--green)">&#10003;</span><span>It is a <strong>deduction up to {TAX['cap_display']} a year</strong>, available for tax years {TAX['years']} — not a blanket exemption on tips.</span></li>
        <li><span class="tick" style="background:var(--green-tint);color:var(--green)">&#10003;</span><span>Only <strong>voluntary</strong> tips count. Mandatory service charges generally do not.</span></li>
        <li><span class="tick" style="background:var(--green-tint);color:var(--green)">&#10003;</span><span>If you owe little federal income tax, a deduction has little to reduce.</span></li>
        <li><span class="tick" style="background:var(--green-tint);color:var(--green)">&#10003;</span><span>It rests on you having <strong>a daily record</strong> — which is the part almost nobody has.</span></li>
      </ul>
    </div>
    <div class="prose" style="margin-top:0">
      <h2>How this estimate is worked out</h2>
      <ol>
        <li>Your figures are scaled to a year — weekly × 52, monthly × 12, or taken as entered.</li>
        <li>Tip-out is subtracted, giving <strong>qualified tips</strong> — what you actually kept.</li>
        <li>The cap is applied: <code>deductible = min(qualified tips, {TAX['cap_display']})</code>.</li>
        <li>The illustration multiplies the deductible amount by the marginal rate you chose.</li>
      </ol>
      <p>That last step is the one to be most careful with. It is a labelled assumption you
        picked, not a calculation of your actual liability, and your real outcome depends on
        your filing status, your total income, your other deductions and your state.</p>

      <h2>Verify the parameters before you rely on them</h2>
      <p>The cap, the eligible years, the treatment of tip-outs and the exclusion of service
        charges are the four things this estimate rests on. They are stated openly here
        rather than buried, so you can check them: see
        <em>{TAX['citation']}</em> and current IRS guidance, and confirm your own position
        with a qualified tax professional. Rules change; this page is not a substitute for
        the source.</p>

      <h2>The part the estimate can't do for you</h2>
      <p>Whatever the number above says, claiming a deduction on tip income depends on
        substantiation — a daily record of what you earned, kept as you earned it. The
        estimate is the easy half. The log is the half that takes a year, ten seconds at a
        time. <a href="/guides/no-tax-on-tips/">Read the full explainer →</a></p>
      {disclaimer()}
      <h2>Questions</h2>
    </div>
    {faq_html(td_faq)}
  </div>
</section>

{related([
  ("No Tax on Tips, explained", "/guides/no-tax-on-tips/", "What the deduction is, who it helps, and who it doesn't."),
  ("Reporting cash tips", "/guides/reporting-cash-tips/", "What you're required to report, and to whom."),
  ("How to track your tips", "/guides/how-to-track-tips/", "Building the daily record the deduction depends on."),
])}

{app_cta_band("The estimate is the easy part.",
              "Tipfolio tracks the real figure against the cap all year, from entries you "
              "made on the night — and exports the daily record behind it.")}
"""
    add(Page("/calculators/tip-tax-deduction/",
             f"Tip Tax Deduction Calculator ({TAX['years']})",
             "Free estimator for the federal tip deduction. See where your qualified tips "
             "land against the $25,000 annual cap and what it could be worth. Not tax "
             "advice.",
             deduction, og_type="article", page_js=CALC_JS,
             trail=[("Home", "/"), ("Calculators", "/calculators/"), ("Tip tax deduction", None)],
             nav="/calculators/", priority="0.8", schema=[faq_schema(td_faq)]))

    # ================================================== SHIFT EARNINGS
    rows = "".join(f"""
        <div class="field-row" data-shift-row style="align-items:end;grid-template-columns:1fr 1fr 1fr auto;gap:10px">
          <div class="field" style="margin-bottom:10px">
            {'<label for="s-tips-' + str(i) + '">Tips</label>' if i == 1 else ''}
            <input class="s-tips" id="s-tips-{i}" type="number" inputmode="decimal" min="0" step="0.01"
                   placeholder="0" aria-label="Shift {i} tips" value="{v[0]}">
          </div>
          <div class="field" style="margin-bottom:10px">
            {'<label for="s-out-' + str(i) + '">Tip-out</label>' if i == 1 else ''}
            <input class="s-out" id="s-out-{i}" type="number" inputmode="decimal" min="0" step="0.01"
                   placeholder="0" aria-label="Shift {i} tip-out" value="{v[1]}">
          </div>
          <div class="field" style="margin-bottom:10px">
            {'<label for="s-hours-' + str(i) + '">Hours</label>' if i == 1 else ''}
            <input class="s-hours" id="s-hours-{i}" type="number" inputmode="decimal" min="0" step="0.25"
                   placeholder="0" aria-label="Shift {i} hours" value="{v[2]}">
          </div>
          <div style="padding-bottom:20px;min-width:120px;text-align:right">
            <span class="s-result small" style="font-family:var(--display);font-weight:700;color:var(--ink)">—</span>
          </div>
        </div>""" for i, v in enumerate(
            [("240", "48", "7.5"), ("185", "37", "6"), ("310", "62", "8.5"),
             ("", "", ""), ("", "", "")], start=1))

    shift = f"""
<section class="article">
  <div class="wrap">
    <div class="article-head">
      <p class="eyebrow green">Free calculator</p>
      <h1>Shift earnings calculator</h1>
      <p class="lede">Add up a week of shifts with base wage and tip-outs handled properly,
        and get the blended rate across all of them — not an average of averages.</p>
    </div>
  </div>
</section>

<section style="padding-top:30px">
  <div class="wrap">
    <div class="calc" id="calc-shift">
      <form class="calc-form" onsubmit="return false">
        {NOSCRIPT}
        <div class="field">
          <label for="se-wage">Base hourly wage <span class="hint">Applied to every shift below. Enter 0 if you have none.</span></label>
          <input type="number" id="se-wage" inputmode="decimal" min="0" step="0.01" value="7.25">
        </div>
        <p class="eyebrow green" style="margin:22px 0 10px">Your shifts</p>
        {rows}
      </form>

      <div class="calc-result" aria-live="polite">
        <p class="eyebrow">Total take-home</p>
        <p class="headline" id="se-headline">$0.00</p>
        <p class="headline-sub" id="se-sub">Fill in a shift to see your total</p>
        <ul class="calc-lines">
          <li><span>Tips kept, after tip-out</span><b id="se-net">$0.00</b></li>
          <li><span>Base wage earned</span><b id="se-wage-earned">$0.00</b></li>
          <li><span>Hours worked</span><b id="se-hours">0 h</b></li>
          <li class="total"><span>Blended real rate</span><b id="se-rate">—</b></li>
        </ul>
        {PRIVACY_NOTE}
      </div>
    </div>
  </div>
</section>

<section style="padding-top:44px">
  <div class="wrap narrow">
    <div class="prose" style="margin-top:0">
      <h2>Why "blended" and not "average"</h2>
      <p>If you take the rate from each shift and average those rates, a two-hour lunch
        counts exactly as much as a ten-hour Saturday. That is almost never what you want,
        and it systematically flatters short shifts — which tend to look better per hour
        because the slow first hour is a smaller share of them.</p>
      <p>The blended rate adds all the take-home, adds all the hours, and divides once:</p>
      <blockquote><p><strong>blended rate = total take-home ÷ total hours</strong></p></blockquote>
      <p>It is the number that answers "what does a week of this job actually pay me per
        hour of my life", which is the question worth asking.</p>

      <h2>What counts as take-home here</h2>
      <table>
        <thead><tr><th>Line</th><th>What it means</th></tr></thead>
        <tbody>
          <tr><td>Tips</td><td>Everything you were tipped, cash and card, before anything comes out.</td></tr>
          <tr><td>Tip-out</td><td>What you handed to bar, bussers, runners and hosts. Capped at your tips.</td></tr>
          <tr><td>Base wage earned</td><td>Your cash wage × the hours on that shift.</td></tr>
          <tr><td><strong>Take-home</strong></td><td><strong>Tips kept + base wage earned.</strong></td></tr>
        </tbody>
      </table>
      <p>Note what is deliberately <em>not</em> here: taxes, withholding and payroll
        deductions. This is gross take-home from the shift, which is the right basis for
        comparing shifts against each other. What lands in your account after withholding is
        a separate question and depends on your whole tax picture.</p>

      <div class="callout">
        <p><strong>Use it to answer a real question.</strong> Enter a typical week from one
          job, then a typical week from another. The blended rate is the only fair way to
          compare them once tip-outs, base wages and shift lengths all differ — and it is
          often not the answer people expect.</p>
      </div>

      <h2>A week is a sample, not the truth</h2>
      <p>One week tells you about that week. Seasonality, section assignment, the weather and
        one big party can move a week's blended rate by a third. If you are making a
        decision — taking a job, dropping a shift, asking for a section — you want months,
        not days. That is the case for logging as you go rather than reconstructing later.
        <a href="/guides/how-to-track-tips/">How to keep that record →</a></p>
      {disclaimer()}
    </div>
  </div>
</section>

{related([
  ("Real hourly rate calculator", "/calculators/real-hourly-rate/", "One shift, in detail, with the tip-out rule applied."),
  ("Tip-out calculator", "/calculators/tip-out/", "Work out the tip-out figure to put in the rows above."),
  ("Proof of income for tipped workers", "/guides/proof-of-income-for-tipped-workers/", "Turning weeks like these into something a landlord accepts."),
])}

{app_cta_band("Five rows is a week. Tipfolio holds the year.",
              "Log each shift as it happens and the blended rate, the weekday pattern and "
              "the annual totals come free — from your own entries, on your own phone.")}
"""
    add(Page("/calculators/shift-earnings/",
             "Shift Earnings Calculator for Servers & Bartenders",
             "Add up a week of shifts with tip-outs and base wage handled properly, and "
             "see the blended hourly rate across all of them. Free, and nothing leaves "
             "your browser.",
             shift, og_type="article", page_js=CALC_JS,
             trail=[("Home", "/"), ("Calculators", "/calculators/"), ("Shift earnings", None)],
             nav="/calculators/", priority="0.8"))
