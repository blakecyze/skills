"""Browser capture for Wipe: headless Chrome or Playwright. Standard library only at import time."""

from __future__ import annotations

import importlib.util
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

PATH_NAMES = ("google-chrome", "chromium", "chromium-browser", "microsoft-edge", "brave-browser")
MAC_APPS = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
)
# Headless Chrome follows the system scheme unless told, so both themes pass a flag.
DARK_FLAG = "--blink-settings=preferredColorScheme=0"
LIGHT_FLAG = "--blink-settings=preferredColorScheme=1"
CHROME_TIMEOUT = 60


class CaptureError(Exception):
    pass


def find_chrome(env: dict, platform: str):
    """Path to a Chromium-family browser, or None."""
    for name in PATH_NAMES:
        found = shutil.which(name, path=env.get("PATH", ""))
        if found:
            return found
    if platform == "darwin":
        for p in MAC_APPS:
            if os.access(p, os.X_OK):
                return p
    return None


def chrome_command(chrome: str, url: str, out: Path, viewport, scale: int, theme: str,
                   profile: Path) -> list:
    cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           f"--force-device-scale-factor={scale}",
           f"--window-size={viewport[0]},{viewport[1]}",
           "--virtual-time-budget=3000",
           f"--user-data-dir={profile}"]
    cmd.append(DARK_FLAG if theme == "dark" else LIGHT_FLAG)
    cmd += [f"--screenshot={out}", url]
    return cmd


def _has_playwright() -> bool:
    return importlib.util.find_spec("playwright") is not None


def _run_chrome(cmd: list) -> None:
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=CHROME_TIMEOUT)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise CaptureError(f"Chrome did not run: {e}")
    if done.returncode != 0:
        raise CaptureError(f"Chrome exited {done.returncode}: {done.stderr.strip()[-300:]}")


def _chrome_capture(url, out, viewport, theme, scale):
    chrome = find_chrome(os.environ, sys.platform)
    if not chrome:
        raise CaptureError("No Chrome, Chromium, Edge or Brave found. Install one, or use --image.")
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="wipe-chrome-") as profile:
        _run_chrome(chrome_command(chrome, url, out, viewport, scale, theme, Path(profile)))
    if not out.is_file():
        raise CaptureError(f"Chrome produced no screenshot for {url}.")


def _playwright_capture(url, out, viewport, theme, scale, full):
    from playwright.sync_api import Error as PlaywrightError
    try:
        _playwright_capture_raw(url, out, viewport, theme, scale, full)
    except PlaywrightError as e:
        raise CaptureError(f"Playwright failed for {url}: {str(e).strip().splitlines()[0]}")


def _playwright_capture_raw(url, out, viewport, theme, scale, full):
    from playwright.sync_api import sync_playwright
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome(os.environ, sys.platform)
    with sync_playwright() as p:
        browser = p.chromium.launch(**({"executable_path": chrome} if chrome else {}))
        try:
            ctx = browser.new_context(viewport={"width": viewport[0], "height": viewport[1]},
                                      device_scale_factor=scale, color_scheme=theme,
                                      reduced_motion="reduce")
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.screenshot(path=str(out), full_page=full, animations="disabled")
        finally:
            browser.close()


def capture(url: str, out: Path, viewport, theme, scale=2, method="auto", full=False) -> str:
    """Screenshot url to out. Returns the method used."""
    if method == "playwright" or (method == "auto" and (full or _has_playwright())):
        if _has_playwright():
            _playwright_capture(url, out, viewport, theme, scale, full)
            return "playwright"
        if method == "playwright":
            raise CaptureError("Playwright is not installed.")
    if full:
        print("warning: full-page needs Playwright; captured the viewport", file=sys.stderr)
    _chrome_capture(url, out, viewport, theme, scale)
    return "chrome"


def measure(url: str, viewport, runs=3) -> dict:
    """Median transfer size, requests, DOM nodes and LCP over several loads. Needs Playwright."""
    from playwright.sync_api import Error as PlaywrightError
    try:
        return _measure_raw(url, viewport, runs)
    except PlaywrightError as e:
        raise CaptureError(f"Playwright failed for {url}: {str(e).strip().splitlines()[0]}")


def _measure_raw(url, viewport, runs):
    from playwright.sync_api import sync_playwright
    script = """async () => {
      const lcp = await new Promise(res => {
        let v = 0;
        try {
          new PerformanceObserver(l => { for (const e of l.getEntries()) v = e.startTime; })
            .observe({type: 'largest-contentful-paint', buffered: true});
        } catch (e) {}
        setTimeout(() => res(v), 500);
      });
      const res = performance.getEntriesByType('resource');
      const nav = performance.getEntriesByType('navigation');
      const size = [...res, ...nav].reduce((a, e) => a + (e.transferSize || 0), 0);
      return {kb: size / 1024, requests: res.length + nav.length,
              nodes: document.querySelectorAll('*').length, lcp};
    }"""
    samples = []
    with sync_playwright() as p:
        chrome = find_chrome(os.environ, sys.platform)
        browser = p.chromium.launch(**({"executable_path": chrome} if chrome else {}))
        try:
            for _ in range(runs):
                ctx = browser.new_context(viewport={"width": viewport[0], "height": viewport[1]})
                page = ctx.new_page()
                page.goto(url, wait_until="networkidle")
                samples.append(page.evaluate(script))
                ctx.close()
        finally:
            browser.close()

    def med(key):
        return statistics.median(s[key] for s in samples)
    return {"transfer_kb": round(med("kb"), 1), "requests": int(med("requests")),
            "dom_nodes": int(med("nodes")), "lcp_ms": round(med("lcp")),
            "host": urlparse(url).netloc or "local file", "runs": runs}
