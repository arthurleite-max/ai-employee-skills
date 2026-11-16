#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ads Manager scan: compares the last 7 days with the 7 before, per ad and per campaign, against the
owner's targets, and flags waste, fatigue, scale and tracking issues. Python 3.8+, standard library only,
no internet. It only reads files; it never changes any ad account.

  python adscan.py ads.csv --today 2026-06-04 --target-cpl 35 [--target-customer 180]
                   [--crm crm.csv] [--budget 4000 --month-spend 1500] [--json out.json]

ads.csv (; or , separated; English or Portuguese headers), one row per ad per day (or per week, dated
on the last day of the week):
  date/data ; platform/plataforma ; campaign/campanha ; ad/anuncio ; spend/gasto ; impressions/impressoes
  ; reach/alcance (optional) ; clicks/cliques ; leads ; status (optional: "limited by budget",
  "learning", "limitada pelo orcamento", "aprendizado")
crm.csv (optional): campaign/campanha ; customers/clientes  (real customers in the last 7 days)
"""
import argparse, csv, io, json, re, calendar
from collections import defaultdict
from datetime import date, timedelta

H = {"date": ["date", "data"], "platform": ["platform", "plataforma"], "campaign": ["campaign", "campanha"],
     "ad": ["ad", "anuncio", "anúncio"], "spend": ["spend", "gasto", "valor gasto"],
     "impressions": ["impressions", "impressoes", "impressões"], "reach": ["reach", "alcance"],
     "clicks": ["clicks", "cliques"], "leads": ["leads", "conversions", "conversoes", "conversões"],
     "status": ["status"], "customers": ["customers", "clientes"]}
LIMITED = re.compile(r"limited|limitad", re.I)
LEARNING = re.compile(r"learning|aprendizado", re.I)


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
    s = re.sub(r"[^\d.,-]", "", v or "")
    if not s:
        return 0.0
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    return float(s)


def div(a, b):
    return a / b if b else None


def f2(x, pct=False):
    if x is None:
        return "n/a"
    return f"{x * 100:.2f}%" if pct else f"{x:,.2f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ads"); ap.add_argument("--today", required=True); ap.add_argument("--target-cpl", type=float, required=True)
    ap.add_argument("--target-customer", type=float); ap.add_argument("--crm"); ap.add_argument("--budget", type=float)
    ap.add_argument("--month-spend", type=float); ap.add_argument("--json")
    a = ap.parse_args()
    today = date.fromisoformat(a.today)
    cur0, prev0 = today - timedelta(days=7), today - timedelta(days=14)
    agg = {"cur": defaultdict(lambda: defaultdict(float)), "prev": defaultdict(lambda: defaultdict(float))}
    status = defaultdict(str)
    for r in read(a.ads):
        d = date.fromisoformat(r["date"])
        per = "cur" if cur0 <= d < today else "prev" if prev0 <= d < cur0 else None
        if not per:
            continue
        k = (r.get("platform", ""), r["campaign"], r["ad"])
        for f in ("spend", "impressions", "reach", "clicks", "leads"):
            agg[per][k][f] += num(r.get(f, ""))
        if per == "cur" and r.get("status"):
            status[k] = r["status"]
    crm = {}
    if a.crm:
        crm = {r["campaign"]: num(r.get("customers", "")) for r in read(a.crm)}

    res = {"window": {"current": f"{cur0} to {today - timedelta(days=1)}", "previous": f"{prev0} to {cur0 - timedelta(days=1)}"},
           "ads": [], "campaigns": [], "flags": [], "totals": {}}
    tgt = a.target_cpl
    for k in sorted(set(agg["cur"]) | set(agg["prev"])):
        c, p = agg["cur"].get(k, {}), agg["prev"].get(k, {})
        row = {"platform": k[0], "campaign": k[1], "ad": k[2], "status": status.get(k, "")}
        for lab, x in (("cur", c), ("prev", p)):
            row[lab] = {"spend": x.get("spend", 0.0), "impressions": x.get("impressions", 0.0), "reach": x.get("reach", 0.0),
                        "clicks": x.get("clicks", 0.0), "leads": x.get("leads", 0.0),
                        "ctr": div(x.get("clicks", 0), x.get("impressions", 0)), "cpc": div(x.get("spend", 0), x.get("clicks", 0)),
                        "cpl": div(x.get("spend", 0), x.get("leads", 0)),
                        "freq": div(x.get("impressions", 0), x.get("reach", 0)) if x.get("reach") else None}
        cc, pp = row["cur"], row["prev"]
        ctr_ch = div((cc["ctr"] or 0) - (pp["ctr"] or 0), pp["ctr"]) if pp["ctr"] else None
        row["ctr_change"] = ctr_ch
        name = f"{k[0]} · {k[1]} · {k[2]}"
        if cc["spend"] and cc["leads"] == 0 and cc["spend"] >= 2 * tgt:
            res["flags"].append({"flag": "waste", "item": name, "why": f"spend {f2(cc['spend'])} ≥ 2 × target CPL {f2(tgt)} = {f2(2 * tgt)} with 0 leads", "propose": "pause (approval)"})
        elif cc["cpl"] and cc["cpl"] >= 2 * tgt:
            res["flags"].append({"flag": "waste", "item": name, "why": f"CPL {f2(cc['cpl'])} ≥ 2 × target", "propose": "pause or fix (approval)"})
        if ctr_ch is not None and ctr_ch <= -0.30 and cc["freq"] and cc["freq"] > 3:
            res["flags"].append({"flag": "fatigue", "item": name, "why": f"CTR {f2(pp['ctr'], True)} → {f2(cc['ctr'], True)} ({ctr_ch * 100:+.1f}%), frequency {cc['freq']:.2f}", "propose": "new creative, same offer"})
        if cc["cpl"] and cc["cpl"] <= 0.7 * tgt and cc["leads"] >= 10 and LIMITED.search(row["status"]):
            res["flags"].append({"flag": "scale", "item": name, "why": f"CPL {f2(cc['cpl'])} ≤ 70% of target ({f2(0.7 * tgt)}), {int(cc['leads'])} leads, limited by budget", "propose": "budget +15–20%, re-check in 3–4 days (approval)"})
        if pp["leads"] >= 5 and cc["leads"] == 0 and cc["spend"] > 0:
            res["flags"].append({"flag": "tracking", "item": name, "why": "leads dropped to 0 with spend", "propose": "test the form/tag first"})
        if LEARNING.search(row["status"]):
            res["flags"].append({"flag": "learning", "item": name, "why": "in learning", "propose": "no big edits for now"})
        res["ads"].append(row)

    camp = defaultdict(lambda: defaultdict(float))
    for r in res["ads"]:
        for f in ("spend", "leads", "clicks", "impressions"):
            camp[(r["platform"], r["campaign"])][f] += r["cur"][f]
    plat = defaultdict(lambda: defaultdict(float))
    for (pl, cp), x in camp.items():
        cust = crm.get(cp)
        item = {"platform": pl, "campaign": cp, "spend": x["spend"], "leads": x["leads"], "cpl": div(x["spend"], x["leads"]),
                "customers": cust, "cost_per_customer": div(x["spend"], cust) if cust is not None else None}
        res["campaigns"].append(item)
        plat[pl]["spend"] += x["spend"]; plat[pl]["leads"] += x["leads"]
        if cust is not None:
            plat[pl]["customers"] += cust
        if a.target_customer and item["cost_per_customer"] and item["cost_per_customer"] > a.target_customer:
            res["flags"].append({"flag": "expensive customers", "item": f"{pl} · {cp}", "why": f"cost per customer {f2(item['cost_per_customer'])} > target {f2(a.target_customer)}", "propose": "check lead quality and follow-up"})
    tot_s = sum(x["spend"] for x in plat.values()); tot_l = sum(x["leads"] for x in plat.values())
    res["platforms"] = {pl: {"spend": x["spend"], "leads": x["leads"], "customers": x.get("customers"),
                             "cpl": div(x["spend"], x["leads"]), "cost_per_customer": div(x["spend"], x.get("customers")) if x.get("customers") else None}
                        for pl, x in plat.items()}
    res["totals"] = {"spend": tot_s, "leads": tot_l, "cpl": div(tot_s, tot_l)}
    if a.budget and a.month_spend is not None:
        days_in = calendar.monthrange(today.year, today.month)[1]
        elapsed = today.day - 1 or 1
        proj = a.month_spend / elapsed * days_in
        res["pacing"] = {"month_spend": a.month_spend, "days_elapsed": elapsed, "days_in_month": days_in, "projected": proj,
                         "budget": a.budget, "projected_pct": proj / a.budget}

    w = res["window"]
    print(f"# Ads scan · current {w['current']} vs previous {w['previous']} · target CPL {f2(tgt)}\n")
    if "pacing" in res:
        pc = res["pacing"]
        print(f"Pacing: {f2(pc['month_spend'])} ÷ {pc['days_elapsed']} days × {pc['days_in_month']} = {f2(pc['projected'])} projected "
              f"({pc['projected_pct'] * 100:.1f}% of budget {f2(pc['budget'])})\n")
    print(f"Total (current): spend {f2(tot_s)} · leads {int(tot_l)} · CPL {f2(tot_s)} ÷ {int(tot_l)} = {f2(res['totals']['cpl'])}\n")
    print("## Campaigns (current)")
    for c in res["campaigns"]:
        cust = "" if c["customers"] is None else f" · customers {int(c['customers'])} · cost/customer {f2(c['spend'])} ÷ {int(c['customers'])} = {f2(c['cost_per_customer'])}"
        print(f"- {c['platform']} · {c['campaign']}: spend {f2(c['spend'])} · leads {int(c['leads'])} · CPL {f2(c['cpl'])}{cust}")
    print("\n## Platforms (current; platform leads are never summed as customers)")
    for pl, x in res["platforms"].items():
        cust = "" if not x["customers"] else f" · customers {int(x['customers'])} · cost/customer {f2(x['spend'])} ÷ {int(x['customers'])} = {f2(x['cost_per_customer'])}"
        print(f"- {pl}: spend {f2(x['spend'])} · leads {int(x['leads'])}{cust}")
    print("\n## Ads (current vs previous)")
    for r in res["ads"]:
        c, p = r["cur"], r["prev"]
        fr = f" · freq {c['freq']:.2f}" if c["freq"] else ""
        ch = f" ({r['ctr_change'] * 100:+.1f}%)" if r["ctr_change"] is not None else ""
        print(f"- {r['platform']} · {r['campaign']} · {r['ad']}: spend {f2(c['spend'])} · CTR {f2(p['ctr'], True)} → {f2(c['ctr'], True)}{ch}"
              f" · CPL {f2(p['cpl'])} → {f2(c['cpl'])} · leads {int(p['leads'])} → {int(c['leads'])}{fr}" + (f" · status: {r['status']}" if r["status"] else ""))
    print(f"\n## Flags: {len(res['flags'])}")
    for f in res["flags"]:
        print(f"- [{f['flag']}] {f['item']}: {f['why']} → {f['propose']}")
    print("\nNothing was changed in any account.")
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=2, default=str)


if __name__ == "__main__":
    main()
