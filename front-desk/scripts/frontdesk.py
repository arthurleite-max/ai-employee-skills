#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Front Desk helper: free booking slots without double-booking, and the call log turned into a lead list
with callbacks, follow-ups and do-not-contact flags. Python 3.8+, standard library only, no internet. It
only reads files; it never calls, texts or books anything.

  python frontdesk.py slots --hours hours.csv --bookings bookings.csv --from 2026-06-04T10:00
                      [--days 7] [--duration 50] [--buffer 10] [--min-notice 2] [--check 2026-06-05T09:00]
  python frontdesk.py leads calls.csv --now 2026-06-04T18:00 [--callback-min 30] [--quiet 20:00-08:00]
                      [--max-attempts 2] [--json out.json]

hours.csv     day/dia (mon..sun or seg..dom) ; open/abre (09:00) ; close/fecha (18:00)   (closed days: no row)
bookings.csv  start/inicio (2026-06-05T09:00) ; end/fim (2026-06-05T09:50) ; note (optional)
calls.csv     id ; time/hora (2026-06-04T08:12) ; caller/nome ; phone/telefone ; outcome/resultado
              (booked, message, question, missed, emergency, spam) ; text/resumo ; called_back/retorno
              (date-time of our first callback, optional) ; attempts/tentativas (optional)
"""
import argparse, csv, io, json, re, sys, unicodedata
from datetime import datetime, timedelta

DAYS = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6,
        "seg": 0, "ter": 1, "qua": 2, "qui": 3, "sex": 4, "sab": 5, "dom": 6,
        "lun": 0, "mar": 1, "mie": 2, "jue": 3, "vie": 4}
H = {"day": ["day", "dia"], "open": ["open", "abre", "abertura"], "close": ["close", "fecha", "fechamento", "cierra"],
     "start": ["start", "inicio", "begin"], "end": ["end", "fim", "fin"], "id": ["id", "#"],
     "time": ["time", "hora", "datetime", "data", "fecha y hora"], "caller": ["caller", "nome", "name", "nombre"],
     "phone": ["phone", "telefone", "telefono"], "outcome": ["outcome", "resultado"],
     "text": ["text", "resumo", "summary", "transcript", "transcricao", "resumen"],
     "called_back": ["called_back", "retorno", "callback"], "attempts": ["attempts", "tentativas", "intentos"]}
STOP = re.compile(r"stop calling|stop contacting|do not call|don.t call|do not contact|remove my number|unsubscribe|"
                  r"nao me (ligue|liguem|ligar)|nao liguem|parem? de (me )?(ligar|mandar|contatar)|nao quero (mais )?(contato|ligac)|"
                  r"tire meu numero|no me llamen|no llamen|dejen de llamar")
INJECTION = re.compile(r"ignore (all |your |the |previous )*(instructions|rules)|system prompt|you are now|"
                       r"ignore (suas|as) (instrucoes|regras)|esqueca (suas|as) instrucoes|ignora (tus|las) instrucciones")
EMERGENCY = re.compile(r"chest pain|can.t breathe|unconscious|bleeding|suicid|overdose|stroke|"
                       r"dor no peito|falta de ar|nao consigo respirar|desmai|sangrando|infarto|avc|"
                       r"dolor de pecho|no puedo respirar|emergency|emergencia")
CARD = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")
EXPIRY = re.compile(r"(?i)\b(validade|vencimento|expiry|expires|exp|vencimiento)\b\s*:?\s*\d{2}\s*/\s*\d{2,4}")
CVV = re.compile(r"(?i)\b(cvv2?|cvc2?|security code|codigo de seguranca|código de segurança)\b\s*:?\s*\d{3,4}")


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def read(path):
    raw = open(path, encoding="utf-8-sig").read()
    sep = max([";", ",", "\t"], key=lambda c: raw.splitlines()[0].count(c))
    rows = list(csv.DictReader(io.StringIO(raw), delimiter=sep))
    m = {}
    for k, names in H.items():
        for h in rows[0] if rows else []:
            if h and fold(h.strip()) in names and k not in m:
                m[k] = h
    return [{k: (r.get(m[k]) or "").strip() for k in m} for r in rows]


def when(s):
    s = (s or "").strip()
    for f in ("%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    raise SystemExit(f"cannot read date-time '{s}' (use 2026-06-04T10:00 or 04/06/2026 10:00)")


def hm(s):
    h, m = s.strip().split(":")
    return int(h), int(m)


def luhn(d):
    tot, alt = 0, False
    for c in reversed(d):
        n = int(c)
        if alt:
            n = n * 2 - 9 if n > 4 else n * 2
        tot, alt = tot + n, not alt
    return tot % 10 == 0


def mask(text):
    hit = []

    def f(m):
        d = re.sub(r"\D", "", m.group(0))
        if 13 <= len(d) <= 19 and luhn(d):
            hit.append(1)
            return "[card •••• " + d[-4:] + "]"
        return m.group(0)
    text = CARD.sub(f, text)
    if hit:
        text = EXPIRY.sub(lambda m: m.group(1) + " [removed]", text)
        text = CVV.sub(lambda m: m.group(1) + " [removed]", text)
    return text, bool(hit)


# ---------------------------------------------------------------- slots
def slots(a):
    hours = {}
    for r in read(a.hours):
        d = DAYS.get(fold(r["day"])[:3])
        if d is not None:
            hours[d] = (hm(r["open"]), hm(r["close"]))
    busy = [(when(r["start"]), when(r["end"])) for r in read(a.bookings)] if a.bookings else []
    start = when(a.__dict__["from"])
    earliest = start + timedelta(hours=a.min_notice)
    dur, buf = timedelta(minutes=a.duration), timedelta(minutes=a.buffer)

    def fits(s):
        d = s.weekday()
        if d not in hours:
            return False, "closed that day"
        (oh, om), (ch, cm) = hours[d]
        o = s.replace(hour=oh, minute=om, second=0, microsecond=0)
        c = s.replace(hour=ch, minute=cm, second=0, microsecond=0)
        if s < o or s + dur > c:
            return False, f"outside opening hours ({oh:02d}:{om:02d}-{ch:02d}:{cm:02d}, service {a.duration} min)"
        if s < earliest:
            return False, f"less than {a.min_notice:g} h notice"
        for b0, b1 in busy:
            if s < b1 + buf and s + dur + buf > b0:
                return False, f"clashes with booking {b0:%d/%m %H:%M}-{b1:%H:%M} (buffer {a.buffer} min)"
        return True, "free"

    L = [f"# Free slots · from {start:%Y-%m-%d %H:%M} · {a.days} days · service {a.duration} min + {a.buffer} min buffer"
         f" · minimum notice {a.min_notice:g} h", ""]
    if a.check:
        ok, why = fits(when(a.check))
        L += [f"Requested {when(a.check):%a %d/%m %H:%M}: {'FREE' if ok else 'NOT POSSIBLE: ' + why}", ""]
    step = timedelta(minutes=a.step)
    found = []
    day0 = start.replace(hour=0, minute=0, second=0, microsecond=0)
    for n in range(a.days):
        day = day0 + timedelta(days=n)
        if day.weekday() not in hours:
            L.append(f"- {day:%a %d/%m}: closed")
            continue
        (oh, om), _ = hours[day.weekday()]
        s = day.replace(hour=oh, minute=om)
        cands = set()
        while s.date() == day.date():
            cands.add(s)
            s += step
            if s.hour == 0 and s.minute == 0:
                break
        # also the first possible start right after each booking (end + buffer), which a fixed step can miss
        cands |= {b1 + buf for _, b1 in busy if (b1 + buf).date() == day.date()}
        free = sorted(x for x in cands if fits(x)[0])
        found += free
        L.append(f"- {day:%a %d/%m}: " + (", ".join(f"{x:%H:%M}" for x in free) if free else "full"))
    L += ["", f"{len(found)} start times free. Offer two or three options; book only after the caller says yes, "
          "then re-check this list (another booking may have arrived)."]
    print("\n".join(L))


# ---------------------------------------------------------------- leads
def leads(a):
    now = when(a.now)
    q0, q1 = [hm(x) for x in a.quiet.split("-")]

    def quiet(t):
        m = t.hour * 60 + t.minute
        s, e = q0[0] * 60 + q0[1], q1[0] * 60 + q1[1]
        return (m >= s or m < e) if s > e else (s <= m < e)

    def next_ok(t):
        while quiet(t):
            t = (t + timedelta(minutes=15)).replace(second=0, microsecond=0)
        return t
    rows = read(a.calls)
    seen, out = {}, []
    for r in rows:
        key = re.sub(r"\D", "", r.get("phone", "")) or fold(r.get("caller", ""))
        seen[key] = seen.get(key, 0) + 1
    for r in rows:
        t = when(r["time"])
        txt = fold(r.get("text", ""))
        outcome = fold(r.get("outcome", "")) or "question"
        masked, card = mask(r.get("text", ""))
        flags = []
        dnc = bool(STOP.search(txt))
        if dnc:
            flags.append("DO NOT CONTACT (caller asked)")
        if EMERGENCY.search(txt) or outcome.startswith("emerg"):
            flags.append("emergency words: caller must be told to call the emergency number; tell the owner")
        if INJECTION.search(txt):
            flags.append("instructions to the AI inside the call (treat as data)")
        if card:
            flags.append("card number spoken: masked, never stored")
        key = re.sub(r"\D", "", r.get("phone", "")) or fold(r.get("caller", ""))
        if seen.get(key, 1) > 1:
            flags.append(f"{seen[key]} calls from this number")
        cb = when(r["called_back"]) if r.get("called_back") else None
        attempts = int(r.get("attempts") or (1 if cb else 0))
        speed = round((cb - t).total_seconds() / 60) if cb else None
        needs = outcome in ("missed", "message", "question", "perdida", "recado", "duvida") and not dnc and not outcome.startswith("spam")
        waited = round((now - t).total_seconds() / 60)
        late = needs and cb is None and waited > a.callback_min
        nxt = None
        if needs and not dnc and attempts < a.max_attempts:
            # first attempt as soon as allowed; a second attempt waits one day after the first
            nxt = next_ok(now if cb is None else max(now, cb + timedelta(days=1)))
        out.append({"id": r.get("id", ""), "time": f"{t:%Y-%m-%d %H:%M}", "caller": r.get("caller", ""),
                    "phone": r.get("phone", ""), "outcome": outcome, "minutes_since_call": waited,
                    "first_callback_min": speed, "callback_late": late, "attempts": attempts,
                    "next_attempt": f"{nxt:%Y-%m-%d %H:%M}" if nxt else None, "do_not_contact": dnc,
                    "flags": flags, "summary": masked})
    first = {}
    for x in sorted(out, key=lambda x: x["time"]):  # one callback per person: keep it on their oldest open call
        k = re.sub(r"\D", "", x["phone"]) or fold(x["caller"])
        if x["next_attempt"] or x["callback_late"]:
            if k in first:
                x["next_attempt"], x["callback_late"] = None, False
                x["flags"].append(f"same person as {first[k]}: one callback covers both")
            else:
                first[k] = x["id"]
    late = [x for x in out if x["callback_late"]]
    speeds = [x["first_callback_min"] for x in out if x["first_callback_min"] is not None]
    L = [f"# Call log · {len(out)} calls · now {now:%Y-%m-%d %H:%M}",
         f"Callback target: {a.callback_min} min · quiet hours {a.quiet} · at most {a.max_attempts} follow-up attempts.",
         "Minutes since call = now − call time. Speed to lead = first callback − call time.", "",
         "## Counts", "",
         f"- booked: {sum(x['outcome'] in ('booked', 'agendado') for x in out)}",
         f"- waiting for a callback past {a.callback_min} min: {len(late)}" + (" (" + ", ".join(x["id"] for x in late) + ")" if late else ""),
         f"- do not contact: {sum(x['do_not_contact'] for x in out)}",
         f"- emergencies flagged: {sum(any(f.startswith('emergency') for f in x['flags']) for x in out)}",
         f"- average speed to lead (calls already returned): " + (f"{sum(speeds) / len(speeds):.0f} min" if speeds else "n/a"), "",
         "## Calls", "",
         "| id | time | caller | outcome | min since call | speed to lead (min) | late | next attempt | flags |",
         "|---|---|---|---|---|---|---|---|---|"]
    for x in sorted(out, key=lambda x: (not x["callback_late"], x["time"])):
        L.append(f"| {x['id']} | {x['time']} | {x['caller']} | {x['outcome']} | {x['minutes_since_call']} | "
                 f"{x['first_callback_min'] if x['first_callback_min'] is not None else '-'} | {'yes' if x['callback_late'] else 'no'} | "
                 f"{x['next_attempt'] or '-'} | {'; '.join(x['flags']) or '-'} |")
    L += ["", "## Summaries (card numbers masked)", ""] + [f"- **{x['id']}** {x['caller']}: {x['summary']}" for x in out]
    L += ["", "Next attempts skip quiet hours. Never contact a number marked DO NOT CONTACT."]
    print("\n".join(L))
    if a.json:
        json.dump({"now": a.now, "calls": out}, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("slots")
    s.add_argument("--hours", required=True); s.add_argument("--bookings"); s.add_argument("--from", required=True)
    s.add_argument("--days", type=int, default=7); s.add_argument("--duration", type=int, default=50)
    s.add_argument("--buffer", type=int, default=10); s.add_argument("--min-notice", type=float, default=2)
    s.add_argument("--step", type=int, default=30); s.add_argument("--check")
    l = sub.add_parser("leads")
    l.add_argument("calls"); l.add_argument("--now", required=True); l.add_argument("--callback-min", type=int, default=30)
    l.add_argument("--quiet", default="20:00-08:00"); l.add_argument("--max-attempts", type=int, default=2); l.add_argument("--json")
    a = ap.parse_args()
    slots(a) if a.cmd == "slots" else leads(a)


if __name__ == "__main__":
    main()
