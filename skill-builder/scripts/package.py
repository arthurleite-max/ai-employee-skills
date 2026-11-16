#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Skill Builder package audit: checks a skill folder before release and builds the zip only when it is
clean. Python 3.8+, standard library only, no internet. It reads the folder and writes one zip file.

  python package.py path/to/my-skill [--forbid forbid.txt] [--words words.txt] [--max-paste 8000]
                    [--max-desc 1024] [-o my-skill.zip] [--check-only]

Blocking (no zip): missing required files · unfinished to-do markers (the word TODO followed by a colon) · name in SKILL.md different from the folder or not kebab-case ·
description too long or missing · compact edition too long · a file cited in SKILL.md that does not exist ·
control characters · secrets (API keys, private keys, tokens) · local paths (C:\\Users, /home/, /Users/) ·
forbidden terms (--forbid: one regular expression per line, e.g. internal names, real clients, test data) ·
leftover words (--words: one regular expression per line, e.g. words of a language the skill must not
contain) · scripts importing modules outside the Python standard library.
Warnings: no TUTORIAL.html · scripts that can reach the network · emails or phone numbers outside .example
domains · total size above 5 MB. Caches (__pycache__, .DS_Store) are never packed.
"""
import argparse, os, re, sys, zipfile

REQUIRED = ["SKILL.md", "README.md", "setup.md", "PASTE-INTO-ANY-AI.md", "INSTALL.md", "LICENSE.md", "CREDITS.md"]
TEXT = {".md", ".py", ".html", ".txt", ".json", ".csv", ".yml", ".yaml", ".js", ".css", ".sh"}
SKIP = {"__pycache__", ".DS_Store", ".git", ".venv", "node_modules"}
SECRETS = [r"sk-[A-Za-z0-9_-]{20,}", r"AKIA[0-9A-Z]{16}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"ghp_[A-Za-z0-9]{30,}",
           r"xox[baprs]-[A-Za-z0-9-]{10,}", r"AIza[0-9A-Za-z_-]{35}", r"(?i)\b(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"]
LOCAL = [r"[A-Za-z]:[\\/]Users[\\/]", r"/home/[a-z]", r"/Users/[A-Za-z]"]
NET = re.compile(r"^\s*(import|from)\s+(urllib|http|socket|requests|httpx|aiohttp|smtplib|ftplib)\b", re.M)
EMAIL = re.compile(r"[\w.+-]+@([\w-]+\.)+[a-z]{2,}", re.I)
PHONE = re.compile(r"(?<![\w.])\+?\d[\d ()-]{8,}\d(?![\w.])")
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
STDLIB = set(getattr(sys, "stdlib_module_names", ())) or {
    "argparse", "csv", "io", "json", "re", "sys", "os", "unicodedata", "datetime", "math", "statistics", "zipfile",
    "pathlib", "html", "collections", "itertools", "functools", "calendar", "subprocess", "shutil", "string",
    "textwrap", "random", "hashlib", "base64", "time", "typing", "dataclasses", "decimal", "fractions", "glob",
    "struct", "xml", "urllib", "http", "socket", "smtplib", "email", "tempfile", "copy", "uuid", "logging"}


def lines(path):
    if not path:
        return []
    return [l.strip() for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#")]


def files(root):
    for d, dirs, fs in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP]
        for f in fs:
            if f not in SKIP:
                yield os.path.join(d, f)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder"); ap.add_argument("--forbid"); ap.add_argument("--words")
    ap.add_argument("--max-paste", type=int, default=8000); ap.add_argument("--max-desc", type=int, default=1024)
    ap.add_argument("-o", "--output"); ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.folder)
    name = os.path.basename(root.rstrip("\\/"))
    block, warn = [], []
    for r in REQUIRED:
        if not os.path.isfile(os.path.join(root, r)):
            block.append(f"missing {r}")
    if not os.path.isfile(os.path.join(root, "TUTORIAL.html")):
        warn.append("no TUTORIAL.html (recommended for non-technical users)")
    desc = ""
    sk = os.path.join(root, "SKILL.md")
    if os.path.isfile(sk):
        txt = open(sk, encoding="utf-8").read()
        m = re.match(r"---\s*\n(.*?)\n---", txt, re.S)
        if not m:
            block.append("SKILL.md has no front matter (--- name / description ---)")
        else:
            fm = m.group(1)
            n = re.search(r"^name:\s*(\S+)\s*$", fm, re.M)
            if not n or n.group(1) != name:
                block.append(f"SKILL.md name must be the folder name '{name}'")
            if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
                block.append(f"folder name '{name}' must be kebab-case (lowercase, digits, hyphens)")
            d = re.search(r"^description:\s*>?\s*\n?(.*?)(?=^\w[\w-]*:|\Z)", fm, re.M | re.S)
            desc = " ".join(d.group(1).split()) if d else ""
            if not desc:
                block.append("SKILL.md description is missing")
            elif len(desc) > a.max_desc:
                block.append(f"SKILL.md description has {len(desc)} characters (max {a.max_desc})")
        for ref in sorted(set(re.findall(r"`((?:reference|templates|assets|scripts)/[^`\s]+)`", txt))):
            if not os.path.exists(os.path.join(root, ref)):
                block.append(f"SKILL.md cites {ref}, which does not exist")
    paste = os.path.join(root, "PASTE-INTO-ANY-AI.md")
    n_paste = len(open(paste, encoding="utf-8").read()) if os.path.isfile(paste) else 0
    if n_paste > a.max_paste:
        block.append(f"PASTE-INTO-ANY-AI.md has {n_paste} characters (max {a.max_paste})")
    forbid = [re.compile(x) for x in lines(a.forbid)]
    words = [re.compile(x, re.I) for x in lines(a.words)]
    total = 0
    for p in files(root):
        rel = os.path.relpath(p, root).replace("\\", "/")
        total += os.path.getsize(p)
        if os.path.splitext(p)[1].lower() not in TEXT:
            continue
        t = open(p, encoding="utf-8", errors="ignore").read()
        where = lambda i: f"{rel}:{t.count(chr(10), 0, i) + 1}"
        if rel != "scripts/new_skill.py":
            for m in re.finditer(r"\bTO" + r"DO:", t):  # split so this file does not match itself
                block.append(f"{where(m.start())}: unfinished to-do marker")
                break
        if CTRL.search(t):
            block.append(f"{rel}: control character (for example a backspace where \\b was meant)")
        for rx in SECRETS:
            for m in re.finditer(rx, t):
                block.append(f"{where(m.start())}: looks like a secret")
        for rx in LOCAL:
            for m in re.finditer(rx, t):
                block.append(f"{where(m.start())}: local path '{m.group(0)}'")
        for rx in forbid + words:
            for m in rx.finditer(t):
                block.append(f"{where(m.start())}: '{m.group(0)}' ({'forbidden term' if rx in forbid else 'leftover word'})")
        if rel.endswith(".py"):
            for m in re.finditer(r"^\s*(?:import\s+([\w.]+(?:\s*,\s*[\w.]+)*)|from\s+([\w.]+)\s+import)", t, re.M):
                mods = (m.group(1) or m.group(2)).split(",")
                for mod in mods:
                    top = mod.strip().split(".")[0]
                    if top and not top.startswith("_") and top not in STDLIB:
                        block.append(f"{where(m.start())}: imports '{top}', which is not in the Python standard library")
            if NET.search(t):
                warn.append(f"{rel}: can reach the network; say so in SKILL.md and README")
        for m in EMAIL.finditer(t):
            if not m.group(0).lower().endswith((".example", "example.com", "example.org")) and "noreply" not in m.group(0):
                warn.append(f"{where(m.start())}: email '{m.group(0)}' (use a .example domain in examples)")
        if rel.endswith((".md", ".html", ".txt", ".csv")):
            for m in PHONE.finditer(t):
                digits = re.sub(r"\D", "", m.group(0))
                placeholder = digits.count("0") * 2 >= len(digits) or "555" in m.group(0) or re.fullmatch(r"(\d)\1+", digits)
                if 10 <= len(digits) <= 13 and not placeholder and not re.search(r"\d{4}-\d{2}-\d{2}", m.group(0)):
                    warn.append(f"{where(m.start())}: phone-like number '{m.group(0).strip()}' (use fictional numbers)")
    if total > 5 * 1024 * 1024:
        warn.append(f"total size {total / 1024 / 1024:.1f} MB (keep skills small)")
    print(f"# Package audit · {name}")
    print(f"description {len(desc)}/{a.max_desc} characters · compact edition {n_paste}/{a.max_paste} characters · {total / 1024:.0f} KB")
    print(f"\nBlocking: {len(block)}")
    for b in block:
        print(f"- {b}")
    print(f"\nWarnings: {len(warn)}")
    for w in dict.fromkeys(warn):
        print(f"- {w}")
    if block:
        print("\nNot packed: fix the blocking items first.")
        sys.exit(1)
    if a.check_only:
        print("\nClean (check only).")
        return
    out = a.output or os.path.join(os.path.dirname(root), name + ".zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files(root)):
            z.write(p, name + "/" + os.path.relpath(p, root).replace("\\", "/"))
    print(f"\nPacked {out}")


if __name__ == "__main__":
    main()
