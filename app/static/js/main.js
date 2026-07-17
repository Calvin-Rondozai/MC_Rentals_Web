(function () {
  "use strict";

  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- Theme toggle ---------------- */
  function initTheme() {
    var root = document.documentElement;
    var toggle = document.querySelector("[data-theme-toggle]");
    var stored = localStorage.getItem("mc-theme");
    if (stored) {
      root.setAttribute("data-theme", stored);
    }

    if (!toggle) return;
    toggle.addEventListener("click", function () {
      var current = root.getAttribute("data-theme");
      var isDark = current === "dark" || (!current && window.matchMedia("(prefers-color-scheme: dark)").matches);
      var next = isDark ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem("mc-theme", next);
    });
  }

  /* ---------------- Sticky nav shadow ---------------- */
  function initHeaderShadow() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    function onScroll() {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------------- Mobile drawer ---------------- */
  function initMobileNav() {
    var toggle = document.querySelector("[data-nav-toggle]");
    var drawer = document.querySelector("[data-mobile-drawer]");
    var closeBtn = document.querySelector("[data-drawer-close]");
    if (!toggle || !drawer) return;

    function open() {
      drawer.setAttribute("data-open", "true");
      document.body.style.overflow = "hidden";
      toggle.setAttribute("aria-expanded", "true");
    }
    function close() {
      drawer.setAttribute("data-open", "false");
      document.body.style.overflow = "";
      toggle.setAttribute("aria-expanded", "false");
    }

    toggle.addEventListener("click", open);
    if (closeBtn) closeBtn.addEventListener("click", close);
    drawer.querySelector(".mobile-drawer-backdrop").addEventListener("click", close);
    drawer.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", close);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  /* ---------------- Scroll reveal ---------------- */
  function initScrollReveal() {
    var items = document.querySelectorAll("[data-reveal]");
    if (!items.length) return;

    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
      items.forEach(function (el) {
        el.setAttribute("data-inview", "true");
      });
      return;
    }

    var groups = {};
    items.forEach(function (el) {
      var group = el.getAttribute("data-reveal-group") || "default";
      groups[group] = groups[group] || [];
      groups[group].push(el);
    });

    Object.keys(groups).forEach(function (key) {
      groups[key].forEach(function (el, index) {
        el.style.setProperty("--reveal-delay", Math.min(index * 60, 360) + "ms");
      });
    });

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.setAttribute("data-inview", "true");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );

    items.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ---------------- Count-up stats ---------------- */
  function initCountUp() {
    var counters = document.querySelectorAll("[data-count-to]");
    if (!counters.length) return;

    function animateCounter(el) {
      var target = parseInt(el.getAttribute("data-count-to"), 10) || 0;
      if (prefersReducedMotion) {
        el.textContent = target;
        return;
      }
      var duration = 900;
      var start = null;

      function step(timestamp) {
        if (!start) start = timestamp;
        var progress = Math.min((timestamp - start) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.floor(eased * target);
        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          el.textContent = target;
        }
      }
      requestAnimationFrame(step);
    }

    if (!("IntersectionObserver" in window)) {
      counters.forEach(animateCounter);
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ---------------- Lazy image fade-in ---------------- */
  function initImageFade() {
    document.querySelectorAll("img.lazy-fade").forEach(function (img) {
      if (img.complete) {
        img.classList.add("is-loaded");
      } else {
        img.addEventListener("load", function () {
          img.classList.add("is-loaded");
        });
      }
    });
  }

  /* ---------------- Flash message auto-dismiss ---------------- */
  function initFlashDismiss() {
    document.querySelectorAll(".flash").forEach(function (flash) {
      setTimeout(function () {
        flash.style.transition = "opacity 300ms ease, transform 300ms ease";
        flash.style.opacity = "0";
        flash.style.transform = "translateY(-8px)";
        setTimeout(function () {
          flash.remove();
        }, 320);
      }, 4500);
    });
  }

  /* ---------------- Confirm dialogs for destructive actions ---------------- */
  function initConfirmForms() {
    document.querySelectorAll("[data-confirm]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        var message = form.getAttribute("data-confirm");
        if (!window.confirm(message)) {
          e.preventDefault();
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTheme();
    initHeaderShadow();
    initMobileNav();
    initScrollReveal();
    initCountUp();
    initImageFade();
    initFlashDismiss();
    initConfirmForms();
  });
})();
