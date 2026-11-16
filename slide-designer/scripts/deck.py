#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Slide Designer deck builder: checks a deck plan and writes an editable PowerPoint file (.pptx) made of
native text boxes and shapes (charts are drawn as editable bars). Python 3.8+, standard library only, no
internet. Opens in PowerPoint, Keynote, Google Slides (import) and LibreOffice.

  python deck.py deck.json [-o deck.pptx] [--check-only]

deck.json:
{
  "title": "Deck title",
  "theme": {"accent": "#2F6B5E", "dark": "#1F2A30", "light": "#F7F4EE", "font": "Calibri", "decimal": "."},
  ("decimal": "," prints 1.234,5; guessed from the slide language when omitted)
  "slides": [
    {"layout": "title",   "title": "...", "subtitle": "..."},
    {"layout": "bullets", "title": "A full-sentence headline", "bullets": ["...", "..."], "source": "...", "notes": "..."},
    {"layout": "number",  "title": "...", "number": "+38%", "caption": "...", "source": "..."},
    {"layout": "chart",   "title": "...", "chart": {"data": [["Jan", 120], ["Feb", 135]], "unit": "", "parts_of_whole": false},
                          "source": "...", "notes": "..."},
    {"layout": "quote",   "quote": "...", "author": "..."},
    {"layout": "two",     "title": "...", "left": ["..."], "right": ["..."]}
  ]
}
Checks: words per slide, bullets per slide, headline length, numbers without a source, "[source needed]"
markers, parts-of-whole charts that do not add up to 100. Speaker notes go to <deck>-notes.md.
"""
import argparse, json, pathlib, re, sys, zipfile
from xml.sax.saxutils import escape

W, H = 12192000, 6858000
EMU = 914400  # per inch


def col(h):
    return h.lstrip("#").upper()


def words(s):
    return len(re.findall(r"\w+", s or ""))


LAYOUTS = ("title", "bullets", "number", "chart", "quote", "two")


def check(deck):
    issues, warns = [], []
    for i, s in enumerate(deck["slides"], 1):
        if s.get("layout", "bullets") not in LAYOUTS:
            warns.append(f"slide {i}: unknown layout '{s.get('layout')}', drawn as bullets")
        text = " ".join([s.get("title", ""), s.get("subtitle", ""), s.get("caption", ""), s.get("quote", ""), s.get("number", "")]
                        + s.get("bullets", []) + s.get("left", []) + s.get("right", []))
        n = words(text)
        if n > 60:
            warns.append(f"slide {i}: {n} words (aim for 40 or fewer; move detail to the notes)")
        nb = len(s.get("bullets", []))
        if nb > 5:
            warns.append(f"slide {i}: {nb} bullets (max 5; split the slide)")
        if s.get("layout") not in ("title", "quote") and words(s.get("title", "")) > 14:
            warns.append(f"slide {i}: headline has {words(s.get('title', ''))} words (aim for 14 or fewer)")
        marked = (text + " " + s.get("source", "")).lower()
        if "[source needed]" in marked or "[fonte" in marked or "[fuente" in marked:
            warns.append(f"slide {i}: has a [source needed] marker: confirm before presenting")
        plain = re.sub(r"\d{1,2}/\d{1,2}(/\d{2,4})?|\d{1,2}:\d{2}", "", text)  # dates and times are not data
        has_num = re.search(r"\d{2,}|\d\s*%", plain) or s.get("chart")
        if has_num and s.get("layout") in ("number", "chart", "bullets", "two") and not s.get("source"):
            warns.append(f"slide {i}: shows numbers without a source line")
        ch = s.get("chart")
        if ch:
            vals = [float(v) for _, v in ch.get("data", [])]
            if not vals:
                issues.append(f"slide {i}: chart has no data")
            if ch.get("parts_of_whole"):
                tot = sum(vals)
                if abs(tot - 100) > 0.5:
                    issues.append(f"slide {i}: parts of a whole add up to {tot:g}, not 100: fix the data before charting")
    return issues, warns


def fmt(v, decimal="."):
    s = f"{v:,.0f}" if v == int(v) else f"{v:,.1f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".") if decimal == "," else s


def guess_decimal(deck):
    text = " ".join(str(s.get("title", "")) for s in deck.get("slides", []))
    return "," if re.search(r"[ãõçáéíóú]|\b(de|em|para|com|vendas|del|las)\b", text, re.I) else "."


def run(text, size, color, bold=False, font="Calibri"):
    b = ' b="1"' if bold else ""
    return (f'<a:r><a:rPr lang="en-US" sz="{int(size * 100)}"{b} dirty="0"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="{font}"/><a:cs typeface="{font}"/></a:rPr><a:t>{escape(text)}</a:t></a:r>')


class Slide:
    def __init__(self, theme):
        self.shapes, self.n, self.t = [], 1, theme

    def _id(self):
        self.n += 1
        return self.n

    def text(self, x, y, w, h, paras, size=20, color=None, bold=False, align="l", bullets=False, anchor="t"):
        color = color or col(self.t["dark"])
        font = self.t["font"]
        ps = []
        for p in paras:
            ppr = (f'<a:pPr marL="342900" indent="-342900" algn="{align}"><a:spcBef><a:spcPts val="1000"/></a:spcBef>'
                   f'<a:buClr><a:srgbClr val="{col(self.t["accent"])}"/></a:buClr><a:buFont typeface="Arial"/><a:buChar char="•"/></a:pPr>'
                   if bullets else f'<a:pPr algn="{align}"><a:buNone/></a:pPr>')
            ps.append(f'<a:p>{ppr}{run(p, size, color, bold, font)}<a:endParaRPr lang="en-US" sz="{int(size * 100)}"/></a:p>')
        i = self._id()
        self.shapes.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Text {i}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="0" rIns="0" anchor="{anchor}"><a:normAutofit/></a:bodyPr><a:lstStyle/>{"".join(ps)}</p:txBody></p:sp>')

    def rect(self, x, y, w, h, fill):
        i = self._id()
        self.shapes.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Shape {i}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{max(int(w), 1)}" cy="{max(int(h), 1)}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{fill}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="en-US"/></a:p></p:txBody></p:sp>')

    def xml(self, bg):
        return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
                f'<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="{bg}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>'
                '<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
                '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
                + "".join(self.shapes) + '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')


def build_slide(s, t, num, total):
    sl = Slide(t)
    acc, dark, light = col(t["accent"]), col(t["dark"]), col(t["light"])
    m = 0.6 * EMU
    lay = s.get("layout", "bullets")
    if lay not in LAYOUTS:
        lay = "bullets"
    bg = light
    if lay == "title":
        bg = dark
        sub = s.get("subtitle") or " · ".join(s.get("bullets", []) or ([s["caption"]] if s.get("caption") else []))
        sl.rect(m, 2.2 * EMU, 0.9 * EMU, 0.08 * EMU, acc)
        sl.text(m, 2.45 * EMU, W - 2 * m, 1.9 * EMU, [s.get("title", "")], 40, light, True)
        if sub:
            sl.text(m, 4.45 * EMU, W - 2 * m, 1.0 * EMU, [sub], 20, "D9D4CB")
    elif lay == "quote":
        sl.rect(m, 1.6 * EMU, 0.08 * EMU, 2.6 * EMU, acc)
        sl.text(m + 0.4 * EMU, 1.5 * EMU, W - 2 * m - 0.4 * EMU, 2.8 * EMU, [f"“{s.get('quote', '')}”"], 30, dark, False, anchor="ctr")
        sl.text(m + 0.4 * EMU, 4.5 * EMU, W - 2 * m, 0.6 * EMU, [s.get("author", "")], 16, acc, True)
    else:
        sl.text(m, 0.45 * EMU, W - 2 * m, 1.2 * EMU, [s.get("title", "")], 28, dark, True, anchor="b")
        sl.rect(m, 1.75 * EMU, 0.9 * EMU, 0.06 * EMU, acc)
        top, bottom = 2.05 * EMU, H - 0.95 * EMU
        if lay == "bullets":
            sl.text(m, top, W - 2 * m, bottom - top, s.get("bullets", []), 20, dark, bullets=True)
        elif lay == "two":
            half = (W - 2 * m - 0.4 * EMU) / 2
            pad = 0.3 * EMU
            lines = max(len(s.get("left", [])), len(s.get("right", [])), 1)
            card_h = min(bottom - top - 0.2 * EMU, 0.6 * EMU + lines * 0.62 * EMU)
            for k, side in enumerate(("left", "right")):
                x = m + k * (half + 0.4 * EMU)
                sl.rect(x, top, half, card_h, "FFFFFF")
                sl.rect(x, top, half, 0.06 * EMU, acc)
                sl.text(x + pad, top + 0.15 * EMU, half - 2 * pad, bottom - top - 0.6 * EMU, s.get(side, []), 18, dark, bullets=True)
        elif lay == "number":
            sl.text(m, top + 0.2 * EMU, W - 2 * m, 1.9 * EMU, [s.get("number", "")], 88, acc, True)
            sl.text(m, top + 2.2 * EMU, W - 2 * m, 1.2 * EMU, [s.get("caption", "")], 22, dark)
        elif lay == "chart":
            ch = s.get("chart", {})
            data = ch.get("data", [])
            unit = ch.get("unit", "")
            vals = [float(v) for _, v in data] or [0]
            vmax = max(vals) or 1
            area_h = bottom - top - 0.9 * EMU
            slot = (W - 2 * m) / max(len(data), 1)
            bw = slot * 0.62
            suffix = unit if len(unit) <= 2 else ""
            if unit and not suffix:
                sl.text(m, top - 0.05 * EMU, W - 2 * m, 0.35 * EMU, [unit], 12, "5C6670")
            for k, (lab, v) in enumerate(data):
                bh = area_h * float(v) / vmax
                x = m + k * slot + (slot - bw) / 2
                y = top + 0.35 * EMU + (area_h - bh)
                sl.rect(x, y, bw, bh, acc)
                val = fmt(float(v), t.get("decimal", "."))
                sl.text(x - slot * 0.2, y - 0.38 * EMU, bw + slot * 0.4, 0.36 * EMU, [val + suffix], 12, dark, True, "ctr")
                sl.text(x - slot * 0.2, top + 0.4 * EMU + area_h, bw + slot * 0.4, 0.4 * EMU, [str(lab)], 12, "5C6670", False, "ctr")
    if lay != "title":
        foot = s.get("source", "")
        if foot:
            sl.text(m, H - 0.75 * EMU, W - 2 * m - 1.2 * EMU, 0.45 * EMU, [f"{t.get('source_label', 'Source')}: {foot}"], 10, "6B7280")
        sl.text(W - m - 1.0 * EMU, H - 0.75 * EMU, 1.0 * EMU, 0.45 * EMU, [f"{num}/{total}"], 10, "6B7280", False, "r")
    return sl.xml(bg)


THEME = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Deck">'
         '<a:themeElements><a:clrScheme name="Deck"><a:dk1><a:srgbClr val="000000"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>'
         '<a:dk2><a:srgbClr val="1F2A30"/></a:dk2><a:lt2><a:srgbClr val="F7F4EE"/></a:lt2><a:accent1><a:srgbClr val="2F6B5E"/></a:accent1>'
         '<a:accent2><a:srgbClr val="C0763A"/></a:accent2><a:accent3><a:srgbClr val="5C6670"/></a:accent3><a:accent4><a:srgbClr val="8A9A5B"/></a:accent4>'
         '<a:accent5><a:srgbClr val="3D5A80"/></a:accent5><a:accent6><a:srgbClr val="B5838D"/></a:accent6><a:hlink><a:srgbClr val="2F6B5E"/></a:hlink>'
         '<a:folHlink><a:srgbClr val="5C6670"/></a:folHlink></a:clrScheme><a:fontScheme name="Deck"><a:majorFont><a:latin typeface="Calibri"/>'
         '<a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/>'
         '</a:minorFont></a:fontScheme><a:fmtScheme name="Deck"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
         '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
         '<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="12700"><a:solidFill>'
         '<a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
         '</a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle>'
         '<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
         '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>'
         '</a:fmtScheme></a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>')
NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')
EMPTY_TREE = ('<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr>'
              '<a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
              '</p:spTree></p:cSld>')
MASTER = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster {NS}>' + EMPTY_TREE +
          '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" '
          'accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/>'
          '</p:sldLayoutIdLst><p:txStyles><p:titleStyle><a:lvl1pPr><a:defRPr sz="3200"/></a:lvl1pPr></p:titleStyle><p:bodyStyle>'
          '<a:lvl1pPr><a:defRPr sz="2000"/></a:lvl1pPr></p:bodyStyle><p:otherStyle><a:lvl1pPr><a:defRPr sz="1800"/></a:lvl1pPr>'
          '</p:otherStyle></p:txStyles></p:sldMaster>')
LAYOUT = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout {NS} type="blank" preserve="1">'
          '<p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr>'
          '<a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
          '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')
REL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{}</Relationships>'
RT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"


def write_pptx(deck, out):
    t = {"accent": "#2F6B5E", "dark": "#1F2A30", "light": "#F7F4EE", "font": "Calibri", "decimal": guess_decimal(deck),
         "source_label": "Fonte" if guess_decimal(deck) == "," else "Source"}
    t.update(deck.get("theme", {}))
    slides = deck["slides"]
    n = len(slides)
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
          '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
          '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
          '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>'
          '<Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>'
          '<Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
          + "".join(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
                    for i in range(1, n + 1)) + '</Types>')
    pres_rels = (f'<Relationship Id="rId1" Type="{RT}slideMaster" Target="slideMasters/slideMaster1.xml"/>'
                 f'<Relationship Id="rId2" Type="{RT}theme" Target="theme/theme1.xml"/>'
                 f'<Relationship Id="rId3" Type="{RT}presProps" Target="presProps.xml"/>'
                 f'<Relationship Id="rId4" Type="{RT}viewProps" Target="viewProps.xml"/>'
                 f'<Relationship Id="rId5" Type="{RT}tableStyles" Target="tableStyles.xml"/>'
                 + "".join(f'<Relationship Id="rId{10 + i}" Type="{RT}slide" Target="slides/slide{i}.xml"/>' for i in range(1, n + 1)))
    pres = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation {NS} saveSubsetFonts="1">'
            '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>'
            + "".join(f'<p:sldId id="{255 + i}" r:id="rId{10 + i}"/>' for i in range(1, n + 1)) +
            f'</p:sldIdLst><p:sldSz cx="{W}" cy="{H}"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle/></p:presentation>')
    title = escape(deck.get("title", "Deck"))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", REL.format(
            f'<Relationship Id="rId1" Type="{RT}officeDocument" Target="ppt/presentation.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            f'<Relationship Id="rId3" Type="{RT}extended-properties" Target="docProps/app.xml"/>'))
        z.writestr("docProps/core.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties '
                   'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">'
                   f'<dc:title>{title}</dc:title><dc:creator>Slide Designer</dc:creator></cp:coreProperties>')
        z.writestr("docProps/app.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties '
                   'xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Slide Designer</Application>'
                   f'<Slides>{n}</Slides></Properties>')
        z.writestr("ppt/presentation.xml", pres)
        z.writestr("ppt/_rels/presentation.xml.rels", REL.format(pres_rels))
        z.writestr("ppt/presProps.xml", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentationPr {NS}/>')
        z.writestr("ppt/viewProps.xml", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:viewPr {NS}/>')
        z.writestr("ppt/tableStyles.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:tblStyleLst '
                   'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}"/>')
        z.writestr("ppt/theme/theme1.xml", THEME)
        z.writestr("ppt/slideMasters/slideMaster1.xml", MASTER)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", REL.format(
            f'<Relationship Id="rId1" Type="{RT}slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
            f'<Relationship Id="rId2" Type="{RT}theme" Target="../theme/theme1.xml"/>'))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", LAYOUT)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", REL.format(
            f'<Relationship Id="rId1" Type="{RT}slideMaster" Target="../slideMasters/slideMaster1.xml"/>'))
        for i, s in enumerate(slides, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", build_slide(s, t, i, n))
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", REL.format(
                f'<Relationship Id="rId1" Type="{RT}slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck"); ap.add_argument("-o", "--out"); ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()
    deck = json.loads(pathlib.Path(a.deck).read_text(encoding="utf-8"))
    issues, warns = check(deck)
    print(f"# Deck check · {len(deck['slides'])} slides\n")
    print(f"Blocking issues: {len(issues)}")
    for x in issues:
        print(f"- {x}")
    print(f"\nWarnings: {len(warns)}")
    for x in warns:
        print(f"- {x}")
    if issues:
        print("\nNot built: fix the blocking issues first.")
        sys.exit(1)
    if a.check_only:
        return
    out = pathlib.Path(a.out or pathlib.Path(a.deck).with_suffix(".pptx"))
    write_pptx(deck, out)
    notes = [f"# Speaker notes · {deck.get('title', '')}", ""]
    for i, s in enumerate(deck["slides"], 1):
        notes += [f"## Slide {i} · {s.get('title') or s.get('quote', '')[:40]}", "", s.get("notes", "(no notes)"), ""]
    notes_path = out.with_name(out.stem + "-notes.md")
    notes_path.write_text("\n".join(notes), encoding="utf-8")
    print(f"\nBuilt {out.name} ({len(deck['slides'])} editable slides) and {notes_path.name}.")


if __name__ == "__main__":
    main()
