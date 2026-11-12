"""Compare page and embed snippet. Standard library only.

The page is one self-contained index.html in the run folder. It inlines the <before-after>
component and the manifest, and points at the version PNGs by relative path, so it works
opened straight from disk (file://) with no server and no fetch.
"""

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

import store

COMPONENT = Path(__file__).resolve().with_name("before-after.js")


def label(version: dict) -> str:
    return f"{version['label']} · {version['note']}" if version.get("note") else version["label"]


def default_route(manifest: dict, b: int):
    """The first run route that version b captured, else the run's first route."""
    images = manifest["versions"][b]["images"]
    return next((r for r in manifest["routes"] if r in images), (manifest["routes"] or [None])[0])


def _sizes(run: Path, manifest: dict) -> dict:
    out = {}
    for v in manifest["versions"]:
        for rel in v["images"].values():
            try:
                out[rel] = list(store.image_size(run / rel))
            except (OSError, ValueError):
                pass  # A missing or broken file shows as a broken image, not a crash.
    return out


def _script_json(data) -> str:
    # < keeps "</script>" and "<!--" in notes from ending the block early.
    return json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")


def build_page(root: Path, manifest: dict, a: int | None = None, b: int | None = None,
               route: str | None = None) -> Path:
    """Write run_dir/index.html. A and B default to the latest two versions."""
    run = store.run_dir(root, manifest["run"])
    n = len(manifest["versions"])
    a = max(n - 2, 0) if a is None else a
    b = max(n - 1, 0) if b is None else b
    data = {"manifest": manifest, "sizes": _sizes(run, manifest), "a": a, "b": b,
            "route": route if route is not None else default_route(manifest, b)}
    # Insert user-controlled text last, so a placeholder inside a note is never substituted.
    page = (PAGE.replace("__COMPONENT__", COMPONENT.read_text())
            .replace("__RUN__", html.escape(manifest["run"]))
            .replace("__DATA__", _script_json(data)))
    run.mkdir(parents=True, exist_ok=True)
    out = run / "index.html"
    out.write_text(page)
    return out


def build_embed(root: Path, manifest: dict, a: int, b: int, route: str, out: Path) -> Path:
    """Write before.png, after.png, before-after.js and snippet.html into out. Returns the snippet."""
    run = store.run_dir(root, manifest["run"])
    va, vb = manifest["versions"][a], manifest["versions"][b]
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(run / va["images"][route], out / "before.png")
    shutil.copyfile(run / vb["images"][route], out / "after.png")
    shutil.copyfile(COMPONENT, out / "before-after.js")
    width = round(store.image_size(out / "after.png")[0] / (vb.get("scale") or 1))
    la, lb = html.escape(label(va)), html.escape(label(vb))
    snippet = out / "snippet.html"
    snippet.write_text(
        f"<!-- Wipe: {la} to {lb}. Keep the four files together, or change the paths. -->\n"
        f'<before-after before="before.png" after="after.png" before-label="{la}" after-label="{lb}"\n'
        f'  position="50" aria-label="Compare {la} with {lb}"\n'
        f'  style="max-width:{width}px;border-radius:12px"></before-after>\n'
        f'<script src="before-after.js"></script>\n')
    return snippet


PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__RUN__ · Wipe</title>
<style>
:root {
  color-scheme: dark;
  --ground: #0e0e0d;
  --ink: #f4f2ee;
  --dim: rgb(244 242 238 / .58);
  --faint: rgb(244 242 238 / .34);
  --chip: rgb(255 255 255 / .06);
  --chip-on: rgb(255 255 255 / .13);
  --accent: #ff3b8b;
  --warn: #f5b94a;
}
* { box-sizing: border-box; }
html, body { height: 100%; margin: 0; }
body {
  display: grid; grid-template-rows: auto minmax(0, 1fr) auto auto;
  height: 100dvh; overflow: hidden;
  background: var(--ground); color: var(--ink);
  font: 500 13px/1.4 system-ui, -apple-system, "Segoe UI", sans-serif;
  -webkit-font-smoothing: antialiased;
}
button { font: inherit; color: inherit; background: none; border: 0; padding: 0; cursor: pointer; }
:focus-visible { outline: 2px solid var(--ink); outline-offset: 2px; }

/* Top bar: brand and run on the left, routes in the middle, views on the right. */
.top {
  display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 16px;
  padding: 14px 20px;
}
.brand { display: flex; align-items: center; gap: 10px; min-width: 0; }
.mark {
  flex: none; width: 16px; height: 16px; border-radius: 5px;
  background: linear-gradient(90deg, var(--ink) 50%, rgb(255 255 255 / .22) 50%);
}
.brand strong { font-weight: 650; letter-spacing: -.01em; }
.run { color: var(--dim); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.run::before { content: "/"; margin-right: 10px; color: var(--faint); }
.seg { display: flex; gap: 2px; padding: 3px; border-radius: 999px; background: var(--chip); }
.seg button {
  display: flex; align-items: center; gap: 7px; padding: 6px 12px; border-radius: 999px;
  color: var(--dim); white-space: nowrap; transition: background-color .15s, color .15s;
}
.seg button:hover { color: var(--ink); }
.seg button[aria-pressed="true"] { background: var(--chip-on); color: var(--ink); }
.seg kbd { font: 600 10px/1 ui-monospace, SFMono-Regular, Menlo, monospace; color: var(--faint); }
.modes { justify-self: end; }
.routes[hidden] { display: none; }

/* Stage: one scroller for every view, so tall pairs always scroll together. */
main { display: grid; place-items: center; padding: 6px 28px 0; min-height: 0; }
.frame {
  position: relative; overflow: hidden auto; overscroll-behavior: contain;
  border-radius: 16px; background: #1b1b19;
  box-shadow: 0 30px 70px -24px rgb(0 0 0 / .85), 0 0 0 1px rgb(255 255 255 / .06);
  scrollbar-width: thin; scrollbar-color: rgb(255 255 255 / .25) transparent;
}
.frame.sbs { background: none; box-shadow: none; border-radius: 12px; }
.frame img { display: block; width: 100%; height: auto; user-select: none; -webkit-user-drag: none; }
before-after:focus-visible { outline: none; }
.stack { display: grid; }
.stack > * { grid-area: 1 / 1; }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; align-items: start; }
.pane { display: grid; border-radius: 12px; overflow: clip; background: #1b1b19; }  /* clip keeps the pill sticky */
.pane > * { grid-area: 1 / 1; }
.pill {
  position: sticky; bottom: 16px; align-self: end; justify-self: start; margin: 16px;
  padding: 8px 14px; border-radius: 99px; background: #111d; color: #fff;
  font: 600 13px/1 system-ui, sans-serif; white-space: nowrap; pointer-events: none;
}
.pill.right { justify-self: end; }
.pill i { display: inline-block; width: 8px; height: 8px; margin-right: 8px; border-radius: 2px; background: var(--accent); }
.top-img { transition: opacity .12s linear; }
.dim { filter: grayscale(1) brightness(.42) contrast(.9); }
.hot { display: grid; isolation: isolate; filter: url(#changed); }
.hot > * { grid-area: 1 / 1; }
.hot img + img { mix-blend-mode: difference; }
.empty { margin: 0; padding: 80px 48px; color: var(--dim); text-align: center; }

/* Tools: the view's own control, and any warning about the pair. */
.tools {
  display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 8px 22px;
  min-height: 52px; padding: 10px 20px 0; color: var(--dim);
}
.tools:empty { visibility: hidden; }
.fade { display: flex; align-items: center; gap: 12px; }
.fade span { white-space: nowrap; }
.fade input { width: min(260px, 40vw); accent-color: var(--ink); }
.legend { display: flex; align-items: center; gap: 8px; }
.legend i { width: 10px; height: 10px; border-radius: 3px; background: var(--accent); }
.notice { display: flex; align-items: center; gap: 8px; color: var(--warn); }
.notice::before { content: ""; width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

/* Version strip: B is the filled pill, A the outlined one. */
footer { display: grid; justify-items: center; gap: 6px; padding: 6px 20px 16px; min-width: 0; }
.strip {
  display: flex; gap: 6px; max-width: 100%; margin: 0; padding: 4px; list-style: none;
  overflow-x: auto; scrollbar-width: none;
}
.ver {
  display: flex; align-items: center; gap: 8px; height: 34px; padding: 0 14px 0 12px;
  border-radius: 999px; color: var(--dim); white-space: nowrap;
  box-shadow: inset 0 0 0 1px transparent; transition: background-color .15s, box-shadow .15s, color .15s;
}
.ver:hover:not(:disabled) { background: var(--chip); color: var(--ink); }
.ver:disabled { opacity: .35; cursor: not-allowed; }
.ver b { font-weight: 650; color: var(--ink); opacity: .55; }
.ver .tag {
  display: none; place-items: center; width: 18px; height: 18px; margin-left: -4px; border-radius: 50%;
  font: 700 10px/1 system-ui, sans-serif;
}
.ver.is-a, .ver.is-b { color: var(--ink); }
.ver.is-a b, .ver.is-b b { opacity: 1; }
.ver.is-a .tag, .ver.is-b .tag { display: grid; }
.ver.is-b { background: var(--chip-on); }
.ver.is-b .tag { background: var(--ink); color: var(--ground); }
.ver.is-a { box-shadow: inset 0 0 0 1px rgb(255 255 255 / .2); }
.ver.is-a .tag { box-shadow: inset 0 0 0 1.5px var(--ink); }
.hint { margin: 0; color: var(--faint); font-size: 12px; text-align: center; }
.hint kbd { font: inherit; color: var(--dim); }

@media (max-width: 760px) {
  .top { grid-template-columns: 1fr auto; }
  .routes { grid-column: 1 / -1; grid-row: 2; justify-self: start; overflow-x: auto; max-width: 100%; }
  .seg kbd, .hint { display: none; }
  main { padding: 4px 16px 0; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before { transition: none !important; }
}
</style>
</head>
<body>
<header class="top">
  <div class="brand"><span class="mark" aria-hidden="true"></span><strong>Wipe</strong><span class="run">__RUN__</span></div>
  <nav class="routes seg" id="routes" aria-label="Routes" hidden></nav>
  <div class="modes seg" role="group" aria-label="View">
    <button type="button" data-mode="wipe" aria-keyshortcuts="1">Wipe <kbd>1</kbd></button>
    <button type="button" data-mode="sbs" aria-keyshortcuts="2">Side by side <kbd>2</kbd></button>
    <button type="button" data-mode="onion" aria-keyshortcuts="3">Onion skin <kbd>3</kbd></button>
    <button type="button" data-mode="diff" aria-keyshortcuts="4">Diff <kbd>4</kbd></button>
  </div>
</header>
<main id="main"><div class="frame" id="frame"></div></main>
<div class="tools" id="tools" aria-live="polite"></div>
<footer>
  <ol class="strip" id="strip" aria-label="Versions"></ol>
  <p class="hint">Click a version to compare it, <kbd>Shift</kbd>-click to set the base · <kbd>1</kbd>–<kbd>4</kbd> views · <kbd>←</kbd> <kbd>→</kbd> move the handle</p>
</footer>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <!-- Diff: colour is the accent; alpha is 3 * |B - A| summed over RGB, less .06. A change of
       about 5/255 starts to show and one of about 90/255 is solid, so a tint reads as a wash. -->
  <filter id="changed" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
    <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 .231  0 0 0 0 .545  3 3 3 0 -.06"/>
  </filter>
</svg>
<script type="application/json" id="wipe-data">__DATA__</script>
<script>
__COMPONENT__
</script>
<script>
(() => {
  const data = JSON.parse(document.getElementById('wipe-data').textContent);
  const versions = data.manifest.versions, routes = data.manifest.routes, sizes = data.sizes;
  const state = {a: data.a, b: data.b, route: data.route, mode: 'wipe', pos: 50, fade: 50};
  const $ = id => document.getElementById(id);
  const main = $('main'), frame = $('frame'), tools = $('tools'), strip = $('strip');

  // h('div', {className: 'x', 'aria-label': 'y'}, child, ...): properties when the element has them.
  const h = (tag, props = {}, ...kids) => {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(props)) {
      if (v == null) continue;
      if (k in el && !k.includes('-')) el[k] = v; else el.setAttribute(k, v);
    }
    el.append(...kids.filter(k => k != null));
    return el;
  };
  const label = v => v.note ? `${v.label} · ${v.note}` : v.label;
  const size = rel => sizes[rel] || [1600, 1000];
  const image = (rel, props = {}) => {
    const [w, hgt] = size(rel);
    return h('img', {src: rel, alt: '', draggable: false, style: `aspect-ratio:${w} / ${hgt}`, ...props});
  };
  const pill = (text, side = 'left', swatch) => h('span', {className: `pill ${side}`}, swatch && h('i'), text);

  const slider = h('before-after');
  slider.addEventListener('input', e => { state.pos = e.detail.position; });

  // Modes.
  const modeButtons = [...document.querySelectorAll('[data-mode]')];
  modeButtons.forEach(btn => btn.addEventListener('click', () => setMode(btn.dataset.mode)));
  function setMode(mode) {
    if (mode === state.mode) return;
    state.mode = mode;
    render();
  }

  // Routes.
  const routeNav = $('routes');
  const routeButtons = routes.map(r => {
    const btn = h('button', {type: 'button', textContent: r});
    btn.addEventListener('click', () => { state.route = r; render(); });
    return btn;
  });
  if (routes.length > 1) { routeNav.append(...routeButtons); routeNav.hidden = false; }

  // Version strip: click sets B, Shift-click sets A. Picking the other side swaps them.
  function pick(i, base) {
    if (base) { if (i === state.b) state.b = state.a; state.a = i; }
    else { if (i === state.a) state.a = state.b; state.b = i; }
    render();
  }
  const verButtons = versions.map((v, i) => {
    const when = v.time ? new Date(v.time).toLocaleString(undefined, {dateStyle: 'medium', timeStyle: 'short'}) : '';
    const title = [when, v.sha && v.sha + (v.dirty ? ' with uncommitted changes' : ''), v.method].filter(Boolean).join(' · ');
    const btn = h('button', {type: 'button', className: 'ver', title},
      h('span', {className: 'tag'}), h('b', {textContent: v.label}), v.note ? h('span', {textContent: v.note}) : null);
    btn.addEventListener('click', e => pick(i, e.shiftKey));
    btn.addEventListener('keydown', e => {
      if (e.shiftKey && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); pick(i, true); }
    });
    strip.append(h('li', {}, btn));
    return btn;
  });

  function drawChrome() {
    modeButtons.forEach(b => b.setAttribute('aria-pressed', b.dataset.mode === state.mode));
    routeButtons.forEach((b, i) => b.setAttribute('aria-pressed', routes[i] === state.route));
    verButtons.forEach((btn, i) => {
      const role = i === state.b ? 'B' : i === state.a ? 'A' : '';
      btn.setAttribute('aria-label', label(versions[i]) + (role ? `, ${role}` : ''));
      btn.className = 'ver' + (role ? ' is-' + role.toLowerCase() : '');
      btn.querySelector('.tag').textContent = role;
      btn.setAttribute('aria-pressed', !!role);
      btn.disabled = !(state.route in versions[i].images);
    });
    verButtons[state.b].scrollIntoView({block: 'nearest', inline: 'nearest'});
  }

  function render() {
    const A = versions[state.a], B = versions[state.b];
    const ia = A.images[state.route], ib = B.images[state.route];
    const la = label(A), lb = label(B);
    const scroller = frame.scrollHeight - frame.clientHeight;
    const keep = scroller > 0 ? frame.scrollTop / scroller : 0;
    drawChrome();
    frame.className = 'frame ' + state.mode;
    tools.replaceChildren();

    if (!ia || !ib) {
      frame.replaceChildren(h('p', {className: 'empty', textContent: `${(ia ? B : A).label} has no capture of ${state.route}.`}));
      fit();
      return;
    }
    const [wa, ha] = size(ia), [wb, hb] = size(ib);
    const ratio = `${Math.max(wa, wb)} / ${Math.max(ha, hb)}`, box = `aspect-ratio:${ratio}`;

    if (state.mode === 'wipe') {
      const attrs = {before: ia, after: ib, 'before-label': la, 'after-label': lb, position: state.pos,
                     'aria-label': `Wipe between ${lb} and ${la}`};
      for (const k in attrs) slider.setAttribute(k, attrs[k]);
      slider.style.aspectRatio = ratio;  // Not the style attribute: the component keeps --p there.
      if (slider.parentNode !== frame) frame.replaceChildren(slider);
    } else if (state.mode === 'sbs') {
      frame.replaceChildren(h('div', {className: 'pair'},
        h('div', {className: 'pane'}, image(ib), pill(lb)),
        h('div', {className: 'pane'}, image(ia), pill(la, 'right'))));
    } else if (state.mode === 'onion') {
      const top = image(ib, {className: 'top-img', style: `aspect-ratio:${wb} / ${hb};opacity:${state.fade / 100}`});
      frame.replaceChildren(h('div', {className: 'stack', style: box}, image(ia), top, pill(lb), pill(la, 'right')));
      const range = h('input', {type: 'range', min: 0, max: 100, value: state.fade, id: 'fade',
                                'aria-label': `Opacity of ${lb}`});
      range.addEventListener('input', () => { state.fade = +range.value; top.style.opacity = state.fade / 100; });
      tools.append(h('label', {className: 'fade'}, h('span', {textContent: la}), range, h('span', {textContent: lb})));
    } else {
      frame.replaceChildren(h('div', {className: 'stack', style: box},
        image(ia, {className: 'dim'}),
        h('div', {className: 'hot'}, image(ia), image(ib)),
        pill(`Changed in ${B.label}`, 'left', true)));
      tools.append(h('span', {className: 'legend'}, h('i'), `Pixels that differ between ${A.label} and ${B.label}, over ${A.label} dimmed`));
    }
    if (wa !== wb || ha !== hb) {
      tools.append(h('span', {className: 'notice',
        textContent: `${A.label} is ${wa}×${ha} and ${B.label} is ${wb}×${hb}, so they are aligned at the top.`}));
    }
    fit();
    const after = frame.scrollHeight - frame.clientHeight;
    frame.scrollTop = keep * Math.max(after, 0);
  }

  // Fit the pair in the stage at no more than 1:1 CSS pixels. Tall pairs fit the width and scroll.
  function fit() {
    const A = versions[state.a], B = versions[state.b];
    const ia = A.images[state.route], ib = B.images[state.route];
    const cs = getComputedStyle(main);
    const availW = main.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    const availH = main.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
    frame.style.maxHeight = availH + 'px';
    if (!ia || !ib) { frame.style.width = Math.min(availW, 640) + 'px'; return; }
    const [wa, ha] = size(ia), [wb, hb] = size(ib), sa = A.scale || 1, sb = B.scale || 1;
    const gap = state.mode === 'sbs' ? 16 : 0;
    const w = Math.max(wa / sa, wb / sb) * (gap ? 2 : 1), hgt = Math.max(ha / sa, hb / sb);
    let s = Math.min((availW - gap) / w, availH / hgt, 1);
    if (w * s < 0.6 * Math.min(availW, w)) s = Math.min((availW - gap) / w, 1);
    frame.style.width = Math.floor(w * s + gap) + 'px';
  }
  addEventListener('resize', fit);

  // Keys: 1-4 switch views; arrows, Home and End drive the wipe or the onion fade from anywhere.
  addEventListener('keydown', e => {
    if (e.metaKey || e.ctrlKey || e.altKey || e.target.matches('input, textarea, select')) return;
    const mode = {1: 'wipe', 2: 'sbs', 3: 'onion', 4: 'diff'}[e.key];
    if (mode) { setMode(mode); return; }
    if (e.target !== document.body) return;
    const step = e.shiftKey ? 10 : 2;
    const move = {ArrowLeft: -step, ArrowRight: step, Home: -1e3, End: 1e3}[e.key];
    if (!move) return;
    e.preventDefault();
    if (state.mode === 'wipe' && slider.isConnected) {
      slider.move(state.pos + move);
      slider.focus({preventScroll: true});
    } else if (state.mode === 'onion') {
      const range = $('fade');
      range.value = Math.min(100, Math.max(0, state.fade + move));
      range.dispatchEvent(new Event('input'));
      range.focus();
    }
  });

  render();
})();
</script>
</body>
</html>
"""
