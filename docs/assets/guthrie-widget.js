/*
 * Guthrie — embedded PKU research chat for pku-commons.org.
 *
 * Self-contained: injects its own styles + DOM, no dependencies. Drop
 *   <script defer src="assets/guthrie-widget.js"></script>
 * before </body> on any page. Matches the site design system (Hanken/Space
 * Grotesk, blue accent, mono labels) via the CSS vars in assets/styles.css.
 *
 * It calls the research agent's POST /api/ask and shows the grounded answer
 * plus its sources (cite-or-refuse — the agent will not invent a citation).
 *
 * ── CONNECTING THE BACKEND (one place) ──────────────────────────────────────
 * Point this at the deployed Railway service, any ONE of:
 *   1. window.GUTHRIE_API_BASE = "https://<service>.up.railway.app"  (before this script)
 *   2. <script defer src="assets/guthrie-widget.js" data-api-base="https://..."></script>
 *   3. edit DEFAULT_API_BASE below.
 * Until it is set, the widget renders but tells users it isn't connected yet.
 */
(function () {
  "use strict";
  if (window.__guthrieWidgetLoaded) return;
  window.__guthrieWidgetLoaded = true;

  var DEFAULT_API_BASE = "https://pku-commons-production.up.railway.app"; // Railway service (public domain)
  var thisScript = document.currentScript;
  var API_BASE = (
    window.GUTHRIE_API_BASE ||
    (thisScript && thisScript.dataset && thisScript.dataset.apiBase) ||
    DEFAULT_API_BASE ||
    ""
  ).replace(/\/+$/, "");

  // ── Optional Cloudflare Turnstile (bot / abuse guard) ────────────────────
  // Public SITE key. Set via window.GUTHRIE_TURNSTILE_SITEKEY, the script's
  // data-turnstile-sitekey attr, or DEFAULT_TURNSTILE_SITEKEY. Blank = disabled
  // (the server also stays dormant until TURNSTILE_SECRET_KEY is set). Use the
  // same value as the other apps' NEXT_PUBLIC_TURNSTILE_SITE_KEY, configured as
  // a Non-Interactive / Invisible widget so it needs no visible UI.
  var DEFAULT_TURNSTILE_SITEKEY = "0x4AAAAAAEX1ioGNbz07cUPE"; // Cloudflare Turnstile site key (public) for pku-commons.org
  var TURNSTILE_SITEKEY =
    window.GUTHRIE_TURNSTILE_SITEKEY ||
    (thisScript && thisScript.dataset && thisScript.dataset.turnstileSitekey) ||
    DEFAULT_TURNSTILE_SITEKEY ||
    "";

  // Cloudflare Turnstile token plumbing. Tokens are single-use and expire
  // (~5 min), so we mint a FRESH one for every request (reset before each)
  // instead of caching — a stale/expired cached token is the usual cause of an
  // intermittent 403. Sends are serialized (the `busy` flag), so one pending
  // resolver is enough. Transient challenge failures are retried.
  var _tsId = null,
    _tsLoading = false,
    _tsPending = null; // (token) => void, set while a send awaits a token
  function _tsDeliver(token) {
    var cb = _tsPending;
    if (cb) cb(token || "");
  }
  function _tsRender() {
    if (_tsId !== null || !window.turnstile) return;
    var box = document.createElement("div");
    box.style.display = "none";
    document.body.appendChild(box);
    _tsId = window.turnstile.render(box, {
      sitekey: TURNSTILE_SITEKEY,
      callback: function (t) { _tsDeliver(t); },
      "error-callback": function () { _tsDeliver(""); },
      "expired-callback": function () { _tsDeliver(""); },
    });
  }
  function _tsLoad() {
    if (_tsLoading || !TURNSTILE_SITEKEY) return;
    _tsLoading = true;
    var s = document.createElement("script");
    s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
    s.async = true;
    s.defer = true;
    s.onload = _tsRender;
    document.head.appendChild(s);
  }
  // Force a fresh challenge: load+render on first use, else reset the widget.
  function _tsTrigger() {
    if (!TURNSTILE_SITEKEY) return;
    if (!window.turnstile) { _tsLoad(); return; }
    if (_tsId === null) { _tsRender(); return; }
    try { window.turnstile.reset(_tsId); } catch (e) { _tsDeliver(""); }
  }
  // Resolve to a FRESH single-use token, or "" if disabled/unavailable. Retries
  // transient failures and never hangs the chat (falls back to "" by ~9s).
  function getTurnstileToken() {
    return new Promise(function (resolve) {
      if (!TURNSTILE_SITEKEY) { resolve(""); return; }
      var done = false,
        tries = 0;
      var timer = setTimeout(function () { finish(""); }, 9000);
      function finish(tok) {
        if (done) return;
        done = true;
        clearTimeout(timer);
        if (_tsPending === handle) _tsPending = null;
        resolve(tok || "");
      }
      function handle(tok) {
        if (done) return;
        if (tok) { finish(tok); return; }
        if (++tries < 4) setTimeout(_tsTrigger, 500); // retry a fresh challenge
        else finish("");
      }
      _tsPending = handle;
      _tsTrigger();
    });
  }

  var GREETING =
    "Hi, I'm Guthrie. I answer questions about PKU from the published literature and clinical guidelines, and I cite my sources. I won't guess. What would you like to know?";
  var SUGGESTED = [
    "What is the target blood Phe range?",
    "How is Phe monitored at home?",
    "Does sapropterin help everyone?",
  ];
  var DISCLAIMER =
    "Guthrie is an AI research aid, not medical advice. Always consult your metabolic clinician.";

  // ── styles ────────────────────────────────────────────────────────────────
  var css =
    "" +
    ".gth-root{--gth-blue:var(--blue,#1e3fd6);--gth-blue-dk:var(--blue-dk,#1833ad);" +
    "--gth-wash:var(--blue-wash,#ecefff);--gth-line:var(--line,#e7e7e3);" +
    "--gth-ink:var(--ink,#101010);--gth-soft:var(--ink-soft,#5c5c5c);" +
    "--gth-paper:var(--paper,#fff);--gth-bg:var(--wash,#faf9f5);" +
    "--gth-font:var(--font,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif);" +
    "--gth-disp:var(--font-disp,var(--gth-font));--gth-mono:var(--font-mono,ui-monospace,Menlo,monospace);}" +
    ".gth-root *{box-sizing:border-box;}" +
    ".gth-launch{position:fixed;bottom:22px;right:22px;z-index:2147483000;display:inline-flex;" +
    "align-items:center;gap:9px;height:52px;padding:0 20px 0 18px;border:none;border-radius:999px;" +
    "background:var(--gth-blue);color:#fff;font-family:var(--gth-disp);font-weight:600;font-size:15px;" +
    "letter-spacing:-0.01em;cursor:pointer;box-shadow:0 6px 22px rgba(30,63,214,.32);" +
    "transition:transform .15s ease,background .15s ease;}" +
    ".gth-launch:hover{background:var(--gth-blue-dk);transform:translateY(-1px);}" +
    ".gth-launch svg{width:21px;height:21px;}" +
    ".gth-panel{position:fixed;bottom:22px;right:22px;z-index:2147483001;width:384px;" +
    "max-width:calc(100vw - 28px);height:560px;max-height:calc(100vh - 44px);background:var(--gth-paper);" +
    "border:1px solid var(--gth-line);border-radius:16px;box-shadow:0 12px 48px rgba(16,16,16,.18);" +
    "display:none;flex-direction:column;overflow:hidden;font-family:var(--gth-font);color:var(--gth-ink);}" +
    ".gth-panel.gth-open{display:flex;}" +
    ".gth-head{display:flex;align-items:center;gap:11px;padding:13px 14px;background:var(--gth-blue);color:#fff;}" +
    ".gth-mark{width:34px;height:34px;border-radius:50%;flex:0 0 auto;background:#fff;display:flex;" +
    "align-items:center;justify-content:center;overflow:hidden;}" +
    ".gth-mark img{width:100%;height:100%;object-fit:cover;}" +
    ".gth-mark svg{width:20px;height:20px;color:var(--gth-blue);}" +
    ".gth-htext{flex:1;min-width:0;line-height:1.2;}" +
    ".gth-htext b{font-family:var(--gth-disp);font-weight:700;font-size:15px;display:block;}" +
    ".gth-htext span{font-family:var(--gth-mono);font-size:11px;letter-spacing:.04em;opacity:.85;text-transform:uppercase;}" +
    ".gth-x{background:none;border:none;color:#fff;cursor:pointer;padding:4px;opacity:.9;line-height:0;}" +
    ".gth-x:hover{opacity:1;}.gth-x svg{width:19px;height:19px;}" +
    ".gth-log{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:12px;background:var(--gth-bg);}" +
    ".gth-row{display:flex;flex-direction:column;gap:7px;max-width:100%;}" +
    ".gth-row.u{align-items:flex-end;}.gth-row.b{align-items:flex-start;}" +
    ".gth-bubble{max-width:86%;padding:10px 13px;border-radius:15px;font-size:14.5px;line-height:1.5;" +
    "white-space:pre-wrap;overflow-wrap:anywhere;}" +
    ".gth-row.u .gth-bubble{background:var(--gth-blue);color:#fff;border-bottom-right-radius:5px;}" +
    ".gth-row.b .gth-bubble{background:var(--gth-paper);color:var(--gth-ink);border:1px solid var(--gth-line);border-bottom-left-radius:5px;}" +
    ".gth-bubble a{color:inherit;text-decoration:underline;text-underline-offset:2px;font-weight:600;}" +
    ".gth-row.b .gth-bubble a{color:var(--gth-blue);}" +
    ".gth-sources{max-width:86%;display:flex;flex-direction:column;gap:6px;}" +
    ".gth-src-h{font-family:var(--gth-mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--gth-soft);}" +
    ".gth-src{display:flex;gap:8px;align-items:flex-start;padding:8px 10px;border:1px solid var(--gth-line);" +
    "border-radius:11px;background:var(--gth-paper);text-decoration:none;color:var(--gth-ink);transition:border-color .12s ease,background .12s ease;}" +
    ".gth-src:hover{border-color:var(--gth-blue);background:var(--gth-wash);}" +
    ".gth-src-tag{font-family:var(--gth-mono);font-size:10px;font-weight:600;color:var(--gth-blue);background:var(--gth-wash);" +
    "border-radius:5px;padding:2px 6px;flex:0 0 auto;white-space:nowrap;}" +
    ".gth-src-tt{font-size:12.5px;line-height:1.35;color:var(--gth-ink);}" +
    ".gth-typing{display:inline-flex;gap:5px;padding:12px 14px;background:var(--gth-paper);border:1px solid var(--gth-line);border-radius:15px;border-bottom-left-radius:5px;}" +
    ".gth-typing i{width:7px;height:7px;border-radius:50%;background:var(--gth-soft);animation:gth-b 1.2s infinite ease-in-out;}" +
    ".gth-typing i:nth-child(2){animation-delay:.15s;}.gth-typing i:nth-child(3){animation-delay:.3s;}" +
    "@keyframes gth-b{0%,80%,100%{transform:translateY(0);opacity:.5;}40%{transform:translateY(-5px);opacity:1;}}" +
    ".gth-suggest{display:flex;flex-wrap:wrap;gap:7px;padding:0 14px 10px;background:var(--gth-bg);}" +
    ".gth-chip{font-family:var(--gth-font);font-size:12.5px;color:var(--gth-blue);background:var(--gth-wash);" +
    "border:1px solid var(--blue-line,#c3ccff);border-radius:999px;padding:6px 12px;cursor:pointer;transition:background .12s ease;}" +
    ".gth-chip:hover{background:#e0e6ff;}" +
    ".gth-form{display:flex;gap:8px;padding:11px 12px;border-top:1px solid var(--gth-line);background:var(--gth-paper);}" +
    ".gth-input{flex:1;font-family:var(--gth-font);font-size:14.5px;color:var(--gth-ink);background:var(--gth-bg);" +
    "border:1px solid var(--gth-line);border-radius:999px;padding:10px 15px;outline:none;}" +
    ".gth-input:focus{border-color:var(--gth-blue);box-shadow:0 0 0 3px var(--gth-wash);}" +
    ".gth-send{flex:0 0 auto;width:40px;height:40px;border-radius:50%;border:none;background:var(--gth-blue);color:#fff;" +
    "cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .12s ease;}" +
    ".gth-send:hover:not(:disabled){background:var(--gth-blue-dk);}" +
    ".gth-send:disabled{background:var(--gth-line);cursor:default;}.gth-send svg{width:17px;height:17px;}" +
    ".gth-foot{font-family:var(--gth-font);font-size:11px;line-height:1.4;color:var(--gth-soft);text-align:center;padding:8px 14px 11px;background:var(--gth-paper);}" +
    "@media (max-width:480px){.gth-panel{width:100vw;height:100vh;max-height:100vh;right:0;bottom:0;border-radius:0;border:none;}" +
    ".gth-launch{bottom:16px;right:16px;}}" +
    "@media (prefers-reduced-motion:reduce){.gth-launch,.gth-typing i{transition:none;animation:none;}}";

  var style = document.createElement("style");
  style.id = "gth-widget-style";
  style.textContent = css;
  document.head.appendChild(style);

  // ── DOM helpers ─────────────────────────────────────────────────────────
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  var URL_RE = /(https?:\/\/[^\s<]+)/gi;
  function stripPunct(u) {
    return u.replace(/[.,;:!?)\]]+$/g, "");
  }
  // Render text safely: plain text nodes, real anchors for URLs. No innerHTML
  // of model/corpus output (avoids injection).
  function renderText(container, text) {
    String(text == null ? "" : text)
      .split(URL_RE)
      .forEach(function (part) {
        if (/^https?:\/\//i.test(part)) {
          var href = stripPunct(part);
          var a = document.createElement("a");
          a.href = href;
          a.target = "_blank";
          a.rel = "noopener noreferrer";
          a.textContent = href;
          container.appendChild(a);
        } else if (part) {
          container.appendChild(document.createTextNode(part));
        }
      });
  }

  var root = el("div", "gth-root");
  root.setAttribute("aria-live", "polite");

  var launch = el(
    "button",
    "gth-launch",
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg><span>Ask Guthrie</span>'
  );
  launch.setAttribute("aria-label", "Open the Guthrie PKU research chat");

  var panel = el("div", "gth-panel");
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-label", "Guthrie PKU research chat");

  var head = el("div", "gth-head");
  var mark = el(
    "div",
    "gth-mark",
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg>'
  );
  // Prefer the site logo; fall back to the inline glyph if it fails to load.
  var logo = new Image();
  logo.alt = "";
  logo.onload = function () {
    mark.innerHTML = "";
    mark.appendChild(logo);
  };
  logo.src = "assets/pku-commons-logo.png";
  var htext = el("div", "gth-htext", "<b>Guthrie</b><span>PKU research agent</span>");
  var closeBtn = el(
    "button",
    "gth-x",
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>'
  );
  closeBtn.setAttribute("aria-label", "Close chat");
  head.appendChild(mark);
  head.appendChild(htext);
  head.appendChild(closeBtn);

  var log = el("div", "gth-log");
  var suggest = el("div", "gth-suggest");
  var form = el("form", "gth-form");
  var input = el("input", "gth-input");
  input.type = "text";
  input.placeholder = "Ask about PKU...";
  input.setAttribute("maxlength", "2000");
  input.setAttribute("aria-label", "Your question");
  var send = el(
    "button",
    "gth-send",
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7"/></svg>'
  );
  send.type = "submit";
  send.disabled = true;
  send.setAttribute("aria-label", "Send");
  form.appendChild(input);
  form.appendChild(send);
  var foot = el("div", "gth-foot");
  foot.textContent = DISCLAIMER;

  panel.appendChild(head);
  panel.appendChild(log);
  panel.appendChild(suggest);
  panel.appendChild(form);
  panel.appendChild(foot);
  root.appendChild(launch);
  root.appendChild(panel);
  document.body.appendChild(root);

  // ── messages ──────────────────────────────────────────────────────────
  function addUser(text) {
    var row = el("div", "gth-row u");
    var b = el("div", "gth-bubble");
    b.textContent = text;
    row.appendChild(b);
    log.appendChild(row);
    scroll();
  }
  function addBot(text, hits, citations) {
    var row = el("div", "gth-row b");
    var b = el("div", "gth-bubble");
    renderText(b, text);
    row.appendChild(b);

    // The API's `citations` are bracketed ("[PMID:123]") while hits are bare
    // ("PMID:123"); also honor any PMID the answer cites inline (the citations
    // field can miss some). Normalize: strip brackets/space, upper-case.
    function normCite(s) {
      return String(s == null ? "" : s).replace(/[[\]\s]/g, "").toUpperCase();
    }
    var refs = {};
    (Array.isArray(citations) ? citations : []).forEach(function (c) {
      var k = normCite(c);
      if (k) refs[k] = 1;
    });
    String(text || "").replace(/PMID:\s*\d+/gi, function (m) {
      refs[normCite(m)] = 1;
      return m;
    });
    var srcHits = (Array.isArray(hits) ? hits : []).filter(function (h) {
      return h && h.url && refs[normCite(h.citation)];
    });
    // de-dup by url
    var seen = {};
    srcHits = srcHits.filter(function (h) {
      if (seen[h.url]) return false;
      seen[h.url] = 1;
      return true;
    });
    if (srcHits.length) {
      var box = el("div", "gth-sources");
      box.appendChild(el("div", "gth-src-h", "Sources"));
      srcHits.slice(0, 5).forEach(function (h) {
        var a = document.createElement("a");
        a.className = "gth-src";
        a.href = /^https?:\/\//i.test(h.url) ? h.url : "#";
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        var tag = el("span", "gth-src-tag");
        tag.textContent = h.citation || h.source || "src";
        var tt = el("span", "gth-src-tt");
        tt.textContent = h.title || h.url;
        a.appendChild(tag);
        a.appendChild(tt);
        box.appendChild(a);
      });
      row.appendChild(box);
    }
    log.appendChild(row);
    scroll();
  }
  var typingRow = null;
  function showTyping() {
    typingRow = el("div", "gth-row b");
    typingRow.appendChild(el("div", "gth-typing", "<i></i><i></i><i></i>"));
    log.appendChild(typingRow);
    scroll();
  }
  function hideTyping() {
    if (typingRow) {
      typingRow.remove();
      typingRow = null;
    }
  }
  function scroll() {
    log.scrollTop = log.scrollHeight;
  }

  // ── networking ────────────────────────────────────────────────────────
  var busy = false;
  function ask(text) {
    text = (text || "").trim();
    if (!text || busy) return;
    if (suggest.childNodes.length) suggest.innerHTML = "";
    addUser(text);
    input.value = "";
    updateSend();

    if (!API_BASE) {
      addBot(
        "Guthrie isn't connected to its research service yet. Please check back soon.",
        [],
        []
      );
      return;
    }

    busy = true;
    send.disabled = true;
    showTyping();
    function doFetch() {
      return getTurnstileToken()
        .then(function (tsToken) {
          var headers = { "Content-Type": "application/json" };
          if (tsToken) headers["cf-turnstile-response"] = tsToken;
          return fetch(API_BASE + "/api/ask", {
            method: "POST",
            headers: headers,
            body: JSON.stringify({ question: text }),
          });
        })
        .then(function (res) {
          return res
            .json()
            .catch(function () {
              return {};
            })
            .then(function (data) {
              return { ok: res.ok, status: res.status, data: data };
            });
        });
    }

    doFetch()
      .then(function (r) {
        // A 403 is almost always a stale/rejected Turnstile token — retry once
        // with a freshly minted token before surfacing an error.
        return r.status === 403 ? doFetch() : r;
      })
      .then(function (r) {
        hideTyping();
        if (!r.ok) {
          if (r.status === 429) {
            addBot("You're sending questions faster than I can answer. Give it a moment and try again.", [], []);
          } else {
            addBot("I'm having trouble reaching the research service right now. Please try again in a moment.", [], []);
          }
          return;
        }
        var d = r.data || {};
        var answer = d.answer;
        if (answer == null || answer === "") {
          answer =
            d.citations && d.citations.length
              ? "I found relevant sources but couldn't compose an answer. See the sources below."
              : "I don't have a grounded source for that in the PKU literature I hold, so I won't guess. Try rephrasing, or ask your metabolic clinician.";
        }
        addBot(answer, d.hits, d.citations);
      })
      .catch(function () {
        hideTyping();
        addBot("I'm having trouble connecting right now. Please try again in a moment.", [], []);
      })
      .then(function () {
        busy = false;
        updateSend();
        input.focus();
      });
  }

  // ── wiring ────────────────────────────────────────────────────────────
  function updateSend() {
    send.disabled = busy || !input.value.trim();
  }
  var greeted = false;
  function openPanel() {
    panel.classList.add("gth-open");
    launch.style.display = "none";
    _tsLoad(); // warm up Turnstile on first open (no-op unless a site key is set)
    if (!greeted) {
      greeted = true;
      addBot(GREETING, [], []);
      SUGGESTED.forEach(function (q) {
        var c = el("button", "gth-chip");
        c.type = "button";
        c.textContent = q;
        c.addEventListener("click", function () {
          ask(q);
        });
        suggest.appendChild(c);
      });
    }
    setTimeout(function () {
      input.focus();
    }, 0);
  }
  function closePanel() {
    panel.classList.remove("gth-open");
    launch.style.display = "";
    launch.focus();
  }
  launch.addEventListener("click", openPanel);
  closeBtn.addEventListener("click", closePanel);
  input.addEventListener("input", updateSend);
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    ask(input.value);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && panel.classList.contains("gth-open")) closePanel();
  });
})();
