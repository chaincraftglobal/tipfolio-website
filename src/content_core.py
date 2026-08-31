"""Home, features, pricing, about."""
from build import (Page, add, TAX, BRAND, cta, disclaimer, app_cta_band,
                   related, SITE)


def shot(name, alt, title, caption):
    return f"""<figure style="margin:0">
  <div class="phone">
    <picture><source srcset="/assets/img/{name}.webp" type="image/webp">
      <img src="/assets/img/{name}.jpg" width="860" height="1869" loading="lazy" alt="{alt}"></picture>
  </div>
  <figcaption class="shot-caption"><strong>{title}</strong><span>{caption}</span></figcaption>
</figure>"""


APP_SCHEMA = ('{"@context":"https://schema.org","@type":"SoftwareApplication",'
              '"name":"Tipfolio","applicationCategory":"FinanceApplication",'
              '"operatingSystem":"iOS 17.0 or later",'
              '"description":"Tip tracking and tax record-keeping for tipped workers. '
              'Log a shift in ten seconds, see your real hourly rate, and build the '
              'contemporaneous daily record the IRS expects \\u2014 stored on your iPhone.",'
              '"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},'
              '"author":{"@type":"Organization","name":"Lacewing Technologies LLC"}}')


def build():
    # ---------------------------------------------------------------- HOME
    home = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow green">For servers, bartenders, baristas &amp; barbers</p>
      <h1>Log tips.<br>Keep the record.</h1>
      <p class="lede">
        Tipfolio is the tip log for people who actually work for tips. Log a shift in
        about ten seconds, see what you really made, and walk into tax season with the
        daily record the IRS expects — already written.
      </p>
      <div class="hero-actions">
        {cta()}
        <a class="btn btn-ghost" href="/calculators/">Try the free calculators</a>
      </div>
      <p class="hero-note">iPhone · Free to log, forever · No account required</p>
    </div>
    <div>
      <div class="phone">
        <picture>
          <source srcset="/assets/img/01-home.webp" type="image/webp">
          <img src="/assets/img/01-home.jpg" width="860" height="1869" fetchpriority="high"
               alt="The Tipfolio home screen showing tonight's shift, take-home total and real hourly rate.">
        </picture>
      </div>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><div class="figure">10 seconds</div>
        <div class="label">To log a shift, with your job, wage, hours and tip-out already filled in.</div></div>
      <div class="stat"><div class="figure">0 servers</div>
        <div class="label">Hold your earnings. There is no Tipfolio backend for your money — nowhere else for it to be.</div></div>
      <div class="stat"><div class="figure">{TAX['cap_display']}</div>
        <div class="label">The annual cap on the federal tip deduction for {TAX['years']} — if you keep a daily log.</div></div>
    </div>
  </div>
</section>

<section id="deduction" style="padding-top:0">
  <div class="wrap">
    <div class="band">
      <div class="band-grid">
        <div>
          <p class="eyebrow">New for {TAX['years']}</p>
          <p class="band-figure">{TAX['cap_display']}</p>
          <h2 style="margin-top:10px">of your tips can come off your federal taxes</h2>
          <p style="margin-top:14px">
            — if you keep a daily log. That is the whole catch, and it is the whole
            reason Tipfolio exists. Every entry is timestamped as you make it, which is
            what turns a pile of numbers into a contemporaneous daily record.
          </p>
          <p style="margin-top:18px"><a href="/guides/no-tax-on-tips/" style="color:var(--amber);font-weight:600">
            Read the full explainer →</a></p>
        </div>
        <div>
          <ul class="band-list">
            <li><span class="tick">&#10003;</span><span>Watch your qualified tips add up against the annual cap all year.</span></li>
            <li><span class="tick">&#10003;</span><span>Check your W-2 against your own log before you file.</span></li>
            <li><span class="tick">&#10003;</span><span>Export a filing-ready daily report as PDF or CSV, with the entry timestamp on every shift.</span></li>
            <li><span class="tick">&#10003;</span><span>Only voluntary tips qualify — mandatory service charges do not, and Tipfolio says so.</span></li>
          </ul>
        </div>
      </div>
    </div>
    {disclaimer("Figures shown are potential deductions derived from your own records, never a guaranteed saving.")}
  </div>
</section>

<section id="how">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow green">How it works</p>
      <h2>Three things, done properly.</h2>
      <p>No dashboards you'll never open. Tipfolio does the small number of things a
         tipped worker actually needs, and does them honestly.</p>
    </div>
    <div class="grid grid-3">
      <div class="card">
        <div class="icon-dot" aria-hidden="true">
          <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
        </div>
        <h3>The ten-second habit</h3>
        <p>Open the app, type tonight's tips, done. Your job, wage, hours and tip-out are
           already filled in from last time. The nightly reminder lands at 11:30 PM and
           opens straight onto the keypad.</p>
      </div>
      <div class="card">
        <div class="icon-dot" aria-hidden="true">
          <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 19V10M10 19V5M16 19v-6M22 19H2"/></svg>
        </div>
        <h3>What you really make</h3>
        <p>Tips, minus tip-outs, plus your base wage, divided by the hours you actually
           worked. That is your <a href="/guides/real-hourly-rate/">real hourly rate</a> —
           per shift, per job, per night of the week.</p>
      </div>
      <div class="card">
        <div class="icon-dot amber" aria-hidden="true">
          <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 14h6M9 17h4"/></svg>
        </div>
        <h3>Built for tax season</h3>
        <p>Your log becomes an IRS-ready daily report, a W-2 reconciliation, and an
           <a href="/guides/proof-of-income-for-tipped-workers/">income statement</a> a
           landlord or lender will accept — timestamped on every line.</p>
      </div>
    </div>
    <p style="margin-top:26px"><a href="/features/" class="btn btn-ghost">See every feature</a></p>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="shots">
      {shot("02-insights", "Insights screen with a bar chart of average take-home by weekday.", "Insights", "Know which nights actually pay.")}
      {shot("03-taxes", "Tax Center showing qualified tips tracked against the annual deduction cap.", "Tax Center", "Watch your deduction add up.")}
      {shot("05-taxreport", "Tax report export screen listing each shift with the time it was entered.", "Tax report", "Filing-ready. Timestamped.")}
      {shot("06-settings", "Tipfolio settings screen, footed by the line: your earnings never leave this iPhone.", "Settings", "Your earnings never leave this iPhone.")}
    </div>
  </div>
</section>

<section id="tools">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow green">Free, no download</p>
      <h2>Run the numbers right now.</h2>
      <p>Four calculators built on the same maths the app uses. Everything happens in your
         browser — nothing you type is sent anywhere.</p>
    </div>
    <div class="grid grid-2">
      <a class="link-card" href="/calculators/real-hourly-rate/">
        <span class="kicker">Most popular</span>
        <h3>Real hourly rate calculator</h3>
        <p>Tips minus tip-outs, plus base wage, over the hours you actually worked. The one
           honest number about your shift.</p>
        <span class="more">Calculate →</span>
      </a>
      <a class="link-card" href="/calculators/tip-out/">
        <span class="kicker">Nightly</span>
        <h3>Tip-out calculator</h3>
        <p>Percent of tips, percent of sales, or a flat amount — work out what you owe the
           bar, the busser and the runner.</p>
        <span class="more">Calculate →</span>
      </a>
      <a class="link-card" href="/calculators/tip-tax-deduction/">
        <span class="kicker">Tax season</span>
        <h3>Tip tax deduction estimator</h3>
        <p>See where your qualified tips land against the {TAX['cap_display']} annual cap,
           and what that could mean at your marginal rate.</p>
        <span class="more">Estimate →</span>
      </a>
      <a class="link-card" href="/calculators/shift-earnings/">
        <span class="kicker">Per shift</span>
        <h3>Shift earnings calculator</h3>
        <p>Total take-home for one shift or a whole week, with base wage and tip-out
           handled properly.</p>
        <span class="more">Calculate →</span>
      </a>
    </div>
  </div>
</section>

<section id="roles" style="background:var(--bg-outer)">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow green">Who it's for</p>
      <h2>Different jobs, different money.</h2>
      <p>A server's tip-out is nothing like a booth renter's chair rent, and a delivery fee
         is not a tip at all. Start with what applies to you.</p>
    </div>
    <div class="grid grid-3">
      <a class="link-card" href="/for/servers/"><h3>Servers &amp; waitstaff</h3>
        <p>The most complicated tip-out in the building, plus auto-grats and side work.</p>
        <span class="more">Read →</span></a>
      <a class="link-card" href="/for/bartenders/"><h3>Bartenders</h3>
        <p>On both sides of the tip-out, cash-heavy, and shifts that cross midnight.</p>
        <span class="more">Read →</span></a>
      <a class="link-card" href="/for/baristas/"><h3>Baristas &amp; café staff</h3>
        <p>Pooled tips split by hours — small per shift, substantial per year.</p>
        <span class="more">Read →</span></a>
      <a class="link-card" href="/for/delivery-drivers/"><h3>Delivery drivers</h3>
        <p>Tips versus fees versus promotions, and the vehicle costs behind all three.</p>
        <span class="more">Read →</span></a>
      <a class="link-card" href="/for/hairstylists/"><h3>Hairstylists &amp; barbers</h3>
        <p>Commission or chair rent — two different tax positions with one job title.</p>
        <span class="more">Read →</span></a>
      <a class="link-card" href="/guides/"><h3>Everyone else</h3>
        <p>Hotel staff, casino dealers, valets, tattoo artists — the guides cover the rules
           that apply across tipped work.</p>
        <span class="more">All guides →</span></a>
    </div>
  </div>
</section>

<section id="privacy">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center;gap:clamp(28px,4vw,64px)">
      <div>
        <p class="eyebrow green">Private by design</p>
        <h2>This is the product, not a feature.</h2>
        <p class="lede" style="margin-top:16px">
          Your shifts, tips, wages and tax totals live on your iPhone. Tipfolio has no
          server for your earnings — there is nowhere else for them to be.
        </p>
        <p style="margin-top:18px"><a href="/privacy/">Read the privacy policy →</a></p>
      </div>
      <div class="card">
        <ul class="privacy-list">
          <li><span class="tick">&#10003;</span><span>No account required. Every feature works signed out.</span></li>
          <li><span class="tick">&#10003;</span><span>No ads, no analytics, no trackers, no data selling — ever.</span></li>
          <li><span class="tick">&#10003;</span><span>Zero third-party SDKs. The app contains no networking code for your earnings at all.</span></li>
          <li><span class="tick">&#10003;</span><span>Receipt scanning reads your closeout slip using your iPhone's own text recognition. The photo never leaves the device.</span></li>
          <li><span class="tick">&#10003;</span><span>Encrypted backup to your <em>own</em> private iCloud is optional and off unless you turn it on. The key lives in your iCloud Keychain.</span></li>
          <li><span class="tick">&#10003;</span><span>Export everything as CSV at any time, free. Delete everything in three taps.</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section id="pricing">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow green">Pricing</p>
      <h2>Free to log. Pro to file.</h2>
      <p>Logging, insights and the nightly reminder are free, forever. Pro exists for the
         two weeks a year you need paperwork.</p>
    </div>
    <div class="grid grid-2">
      <div class="card plan">
        <span class="badge" style="background:var(--green-tint);color:var(--green)">Free</span>
        <p class="plan-price" style="margin-top:14px">$0<span> / forever</span></p>
        <ul>
          <li><span class="tick">&#10003;</span><span>Unlimited shift logging</span></li>
          <li><span class="tick">&#10003;</span><span>Real hourly rate and weekday insights</span></li>
          <li><span class="tick">&#10003;</span><span>Nightly 11:30 PM reminder</span></li>
          <li><span class="tick">&#10003;</span><span>One job</span></li>
          <li><span class="tick">&#10003;</span><span>Full CSV export of everything you've logged</span></li>
        </ul>
      </div>
      <div class="card plan featured">
        <span class="badge">Tipfolio Pro · {BRAND['trial']}</span>
        <p class="plan-price" style="margin-top:14px">{BRAND['price_monthly']}<span> / month</span></p>
        <p class="small" style="margin-top:4px">or {BRAND['price_annual']} / year</p>
        <ul>
          <li><span class="tick">&#10003;</span><span>AI closeout scan — log a shift in two seconds</span></li>
          <li><span class="tick">&#10003;</span><span>IRS-ready tax report (PDF + CSV)</span></li>
          <li><span class="tick">&#10003;</span><span>W-2 reconciliation and occupation code</span></li>
          <li><span class="tick">&#10003;</span><span>Unlimited jobs and income-proof statements</span></li>
        </ul>
        <p class="small" style="margin-top:20px">
          Billed through your Apple Account. Renews automatically unless cancelled at least
          24 hours before the period ends. <a href="/pricing/">Full pricing detail →</a>
        </p>
      </div>
    </div>
  </div>
</section>

<section id="faq">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow green">FAQ</p>
      <h2>Questions worth asking.</h2>
    </div>
    <div class="faq">
      <details><summary>Does Tipfolio work offline?</summary>
        <p>Yes — everything is stored on your phone. You can log shifts with zero signal; nothing needs a server.</p></details>
      <details><summary>Will this really lower my taxes?</summary>
        <p>If you owe federal income tax, tips you log here count toward the No Tax on Tips deduction — up to {TAX['cap_display']}/year for {TAX['years']}. Your daily log is the record the IRS expects. <a href="/guides/no-tax-on-tips/">Read the full explainer.</a></p></details>
      <details><summary>What if I don't owe federal tax?</summary>
        <p>About a third of tipped workers don't. Tipfolio still shows your real hourly rate and builds income-proof statements for apartments, loans, and visas.</p></details>
      <details><summary>What happens in an audit?</summary>
        <p>Your export includes every shift with its date and the time it was entered — a contemporaneous daily record, which is exactly what the IRS asks for.</p></details>
      <details><summary>How do I cancel?</summary>
        <p>Settings → Subscription → Cancel. It runs through Apple, takes about 10 seconds, and your data stays yours — export is always free.</p></details>
    </div>
    {disclaimer()}
  </div>
</section>

{app_cta_band()}
"""

    add(Page(
        "/", "Tipfolio — Tip Tracker & Tax Record for Tipped Workers",
        "Log a shift in ten seconds, see your real hourly rate, and build the daily "
        "record the IRS expects. A free iPhone tip tracker that keeps your earnings "
        "on your phone.",
        home, og_title="Tipfolio — Log tips. Keep the record.",
        priority="1.0",
        schema=[APP_SCHEMA],
    ))

    # ------------------------------------------------------------ FEATURES
    features = f"""
<section class="article">
  <div class="wrap">
    <div class="article-head">
      <p class="eyebrow green">Features</p>
      <h1>Everything Tipfolio does, and why.</h1>
      <p class="lede">Tipfolio is deliberately small. Every screen below exists because a
        tipped worker needs it in a specific moment — closing out, picking up a shift,
        filing a return, or proving what they earn.</p>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center;gap:clamp(28px,4vw,64px)">
      <div>
        <p class="eyebrow green">Logging</p>
        <h2>Ten seconds, or it doesn't get done.</h2>
        <p class="lede" style="margin-top:16px">Every tip-tracking app dies the same way:
          it asks for too much at 1 AM. Tipfolio opens straight onto a custom keypad with
          your job, wage, hours and tip-out rule already filled in from last time.</p>
        <ul class="privacy-list" style="margin-top:22px">
          <li><span class="tick">&#10003;</span><span>Big one-thumb keys, well above the 44pt minimum — not the system keyboard.</span></li>
          <li><span class="tick">&#10003;</span><span>A live "≈ $/hr" readout as you type, so you see the shift's real rate before you save.</span></li>
          <li><span class="tick">&#10003;</span><span>Cash/card split on a slider. The two always sum to exactly what you typed.</span></li>
          <li><span class="tick">&#10003;</span><span>Overnight shifts handled properly — an end time before the start means it crossed midnight.</span></li>
          <li><span class="tick">&#10003;</span><span>A nightly reminder at 11:30 PM that opens directly into the keypad, and softens itself if you already logged.</span></li>
        </ul>
      </div>
      <div class="phone"><picture><source srcset="/assets/img/01-home.webp" type="image/webp">
        <img src="/assets/img/01-home.jpg" width="860" height="1869" loading="lazy"
             alt="Tipfolio home screen showing the shift log and take-home totals."></picture></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center;gap:clamp(28px,4vw,64px)">
      <div class="phone" style="order:2"><picture><source srcset="/assets/img/02-insights.webp" type="image/webp">
        <img src="/assets/img/02-insights.jpg" width="860" height="1869" loading="lazy"
             alt="Insights screen: real hourly rate, average by night, and the best shift."></picture></div>
      <div style="order:1">
        <p class="eyebrow green">Insights</p>
        <h2>Which nights are actually worth it.</h2>
        <p class="lede" style="margin-top:16px">Everything is computed on your device from
          your own shifts. There is no model, no server, and no guessing — where there isn't
          enough evidence for a claim, Tipfolio hides the card rather than filling it with a
          number it can't stand behind.</p>
        <ul class="privacy-list" style="margin-top:22px">
          <li><span class="tick">&#10003;</span><span>Your <a href="/guides/real-hourly-rate/">true hourly rate</a>, blended correctly across shifts — not an average of averages.</span></li>
          <li><span class="tick">&#10003;</span><span>Average take-home by night of the week, so "Thursdays are your money nights" is a fact, not a feeling.</span></li>
          <li><span class="tick">&#10003;</span><span>Month-over-month trend compared like for like: this month to date against the same days of last month.</span></li>
          <li><span class="tick">&#10003;</span><span>Every suggestion shows its evidence — "from your last 32 shifts, computed on-device".</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center;gap:clamp(28px,4vw,64px)">
      <div>
        <p class="eyebrow green">Tax Center</p>
        <h2>The record, not just the total.</h2>
        <p class="lede" style="margin-top:16px">A pile of numbers is not a tax record. What
          makes a log credible is that each entry was made at the time — and that any later
          correction is visible rather than painted over.</p>
        <ul class="privacy-list" style="margin-top:22px">
          <li><span class="tick">&#10003;</span><span>Qualified tips tracked against the {TAX['cap_display']} annual cap, with raw and capped figures shown separately.</span></li>
          <li><span class="tick">&#10003;</span><span>A tax-year switcher — all figures and exports scope to the year you pick.</span></li>
          <li><span class="tick">&#10003;</span><span>W-2 reconciliation with a ±2% tolerance, so you check your employer's number against your own before you file.</span></li>
          <li><span class="tick">&#10003;</span><span>Your Treasury Tipped Occupation Code, surfaced where you need it.</span></li>
          <li><span class="tick">&#10003;</span><span>Entries made long after the shift are <em>flagged</em>, not hidden. An honest record survives scrutiny; a tidy one doesn't.</span></li>
        </ul>
      </div>
      <div class="phone"><picture><source srcset="/assets/img/03-taxes.webp" type="image/webp">
        <img src="/assets/img/03-taxes.jpg" width="860" height="1869" loading="lazy"
             alt="Tax Center showing qualified tips against the annual deduction cap."></picture></div>
    </div>
    {disclaimer()}
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head"><p class="eyebrow green">And the rest</p>
      <h2>The parts you'll need twice a year.</h2></div>
    <div class="grid grid-3">
      <div class="card"><h3>Closeout scan</h3>
        <p>Point the camera at your register slip and the shift fills itself in. Recognition
           runs on your iPhone with Apple's Vision framework — the photo is never uploaded,
           and is discarded once parsed. Every field it read is shown editable, next to the
           line it came from, with low-confidence values marked. It never saves silently.</p></div>
      <div class="card"><h3>Exports that hold up</h3>
        <p>A filing-ready daily report as PDF or CSV, with the entry timestamp on every
           line, the year's summary, the cap stated alongside the deductible figure, and the
           disclaimer on the document itself. A full year paginates rather than clipping.</p></div>
      <div class="card"><h3>Proof of income</h3>
        <p>A clean statement for any period — total earnings, monthly average, shift count,
           hours and average rate — for landlords, lenders and visa applications. Labelled
           as self-reported, because that is what it is.</p></div>
      <div class="card"><h3>Multiple jobs</h3>
        <p>Two restaurants and a catering gig, each with its own wage and tip-out rule, all
           aggregating into one tax year. Delete a job and its shifts survive, keeping the
           job name they were logged under.</p></div>
      <div class="card"><h3>Encrypted backup</h3>
        <p>Optional, off by default. An AES-GCM archive written to <em>your</em> iCloud
           Drive, with the key in <em>your</em> iCloud Keychain. Restores carry your original
           entry timestamps across exactly — a restore that re-stamped them would quietly
           downgrade your record.</p></div>
      <div class="card"><h3>Accessibility</h3>
        <p>Full Dynamic Type support up to the largest sizes, VoiceOver labels on every
           control, an audio-graph description of the weekday chart, and status never
           conveyed by colour alone.</p></div>
    </div>
  </div>
</section>

{app_cta_band("Free to log. Forever.",
              "Logging, insights and the nightly reminder cost nothing and always will. "
              "Pro is there for the fortnight a year you need paperwork.")}
"""

    add(Page(
        "/features/", "Features — Tipfolio Tip Tracker for iPhone",
        "Every Tipfolio feature: ten-second shift logging, real hourly rate insights, "
        "the Tax Center, on-device closeout scanning, exports, and encrypted backup.",
        features, trail=[("Home", "/"), ("Features", None)],
        nav="/features/", priority="0.9",
    ))

    # ------------------------------------------------------------- PRICING
    pricing = f"""
<section class="article">
  <div class="wrap">
    <div class="article-head">
      <p class="eyebrow green">Pricing</p>
      <h1>Free to log. Pro to file.</h1>
      <p class="lede">The habit is the product, and habits can't cost money — so logging is
        free forever, for everyone. Pro exists for the fortnight a year you need paperwork
        out of the app.</p>
    </div>
  </div>
</section>

<section style="padding-top:34px">
  <div class="wrap">
    <div class="grid grid-2">
      <div class="card plan">
        <span class="badge" style="background:var(--green-tint);color:var(--green)">Free</span>
        <p class="plan-price" style="margin-top:14px">$0<span> / forever</span></p>
        <p class="small" style="margin-top:6px">No account. No trial clock. No card.</p>
        <ul>
          <li><span class="tick">&#10003;</span><span>Unlimited shift logging, offline</span></li>
          <li><span class="tick">&#10003;</span><span>Real hourly rate, per shift and blended</span></li>
          <li><span class="tick">&#10003;</span><span>Average-by-night insights and best-shift</span></li>
          <li><span class="tick">&#10003;</span><span>Nightly 11:30 PM reminder and weekly summary</span></li>
          <li><span class="tick">&#10003;</span><span>Tax Center: qualified tips tracked against the cap</span></li>
          <li><span class="tick">&#10003;</span><span>One job</span></li>
          <li><span class="tick">&#10003;</span><span>Full CSV export of everything you have logged</span></li>
          <li><span class="tick">&#10003;</span><span>Optional encrypted iCloud backup</span></li>
        </ul>
      </div>
      <div class="card plan featured">
        <span class="badge">Tipfolio Pro · {BRAND['trial']}</span>
        <p class="plan-price" style="margin-top:14px">{BRAND['price_monthly']}<span> / month</span></p>
        <p class="small" style="margin-top:6px">or {BRAND['price_annual']} / year — about {BRAND['price_annual']} for the whole tax year</p>
        <ul>
          <li><span class="tick">&#10003;</span><span>Everything in Free</span></li>
          <li><span class="tick">&#10003;</span><span>AI closeout scan — log a shift in two seconds</span></li>
          <li><span class="tick">&#10003;</span><span>IRS-ready tax report, PDF and CSV</span></li>
          <li><span class="tick">&#10003;</span><span>W-2 reconciliation and occupation code</span></li>
          <li><span class="tick">&#10003;</span><span>Income-proof statements for any period</span></li>
          <li><span class="tick">&#10003;</span><span>Unlimited jobs</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap narrow">
    <div class="prose" style="margin-top:0">
      <h2>What happens when Pro ends</h2>
      <p>Nothing happens to your data. Not one shift is deleted, hidden or locked. Your log,
        your history and your insights stay exactly as they were, and <strong>CSV export
        stays free</strong> — so you can always take everything with you. What stops is the
        scan, the formatted tax report, the income-proof statement and extra jobs.</p>
      <p>This is deliberate. An app that holds your own earnings hostage to a subscription
        is not a record-keeping tool, it is a hostage situation.</p>

      <h2>How billing works</h2>
      <ul>
        <li>Subscriptions are sold and billed by <strong>Apple</strong>, through In-App
          Purchase. We never see or handle your card.</li>
        <li>Both plans start with a {BRAND['trial']}. Cancel at any point during it and you
          are not charged.</li>
        <li>Subscriptions renew automatically unless cancelled at least 24 hours before the
          end of the period.</li>
        <li>Cancel from <em>Settings → Subscription</em> in the app, which links straight to
          Apple's subscription settings — or from iOS Settings directly. We never obstruct
          that path.</li>
        <li>Refunds are handled by Apple at
          <a href="https://reportaproblem.apple.com" rel="noopener">reportaproblem.apple.com</a>.</li>
      </ul>
      <p>Prices shown are in US dollars and may differ by territory. The price and trial
        length shown on the purchase screen at the time you buy are the ones that apply.
        Full detail in the <a href="/terms/">terms of service</a>.</p>

      <h2>Why not free with ads?</h2>
      <p>Because an advertising business needs to know things about you, and the entire point
        of Tipfolio is that it knows nothing about you. There is no server holding your
        earnings, no analytics, and no third-party SDK — which means there is no version of
        this app that can be paid for with attention instead of money.
        <a href="/privacy/">That is a property of how it is built</a>, and a subscription is
        what keeps it that way.</p>
    </div>
    {disclaimer()}
  </div>
</section>

{app_cta_band("Start free. Decide in April.",
              "Log all year for nothing. If the report is worth "
              + BRAND['price_annual'] + " when you file, it will still be there.")}
"""

    add(Page(
        "/pricing/", "Pricing — Tipfolio Pro for iPhone",
        "Tipfolio is free to log forever. Pro is $3.99 a month or $29.99 a year with a "
        "7-day free trial, and unlocks scanning, tax reports and income proof.",
        pricing, trail=[("Home", "/"), ("Pricing", None)],
        nav="/pricing/", priority="0.9",
    ))

    # --------------------------------------------------------------- ABOUT
    about = f"""
<section class="article">
  <div class="wrap narrow">
    <div class="article-head">
      <p class="eyebrow green">About</p>
      <h1>Built for the people the paperwork forgets.</h1>
      <p class="lede">Tipfolio came out of a specific, unglamorous problem: the tax break
        that helps tipped workers most is the one that is hardest for them to actually
        claim.</p>
    </div>
    <div class="prose">
      <h2>The problem</h2>
      <p>A deduction on tip income is worth real money to someone making most of it in cash
        and card tips. But claiming it properly depends on something almost nobody has: a
        <em>contemporaneous daily record</em> — a log written as the money was earned, not
        reconstructed from memory in March.</p>
      <p>Most tipped workers keep that record in a notes app, a shoebox, or not at all. Not
        through carelessness. Because at 1 AM after a double, filling in a spreadsheet is
        the last thing that is going to happen.</p>

      <h2>The design constraint</h2>
      <p>So the whole app is built around one number: <strong>ten seconds</strong>. If
        logging a shift takes longer than that, the habit dies, and without the habit there
        is no record and no deduction. Everything else — the pre-filled defaults, the custom
        keypad, the reminder that opens straight into it — exists to protect that number.</p>
      <blockquote><p>A year of ten-second entries <em>is</em> the record. That is the
        entire product.</p></blockquote>

      <h2>Why there is no server</h2>
      <p>An app holding a year of someone's undeclared-feeling income is holding something
        sensitive. The safest architecture for that data is the one where we never have it.</p>
      <p>So Tipfolio has no backend for your earnings. Not "we don't look at it" — there is
        no networking code in the app that could send it. No analytics, no crash reporting,
        no third-party SDKs, no advertising identifiers. The optional iCloud backup is
        encrypted on your device with a key held in your own iCloud Keychain, so even the
        copy in the cloud is one we could not read if we were compelled to.</p>
      <p>That decision costs us things. We cannot see how the app is used, cannot debug from
        telemetry, and cannot build a growth loop out of your data. We think that is the
        correct trade for this particular product.
        <a href="/privacy/">The privacy policy spells out exactly what that means.</a></p>

      <h2>Honesty about numbers</h2>
      <p>Money apps are unusually tempting to lie with. A rate looks better if you ignore
        tip-outs; a trend looks dramatic if you compare a partial month to a whole one; an
        insight looks smart if you generate it from four shifts.</p>
      <p>Tipfolio refuses all three. Where there is not enough evidence for a claim, the
        card is hidden rather than filled with a guess. Where a figure can't be computed, it
        shows a dash rather than a zero. And tax figures are always framed as potential
        deductions derived from your own records — never as a promised saving.</p>

      <h2>Who makes it</h2>
      <p>Tipfolio is built by <strong>{BRAND['entity']}</strong>, a small independent
        software company. It is not venture funded, does not sell data, and has no growth
        target that depends on you doing anything other than logging your shifts.</p>
      <p>If something is wrong, or the app misses something your job needs, write to
        <a href="mailto:{BRAND['email']}">{BRAND['email']}</a>. A person reads it.</p>
      <p class="small">{BRAND['entity']} · {BRAND['address']}</p>
    </div>
    {disclaimer()}
  </div>
</section>

{app_cta_band()}
"""

    add(Page(
        "/about/", "About Tipfolio — Why we built a tip log with no server",
        "Tipfolio exists because the tax break that helps tipped workers most is the "
        "hardest to claim. Here is the ten-second design constraint, and why there is no "
        "backend.",
        about, trail=[("Home", "/"), ("About", None)], priority="0.6",
    ))
