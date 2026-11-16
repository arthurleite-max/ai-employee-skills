#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Head of Marketing pulse: reads daily marketing numbers (CSV) and prints the pulse, the week-over-week
table, anomalies (including possible tracking failures) and the attribution check.
Python 3.8+, standard library only, no internet.

  python pulse.py daily.csv [--today YYYY-MM-DD] [--json out.json]

daily.csv: one row per day and channel. Columns (English or Portuguese, matched loosely):
  date/data, channel/canal, spend/investimento, impressions/impressoes, clicks/cliques, leads,
  sales/vendas (real sales from the CRM for that channel), revenue/receita,
  platform_conversions/conversoes_plataforma (what the ad platform claims; optional).
Use channel "TOTAL_CRM" (or "CRM") for the real daily total of sales/revenue if you have it.
"""
import argparse, csv, io, json, re, statistics, sys
from collections import defaultdict
from datetime import date, datetime, timedelta

COLS = {"date": ["date", "data", "dia"], "channel": ["channel", "canal"], "spend": ["spend", "investimento", "gasto", "custo"],
        "impressions": ["impressions", "impressoes", "impressões"], "clicks": ["clicks", "cliques"], "leads": ["leads"],
        "sales": ["sales", "vendas", "matriculas", "matrículas"], "revenue": ["revenue", "receita"],
        "platform_conversions": ["platform_conversions", "conversoes_plataforma", "conversões_plataforma", "conversions"]}
NUMS = ["spend", "impressions", "clicks", "leads", "sales", "revenue", "platform_conversions"]


def num(s):
    s = re.sub(r"[^\d.,-]", "", str(s or ""))
    if not s:
        return 0.0
    if re.fullmatch(r"-?\d{1,3}([.,]\d{3})+", s):
        return float(re.sub(r"[.,]", "", s))
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    return float(s.replace(",", "."))


def pdate(s):
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(str(s).strip(), f).date()
        except ValueError:
            pass
    raise ValueError(f"bad date {s!r}")


def load(path):
    raw = open(path, encoding="utf-8-sig").read()
    sep = max([",", ";", "\t"], key=lambda c: raw.splitlines()[0].count(c))
    rows = list(csv.DictReader(io.StringIO(raw), delimiter=sep))
    head = {h: h.strip().lower() for h in rows[0]}
    m = {}
    for k, names in COLS.items():
        for h, low in head.items():
            if low in names:
                m[k] = h; break
    data = []
    for r in rows:
        d = {"date": pdate(r[m["date"]]), "channel": r[m["channel"]].strip()}
        for k in NUMS:
            d[k] = num(r.get(m.get(k), "")) if k in m else None
        data.append(d)
    return data, m


def agg(rows):
    out = defaultdict(float)
    for r in rows:
        for k in NUMS:
            if r[k] is not None:
                out[k] += r[k]
    return out


def rates(a):
    def div(x, y):
        return round(x / y, 2) if y else None
    paid = a["spend"] > 0
    return {"cpl": div(a["spend"], a["leads"]) if paid else None, "cost_per_sale": div(a["spend"], a["sales"]) if paid else None,
            "lead_to_sale_%": div(100 * a["sales"], a["leads"]), "ctr_%": div(100 * a["clicks"], a["impressions"]),
            "roas": div(a["revenue"], a["spend"])}


def pct(new, old):
    if old in (None, 0) or new is None:
        return None
    return round(100 * (new - old) / old, 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv"); ap.add_argument("--today"); ap.add_argument("--json")
    a = ap.parse_args()
    data, m = load(a.csv)
    last_day = max(r["date"] for r in data)
    today = pdate(a.today) if a.today else last_day + timedelta(days=1)
    w1 = [last_day - timedelta(days=i) for i in range(7)]
    w0 = [last_day - timedelta(days=i) for i in range(7, 14)]
    crm_names = {"total_crm", "crm", "total"}
    chans = sorted({r["channel"] for r in data if r["channel"].lower() not in crm_names})
    res = {"as_of": str(last_day), "today": str(today), "channels": {}, "anomalies": [], "attribution": {}}
    print(f"# Marketing pulse — data to {last_day} (report {today})\n")
    print("## Last 7 days vs previous 7\n")
    print("| Channel | Spend | Δ% | Leads | Δ% | CPL | Prev CPL | Δ% | Real sales | Cost/sale | Lead→sale % |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    tot1, tot0 = defaultdict(float), defaultdict(float)
    for c in chans:
        a1 = agg([r for r in data if r["channel"] == c and r["date"] in w1])
        a0 = agg([r for r in data if r["channel"] == c and r["date"] in w0])
        r1, r0 = rates(a1), rates(a0)
        for k in NUMS:
            tot1[k] += a1[k]; tot0[k] += a0[k]
        res["channels"][c] = {"last7": dict(a1), "prev7": dict(a0), "rates_last7": r1, "rates_prev7": r0}
        print(f"| {c} | {a1['spend']:,.2f} | {pct(a1['spend'], a0['spend'])} | {a1['leads']:.0f} | {pct(a1['leads'], a0['leads'])} | "
              f"{r1['cpl']} | {r0['cpl']} | {pct(r1['cpl'], r0['cpl'])} | {a1['sales']:.0f} | {r1['cost_per_sale']} | {r1['lead_to_sale_%']} |")
    crm = [r for r in data if r["channel"].lower() in crm_names]
    real1 = agg([r for r in crm if r["date"] in w1]) if crm else tot1
    real0 = agg([r for r in crm if r["date"] in w0]) if crm else tot0
    print(f"\nTotals (sales from {'CRM' if crm else 'sum of channels'}): spend {tot1['spend']:,.2f} ({pct(tot1['spend'], tot0['spend'])}%) · "
          f"leads {tot1['leads']:.0f} ({pct(tot1['leads'], tot0['leads'])}%) · sales {real1['sales']:.0f} (prev {real0['sales']:.0f}) · "
          f"revenue {real1['revenue']:,.2f} · CAC {round(tot1['spend'] / real1['sales'], 2) if real1['sales'] else None}")
    # attribution check over the whole file
    allreal = agg(crm)["sales"] if crm else None
    claims = {c: agg([r for r in data if r["channel"] == c])["platform_conversions"] for c in chans}
    claims = {c: v for c, v in claims.items() if v}
    if claims and allreal is not None:
        s = sum(claims.values())
        res["attribution"] = {"real_sales": allreal, "platform_claims": claims, "sum_claims": s, "overlap": s - allreal}
        print(f"\n## Attribution check (whole period)\nReal sales (CRM): {allreal:.0f} · platforms claim "
              + " · ".join(f"{c} {v:.0f}" for c, v in claims.items()) + f" · sum {s:.0f} → {s - allreal:+.0f} vs real. Never add platform claims.")
    # anomalies per channel per day vs trailing 14 days
    print("\n## Anomalies")
    for c in chans:
        rows = sorted([r for r in data if r["channel"] == c], key=lambda r: r["date"])
        zero_run = 0
        for r in rows:
            hist = [x for x in rows if r["date"] - timedelta(days=14) <= x["date"] < r["date"]]
            if r["spend"] and r["spend"] > 0 and r["leads"] == 0 and hist and statistics.mean([x["leads"] for x in hist]) >= 2:
                zero_run += 1
                if r["date"] >= last_day - timedelta(days=6):
                    res["anomalies"].append({"channel": c, "date": str(r["date"]), "type": "possible tracking failure",
                                             "detail": f"0 leads with spend {r['spend']:.2f}; trailing mean {statistics.mean([x['leads'] for x in hist]):.1f}"})
            elif len(hist) >= 7 and r["date"] >= last_day - timedelta(days=6):
                for k in ("spend", "leads"):
                    vals = [x[k] for x in hist]
                    mu, sd = statistics.mean(vals), statistics.pstdev(vals)
                    if sd and abs(r[k] - mu) / sd >= 2.5 and abs(r[k] - mu) >= 0.4 * mu:
                        res["anomalies"].append({"channel": c, "date": str(r["date"]), "type": f"{k} unusual",
                                                 "detail": f"{r[k]:.2f} vs mean {mu:.2f} (sd {sd:.2f})"})
    if not res["anomalies"]:
        print("- none beyond normal noise")
    for x in res["anomalies"]:
        print(f"- {x['date']} · {x['channel']} · {x['type']} · {x['detail']}")
    small = [c for c in chans if res["channels"][c]["last7"]["sales"] < 30]
    if small:
        print(f"\nFewer than 30 sales in the last 7 days for: {', '.join(small)} — changes may be noise.")
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
