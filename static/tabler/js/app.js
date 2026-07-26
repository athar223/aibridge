/* AIBridge front-end interactions — lightweight, dependency-light. */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    initNavbarScrollState();
    initScrollReveal();
    initCopyButtons();
    initSmoothAnchors();
  });

  function initNavbarScrollState() {
    var navbar = document.querySelector(".ab-navbar");
    if (!navbar) return;
    var toggle = function () {
      navbar.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    toggle();
    window.addEventListener("scroll", toggle, { passive: true });
  }

  function initScrollReveal() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) return;

    if (!("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("in-view"); });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );

    items.forEach(function (el) { observer.observe(el); });
  }

  function initCopyButtons() {
    document.querySelectorAll("[data-copy-target]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var target = document.querySelector(btn.getAttribute("data-copy-target"));
        if (!target) return;
        var text = target.innerText || target.textContent || "";

        var done = function () {
          var original = btn.innerHTML;
          btn.classList.add("copied");
          setTimeout(function () {
            btn.classList.remove("copied");
          }, 1500);
        };

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done).catch(function () {
            fallbackCopy(text);
            done();
          });
        } else {
          fallbackCopy(text);
          done();
        }
      });
    });
  }

  function fallbackCopy(text) {
    var textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    try { document.execCommand("copy"); } catch (err) { /* no-op */ }
    document.body.removeChild(textarea);
  }

  function initSmoothAnchors() {
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener("click", function (e) {
        var id = link.getAttribute("href");
        if (id.length < 2) return;
        var el = document.querySelector(id);
        if (!el) return;
        e.preventDefault();
        el.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }

  // Expose a small helper other pages can use to show a loading state
  // on form submit (Recommender / Prompt Generator).
  window.AIBridge = {
    submitWithLoading: function (formEl, buttonEl, loadingText) {
      formEl.addEventListener("submit", function () {
        if (!formEl.checkValidity()) return;
        buttonEl.disabled = true;
        buttonEl.innerHTML = '<span class="ab-spinner me-2"></span>' + (loadingText || "Working...");
      });
    },
  };
})();
