#!/usr/bin/env python3
"""Compare what was asked with what changed, show it, and undo the parts nobody asked for.

  unasked.py collect [--base REF]    number every changed hunk
  unasked.py show h3                 print one hunk in full
  unasked.py render ITEMS.json       check the classification, write the report
  unasked.py cut 2 3                 reverse those items in the working tree, saving an undo patch
  unasked.py undo                    put back the last cut

Files live in the repo's git directory, or a temp folder if that is protected, so nothing here appears in a diff. Python 3.9+ and git only.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
import webbrowser
from pathlib import Path

LOCKFILE = re.compile(r"(^|/)(package-lock\.json|pnpm-lock\.yaml|yarn\.lock|bun\.lockb?|Cargo\.lock|poetry\.lock|uv\.lock|Gemfile\.lock|composer\.lock|go\.sum|Podfile\.lock|pubspec\.lock)$")
HUNK = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")
KINDS = {"removed": 0, "behaviour": 1, "added": 2, "drive-by": 3, "decision": 4}
IMPACTS = {"high": 0, "med": 1, "low": 2}
PRINT_LIMIT = 1500
TEMPLATE = Path(__file__).with_name("report.html")


def run(*args, check=True, ok=(0,)):
    done = subprocess.run(args, cwd=ROOT, capture_output=True)
    if check and done.returncode not in ok:
        sys.exit(f"{' '.join(args[:3])} failed: {done.stderr.decode(errors='replace').strip()}")
    return done.stdout.decode(errors="surrogateescape")


top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
if top.returncode:
    sys.exit("unasked needs a git repository")
ROOT = Path(top.stdout.strip())


def writable_store():
    """The git directory keeps this out of every diff. Sandboxes that protect it get a temp folder per repo."""
    store = Path(run("git", "rev-parse", "--absolute-git-dir").strip()) / "unasked"
    try:
        store.mkdir(exist_ok=True)
        (store / ".probe").touch()
        (store / ".probe").unlink()
    except OSError:
        store = Path(tempfile.gettempdir()) / ("unasked-" + hashlib.sha1(str(ROOT).encode()).hexdigest()[:12])
        store.mkdir(exist_ok=True)
    return store


STORE = writable_store()
GIT_DIFF = ("git", "-c", "core.quotepath=off", "diff", "--no-color", "--no-ext-diff", "--no-renames", "--binary", "-U1")


def resolve_base(requested):
    if requested:
        return requested, run("git", "rev-parse", requested + "^{commit}").strip()
    head = run("git", "rev-parse", "--verify", "-q", "HEAD", check=False).strip()
    if not head:
        return "(no commits)", run("git", "hash-object", "-t", "tree", "/dev/null").strip()
    origin = run("git", "symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD", check=False).strip()
    for ref in filter(None, (origin, "origin/main", "main", "origin/master", "master")):
        base = run("git", "merge-base", "HEAD", ref, check=False).strip()
        if base:
            return ref, base
    return "HEAD", head


def parse_sections(text):
    """Split a diff into file sections: header lines plus hunks, keeping raw text so a cut can replay it."""
    sections, current, hunk = [], None, None
    for line in text.split("\n"):
        if line.startswith("diff --git ") or line.startswith("diff --no-index"):
            current = {"header": [line], "hunks": [], "path": None, "raw": [line]}
            sections.append(current)
            hunk = None
            continue
        if current is None:
            continue
        current["raw"].append(line)
        match = HUNK.match(line)
        if match:
            hunk = {"old": int(match[1]), "new": int(match[2]), "lines": []}
            current["hunks"].append(hunk)
        elif hunk is not None:
            if line[:1] in (" ", "+", "-", "\\"):
                hunk["lines"].append(line)
        else:
            current["header"].append(line)
    for section in sections:
        # A binary patch ends at a blank line, and git apply needs it.
        raw = "\n".join(section["raw"]).rstrip("\n")
        section["raw"] = raw + ("\n\n" if "GIT binary patch" in raw else "\n")
        for line in section["header"]:
            if line.startswith("+++ ") and line[4:] != "/dev/null":
                section["path"] = line[4:].split("\t")[0].removeprefix("b/")
            elif line.startswith("--- ") and line[4:] != "/dev/null" and not section["path"]:
                section["path"] = line[4:].split("\t")[0].removeprefix("a/")
        if not section["path"]:
            match = re.match(r"diff --git a/(.*) b/\1$", section["header"][0])
            section["path"] = match[1] if match else section["header"][0].split(" b/")[-1]
        section["new_file"] = any(h.startswith("new file mode") or h == "--- /dev/null" for h in section["header"])
    return sections


def numbered(hunk):
    """Yield (new-file line number or None, line)."""
    new = hunk["new"]
    for line in hunk["lines"]:
        if line.startswith("-") or line.startswith("\\"):
            yield None, line
        else:
            yield new, line
            new += 1


def cmd_collect(args):
    label, base = resolve_base(args.base)
    text = run(*GIT_DIFF, base)
    for path in filter(None, run("git", "ls-files", "-o", "--exclude-standard", "-z").split("\0")):
        text += run(*GIT_DIFF[:3], "diff", "--no-color", "--no-ext-diff", "--no-renames", "--binary", "-U1", "--no-index", "/dev/null", path, ok=(0, 1))
    sections = parse_sections(text)
    hunks, count = [], 0
    for index, section in enumerate(sections):
        parts = section["hunks"] or [None]
        for part in parts:
            count += 1
            added = sum(l.startswith("+") for l in part["lines"]) if part else 0
            removed = sum(l.startswith("-") for l in part["lines"]) if part else 0
            hunks.append({"id": f"h{count}", "section": index, "path": section["path"], "added": added, "removed": removed, "old": part["old"] if part else 0, "new": part["new"] if part else 0, "lines": part["lines"] if part else [], "whole_file": part is None, "noise": bool(LOCKFILE.search(section["path"]))})
    state = {"base": base, "base_label": label, "branch": run("git", "branch", "--show-current").strip() or "(detached)", "sections": [{"path": s["path"], "header": s["header"], "raw": s["raw"], "new_file": s["new_file"]} for s in sections], "hunks": hunks}
    (STORE / "hunks.json").write_text(json.dumps(state, ensure_ascii=True))
    total = sum(h["added"] + h["removed"] for h in hunks if not h["noise"])
    print(f"base {base[:8]} ({label}) on {state['branch']}: {len(sections)} files, {len(hunks)} hunks, {total} changed lines")
    if not hunks:
        print("No changes against this base. Pass --base REF to compare with something else.")
        return
    long_form = sum(len(h["lines"]) for h in hunks) <= PRINT_LIMIT
    for hunk in hunks:
        print(f"\n{hunk['id']} {hunk['path']} +{hunk['added']} -{hunk['removed']}" + (" (whole file: binary, mode, or empty)" if hunk["whole_file"] else "") + (" (lockfile: not counted)" if hunk["noise"] else ""))
        if hunk["noise"]:
            continue
        print_hunk(hunk, None if long_form else 30)


def print_hunk(hunk, limit):
    rows = list(numbered(hunk))
    for number, line in rows[:limit]:
        print(f"{number or '':>5} {line}")
    if limit and len(rows) > limit:
        print(f"      ... {len(rows) - limit} more lines: unasked.py show {hunk['id']}")


def load_state():
    path = STORE / "hunks.json"
    if not path.exists():
        sys.exit("Run collect first.")
    return json.loads(path.read_text())


def cmd_show(args):
    state = load_state()
    by_id = {h["id"]: h for h in state["hunks"]}
    for hunk_id in args.hunks:
        if hunk_id not in by_id:
            sys.exit(f"no hunk {hunk_id}")
        print(f"{hunk_id} {by_id[hunk_id]['path']}")
        print_hunk(by_id[hunk_id], None)


def parse_ref(ref, by_id, errors):
    """'h3' or 'h3:17-21' (new-file lines) -> (hunk, set of line positions it selects)."""
    match = re.fullmatch(r"(h\d+)(?::(\d+)(?:-(\d+))?)?", ref)
    if not match or match[1] not in by_id:
        errors.append(f"unknown hunk reference: {ref}")
        return None, set()
    hunk = by_id[match[1]]
    if match[2] is None:
        return hunk, set(range(len(hunk["lines"])))
    low, high = int(match[2]), int(match[3] or match[2])
    rows = list(numbered(hunk))
    chosen = {i for i, (number, line) in enumerate(rows) if number and low <= number <= high and line.startswith("+")}
    if not chosen:
        errors.append(f"{ref} selects no added lines")
        return hunk, chosen
    # A removal directly above a selected addition is what that addition replaced.
    for i in sorted(chosen):
        j = i - 1
        while j >= 0 and rows[j][1].startswith(("-", "\\")):
            chosen.add(j)
            j -= 1
    return hunk, chosen


def changed_positions(hunk):
    return {i for i, line in enumerate(hunk["lines"]) if line.startswith(("+", "-"))}


def squeeze(text):
    return " ".join(text.split()).lower()


def classify(state, data):
    """Every changed line must be traced to the request or named as unasked. Returns claims or exits with every problem."""
    errors = []
    by_id = {h["id"]: h for h in state["hunks"]}
    asks = data.get("ask") or []
    if isinstance(asks, str):
        asks = [asks]
    if not any(a.strip() for a in asks):
        errors.append("ask: quote the user's own words")
    ask_text = squeeze(" ".join(asks))
    claims = {}

    def claim(refs, owner, overlay=False):
        for ref in refs:
            hunk, chosen = parse_ref(ref, by_id, errors)
            if hunk is None or overlay:
                continue
            for position in chosen & changed_positions(hunk) or ({-1} if hunk["whole_file"] else set()):
                existing = claims.get((hunk["id"], position))
                if existing and existing != owner:
                    errors.append(f"{ref}: claimed twice ({existing} and {owner})")
                claims[(hunk["id"], position)] = owner

    for entry in data.get("asked") or []:
        kind = entry.get("kind", "asked")
        if kind not in ("asked", "needed"):
            errors.append(f"asked entry {entry.get('hunks')}: kind must be asked or needed")
        quote = entry.get("quote", "")
        if not quote or squeeze(quote) not in ask_text:
            errors.append(f"asked entry {entry.get('hunks')}: quote must be verbatim from ask, got {quote!r}")
        if kind == "needed" and not entry.get("because"):
            errors.append(f"needed entry {entry.get('hunks')}: say why the request fails without it")
        claim(entry.get("hunks") or [], kind)
    items = data.get("items") or []
    for index, item in enumerate(items):
        name = item.get("title") or f"item {index + 1}"
        for field in ("title", "why"):
            if not item.get(field):
                errors.append(f"{name}: {field} is required")
        if item.get("kind") not in KINDS:
            errors.append(f"{name}: kind must be one of {', '.join(KINDS)}")
        if item.get("impact") not in IMPACTS:
            errors.append(f"{name}: impact must be high, med, or low")
        if not item.get("hunks"):
            errors.append(f"{name}: cite the hunks it comes from")
        claim(item.get("hunks") or [], f"item:{index}", overlay=item.get("kind") == "decision")
    for hunk in state["hunks"]:
        if hunk["noise"]:
            continue
        positions = changed_positions(hunk) or {-1}
        loose = sorted(p for p in positions if (hunk["id"], p) not in claims)
        if loose:
            rows = list(numbered(hunk))
            lines = [rows[p][0] for p in loose if p >= 0 and rows[p][0]]
            where = f" (new lines {min(lines)}-{max(lines)})" if lines else ""
            errors.append(f"{hunk['id']} {hunk['path']}{where}: not classified. Trace it to a quote or name it as unasked")
    if errors:
        sys.exit("Fix the classification, then render again:\n- " + "\n- ".join(errors))
    return asks, items, claims


def evidence(state, refs):
    by_id = {h["id"]: h for h in state["hunks"]}
    shown = []
    for ref in refs:
        hunk, chosen = parse_ref(ref, by_id, [])
        rows = list(numbered(hunk))
        near = {i + step for i in chosen for step in (-1, 0, 1)}
        shown.append({"path": hunk["path"], "ref": ref, "rows": [{"n": n, "t": line[:400], "on": i in chosen} for i, (n, line) in enumerate(rows) if i in near] if rows else [{"n": None, "t": "(whole file: binary, mode, or empty)", "on": True}]})
    return shown


def cmd_render(args):
    state = load_state()
    data = json.loads(Path(args.items).read_text())
    asks, items, claims = classify(state, data)
    order = sorted(range(len(items)), key=lambda i: (KINDS[items[i]["kind"]] == KINDS["decision"], IMPACTS[items[i]["impact"]], KINDS[items[i]["kind"]]))
    numbers = {index: rank + 1 for rank, index in enumerate(order)}

    totals = {"asked": 0, "needed": 0, "unasked": 0}
    item_lines = {i: 0 for i in range(len(items))}
    files = {}
    for hunk in state["hunks"]:
        if hunk["noise"]:
            continue
        row = files.setdefault(hunk["path"], {"path": hunk["path"], "chunks": [], "unasked": 0, "total": 0})
        previous = None
        for position in sorted(changed_positions(hunk)) or [-1]:
            owner = claims[(hunk["id"], position)]
            if owner.startswith("item:"):
                index = int(owner[5:])
                cls, n = "unasked", numbers[index]
                item_lines[index] += 1
            else:
                cls, n = owner, None
            totals[cls] += 1
            row["total"] += 1
            row["unasked"] += cls == "unasked"
            if previous and previous["cls"] == cls and previous["item"] == n:
                previous["lines"] += 1
            else:
                previous = {"cls": cls, "item": n, "lines": 1}
                row["chunks"].append(previous)
    resolved = []
    for index in order:
        item = items[index]
        resolved.append({
            "n": numbers[index],
            "title": item["title"],
            "kind": item["kind"],
            "impact": item["impact"],
            "why": item["why"],
            "question": item.get("question", ""),
            "lines": item_lines[index],
            "hunks": item["hunks"],
            "cuttable": item["kind"] != "decision",
            "evidence": evidence(state, item["hunks"]),
        })
    report = {
        "ask": asks,
        "branch": state["branch"],
        "base": state["base_label"],
        "baseSha": state["base"][:8],
        "totals": totals,
        "files": sorted(files.values(), key=lambda f: (-f["unasked"], -f["total"])),
        "items": resolved,
        "asked": [{"kind": e.get("kind", "asked"), "quote": e["quote"], "because": e.get("because", ""), "hunks": e["hunks"], "paths": sorted({r.split(":")[0] for r in e["hunks"]})} for e in data.get("asked") or []],
    }
    by_id = {h["id"]: h["path"] for h in state["hunks"]}
    for entry in report["asked"]:
        entry["paths"] = sorted({by_id[h] for h in entry["paths"]})
    (STORE / "items.json").write_text(json.dumps(resolved, ensure_ascii=True))
    total = sum(totals.values())
    if not resolved:
        print(f"Nothing unasked: all {total} changed lines trace to the request. No report written.")
        return
    payload = json.dumps(report, ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    out = STORE / "report.html"
    out.write_text(TEMPLATE.read_text().replace("/*DATA*/null", payload))
    share = round(100 * totals["unasked"] / total) if total else 0
    print(f"{totals['unasked']} of {total} changed lines ({share}%) were not asked for. {totals['asked']} asked, {totals['needed']} needed.")
    for item in resolved:
        size = f"{item['lines']} lines" if item["cuttable"] else "inside requested work"
        print(f"{item['n']}. [{item['impact']}] {item['kind']}: {item['title']} ({size})")
    print(f"report: {out}")
    if not args.no_open:
        webbrowser.open(out.as_uri())


def patch_for(state, refs):
    """Build a patch of the selected hunks. Unselected additions become context, unselected removals vanish."""
    by_id = {h["id"]: h for h in state["hunks"]}
    errors = []
    selected = {}
    for ref in refs:
        hunk, chosen = parse_ref(ref, by_id, errors)
        if hunk:
            selected.setdefault(hunk["id"], set()).update(chosen)
    if errors:
        sys.exit("\n".join(errors))
    out = []
    for index, section in enumerate(state["sections"]):
        hunks = [h for h in state["hunks"] if h["section"] == index and h["id"] in selected]
        if not hunks:
            continue
        whole = all(selected[h["id"]] >= changed_positions(h) for h in hunks) and len(hunks) == sum(h["section"] == index for h in state["hunks"])
        if hunks[0]["whole_file"] or (whole and section["new_file"]):
            out.append(section["raw"])
            continue
        header = section["header"]
        if section["new_file"]:
            # Only part of a new file is going, so the file itself stays: patch it as a modification.
            path = section["path"]
            header = [header[0], f"--- a/{path}", f"+++ b/{path}"]
        out.append("\n".join(header) + "\n")
        for hunk in hunks:
            chosen = selected[hunk["id"]]
            body, previous_kept = [], True
            for i, line in enumerate(hunk["lines"]):
                if line.startswith("\\"):
                    if previous_kept:
                        body.append(line)
                elif line.startswith("+") and i not in chosen:
                    body.append(" " + line[1:])
                    previous_kept = True
                elif line.startswith("-") and i not in chosen:
                    previous_kept = False
                else:
                    body.append(line)
                    previous_kept = True
            old = sum(not l.startswith(("+", "\\")) for l in body)
            new = sum(not l.startswith(("-", "\\")) for l in body)
            out.append(f"@@ -{hunk['old'] if not section['new_file'] else hunk['new']},{old} +{hunk['new']},{new} @@\n" + "\n".join(body) + "\n")
    return "".join(out)


def apply_patch(patch_path, reverse):
    flags = ["--recount", "--whitespace=nowarn"] + (["-R"] if reverse else [])
    check = subprocess.run(["git", "apply", "--check", *flags, str(patch_path)], cwd=ROOT, capture_output=True, text=True)
    if check.returncode:
        return check.stderr.strip()
    subprocess.run(["git", "apply", *flags, str(patch_path)], cwd=ROOT, check=True, capture_output=True)
    return ""


def cmd_cut(args):
    state = load_state()
    path = STORE / "items.json"
    if not path.exists():
        sys.exit("Run render first.")
    items = {str(item["n"]): item for item in json.loads(path.read_text())}
    refs = []
    for number in args.items:
        if number not in items:
            sys.exit(f"no item {number}")
        if not items[number]["cuttable"]:
            sys.exit(f"item {number} is a decision inside requested work. Change it by hand; nothing was cut.")
        refs += items[number]["hunks"]
    patch = patch_for(state, refs)
    undo_dir = STORE / "undo"
    undo_dir.mkdir(exist_ok=True)
    undo = undo_dir / f"{time.strftime('%Y%m%d-%H%M%S')}-{'-'.join(args.items)}.patch"
    undo.write_text(patch, errors="surrogateescape")
    failure = apply_patch(undo, reverse=True)
    if failure:
        undo.unlink()
        sys.exit(f"Nothing was cut: those lines no longer match, so collect and classify again.\n{failure}")
    print(f"cut {', '.join(args.items)}. Uncommitted in the working tree; history untouched.")
    print(f"undo patch: {undo}")


def cmd_undo(args):
    undo_dir = STORE / "undo"
    patches = sorted(undo_dir.glob("*.patch"), key=lambda p: p.stat().st_mtime) if undo_dir.exists() else []
    if not patches:
        sys.exit("Nothing to undo.")
    failure = apply_patch(patches[-1], reverse=False)
    if failure:
        sys.exit(f"Could not undo, because those lines have changed since. Patch kept at {patches[-1]}.\n{failure}")
    patches[-1].rename(patches[-1].with_suffix(".restored"))
    print(f"restored from {patches[-1].name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    collect = commands.add_parser("collect")
    collect.add_argument("--base")
    show = commands.add_parser("show")
    show.add_argument("hunks", nargs="+")
    render = commands.add_parser("render")
    render.add_argument("items")
    render.add_argument("--no-open", action="store_true")
    cut = commands.add_parser("cut")
    cut.add_argument("items", nargs="+")
    commands.add_parser("undo")
    args = parser.parse_args()
    {"collect": cmd_collect, "show": cmd_show, "render": cmd_render, "cut": cmd_cut, "undo": cmd_undo}[args.command](args)


if __name__ == "__main__":
    main()
