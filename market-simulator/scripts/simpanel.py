#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Market Simulator helper: builds a balanced panel of simulated customers from your segments, and tallies
their reactions into weighted results (purchase intent, revenue and margin per 100 people, objections,
segments, variant differences). Python 3.8+, standard library only, no internet. It never calls an AI and
never contacts anyone; the reactions come from the simulation you run in your AI.

  python simpanel.py panel segments.csv [--size 24] [--seed 7] [-o panel.json]
  python simpanel.py tally reactions.csv --segments segments.csv [--price A=29.90 --price B=24.90]
                     [--cost 18] [--json out.json]

segments.csv (; or ,):  segment ; weight (share of your market, %) ; traits (optional, | separated)
reactions.csv (; or ,): persona ; segment ; variant ; decision (buy / maybe / no) ; objection (optional,
                        | separated tags) ; round (optional: 1 = first, independent reaction; 2 = after
                        hearing others) ; quote (optional)

Results are SIMULATED: use them to sharpen questions and pick what to test with real people, never as
market data or in advertising.
"""
import argparse, csv, io, json, random, re, sys
from collections import Counter, defaultdict

H = {"segment": ["segment", "segmento", "segmento de mercado"], "weight": ["weight", "peso", "share", "%"],
     "traits": ["traits", "tracos", "traços", "caracteristicas", "características"],
     "persona": ["persona", "id"], "variant": ["variant", "variante", "version", "versao", "versão"],
     "decision": ["decision", "decisao", "decisão"], "objection": ["objection", "objecao", "objeção", "objections"],
     "round": ["round", "rodada"], "quote": ["quote", "fala", "citacao", "citação"]}
BUY = re.compile(r"^(buy|yes|sim|compra|compraria|compro)", re.I)
MAYBE = re.compile(r"^(maybe|talvez|wait|esperar)", re.I)


def read(path):
    raw = open(path, encoding="utf-8-sig").read()
    sep = max([";", ",", "\t"], key=lambda c: raw.splitlines()[0].count(c))
    rows = list(csv.DictReader(io.StringIO(raw), delimiter=sep))
    m = {}
    for k, names in H.items():
        for h in rows[0] if rows else []:
            if h and h.strip().lower() in names and k not in m:
                m[k] = h
    return [{k: (r.get(m[k]) or "").strip() for k in m} for r in rows]


def num(v):
    s = re.sub(r"[^\d.,-]", "", v or "")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    return float(s) if s else 0.0


def segments(path):
    segs = [(r["segment"], num(r.get("weight", "")), [t.strip() for t in r.get("traits", "").split("|") if t.strip()])
            for r in read(path) if r.get("segment")]
    total = sum(w for _, w, _ in segs)
    note = None
    if abs(total - 100) > 0.01:
        note = (f"segment weights add up to {total:g}%, not 100%: results below use each weight divided by "
                f"{total:g} (normalised). Confirm the real shares with the owner.")
    return segs, total, note


def panel(a):
    segs, total, note = segments(a.segments)
    rng = random.Random(a.seed)
    exact = [(s, w / total * a.size, t) for s, w, t in segs]
    alloc = {s: int(x) for s, x, _ in exact}
    left = a.size - sum(alloc.values())
    for s, x, _ in sorted(exact, key=lambda e: -(e[1] - int(e[1])))[:left]:  # largest remainder
        alloc[s] += 1
    stance = ["enthusiast", "pragmatic", "sceptic", "price-sensitive", "loyal to a competitor", "undecided"]
    people, n = [], 0
    for s, _, traits in segs:
        for i in range(alloc[s]):
            n += 1
            people.append({"persona": f"P{n:02d}", "segment": s, "stance": stance[(i + n) % len(stance)],
                           "trait": rng.choice(traits) if traits else "", "seed": a.seed})
    out = {"size": a.size, "seed": a.seed, "weights_total": total, "note": note,
           "allocation": alloc, "panel": people}
    text = json.dumps(out, ensure_ascii=False, indent=1)
    if a.output:
        open(a.output, "w", encoding="utf-8").write(text)
    print(f"# Panel · {a.size} simulated customers · seed {a.seed}")
    if note:
        print(f"\n⚠️ {note}")
    print("\n| segment | weight | personas |\n|---|---|---|")
    for s, w, _ in segs:
        print(f"| {s} | {w:g}% | {alloc[s]} |")
    print("\nEvery segment mixes stances (enthusiast, pragmatic, sceptic, price-sensitive, loyal to a competitor, "
          "undecided) so the panel is not a fan club. Same seed = same panel.")
    if a.output:
        print(f"\nSaved {a.output}")


def tally(a):
    segs, total, note = segments(a.segments)
    weight = {s: w / total for s, w, _ in segs}
    prices = dict(p.split("=", 1) for p in (a.price or []))
    rows = read(a.reactions)
    rounds = sorted({r.get("round") or "1" for r in rows})
    last = rounds[-1]
    final = [r for r in rows if (r.get("round") or "1") == last]
    variants = sorted({r.get("variant") or "-" for r in final})
    L = [f"# Simulated panel results · {len(set(r['persona'] for r in final))} personas · round {last}", "",
         "SIMULATED reactions, not market data. Use them to choose what to test with real people.", ""]
    if note:
        L += [f"⚠️ {note}", ""]
    unknown = sorted({r["segment"] for r in final} - set(weight))
    if unknown:
        L += [f"⚠️ reactions from segments not in segments.csv (left out): {', '.join(unknown)}", ""]
    res = {}
    for v in variants:
        rv = [r for r in final if (r.get("variant") or "-") == v and r["segment"] in weight]
        by = defaultdict(lambda: [0, 0, 0])
        for r in rv:
            d = r.get("decision", "")
            by[r["segment"]][0] += 1
            by[r["segment"]][1] += 1 if BUY.match(d) else 0
            by[r["segment"]][2] += 1 if MAYBE.match(d) else 0
        L += [f"## Variant {v}", "", "| segment | weight (normalised) | personas | buy | buy rate | weighted |",
              "|---|---|---|---|---|---|"]
        wsum, wtot = 0.0, 0.0
        for s, _, _ in segs:
            n, b, m = by[s]
            if not n:
                L.append(f"| {s} | {weight[s] * 100:.1f}% | 0 | – | – | not tested |")
                continue
            rate = b / n
            wsum += weight[s] * rate
            wtot += weight[s]
            L.append(f"| {s} | {weight[s] * 100:.1f}% | {n} | {b} | {b}/{n} = {rate * 100:.1f}% | {weight[s] * 100:.1f}% × {rate * 100:.1f}% = {weight[s] * rate * 100:.2f} |")
        intent = wsum / wtot if wtot else 0
        raw = sum(x[1] for x in by.values()) / max(1, sum(x[0] for x in by.values()))
        L += ["", f"Weighted purchase intent = {wsum * 100:.2f} ÷ {wtot * 100:.1f} = **{intent * 100:.2f}%** "
              f"(unweighted head count: {raw * 100:.1f}%)."]
        item = {"intent": round(intent * 100, 2), "unweighted": round(raw * 100, 1), "n": len(rv)}
        if v in prices:
            p = num(prices[v])
            item["revenue_per_100"] = round(intent * 100 * p, 2)
            L.append(f"Revenue per 100 people reached = {intent * 100:.2f} × {p:.2f} = {intent * 100 * p:,.2f}.")
            if a.cost is not None:
                item["margin_per_100"] = round(intent * 100 * (p - a.cost), 2)
                L.append(f"Margin per 100 people reached = {intent * 100:.2f} × ({p:.2f} − {a.cost:.2f}) = "
                         f"{intent * 100 * (p - a.cost):,.2f}.")
        obj = Counter(t.strip().lower() for r in rv if not BUY.match(r.get("decision", ""))
                      for t in r.get("objection", "").split("|") if t.strip())
        if obj:
            L += ["", "Top objections (people who did not buy): " + ", ".join(f"{k} ({c})" for k, c in obj.most_common(5))]
        if len(rv) < 30:
            L.append(f"Only {len(rv)} simulated personas: directional, not a measurement.")
        L.append("")
        res[v] = item
    if len(variants) > 1:
        L += ["## Comparison", "", "| variant | weighted intent | revenue / 100 | margin / 100 |", "|---|---|---|---|"]
        for v in variants:
            x = res[v]
            L.append(f"| {v} | {x['intent']:.2f}% | {x.get('revenue_per_100', '–')} | {x.get('margin_per_100', '–')} |")
        best_i = max(variants, key=lambda v: res[v]["intent"])
        L.append("")
        L.append(f"Highest intent: {best_i}.")
        if all("margin_per_100" in res[v] for v in variants):
            best_m = max(variants, key=lambda v: res[v]["margin_per_100"])
            L.append(f"Highest margin: {best_m}." + (" Intent and margin point to different variants: decide on the goal first." if best_m != best_i else ""))
        L.append("")
    if len(rounds) > 1:
        first = {(r["persona"], r.get("variant") or "-"): r.get("decision", "") for r in rows if (r.get("round") or "1") == rounds[0]}
        changed = [(p, v) for (p, v), d in first.items()
                   if any(r["persona"] == p and (r.get("variant") or "-") == v and bool(BUY.match(r.get("decision", ""))) != bool(BUY.match(d)) for r in final)]
        L += [f"## Social influence", "", f"{len(changed)} of {len(first)} reactions changed between round {rounds[0]} and round {last} "
              "(after hearing others). Big swings mean opinions spread by word of mouth: test the first impression and the social proof separately.", ""]
    L.append("Next: pick the riskiest assumption and test it with real people (see reference/validation.md).")
    print("\n".join(L))
    if a.json:
        json.dump({"weights_total": total, "note": note, "variants": res}, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("panel"); p.add_argument("segments"); p.add_argument("--size", type=int, default=24)
    p.add_argument("--seed", type=int, default=7); p.add_argument("-o", "--output")
    t = sub.add_parser("tally"); t.add_argument("reactions"); t.add_argument("--segments", required=True)
    t.add_argument("--price", action="append"); t.add_argument("--cost", type=float); t.add_argument("--json")
    a = ap.parse_args()
    panel(a) if a.cmd == "panel" else tally(a)


if __name__ == "__main__":
    main()
