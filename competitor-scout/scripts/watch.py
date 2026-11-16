#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Competitor Scout watch: compares two snapshots of competitor observations and positions the owner's
prices. Python 3.8+, standard library only, no internet.

  python watch.py old.csv new.csv [--owner owner.csv] [--json out.json]

Snapshot CSV columns (; or , separated; English or Portuguese headers):
  competitor/concorrente ; item ; kind/tipo (price, offer, product, ad, rating, content, news, hiring)
  ; value/valor ; source/fonte ; date/data
owner.csv (optional): item ; price  (the owner's own prices, to position against competitors)
Rows in the new snapshot with value "not checked"/"nao verificado" mark a source that could not be read.
"""
import argparse, csv, io, json, re, sys
from collections import defaultdict

H = {"competitor": ["competitor", "concorrente"], "item": ["item"], "kind": ["kind", "tipo"],
     "value": ["value", "valor"], "source": ["source", "fonte"], "date": ["date", "data"], "price": ["price", "preco", "preço"]}
NOT_CHECKED = re.compile(r"not checked|n[aã]o verificad", re.I)


def read(path):
    raw = open(path, encoding="utf-8-sig").read()
    sep = max([";", ",", "\t"], key=lambda c: raw.splitlines()[0].count(c))
    rows = list(csv.DictReader(io.StringIO(raw), delimiter=sep))
    m = {}
    for k, names in H.items():
        for h in rows[0]:
            if h.strip().lower() in names:
                m[k] = h
    return [{k: (r.get(m[k]) or "").strip() for k in m} for r in rows]


def num(v):
    s = re.sub(r"[^\d.,]", "", v)
    if not s:
        return None
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("old"); ap.add_argument("new"); ap.add_argument("--owner"); ap.add_argument("--json")
    a = ap.parse_args()
    old, new = read(a.old), read(a.new)
    key = lambda r: (r["competitor"], r["item"], r.get("kind", ""))
    o = {key(r): r for r in old}
    n = {key(r): r for r in new}
    not_checked = sorted({r["competitor"] for r in new if NOT_CHECKED.search(r["value"])})
    res = {"changes": [], "first_seen": [], "not_seen_now": [], "not_checked": not_checked, "positions": []}
    for k, r in n.items():
        if NOT_CHECKED.search(r["value"]):
            continue
        if k not in o:
            res["first_seen"].append(r)
            continue
        before = o[k]
        if before["value"] != r["value"]:
            ch = {"competitor": k[0], "item": k[1], "kind": k[2], "before": before["value"], "now": r["value"],
                  "date_before": before.get("date"), "date_now": r.get("date"), "source": r.get("source")}
            b, c = num(before["value"]), num(r["value"])
            if k[2] == "price" and b and c:
                ch["pct"] = round(100 * (c - b) / b, 1)
            res["changes"].append(ch)
    for k, r in o.items():
        if k not in n and k[0] not in not_checked:
            res["not_seen_now"].append(r)
    if a.owner:
        own = read(a.owner)
        prices = defaultdict(list)
        for r in new:
            if r.get("kind") == "price" and num(r["value"]) is not None:
                prices[r["item"].lower()].append((r["competitor"], num(r["value"])))
        for r in own:
            p = num(r.get("price", ""))
            comp = prices.get(r["item"].lower(), [])
            if p is not None and comp:
                cheaper = [c for c, v in comp if v < p]
                res["positions"].append({"item": r["item"], "owner": p, "competitors": comp,
                                         "rank_cheapest_first": 1 + len(cheaper), "of": len(comp) + 1})
    print("# Competitor watch\n")
    if not_checked:
        print("Not checked this time: " + ", ".join(not_checked) + "\n")
    print(f"## Changes: {len(res['changes'])}")
    for c in res["changes"]:
        pct = f" ({c['pct']:+.1f}%)" if "pct" in c else ""
        print(f"- {c['competitor']} · {c['item']} · {c['kind']}: {c['before']} ({c['date_before']}) → {c['now']} ({c['date_now']}){pct} · {c['source']}")
    print(f"\n## First seen (no earlier observation): {len(res['first_seen'])}")
    for r in res["first_seen"]:
        print(f"- {r['competitor']} · {r['item']} · {r.get('kind')}: {r['value']} ({r.get('date')}) · {r.get('source')}")
    print(f"\n## Seen before, not seen now: {len(res['not_seen_now'])}")
    for r in res["not_seen_now"]:
        print(f"- {r['competitor']} · {r['item']} · {r.get('kind')}: last {r['value']} ({r.get('date')})")
    if res["positions"]:
        print("\n## Your prices vs theirs (current snapshot)")
        for p in res["positions"]:
            others = ", ".join(f"{c} {v:.2f}" for c, v in sorted(p["competitors"], key=lambda x: x[1]))
            print(f"- {p['item']}: you {p['owner']:.2f} · {others} · you are #{p['rank_cheapest_first']} cheapest of {p['of']}")
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
