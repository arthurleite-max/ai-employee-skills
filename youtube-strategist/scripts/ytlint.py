#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""YouTube Strategist helper. Python 3.8+, standard library only, no internet.

  python ytlint.py outliers videos.csv [--today YYYY-MM-DD] [--min 3.0] [--json out.json]
  python ytlint.py titles titles.txt [--thumb "THUMB TEXT"]
  python ytlint.py title "One title" [--thumb "THUMB TEXT"]

videos.csv: one row per video. Columns matched loosely (English or Portuguese):
channel/canal, subscribers/inscritos, title/titulo, views/visualizacoes, date/data (YYYY-MM-DD or
DD/MM/YYYY), format/formato (long/short; optional). Numbers like 1.200.000 or 1,200,000 are fine.
"""
import argparse, csv, io, json, re, statistics, sys
from collections import defaultdict
from datetime import date, datetime

COLS = {"channel": ["channel", "canal"], "subs": ["subscribers", "subs", "inscritos"],
        "title": ["title", "titulo", "título"], "views": ["views", "visualizacoes", "visualizações", "views count"],
        "date": ["date", "data", "published", "publicado"], "format": ["format", "formato", "type", "tipo"]}
HYPE = r"\b(insane|insano|insana|absurdo|crazy|shocking|you won't believe|hack|segredo|ninguém te conta|inacreditável|chocante|milagre|miracle)\b"
FAKE_PROOF = r"(\d[\d.,]*\s*(mi|mil|k|m|million|milhão|milhões)?\s*(views|visualiza)|aprovad[oa] por|approved by|recomendad[oa] por|garantid|guaranteed|doctors hate|médicos odeiam)"


def num(s):
    s = re.sub(r"[^\d.,]", "", str(s or ""))
    if not s:
        return 0.0
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", s):
        return float(re.sub(r"[.,]", "", s))
    return float(s.replace(",", "."))


def pdate(s):
    s = str(s).strip()
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y", "%m/%d/%Y"):
        try:
            return datetime.strptime(s, f).date()
        except ValueError:
            pass
    return None


def outliers(path, today, k):
    raw = open(path, encoding="utf-8-sig", errors="replace").read()
    sep = max([",", ";", "\t"], key=lambda c: raw.splitlines()[0].count(c))
    rows = list(csv.DictReader(io.StringIO(raw), delimiter=sep))
    head = {h: h.strip().lower() for h in rows[0]}
    m = {}
    for key, names in COLS.items():
        for h, low in head.items():
            if low in names:
                m[key] = h; break
    vids = []
    for r in rows:
        v = {"channel": r[m["channel"]].strip(), "subs": num(r.get(m.get("subs"), 0)), "title": r[m["title"]].strip(),
             "views": num(r[m["views"]]), "date": pdate(r[m["date"]]) if "date" in m else None,
             "format": (r.get(m.get("format"), "") or "long").strip().lower()}
        v["format"] = "short" if v["format"].startswith(("short", "curto")) else "long"
        vids.append(v)
    groups = defaultdict(list)
    for v in vids:
        groups[(v["channel"], v["format"])].append(v)
    channels = []
    for (ch, fmt), vs in groups.items():
        med = statistics.median([v["views"] for v in vs])
        subs = max(v["subs"] for v in vs)
        for v in vs:
            v["channel_median"] = med
            v["ratio"] = round(v["views"] / med, 2) if med else None
            v["views_per_sub"] = round(v["views"] / subs, 2) if subs else None
            v["age_days"] = (today - v["date"]).days if v["date"] else None
            v["views_per_day"] = round(v["views"] / max(v["age_days"], 1), 1) if v["age_days"] is not None else None
        recent = sorted([v for v in vs if v["date"]], key=lambda v: v["date"])[-5:]
        channels.append({"channel": ch, "format": fmt, "subscribers": subs, "videos": len(vs), "median_views": med,
                         "recent5_median": statistics.median([v["views"] for v in recent]) if recent else None})
    outs = sorted([v for v in vids if v["ratio"] and v["ratio"] >= k], key=lambda v: -v["ratio"])
    return channels, outs, vids


def lint(title, thumb=""):
    t = title.strip()
    issues = []
    n = len(t)
    if n > 60:
        issues.append(f"{n} chars: cut in desktop search after 60")
    elif n > 40:
        issues.append(f"{n} chars: mobile feeds may cut after 40 — keep the subject in the first 40")
    caps = [w for w in re.findall(r"\b[A-ZÀ-Ý]{3,}\b", t)]
    if len(caps) > 2:
        issues.append(f"{len(caps)} ALL-CAPS words")
    if len(re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", t)) > 1:
        issues.append("more than one emoji")
    if re.search(r"[!?]{2,}", t):
        issues.append("repeated punctuation")
    if re.search(HYPE, t, re.I):
        issues.append("hype word")
    if re.search(FAKE_PROOF, t, re.I):
        issues.append("claims proof/views/endorsement — must be true and sourced")
    if not re.search(r"\d", t):
        issues.append("no number (optional, but numbers often add specificity)")
    if thumb:
        tw = {w.lower() for w in re.findall(r"\w{3,}", thumb)}
        shared = tw & {w.lower() for w in re.findall(r"\w{3,}", t)}
        if len(shared) > 1:
            issues.append(f"repeats thumbnail words: {', '.join(sorted(shared))}")
        if len(thumb.split()) > 3:
            issues.append(f"thumbnail text has {len(thumb.split())} words (max 3)")
    score = 10 - sum(3 if "claims" in i or "hype" in i else 2 if "chars: cut" in i or "repeats" in i else 1 for i in issues if not i.startswith("no number"))
    return {"title": t, "chars": n, "score": max(score, 0), "issues": issues}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("outliers"); o.add_argument("csv"); o.add_argument("--today"); o.add_argument("--min", type=float, default=3.0); o.add_argument("--json")
    t = sub.add_parser("titles"); t.add_argument("file"); t.add_argument("--thumb", default="")
    s = sub.add_parser("title"); s.add_argument("title"); s.add_argument("--thumb", default="")
    a = ap.parse_args()
    if a.cmd == "outliers":
        today = pdate(a.today) if a.today else date.today()
        chans, outs, vids = outliers(a.csv, today, a.min)
        print(f"# Niche read — {len(vids)} videos, {len(chans)} channel/format groups, as of {today}\n")
        print("| Channel | Format | Subs | Videos | Median views | Last-5 median |\n|---|---|---:|---:|---:|---:|")
        for c in sorted(chans, key=lambda c: -c["subscribers"]):
            print(f"| {c['channel']} | {c['format']} | {c['subscribers']:,.0f} | {c['videos']} | {c['median_views']:,.0f} | {c['recent5_median'] or 0:,.0f} |")
        print(f"\n## Outliers (≥ {a.min}× the channel's median): {len(outs)}\n")
        print("| Ratio | Views | Channel median | Views/subs | Views/day | Date | Channel | Title |\n|---:|---:|---:|---:|---:|---|---|---|")
        for v in outs:
            print(f"| {v['ratio']}× | {v['views']:,.0f} | {v['channel_median']:,.0f} | {v['views_per_sub']} | {v['views_per_day']} | {v['date']} | {v['channel']} | {v['title']} |")
        if a.json:
            json.dump({"channels": chans, "outliers": outs}, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    else:
        titles = [a.title] if a.cmd == "title" else [l for l in open(a.file, encoding="utf-8").read().splitlines() if l.strip()]
        res = sorted((lint(x, a.thumb) for x in titles), key=lambda r: -r["score"])
        for r in res:
            print(f"{r['score']:>2}/10 · {r['chars']:>3} chars · {r['title']}")
            for i in r["issues"]:
                print(f"         - {i}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
