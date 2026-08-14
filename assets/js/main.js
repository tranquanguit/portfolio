/* Tran Van Quang — Portfolio
   Theme, navigation, scroll reveal, section spy, project filters. */

(function () {
  'use strict';

  /* --- Theme ------------------------------------------------------------- */

  var STORAGE_KEY = 'tvq-theme';

  function systemTheme() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', theme === 'dark' ? '#0d1317' : '#faf9f6');
  }

  function initTheme() {
    var stored = null;
    try { stored = localStorage.getItem(STORAGE_KEY); } catch (e) { /* private mode */ }
    applyTheme(stored || systemTheme());

    var toggle = document.querySelector('.theme-toggle');
    if (toggle) {
      toggle.addEventListener('click', function () {
        var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        applyTheme(next);
        try { localStorage.setItem(STORAGE_KEY, next); } catch (e) { /* ignore */ }
      });
    }

    if (window.matchMedia) {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      var onChange = function () {
        var saved = null;
        try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) { /* ignore */ }
        if (!saved) applyTheme(systemTheme());
      };
      if (mq.addEventListener) mq.addEventListener('change', onChange);
      else if (mq.addListener) mq.addListener(onChange);
    }
  }

  /* --- Sticky nav shadow -------------------------------------------------- */

  function initStickyNav() {
    var nav = document.querySelector('.nav');
    if (!nav) return;
    var update = function () { nav.classList.toggle('is-stuck', window.scrollY > 8); };
    update();
    window.addEventListener('scroll', update, { passive: true });
  }

  /* --- Mobile drawer ------------------------------------------------------ */

  function initDrawer() {
    var burger = document.querySelector('.nav__burger');
    var drawer = document.querySelector('.nav__drawer');
    if (!burger || !drawer) return;

    var setOpen = function (open) {
      drawer.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', String(open));
    };

    burger.addEventListener('click', function (e) {
      e.stopPropagation();
      setOpen(!drawer.classList.contains('is-open'));
    });

    drawer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setOpen(false);
    });

    document.addEventListener('click', function (e) {
      if (drawer.classList.contains('is-open') && !drawer.contains(e.target) && !burger.contains(e.target)) {
        setOpen(false);
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }

  /* --- Scroll reveal ------------------------------------------------------ */

  function initReveal() {
    var items = document.querySelectorAll('.reveal');
    if (!items.length) return;

    if (!('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    items.forEach(function (el) { io.observe(el); });

    // Safety net: if anything prevents the observer from firing, never leave
    // content permanently invisible.
    setTimeout(function () {
      document.querySelectorAll('.reveal:not(.is-visible)').forEach(function (el) {
        if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('is-visible');
      });
    }, 2500);
  }

  /* --- Skill meters ------------------------------------------------------- */

  function initMeters() {
    var meters = document.querySelectorAll('.meter__fill[data-level]');
    if (!meters.length) return;

    var fill = function (el) { el.style.width = Math.max(0, Math.min(100, +el.dataset.level)) + '%'; };

    if (!('IntersectionObserver' in window)) {
      meters.forEach(fill);
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        fill(entry.target);
        io.unobserve(entry.target);
      });
    }, { threshold: 0.4 });

    meters.forEach(function (el) { io.observe(el); });
  }

  /* --- Section spy -------------------------------------------------------- */

  function initSpy() {
    var links = Array.prototype.slice.call(document.querySelectorAll('.nav__links a[href^="#"]'));
    if (!links.length) return;

    var sections = links
      .map(function (a) { return document.querySelector(a.getAttribute('href')); })
      .filter(Boolean);
    if (!sections.length) return;

    var setActive = function (id) {
      links.forEach(function (a) {
        a.classList.toggle('is-active', a.getAttribute('href') === '#' + id);
      });
    };

    if (!('IntersectionObserver' in window)) return;

    var visible = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { visible[entry.target.id] = entry.isIntersecting; });
      for (var i = 0; i < sections.length; i++) {
        if (visible[sections[i].id]) { setActive(sections[i].id); return; }
      }
    }, { rootMargin: '-45% 0px -50% 0px' });

    sections.forEach(function (s) { io.observe(s); });
  }

  /* --- Filters ------------------------------------------------------------ */

  function initFilters() {
    document.querySelectorAll('[data-filter-group]').forEach(function (group) {
      var name = group.dataset.filterGroup;
      var buttons = group.querySelectorAll('.filter');
      var targets = document.querySelectorAll('[data-filter-target="' + name + '"]');

      buttons.forEach(function (btn) {
        btn.addEventListener('click', function () {
          var value = btn.dataset.value;

          buttons.forEach(function (b) {
            var on = b === btn;
            b.classList.toggle('is-active', on);
            b.setAttribute('aria-pressed', String(on));
          });

          targets.forEach(function (el) {
            var match = value === 'all' || (el.dataset.key || '').split(' ').indexOf(value) !== -1;
            el.classList.toggle('is-hidden', !match);
          });

          // Hide group wrappers that no longer contain a visible item.
          document.querySelectorAll('[data-filter-section="' + name + '"]').forEach(function (sec) {
            var any = sec.querySelector('[data-filter-target="' + name + '"]:not(.is-hidden)');
            sec.classList.toggle('is-hidden', !any);
          });
        });
      });
    });
  }

  /* --- Current year ------------------------------------------------------- */

  function initYear() {
    var y = String(new Date().getFullYear());
    document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = y; });
  }

  /* --- Boot --------------------------------------------------------------- */

  function boot() {
    initTheme();
    initStickyNav();
    initDrawer();
    initReveal();
    initMeters();
    initSpy();
    initFilters();
    initYear();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
