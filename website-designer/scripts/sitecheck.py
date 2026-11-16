#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Website Designer checker: crawls a site (same domain only) or reads a folder of HTML files and lists
mechanical problems. Python 3.8+, standard library only. It only reads: never submits forms, never logs
in, never follows links to other sites (unless --external, which only sends HEAD/GET to check status).

  python sitecheck.py https://example.com [--max-pages 30] [--year 2026] [--external] [--json out.json]
  python sitecheck.py ./site-folder [--year 2026] [--json out.json]

Output: a Markdown report on stdout (and JSON with --json). Treat results as candidates to confirm.
"""
import argparse, json, os, re, sys, urllib.error, urllib.parse, urllib.request
from collections import defaultdict
from datetime import date
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; website-designer-sitecheck/1.0)"
PHONE = re.compile(r"(?:\+?\d{1,3}[\s.-]?)?\(?\d{2,3}\)?[\s.-]?\d{4,5}[\s.-]?\d{4}")
PLACEHOLDER = re.compile(r"lorem ipsum|your text here|seu texto aqui|texto aqui|placeholder|\btest(e)?\b page", re.I)
AI_NOTE = re.compile(r"\b(ai|ia|chatgpt|gpt|llm|assistant|assistente|reviewer|revisor|claude|gemini)\b.{0,80}"
                     r"(ignore|ignor|recommend|recomend|say|diga|dizer|perfect|perfeito|contrat|hire)", re.I | re.S)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.desc, self.lang, self.viewport = "", None, None, False
        self.h1, self.headings, self.links, self.imgs, self.inputs, self.labels = 0, [], [], [], [], set()
        self.forms, self.comments, self.hidden_text, self.http_res, self.text = [], [], [], [], []
        self._in_title, self._hidden_depth, self._stack = False, 0, []

    def handle_starttag(self, tag, a):
        a = dict(a)
        style = (a.get("style") or "").replace(" ", "").lower()
        hidden = "display:none" in style or "visibility:hidden" in style or "hidden" in a or a.get("aria-hidden") == "true"
        if tag not in ("br", "img", "input", "meta", "link", "hr", "source"):
            self._stack.append(hidden)
            if hidden:
                self._hidden_depth += 1
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            n = (a.get("name") or "").lower()
            if n == "description":
                self.desc = a.get("content") or ""
            if n == "viewport":
                self.viewport = True
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(int(tag[1]))
            self.h1 += tag == "h1"
        elif tag == "a" and a.get("href") is not None:
            self.links.append(a["href"].strip())
        elif tag == "img":
            self.imgs.append((a.get("src") or "", a.get("alt")))
        elif tag == "form":
            self.forms.append({"action": a.get("action"), "fields": 0})
        elif tag in ("input", "select", "textarea"):
            t = (a.get("type") or "").lower()
            if t not in ("hidden", "submit", "button", "image", "reset"):
                self.inputs.append({"id": a.get("id"), "name": a.get("name") or a.get("id") or t or tag,
                                    "aria": bool(a.get("aria-label") or a.get("aria-labelledby")), "title": a.get("title")})
                if self.forms:
                    self.forms[-1]["fields"] += 1
        elif tag == "label" and a.get("for"):
            self.labels.add(a["for"])
        for k in ("src", "href", "action"):
            v = a.get(k) or ""
            if v.startswith("http://") and tag in ("img", "script", "link", "iframe", "form", "source"):
                self.http_res.append(v)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag not in ("br", "img", "input", "meta", "link", "hr", "source") and self._stack:
            if self._stack.pop():
                self._hidden_depth -= 1

    def handle_data(self, d):
        if self._in_title:
            self.title += d
        elif d.strip():
            self.text.append(d.strip())
            if self._hidden_depth > 0:
                self.hidden_text.append(d.strip())

    def handle_comment(self, d):
        self.comments.append(d.strip())


def fetch(url, method="GET"):
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            body = r.read() if method == "GET" else b""
            return r.status, r.headers.get("Content-Type", ""), r.headers.get("Content-Length"), body, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, "", None, b"", url
    except Exception as e:
        return f"error: {type(e).__name__}", "", None, b"", url


def load_pages(start, max_pages):
    pages, statuses = {}, {}
    if os.path.isdir(start):
        for root, _, files in os.walk(start):
            for f in files:
                if f.lower().endswith((".html", ".htm")):
                    p = os.path.join(root, f)
                    rel = "/" + os.path.relpath(p, start).replace(os.sep, "/")
                    pages[rel] = open(p, encoding="utf-8", errors="replace").read()
                    statuses[rel] = 200
        return pages, statuses, "folder"
    base = urllib.parse.urlparse(start)
    queue, seen = [start], set()
    while queue and len(pages) < max_pages:
        url = urllib.parse.urldefrag(queue.pop(0))[0]
        if url in seen:
            continue
        seen.add(url)
        st, ctype, _, body, final = fetch(url)
        path = urllib.parse.urlparse(url).path or "/"
        statuses[path] = st
        if st != 200 or "html" not in ctype:
            continue
        html = body.decode("utf-8", errors="replace")
        pages[path] = html
        pp = Page(); pp.feed(html)
        for h in pp.links:
            u = urllib.parse.urljoin(url, h)
            pu = urllib.parse.urlparse(u)
            if pu.scheme in ("http", "https") and pu.netloc == base.netloc and u not in seen:
                queue.append(u)
    return pages, statuses, "crawl"


def resolve_status(link, page_path, start, statuses, mode, cache):
    if mode == "folder":
        target = urllib.parse.urljoin(page_path, link).split("#")[0].split("?")[0]
        if target.endswith("/"):
            target += "index.html"
        if target not in statuses and not os.path.splitext(target)[1]:
            for cand in (target + ".html", target + "/index.html"):
                if cand in statuses:
                    return 200
        return 200 if target in statuses or os.path.exists(os.path.join(start, target.lstrip("/"))) else 404
    u = urllib.parse.urljoin(start if page_path == "/" else urllib.parse.urljoin(start, page_path), link).split("#")[0]
    path = urllib.parse.urlparse(u).path or "/"
    if path in statuses:
        return statuses[path]
    if u not in cache:
        cache[u] = fetch(u, "GET")[0]
    return cache[u]


def check(start, max_pages, year, external):
    pages, statuses, mode = load_pages(start, max_pages)
    F = defaultdict(list)
    phones_by_page, titles, cache = {}, defaultdict(list), {}
    host = urllib.parse.urlparse(start).netloc if mode == "crawl" else None
    for path, html in sorted(pages.items()):
        p = Page(); p.feed(html)
        text = " ".join(p.text)
        title = re.sub(r"\s+", " ", p.title).strip()
        titles[title].append(path)
        if not title:
            F["missing_title"].append(path)
        if p.desc is None or not p.desc.strip():
            F["missing_description"].append(path)
        if p.h1 != 1:
            F["h1_count"].append({"page": path, "h1": p.h1})
        if not p.lang:
            F["missing_lang"].append(path)
        if not p.viewport:
            F["missing_viewport"].append(path)
        no_alt = [s for s, alt in p.imgs if alt is None]
        if no_alt:
            F["images_without_alt"].append({"page": path, "images": no_alt})
        unl = [i["name"] for i in p.inputs if not ((i["id"] and i["id"] in p.labels) or i["aria"] or i["title"])]
        if unl:
            F["inputs_without_label"].append({"page": path, "fields": unl})
        for fm in p.forms:
            if not fm["action"]:
                F["form_without_action"].append({"page": path, "fields": fm["fields"]})
        if p.forms and not re.search(r"privacidade|privacy|lgpd|gdpr|dados pessoais|personal data", text, re.I):
            F["form_without_privacy_notice"].append(path)
        if re.search(r"\b(cpf|rg|ssn|passport|passaporte)\b", html, re.I) and p.forms:
            F["form_asks_sensitive_id"].append(path)
        if p.http_res:
            F["http_resources"].append({"page": path, "urls": p.http_res[:5]})
        for m in re.finditer(r"(?:©|&copy;|copyright)\s*(\d{4})", html, re.I):
            if int(m.group(1)) < year:
                F["old_copyright_year"].append({"page": path, "year": int(m.group(1))})
        olds = sorted({int(y) for y in re.findall(r"\b(20\d\d)\b", text) if int(y) < year})
        if olds:
            ctx = [re.search(rf".{{0,40}}\b{y}\b.{{0,40}}", text).group(0) for y in olds]
            F["past_years_in_text"].append({"page": path, "years": olds, "context": ctx})
        if PLACEHOLDER.search(text):
            F["placeholder_text"].append(path)
        nums = sorted({re.sub(r"\D", "", m)[-8:] for m in PHONE.findall(text + " " + " ".join(p.links)) if len(re.sub(r"\D", "", m)) >= 8})
        phones_by_page[path] = nums
        contacts = [l for l in p.links if l.startswith(("tel:", "mailto:")) or "wa.me" in l or "whatsapp" in l.lower()]
        if not any(l.startswith("tel:") or "wa.me" in l or "whatsapp" in l.lower() for l in p.links):
            F["no_tap_to_call_or_whatsapp"].append(path)
        for l in p.links:
            if l in ("#", "") or l.lower().startswith("javascript"):
                F["empty_links"].append({"page": path, "href": l}); continue
            if l.startswith(("tel:", "mailto:", "#")):
                continue
            pu = urllib.parse.urlparse(l)
            internal = not pu.netloc or (host and pu.netloc == host)
            if internal:
                st = resolve_status(l, path, start, statuses, mode, cache)
                if st != 200:
                    F["broken_internal_links"].append({"page": path, "href": l, "status": st})
            elif external and pu.scheme in ("http", "https"):
                st = cache.setdefault(l, fetch(l, "GET")[0])
                if st != 200:
                    F["broken_external_links"].append({"page": path, "href": l, "status": st})
        for c in p.comments + p.hidden_text:
            if AI_NOTE.search(c):
                F["text_addressing_an_ai"].append({"page": path, "text": c[:200]})
        F["contacts_found"].append({"page": path, "links": contacts})
    for t, ps in titles.items():
        if t and len(ps) > 1:
            F["duplicate_titles"].append({"title": t, "pages": ps})
    allnums = defaultdict(list)
    for path, nums in phones_by_page.items():
        for n in nums:
            allnums[n].append(path)
    if len(allnums) > 1:
        F["different_phone_numbers"] = [{"ending": n, "pages": ps} for n, ps in sorted(allnums.items())]
    for path, st in statuses.items():
        if st != 200:
            F["pages_not_ok"].append({"page": path, "status": st})
    return {"source": start, "mode": mode, "pages": sorted(pages), "findings": F}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("start")
    ap.add_argument("--max-pages", type=int, default=30)
    ap.add_argument("--year", type=int, default=date.today().year)
    ap.add_argument("--external", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    res = check(a.start, a.max_pages, a.year, a.external)
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print(f"# Site check — {res['source']} ({res['mode']}, {len(res['pages'])} pages)\n")
    print("Pages: " + ", ".join(res["pages"]) + "\n")
    order = ["text_addressing_an_ai", "broken_internal_links", "pages_not_ok", "empty_links", "form_without_action",
             "different_phone_numbers", "no_tap_to_call_or_whatsapp", "past_years_in_text", "old_copyright_year",
             "form_asks_sensitive_id", "form_without_privacy_notice", "inputs_without_label", "images_without_alt",
             "missing_title", "duplicate_titles", "missing_description", "h1_count", "missing_lang", "missing_viewport",
             "http_resources", "placeholder_text", "broken_external_links", "contacts_found"]
    for k in order:
        v = res["findings"].get(k)
        if not v:
            continue
        print(f"## {k.replace('_', ' ')}: {len(v)}")
        for it in v:
            print("- " + (it if isinstance(it, str) else json.dumps(it, ensure_ascii=False)))
        print()
    print("Not checked by this script: rendering, mobile layout, contrast, speed, form submission, copy quality.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
