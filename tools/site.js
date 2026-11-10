(function () {
  'use strict';
  var order = ['home', 'about', 'services', 'onshore', 'offshore', 'manpower', 'hse', 'experience', 'contact', 'privacy'];
  var META = window.BEGAS_META || {};
  var main = document.getElementById('main');
  var panels = {};
  [].forEach.call(document.querySelectorAll('.panel[data-page]'), function (el) { panels[el.getAttribute('data-page')] = el; });
  var current = order.filter(function (p) { return panels[p] && !panels[p].hidden; })[0] || 'home';
  var timer = null;
  var burger = document.querySelector('.burger');
  var mpanel = document.getElementById('mobile-menu');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function pathFor(p) { return p === 'home' ? '/' : p === 'manpower' ? '/manpower-outsourcing' : p === 'privacy' ? '/privacy-policy' : '/' + p; }
  function pageFor(path) {
    path = path.replace(/\/index\.html$/, '').replace(/\/+$/, '') || '/';
    var m = META[path];
    return m ? m.p : null;
  }
  function setMenu(open) {
    if (!burger || !mpanel) return;
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    mpanel.hidden = !open;
  }
  function markNav() {
    [].forEach.call(document.querySelectorAll('a[data-go]'), function (a) {
      var on = a.getAttribute('data-go') === current && (a.closest('.nav-links') || a.classList.contains('ml'));
      if (on) { a.classList.add('on'); a.setAttribute('aria-current', 'page'); }
      else { a.classList.remove('on'); a.removeAttribute('aria-current'); }
    });
  }
  function setMeta(p) {
    var m = META[pathFor(p)];
    if (!m) return;
    document.title = m.t;
    var d = document.querySelector('meta[name="description"]'); if (d) d.setAttribute('content', m.d);
    var c = document.querySelector('link[rel="canonical"]');
    if (c) c.setAttribute('href', 'https://begasenergy.com' + pathFor(p));
    var a = document.getElementById('announce'); if (a) a.textContent = m.t;
  }
  function show(p, push) {
    setMenu(false);
    if (!panels[p]) return;
    if (p === current) { if (push) history.replaceState({}, '', pathFor(p)); window.scrollTo(0, 0); return; }
    var from = panels[current], to = panels[p];
    var dir = order.indexOf(p) > order.indexOf(current) ? 'next' : 'prev';
    if (timer) clearTimeout(timer);
    order.forEach(function (k) { if (k !== current && k !== p) { panels[k].hidden = true; panels[k].className = 'panel'; } });
    current = p;
    to.hidden = false;
    if (reduce) { from.hidden = true; from.className = 'panel'; to.className = 'panel'; }
    else {
      from.className = 'panel out-' + dir;
      to.className = 'panel in-' + dir;
      timer = setTimeout(function () { from.hidden = true; from.className = 'panel'; to.className = 'panel'; }, 520);
    }
    if (push) history.pushState({}, '', pathFor(p));
    window.scrollTo(0, 0);
    setMeta(p); markNav();
    main.focus({ preventScroll: true });
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-go]');
    if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    e.preventDefault();
    show(a.getAttribute('data-go'), true);
  });
  window.addEventListener('popstate', function () { var p = pageFor(location.pathname); if (p) show(p, false); });
  if (burger) burger.addEventListener('click', function () { setMenu(burger.getAttribute('aria-expanded') !== 'true'); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  markNav();

  /* enquiry form */
  var form = document.getElementById('enquiry');
  if (form) {
    var sent = document.getElementById('form-sent');
    var fields = ['fullName', 'email', 'phone', 'message', 'consent'];
    function err(id, msg) {
      var s = document.getElementById(id + '-err'), el = form.elements[id];
      if (!s) return;
      s.textContent = msg || ''; s.hidden = !msg;
      if (el && el.type !== 'checkbox') { if (msg) el.setAttribute('aria-invalid', 'true'); else el.removeAttribute('aria-invalid'); }
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = function (n) { var el = form.elements[n]; return el.type === 'checkbox' ? el.checked : String(el.value || '').trim(); };
      var m = {};
      if (!v('fullName')) m.fullName = 'Please enter your name.';
      if (!v('email')) m.email = 'Please enter your email address.';
      else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v('email'))) m.email = 'Enter a valid email address, for example name@company.com.';
      if (v('phone') && !/^[+0-9 ()\-]{7,20}$/.test(v('phone'))) m.phone = 'Enter a valid telephone number.';
      if (v('message').length < 10) m.message = 'Please describe your requirement in at least 10 characters.';
      if (!v('consent')) m.consent = 'Please confirm that we may contact you about this enquiry.';
      fields.forEach(function (f) { err(f, m[f]); });
      var first = fields.filter(function (f) { return m[f]; })[0];
      if (first) { form.elements[first].focus(); return; }
      var btn = form.querySelector('button[type=submit]'); btn.disabled = true;
      var body = new URLSearchParams(new FormData(form)).toString();
      fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body })
        .then(function (r) { if (!r.ok) throw new Error(); form.hidden = true; sent.hidden = false; sent.focus(); form.reset(); })
        .catch(function () { err('message', 'Sorry, the enquiry could not be sent. Please email admin@begasenergy.com.'); })
        .then(function () { btn.disabled = false; });
    });
    var again = document.getElementById('form-again');
    if (again) again.addEventListener('click', function () { sent.hidden = true; form.hidden = false; form.elements.fullName.focus(); });
  }
})();
