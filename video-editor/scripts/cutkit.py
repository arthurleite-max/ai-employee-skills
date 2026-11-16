#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Video Editor cut kit: probe, find silences, build a cut plan, render the cut, re-time captions,
export an EDL and burn captions. Python 3.8+ standard library + ffmpeg/ffprobe on PATH.
Never modifies the source; every output goes where -o / > points. No internet.

  python cutkit.py probe raw.mp4
  python cutkit.py silences raw.mp4 [--min 0.4] [--noise -35dB]            > silences.json
  python cutkit.py plan raw.mp4 --silences silences.json [--remove cuts.json]
                    [--keep-air 0.15] [--pad 0.05 0.08] [--order 3,1,2,...]  > cut-plan.json
  python cutkit.py render raw.mp4 cut-plan.json -o v1/v1.mp4 [--vertical] [--preview]
  python cutkit.py srt transcript.srt cut-plan.json -o v1/captions.srt [--max-chars 32] [--lines 2]
  python cutkit.py edl cut-plan.json -o v1/edit.edl [--fps 30] [--reel RAW]
  python cutkit.py burn v1.mp4 captions.srt -o v1_captions.mp4 [--style clean|bold]

cuts.json (editorial cuts decided from the transcript):
  {"remove": [{"in": 31.4, "out": 39.0, "reason": "retake of point 2"}]}
cut-plan.json can also be written by hand (or by the AI) and passed straight to render/srt/edl:
  {"source": "raw.mp4", "segments": [{"in": 102.3, "out": 105.1, "note": "hook"}, ...]}
"""
import argparse, json, os, re, subprocess, sys, tempfile


def run(cmd, capture=True):
    p = subprocess.run(cmd, capture_output=capture, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{p.stderr[-2000:]}")
    return p


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "format=duration:stream=codec_type,width,height,r_frame_rate,channels,sample_rate",
               "-of", "json", path]).stdout
    d = json.loads(out)
    info = {"file": path, "duration": round(float(d["format"]["duration"]), 3)}
    for s in d.get("streams", []):
        if s.get("codec_type") == "video" and "width" not in info:
            num, den = (s.get("r_frame_rate") or "0/1").split("/")
            info.update(width=s["width"], height=s["height"], fps=round(float(num) / float(den or 1), 3))
        elif s.get("codec_type") == "audio" and "channels" not in info:
            info.update(channels=s.get("channels"), sample_rate=s.get("sample_rate"))
    info["orientation"] = ("vertical" if info.get("height", 0) > info.get("width", 0) else "horizontal") if "width" in info else "audio only"
    return info


def silences(path, min_len, noise):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
               f"silencedetect=noise={noise}:d={min_len}", "-f", "null", "-"]).stderr
    out, start = [], None
    for line in err.splitlines():
        m = re.search(r"silence_start: (-?[\d.]+)", line)
        if m:
            start = max(0.0, float(m[1]))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m and start is not None:
            out.append({"start": round(start, 3), "end": round(float(m[1]), 3)}); start = None
    if start is not None:
        out.append({"start": round(start, 3), "end": probe(path)["duration"]})
    return out


def subtract(keep, rng):
    a, b = rng
    res = []
    for s, e in keep:
        if b <= s or a >= e:
            res.append((s, e)); continue
        if a > s:
            res.append((s, a))
        if b < e:
            res.append((b, e))
    return res


def plan(path, sil, removes, keep_air, pad, order):
    dur = probe(path)["duration"]
    keep = [(0.0, dur)]
    removed = []
    for s in sil:
        a, b = s["start"] + keep_air / 2, s["end"] - keep_air / 2
        if b - a > 0.05:
            keep = subtract(keep, (a, b)); removed.append({"in": round(a, 3), "out": round(b, 3), "reason": "pause"})
    for r in removes:
        keep = subtract(keep, (float(r["in"]), float(r["out"])))
        removed.append({"in": float(r["in"]), "out": float(r["out"]), "reason": r.get("reason", "editorial")})
    pre, post = pad
    segs = []
    for s, e in keep:
        if e - s < 0.12:
            continue
        segs.append({"in": round(max(0.0, s - pre if s > 0 else s), 3), "out": round(min(dur, e + post if e < dur else e), 3)})
    # padding must not make neighbours overlap
    for i in range(1, len(segs)):
        if segs[i]["in"] < segs[i - 1]["out"]:
            mid = round((segs[i]["in"] + segs[i - 1]["out"]) / 2, 3)
            segs[i - 1]["out"], segs[i]["in"] = mid, mid
    if order:
        idx = [int(x) - 1 for x in order.split(",")]
        segs = [segs[i] for i in idx]
    return finish({"source": path, "source_duration": dur, "segments": segs,
                   "removed": sorted(removed, key=lambda r: r["in"])})


def finish(p):
    t = 0.0
    for s in p["segments"]:
        s["duration"] = round(s["out"] - s["in"], 3)
        s["new_start"] = round(t, 3)
        t += s["duration"]
    p["new_duration"] = round(t, 3)
    p["sum"] = " + ".join(f"{s['duration']:.2f}" for s in p["segments"]) + f" = {t:.2f}"
    return p


def load_plan(path):
    p = json.load(open(path, encoding="utf-8"))
    return finish(p)


def render(src, plan_p, out, vertical, preview):
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    info = probe(src)
    has_video = "width" in info
    vf = []
    if vertical and has_video and info["width"] > info["height"]:
        vf.append("crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920")
    elif preview and has_video:
        vf.append("scale=-2:720")
    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        for i, s in enumerate(plan_p["segments"]):
            d = s["duration"]
            part = os.path.join(tmp, f"p{i:03d}.mkv")
            af = f"afade=t=in:st=0:d=0.03,afade=t=out:st={max(0.0, d - 0.03):.3f}:d=0.03"
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{s['in']:.3f}", "-i", src, "-t", f"{d:.3f}"]
            if has_video:
                cmd += ["-vf", ",".join(vf) if vf else "null", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                        "-pix_fmt", "yuv420p"]
            cmd += ["-af", af, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", part]
            run(cmd); parts.append(part)
        lst = os.path.join(tmp, "list.txt")
        with open(lst, "w", encoding="utf-8") as f:
            f.writelines(f"file '{p}'\n" for p in parts)
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
             "-c", "copy", "-movflags", "+faststart", out])
    got = probe(out)["duration"]
    diff = round(got - plan_p["new_duration"], 3)
    tol = 0.1 * max(1, len(plan_p["segments"])) ** 0.5
    return {"output": out, "planned": plan_p["new_duration"], "actual": got, "difference": diff,
            "ok": abs(diff) <= tol}


def ts(sec):
    ms = int(round(sec * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def parse_srt(path):
    raw = open(path, encoding="utf-8-sig").read().replace("\r", "")
    out = []
    for blk in re.split(r"\n\s*\n", raw.strip()):
        m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", blk)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        text = " ".join(blk[m.end():].strip().split("\n")).strip()
        if text:
            out.append((a, b, text))
    return out


def wrap(text, max_chars, lines):
    words, rows, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_chars:
            rows.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        rows.append(cur)
    return [rows[i:i + lines] for i in range(0, len(rows), lines)]


def retime(cues, plan_p, max_chars, lines):
    out = []
    for a, b, text in cues:
        for s in plan_p["segments"]:
            lo, hi = max(a, s["in"]), min(b, s["out"])
            if hi - lo < 0.2:
                continue
            na, nb = lo - s["in"] + s["new_start"], hi - s["in"] + s["new_start"]
            chunks = wrap(text, max_chars, lines)
            step = (nb - na) / len(chunks)
            for i, ch in enumerate(chunks):
                out.append((na + i * step, na + (i + 1) * step, "\n".join(ch)))
    out.sort()
    return out


def write_srt(cues, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for i, (a, b, t) in enumerate(cues, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n")


def tc(sec, fps):
    f = int(round(sec * fps))
    fr = int(round(fps))
    return f"{f // (3600 * fr):02d}:{f // (60 * fr) % 60:02d}:{f // fr % 60:02d}:{f % fr:02d}"


def edl(plan_p, path, fps, reel):
    lines = ["TITLE: VIDEO EDITOR CUT", "FCM: NON-DROP FRAME", ""]
    for i, s in enumerate(plan_p["segments"], 1):
        rec_in, rec_out = s["new_start"], s["new_start"] + s["duration"]
        lines.append(f"{i:03d}  {reel[:8]:<8} AA/V  C        {tc(s['in'], fps)} {tc(s['out'], fps)} {tc(rec_in, fps)} {tc(rec_out, fps)}")
        lines.append(f"* FROM CLIP NAME: {os.path.basename(plan_p.get('source', reel))}")
        if s.get("note"):
            lines.append(f"* COMMENT: {s['note']}")
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def burn(video, srt, out, style):
    styles = {"clean": "FontName=Arial,FontSize=11,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=20",
              "bold": "FontName=Arial,FontSize=16,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=0,Alignment=2,MarginV=55"}
    tmpdir = tempfile.mkdtemp()
    local = os.path.join(tmpdir, "c.srt")  # avoids escaping problems with drive letters and spaces
    with open(srt, encoding="utf-8") as a, open(local, "w", encoding="utf-8") as b:
        b.write(a.read())
    cwd = os.getcwd()
    out_abs, video_abs = os.path.abspath(out), os.path.abspath(video)
    os.chdir(tmpdir)
    try:
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", video_abs, "-vf",
             f"subtitles=c.srt:force_style='{styles[style]}'", "-c:a", "copy", out_abs])
    finally:
        os.chdir(cwd)
    return out_abs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("probe"); s.add_argument("video")
    s = sub.add_parser("silences"); s.add_argument("video"); s.add_argument("--min", type=float, default=0.4); s.add_argument("--noise", default="-35dB")
    s = sub.add_parser("plan"); s.add_argument("video"); s.add_argument("--silences"); s.add_argument("--remove")
    s.add_argument("--keep-air", type=float, default=0.15); s.add_argument("--pad", nargs=2, type=float, default=[0.05, 0.08]); s.add_argument("--order")
    s = sub.add_parser("render"); s.add_argument("video"); s.add_argument("plan"); s.add_argument("-o", required=True)
    s.add_argument("--vertical", action="store_true"); s.add_argument("--preview", action="store_true")
    s = sub.add_parser("srt"); s.add_argument("transcript"); s.add_argument("plan"); s.add_argument("-o", required=True)
    s.add_argument("--max-chars", type=int, default=32); s.add_argument("--lines", type=int, default=2)
    s = sub.add_parser("edl"); s.add_argument("plan"); s.add_argument("-o", required=True); s.add_argument("--fps", type=float, default=30); s.add_argument("--reel", default="RAW")
    s = sub.add_parser("burn"); s.add_argument("video"); s.add_argument("srt"); s.add_argument("-o", required=True); s.add_argument("--style", default="bold", choices=["clean", "bold"])
    a = ap.parse_args()
    if a.cmd == "probe":
        print(json.dumps(probe(a.video), indent=1))
    elif a.cmd == "silences":
        print(json.dumps(silences(a.video, a.min, a.noise), indent=1))
    elif a.cmd == "plan":
        sil = json.load(open(a.silences, encoding="utf-8")) if a.silences else []
        rem = json.load(open(a.remove, encoding="utf-8")).get("remove", []) if a.remove else []
        print(json.dumps(plan(a.video, sil, rem, a.keep_air, a.pad, a.order), indent=1, ensure_ascii=False))
    elif a.cmd == "render":
        print(json.dumps(render(a.video, load_plan(a.plan), a.o, a.vertical, a.preview), indent=1))
    elif a.cmd == "srt":
        cues = retime(parse_srt(a.transcript), load_plan(a.plan), a.max_chars, a.lines)
        write_srt(cues, a.o); print(f"{len(cues)} captions -> {a.o}")
    elif a.cmd == "edl":
        edl(load_plan(a.plan), a.o, a.fps, a.reel); print(f"EDL -> {a.o}")
    elif a.cmd == "burn":
        print(burn(a.video, a.srt, a.o, a.style))


if __name__ == "__main__":
    main()
