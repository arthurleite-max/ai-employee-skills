#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Partnerships Scout pipeline: lists follow-ups due, conversations to close, replies to answer and the
do-not-contact list; optionally scores candidates. Python 3.8+, standard library only, no internet.

  python pipeline.py pipeline.csv --today 2026-06-04 [--wait 5] [--max-followups 2] [--json out.json]
  python pipeline.py --score candidates.csv

pipeline.csv columns (; or , separated; English or Portuguese headers):
  partner/parceiro ; status ; last_contact/ultimo_contato (YYYY-MM-DD) ; followups ; reply/resposta
  (other columns are kept as they are)
candidates.csv columns: name/nome ; audience/publico ; relevance/relevancia ; reach/alcance ;
  activity/atividade (each 0-3) ; contact/contato (yes/no)
"""
import argparse, csv, io, json, re, sys
from datetime import date

H = {"partner": ["partner", "parceiro", "name", "nome"], "status": ["status"],
     "last": ["last_contact", "ultimo_contato", "último_contato"], "followups": ["followups", "follow-ups"],
     "reply": ["reply", "resposta"], "audience": ["audience", "publico", "público"],
     "relevance": ["relevance", "relevancia", "relevância"], "reach": ["reach", "alcance"],
     "activity": ["activity", "atividade"], "contact": ["contact", "contato"]}
STOP = re.compile(r"do not contact|not interested|unsubscribe|remove me|stop|declin|"
                  r"n[aã]o (nos |me )?contat|sem interesse|n[aã]o temos interesse|descadastr|n[aã]o quero", re.I)
SUSPICIOUS = re.compile(r"\b(AI|IA)\b.*(send|envie|mande|list|lista)|password|senha|gift card|"
                        r"customer list|lista (completa )?de clientes|pix|transfer", re.I)


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


def to_int(v):
    try:
        return int(float(v.replace(",", ".")))
    except ValueError:
        return 0


def score(path):
    out = []
    for r in read(path):
        parts = [to_int(r.get(k, "0")) for k in ("audience", "relevance", "reach", "activity")]
        out.append({"name": r["partner"], "parts": parts, "total": sum(parts),
                    "contact": r.get("contact", "").lower() in ("yes", "sim", "y", "s", "true")})
    out.sort(key=lambda x: (-x["total"], -x["parts"][0], x["name"]))
    print("# Fit scores (0-12)\n")
    for i, c in enumerate(out, 1):
        p = c["parts"]
        band = "approach now" if c["total"] >= 9 else "if capacity" if c["total"] >= 6 else "skip for now"
        nxt = "" if c["contact"] else " · no public contact: find a public channel first"
        print(f"{i}. {c['name']}: {p[0]} + {p[1]} + {p[2]} + {p[3]} = {c['total']} · {band}{nxt}")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pipeline", nargs="?"); ap.add_argument("--today"); ap.add_argument("--wait", type=int, default=5)
    ap.add_argument("--max-followups", type=int, default=2); ap.add_argument("--score"); ap.add_argument("--json")
    a = ap.parse_args()
    res = {}
    if a.score:
        res["scores"] = score(a.score)
    if a.pipeline:
        if not a.today:
            sys.exit("--today YYYY-MM-DD is required with a pipeline")
        today = date.fromisoformat(a.today)
        res.update({"answer": [], "due": [], "close": [], "wait": [], "dnc": [], "suspicious": []})
        for r in read(a.pipeline):
            st, rep = r.get("status", "").lower(), r.get("reply", "")
            last = r.get("last", "")
            days = (today - date.fromisoformat(last)).days if re.match(r"\d{4}-\d{2}-\d{2}$", last) else None
            fu = to_int(r.get("followups", "0") or "0")
            item = {"partner": r["partner"], "status": st, "days": days, "followups": fu, "reply": rep}
            if SUSPICIOUS.search(rep):
                res["suspicious"].append(item)
            if "do not contact" in st or "declined" in st or STOP.search(rep):
                res["dnc"].append(item)
            elif rep and not SUSPICIOUS.search(rep) and not st.startswith("closed"):
                res["answer"].append(item)
            elif st == "sent" and days is not None:
                if fu >= a.max_followups and days >= a.wait:
                    res["close"].append(item)
                elif fu < a.max_followups and days >= a.wait:
                    res["due"].append(item)
                else:
                    res["wait"].append(item)
        print(f"\n# Pipeline on {a.today} (wait {a.wait} days, max {a.max_followups} follow-ups)\n")
        lab = {"suspicious": "Suspicious replies (report to the owner, do not follow)",
               "dnc": "Do not contact (never follow up)", "answer": "Replies to answer",
               "due": "Follow-ups due", "close": "Close as no reply", "wait": "Waiting (not due yet)"}
        for k in ("suspicious", "dnc", "answer", "due", "close", "wait"):
            print(f"## {lab[k]}: {len(res[k])}")
            for i in res[k]:
                d = "" if i["days"] is None else f" · {a.today} - last contact = {i['days']} days"
                extra = f" · follow-up {i['followups'] + 1}" if k == "due" else f" · {i['followups']} follow-ups sent" if k in ("close", "wait") else ""
                print(f"- {i['partner']}{d}{extra}" + (f" · reply: {i['reply'][:80]}" if i["reply"] and k in ("answer", "dnc", "suspicious") else ""))
            print()
    if not res:
        ap.print_help()
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=2, default=str)


if __name__ == "__main__":
    main()
