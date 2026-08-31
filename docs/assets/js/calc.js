/* ==========================================================================
   Tipfolio calculators.

   Ported from Tipfolio/Services/TipCalculator.swift and TaxEngine.swift so the
   web tools and the app agree to the cent. Rules carried across deliberately:

     * A tip-out can never exceed the tips earned, nor be negative.
     * A percent-of-sales rule with no sales figure yields zero, not a guess.
     * Net tips never go below zero.
     * A rate with zero hours is not shown at all, rather than shown as a
       divide-by-zero artefact or an inflated number.

   Everything runs in the browser. Nothing typed here is sent anywhere.
   ========================================================================== */
(function () {
  'use strict';

  // Money is held in cents as integers, so a night of arithmetic cannot drift
  // the way repeated float addition does. The app uses Decimal for the same
  // reason (see Decimal+Exact.swift).
  function cents(v) { return Math.round((parseFloat(v) || 0) * 100); }
  function num(v) { var n = parseFloat(v); return isFinite(n) ? n : 0; }

  function money(c, dp) {
    if (dp === undefined) dp = 2;
    return '$' + (c / 100).toLocaleString('en-US', {
      minimumFractionDigits: dp, maximumFractionDigits: dp
    });
  }
  function money0(c) { return money(c, 0); }

  function val(id) { var el = document.getElementById(id); return el ? el.value : ''; }
  function set(id, text) { var el = document.getElementById(id); if (el) el.textContent = text; }
  function show(id, on) { var el = document.getElementById(id); if (el) el.hidden = !on; }
  function checked(name) {
    var el = document.querySelector('input[name="' + name + '"]:checked');
    return el ? el.value : null;
  }

  /* --- TipCalculator.tipOut ---------------------------------------------- */
  function tipOutCents(basis, value, grossC, salesC) {
    if (!(value > 0)) return 0;
    var raw = 0;
    if (basis === 'tips')       raw = grossC * value / 100;
    else if (basis === 'sales') { if (!(salesC > 0)) return 0; raw = salesC * value / 100; }
    else                        raw = cents(value);
    raw = Math.round(raw);
    return Math.min(Math.max(0, raw), Math.max(0, grossC));   // never exceeds tips
  }

  function bind(ids, fn) {
    ids.forEach(function (id) {
      var el = document.getElementById(id);
      if (el) { el.addEventListener('input', fn); el.addEventListener('change', fn); }
    });
    document.querySelectorAll('input[type="radio"]').forEach(function (el) {
      el.addEventListener('change', fn);
    });
    fn();
  }

  /* ======================= 1. Tip-out calculator ========================= */
  if (document.getElementById('calc-tipout')) {
    var toRun = function () {
      var basis = checked('basis') || 'tips';
      var grossC = cents(val('to-tips'));
      var salesC = cents(val('to-sales'));
      var rate   = num(val('to-rate'));

      show('to-sales-field', basis === 'sales');
      set('to-rate-label', basis === 'flat' ? 'Flat amount you owe' :
          basis === 'sales' ? 'Percent of sales' : 'Percent of your tips');
      set('to-rate-unit', basis === 'flat' ? '$' : '%');

      var outC = tipOutCents(basis, rate, grossC, salesC);
      var keptC = Math.max(0, grossC - outC);

      set('to-out', money(outC));
      set('to-kept', money(keptC));
      set('to-gross', money(grossC));
      set('to-share', grossC > 0 ? (outC / grossC * 100).toFixed(1) + '% of your tips' : '—');
      show('to-warn-sales', basis === 'sales' && !(salesC > 0));
      show('to-warn-cap', outC > 0 && outC === grossC && grossC > 0);
    };
    bind(['to-tips', 'to-sales', 'to-rate'], toRun);
  }

  /* =================== 2. Real hourly rate calculator ==================== */
  if (document.getElementById('calc-rate')) {
    var rateRun = function () {
      var grossC = cents(val('hr-tips'));
      var salesC = cents(val('hr-sales'));
      var hours  = num(val('hr-hours'));
      var wageC  = cents(val('hr-wage'));
      var basis  = checked('basis') || 'tips';
      var rate   = num(val('hr-rate'));

      show('hr-sales-field', basis === 'sales');
      set('hr-rate-unit', basis === 'flat' ? '$' : '%');
      set('hr-rate-label', basis === 'flat' ? 'Flat tip-out' :
          basis === 'sales' ? 'Tip-out, percent of sales' : 'Tip-out, percent of tips');

      var outC   = tipOutCents(basis, rate, grossC, salesC);
      var netC   = Math.max(0, grossC - outC);
      var wageEC = Math.round(wageC * hours);
      var takeC  = netC + wageEC;

      set('hr-gross', money(grossC));
      set('hr-out', outC ? '−' + money(outC) : money(0));
      set('hr-net', money(netC));
      set('hr-wage-earned', money(wageEC));
      set('hr-take', money(takeC));

      if (hours > 0) {
        // TipCalculator.trueHourlyRate: (net + wage x hours) / hours
        set('hr-headline', money(Math.round(takeC / hours)) + '/hr');
        set('hr-sub', 'Take-home ' + money(takeC) + ' over ' +
            (Math.round(hours * 10) / 10) + ' hours');
        show('hr-lines', true); show('hr-nohours', false);
      } else {
        // The app hides the figure rather than showing a divide-by-zero artefact.
        set('hr-headline', '—');
        set('hr-sub', 'Enter your hours to see a rate');
        show('hr-lines', false); show('hr-nohours', true);
      }
    };
    bind(['hr-tips', 'hr-sales', 'hr-hours', 'hr-wage', 'hr-rate'], rateRun);
  }

  /* ================== 3. Tip tax deduction estimator ===================== */
  if (document.getElementById('calc-deduction')) {
    var CAP = cents(document.getElementById('calc-deduction').dataset.cap);
    var dedRun = function () {
      var period  = checked('period') || 'year';
      var amountC = cents(val('td-tips'));
      var outC    = cents(val('td-tipout'));
      var rate    = num(val('td-rate'));

      var mult = period === 'week' ? 52 : period === 'month' ? 12 : period === 'shift' ? 0 : 1;
      var shifts = num(val('td-shifts'));
      if (period === 'shift') mult = shifts > 0 ? shifts : 0;

      var yearGrossC = Math.round(amountC * mult);
      var yearOutC   = Math.round(outC * mult);
      // TaxEngine: qualified tips are net of tip-out under the app's config.
      var qualifiedC = Math.max(0, yearGrossC - yearOutC);
      var deductC    = Math.min(qualifiedC, CAP);
      var overC      = Math.max(0, qualifiedC - deductC);
      var savingC    = Math.round(deductC * rate / 100);

      set('td-headline', money0(deductC));
      set('td-sub', overC > 0
        ? 'Capped. ' + money0(overC) + ' of qualified tips sits above the limit.'
        : 'Deductible, based on what you entered.');
      set('td-gross', money0(yearGrossC));
      set('td-out', yearOutC ? '−' + money0(yearOutC) : money0(0));
      set('td-qualified', money0(qualifiedC));
      set('td-cap', money0(CAP));
      set('td-saving', money0(savingC));
      set('td-rate-echo', rate + '%');
      show('td-warn-cap', overC > 0);
      show('td-shifts-field', period === 'shift');
    };
    bind(['td-tips', 'td-tipout', 'td-rate', 'td-shifts'], dedRun);
  }

  /* =================== 4. Shift earnings calculator ====================== */
  if (document.getElementById('calc-shift')) {
    var shiftRun = function () {
      var rows = document.querySelectorAll('[data-shift-row]');
      var totalTakeC = 0, totalHours = 0, totalNetC = 0, totalWageC = 0, worked = 0;

      rows.forEach(function (row) {
        var tipsC = cents(row.querySelector('.s-tips').value);
        var outC  = Math.min(cents(row.querySelector('.s-out').value), tipsC);
        var hours = num(row.querySelector('.s-hours').value);
        var wageC = cents(val('se-wage'));
        var netC  = Math.max(0, tipsC - outC);
        var wEC   = Math.round(wageC * hours);
        var takeC = netC + wEC;

        var out = row.querySelector('.s-result');
        if (out) {
          out.textContent = hours > 0
            ? money(takeC) + '  ·  ' + money(Math.round(takeC / hours)) + '/hr'
            : (tipsC || outC ? money(takeC) : '—');
        }
        if (tipsC > 0 || hours > 0) worked++;
        totalTakeC += takeC; totalHours += hours; totalNetC += netC; totalWageC += wEC;
      });

      set('se-headline', money(totalTakeC));
      set('se-sub', worked
        ? worked + (worked === 1 ? ' shift' : ' shifts') + ' · ' +
          (Math.round(totalHours * 10) / 10) + ' hours'
        : 'Fill in a shift to see your total');
      set('se-net', money(totalNetC));
      set('se-wage-earned', money(totalWageC));
      set('se-hours', (Math.round(totalHours * 10) / 10) + ' h');
      set('se-rate', totalHours > 0
        ? money(Math.round(totalTakeC / totalHours)) + '/hr' : '—');
    };
    var ids = ['se-wage'];
    document.querySelectorAll('[data-shift-row] input').forEach(function (el, i) {
      el.addEventListener('input', shiftRun);
    });
    bind(ids, shiftRun);
  }
})();
