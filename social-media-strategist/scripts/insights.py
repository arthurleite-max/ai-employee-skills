#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Social Media Strategist insights: reads a post-level metrics export (CSV) and shows what works.
Python 3.8+, standard library only, no internet.

  python insights.py posts.csv [--metric saves|shares|engaged|follows|reach] [--outlier 2.0] [--json out.json]

The CSV needs one row per post. Column names are matched loosely (English or Portuguese):
date/data, format/formato/type, caption/legenda/title/titulo, reach/alcance/views/visualizações,
likes/curtidas, comments/comentários, shares/compartilhamentos, saves/salvamentos, follows/seguidores.
Optional: pillar/pilar, hook/gancho. Numbers like 1.234 or 1,234 are read correctly.
"""
import argparse, csv, io, json, re, statistics, sys
from collections import defaultdict

COLS = {
    "date": ["date", "data", "publish time", "horário de publicação", "published"],
    "format": ["format", "formato", "type", "tipo", "post type"],
    "caption": ["caption", "legenda", "title", "titulo", "título", "description", "descrição"],
    "reach": ["reach", "alcance", "views", "visualizações", "visualizacoes", "plays", "impressions"],
    "likes": ["likes", "curtidas"],
    "comments": ["comments", "comentários", "comentarios"],
    "shares": ["shares", "compartilhamentos"],
    "saves": ["saves", "salvamentos", "salvos"],
    "follows": ["follows", "seguidores", "new followers", "follows from post"],
    "pillar": ["pillar", "pilar"],
    "hook": ["hook", "gancho"],
}


def num(s):
    s = str(s or "").strip().replace(" ", "")
    if not s:
        return 0.0
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", s):
        return float(re.sub(r"[.,]", "", s))
    return float(s.replace(",", "."))


def load(path):
    raw = open(path, encoding="utf-8-sig", errors="replace").read()
    sep = max([",", ";", "\t"], key=lambda c: raw.splitlines()[0].count(c))
    rows = list(csv.DictReader(io.StringIO(raw), delimiter=sep))
    head = {h: h.strip().lower() for h in rows[0].keys()} if rows else {}
    mapping = {}
    for key, names in COLS.items():
        for h, low in head.items():
            if low in names or any(low.startswith(n) for n in names):
                mapping[key] = h; break
    if "reach" not in mapping:
        sys.exit(f"no reach/views column found in {list(head)}")
    posts = []
    for r in rows:
        p = {k: (r.get(h) or "").strip() for k, h in mapping.items()}
        for k in ("reach", "likes", "comments", "shares", "saves", "follows"):
            p[k] = num(p.get(k))
        p["engaged"] = p["likes"] + p["comments"] + p["shares"] + p["saves"]
        r_ = p["reach"] or 1
        p["engaged_rate"] = round(100 * p["engaged"] / r_, 2)
        p["saves_per_1k"] = round(1000 * p["saves"] / r_, 1)
        p["shares_per_1k"] = round(1000 * p["shares"] / r_, 1)
        p["follows_per_1k"] = round(1000 * p["follows"] / r_, 1)
        p["format"] = p.get("format") or "unknown"
        posts.append(p)
    return posts, mapping


METRIC = {"saves": "saves_per_1k", "shares": "shares_per_1k", "engaged": "engaged_rate", "follows": "follows_per_1k", "reach": "reach"}


def analyse(posts, metric, k):
    key = METRIC[metric]
    by = defaultdict(list)
    for p in posts:
        by[p["format"]].append(p)
    table = []
    for f, ps in sorted(by.items(), key=lambda x: -statistics.median([p[key] for p in x[1]])):
        med = statistics.median([p[key] for p in ps])
        best = max(ps, key=lambda p: p[key])
        table.append({"format": f, "posts": len(ps), "median": round(med, 2), "median_reach": statistics.median([p["reach"] for p in ps]),
                      "best": {"date": best.get("date"), "caption": best.get("caption", "")[:70], key: best[key]}})
    overall = statistics.median([p[key] for p in posts])
    outliers = sorted([p for p in posts if overall and p[key] >= k * overall], key=lambda p: -p[key])
    groups = {}
    for field in ("pillar", "hook"):
        if any(p.get(field) for p in posts):
            g = defaultdict(list)
            for p in posts:
                g[p.get(field) or "-"].append(p[key])
            groups[field] = {n: {"posts": len(v), "median": round(statistics.median(v), 2)} for n, v in g.items()}
    return {"metric": key, "posts": len(posts), "overall_median": round(overall, 2), "by_format": table,
            "outliers": [{"date": p.get("date"), "format": p["format"], "caption": p.get("caption", "")[:80], key: p[key],
                          "x_median": round(p[key] / overall, 1) if overall else None} for p in outliers],
            "groups": groups}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--metric", default="saves", choices=list(METRIC))
    ap.add_argument("--outlier", type=float, default=2.0)
    ap.add_argument("--json")
    a = ap.parse_args()
    posts, mapping = load(a.csv)
    res = analyse(posts, a.metric, a.outlier)
    res["columns"] = mapping
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    dates = sorted(p.get("date", "") for p in posts if p.get("date"))
    print(f"# What works — {res['posts']} posts" + (f", {dates[0]} to {dates[-1]}" if dates else ""))
    print(f"\nMetric: {res['metric']} · overall median {res['overall_median']}\n")
    print("| Format | Posts | Median | Median reach | Best post |\n|---|---:|---:|---:|---|")
    for t in res["by_format"]:
        print(f"| {t['format']} | {t['posts']} | {t['median']} | {t['median_reach']:.0f} | {t['best']['date']} · {t['best']['caption']} |")
    print(f"\n## Outliers (≥ {a.outlier}× the overall median): {len(res['outliers'])}")
    for o in res["outliers"]:
        print(f"- {o['date']} · {o['format']} · {o[res['metric']]} ({o['x_median']}×) · {o['caption']}")
    for field, g in res["groups"].items():
        print(f"\n## By {field}")
        for n, v in sorted(g.items(), key=lambda x: -x[1]["median"]):
            print(f"- {n}: median {v['median']} ({v['posts']} posts)")
    small = [t["format"] for t in res["by_format"] if t["posts"] < 10]
    if small:
        print(f"\nFewer than 10 posts in: {', '.join(small)} — treat as early signs.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
