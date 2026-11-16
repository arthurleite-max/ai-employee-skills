#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Content Producer cards: renders on-brand slides as SVG files and checks them; lints captions for
AI-sounding patterns. Python 3.8+, standard library only, no internet.

  python cards.py render slides.json --brand brand.json -o out/
  python cards.py contrast "#FFFFFF" "#1A3C34"
  python cards.py lint caption.txt [--lang en|pt]

slides.json:
  {"size": "1080x1350", "slides": [
     {"title": "Bread storage: 3 rules", "body": "Most loaves die in plastic.", "style": "dark", "kicker": "1/6"},
     ...]}
brand.json:
  {"bg": "#FAF6EF", "ink": "#22201C", "dark_bg": "#22201C", "dark_ink": "#FAF6EF", "accent": "#C8553D",
   "font": "Inter, Arial, sans-serif", "handle": "@brand.example"}

A slide FAILS when its text does not fit or its contrast is below 4.5:1 (3:1 for the big title).
The SVGs open in any browser and import into Canva, Figma or Illustrator; the font must be installed
(or licensed as a web font) where they are opened.
"""
import argparse, json, os, re, sys
from xml.sax.saxutils import escape

AI_TELLS = {
    "en": [r"\bdelve\b", r"\belevate\b", r"\bunlock\b", r"\bseamless(ly)?\b", r"\bgame[- ]changer\b", r"\btapestry\b",
           r"\bjourney\b", r"in today'?s fast[- ]paced world", r"\bnot just\b.{0,40}\bit'?s\b", r"\bit'?s not (just )?about\b",
           r"\bhave you ever wondered\b", r"\bin conclusion\b", r"\bnavigate the\b", r"\bharness\b", r"\brevolutioni[sz]e\b"],
    "pt": [r"\bdesvend", r"\beleve\b|\belevar sua\b", r"\bpotencializ", r"\bjornada\b", r"no mundo (de hoje|atual)",
           r"n[aã]o [eé] apenas.{0,60}[eé]", r"\bmergulh(e|ar) (fundo|nesse)", r"\btransform(e|ar) (sua|seu)",
           r"\bvoc[eê] j[aá] se perguntou\b", r"\bem resumo\b", r"\bdesbloque", r"\brevolucion", r"\bimpulsion"],
}


def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def luminance(h):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in hex_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


def wrap(text, max_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def render(spec, brand, out):
    os.makedirs(out, exist_ok=True)
    W, H = (int(x) for x in spec.get("size", "1080x1350").lower().split("x"))
    margin = 80
    report = []
    for i, s in enumerate(spec["slides"], 1):
        dark = s.get("style") == "dark"
        bg = brand.get("dark_bg" if dark else "bg", "#FFFFFF")
        ink = brand.get("dark_ink" if dark else "ink", "#111111")
        accent = brand.get("accent", ink)
        font = brand.get("font", "Arial, sans-serif")
        t_size, b_size = s.get("title_size", 84), s.get("body_size", 40)
        t_lines = wrap(s.get("title", ""), max(8, int((W - 2 * margin) / (t_size * 0.55))))
        b_lines = wrap(s.get("body", ""), max(10, int((W - 2 * margin) / (b_size * 0.5))))
        y = margin + 120
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
                 f'<rect width="100%" height="100%" fill="{bg}"/>']
        if s.get("kicker"):
            parts.append(f'<text x="{margin}" y="{margin + 30}" font-family="{escape(font)}" font-size="32" font-weight="700" fill="{accent}">{escape(s["kicker"])}</text>')
        for ln in t_lines:
            parts.append(f'<text x="{margin}" y="{y}" font-family="{escape(font)}" font-size="{t_size}" font-weight="800" fill="{ink}">{escape(ln)}</text>')
            y += int(t_size * 1.12)
        y += 40
        for ln in b_lines:
            parts.append(f'<text x="{margin}" y="{y}" font-family="{escape(font)}" font-size="{b_size}" fill="{ink}">{escape(ln)}</text>')
            y += int(b_size * 1.4)
        if brand.get("handle"):
            parts.append(f'<text x="{margin}" y="{H - margin}" font-family="{escape(font)}" font-size="28" fill="{ink}" opacity="0.8">{escape(brand["handle"])}</text>')
        parts.append("</svg>")
        c_body = contrast(ink, bg)
        issues = []
        if c_body < 4.5:
            issues.append(f"contrast {c_body}:1 < 4.5:1")
        if y > H - margin - 60:
            issues.append(f"text does not fit (ends at {y}px of {H - margin - 60}px)")
        if len(s.get("title", "").split()) > 8:
            issues.append("title over 8 words")
        if len(s.get("body", "").split()) > 25:
            issues.append("body over 25 words")
        if s.get("kicker") and contrast(accent, bg) < 3:
            issues.append(f"accent contrast {contrast(accent, bg)}:1 < 3:1")
        path = os.path.join(out, f"slide-{i:02d}.svg")
        open(path, "w", encoding="utf-8").write("\n".join(parts))
        report.append({"slide": i, "file": path, "contrast": c_body, "ok": not issues, "issues": issues})
    return report


def lint(text, lang):
    found = []
    pats = AI_TELLS["en"] + AI_TELLS["pt"] if lang == "both" else AI_TELLS[lang]
    for p in pats:
        for m in re.finditer(p, text, re.I):
            found.append(m.group(0))
    dashes = text.count("—") + text.count(" – ")
    lines = [l for l in text.splitlines() if l.strip()]
    emoji_lines = sum(1 for l in lines if re.match(r"^\s*[\U0001F300-\U0001FAFF☀-➿]", l))
    extra = []
    if dashes >= 3:
        extra.append(f"{dashes} long dashes")
    if lines and emoji_lines >= max(3, len(lines) // 2):
        extra.append(f"{emoji_lines} lines start with an emoji")
    if len(re.findall(r"\*\*[^*]+:\*\*", text)) >= 3:
        extra.append("bold labels on many items")
    return found, extra


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render"); r.add_argument("slides"); r.add_argument("--brand", required=True); r.add_argument("-o", required=True)
    c = sub.add_parser("contrast"); c.add_argument("fg"); c.add_argument("bg")
    l = sub.add_parser("lint"); l.add_argument("file"); l.add_argument("--lang", default="both", choices=["en", "pt", "both"])
    a = ap.parse_args()
    if a.cmd == "render":
        rep = render(json.load(open(a.slides, encoding="utf-8")), json.load(open(a.brand, encoding="utf-8")), a.o)
        for x in rep:
            print(f"slide {x['slide']:02d} · contrast {x['contrast']}:1 · {'OK' if x['ok'] else 'FAIL: ' + '; '.join(x['issues'])} · {x['file']}")
        sys.exit(0 if all(x["ok"] for x in rep) else 1)
    elif a.cmd == "contrast":
        v = contrast(a.fg, a.bg)
        print(f"{v}:1 · body text {'OK' if v >= 4.5 else 'FAIL'} · large text {'OK' if v >= 3 else 'FAIL'}")
    else:
        found, extra = lint(open(a.file, encoding="utf-8").read(), a.lang)
        if not found and not extra:
            print("clean")
        for f in found:
            print(f"- AI tell: \"{f}\"")
        for e in extra:
            print(f"- pattern: {e}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
