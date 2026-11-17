#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bridge from the approved cut to the motion template (Remotion, see reference/motion.md).

Re-times every transcript word onto the cut timeline, groups words into caption pages, optionally
speeds up the video (pitch preserved), cleans the voice and grades the image, then writes props.json.
The processed video goes into the template's public/ folder (Remotion only reads files from there).

  python prepare_motion.py v1/v1.mp4 words.json cut-plan.json -o v1/props.json --public motion/public \
      [--elements elements.json] [--style highlight|karaoke|clean] [--color "#FFD400"|multicolor]
      [--max-words 3] [--zoom] [--progress] [--speed 1.12] [--audio --models models/] [--image]

Element times in elements.json are on the cut timeline (as in the cut plan); --speed rescales them.
"""
import argparse, json, os, subprocess

# light grade: removes an orange/pink LED cast, smooths skin and compression blocks, restores sharpness.
# It does not reshape or "beautify" the face.
IMAGE_FILTER = ("bilateral=sigmaS=3:sigmaR=0.06,colorbalance=rs=-0.03:rm=-0.07:rh=-0.04:gm=0.01:bm=0.03,"
                "eq=contrast=1.07:saturation=0.9:gamma=1.02,unsharp=5:5:0.7:5:5:0.0")


def audio_filter(models):
    """Voice clean-up: rumble cut, RNNoise (if the model file exists), light FFT denoise, presence EQ,
    de-esser, compressor and social-media loudness (-14 LUFS)."""
    chain = ["highpass=f=80"]
    rnn = os.path.join(models or "", "sh.rnnn")
    if models and os.path.isfile(rnn):
        p = os.path.abspath(rnn).replace("\\", "/").replace(":", "\\:")
        # RNNoise can emit NaN on digital silence at the joins: zero those samples
        chain += [f"arnndn=m='{p}':mix=0.9", "aeval='if(isnan(val(ch)),0,val(ch))':c=same"]
    chain += ["afftdn=nr=6:nf=-42", "equalizer=f=250:t=q:w=1.2:g=-2.5", "equalizer=f=3500:t=q:w=1.0:g=3",
              "deesser", "acompressor=threshold=-20dB:ratio=3:attack=10:release=150:makeup=2",
              "loudnorm=I=-14:TP=-1.5:LRA=9"]
    return ",".join(chain)


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate:format=duration", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    s = d["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    fps = round(float(num) / float(den or 1))
    return {"width": s["width"], "height": s["height"], "fps": 30 if fps > 120 else fps,
            "duration": float(d["format"]["duration"])}


def rescale(obj, v):
    """Divide every time field (start/end/at) by the speed factor."""
    if isinstance(obj, list):
        return [rescale(x, v) for x in obj]
    if isinstance(obj, dict):
        return {k: (round(x / v, 3) if k in ("start", "end", "at") and isinstance(x, (int, float)) else rescale(x, v))
                for k, x in obj.items()}
    return obj


def retime(words, plan):
    t, segs = 0.0, []
    for s in plan["segments"]:
        segs.append((s["in"], s["out"], t)); t += s["out"] - s["in"]
    out = []
    for w in words:
        # the segment with the largest overlap (Whisper stretches word starts into the pause before)
        ov, a, b, new = max((min(w["end"], b) - max(w["start"], a), a, b, new) for a, b, new in segs)
        if ov >= min(0.12, (w["end"] - w["start"]) / 2):
            out.append({"start": round(max(w["start"], a) - a + new, 3),
                        "end": round(min(w["end"], b) - a + new, 3), "word": w["word"]})
    return sorted(out, key=lambda w: w["start"])


def paginate(words, max_words, max_chars=22, pause=0.45):
    pages, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or len(" ".join(x["word"] for x in cur + [w])) > max_chars
                    or w["start"] - cur[-1]["end"] > pause or cur[-1]["word"][-1:] in ".?!,;:"):
            pages.append(cur); cur = []
        cur.append(w)
    if cur:
        pages.append(cur)
    res = []
    for i, p in enumerate(pages):
        end = p[-1]["end"]
        if i + 1 < len(pages):  # hold the caption until the next one when the gap is short
            nxt = pages[i + 1][0]["start"]
            end = nxt if nxt - end < 0.35 else end + 0.15
        res.append({"start": p[0]["start"], "end": round(end, 3), "words": p})
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("words"); ap.add_argument("plan")
    ap.add_argument("-o", required=True)
    ap.add_argument("--public", required=True, help="the motion template's public/ folder")
    ap.add_argument("--elements")
    ap.add_argument("--style", default="highlight", choices=["highlight", "karaoke", "clean"])
    ap.add_argument("--color", default="#FFD400", help='highlight colour, or "multicolor" to rotate the palette')
    ap.add_argument("--max-words", type=int, default=3)
    ap.add_argument("--zoom", action="store_true", help="alternate punch-in at every cut (hides jump cuts)")
    ap.add_argument("--progress", action="store_true", help="progress bar on top")
    ap.add_argument("--speed", type=float, default=1.0, help="1.12 = 12%% faster, voice pitch preserved")
    ap.add_argument("--audio", action="store_true", help="clean and level the voice")
    ap.add_argument("--models", help="folder with sh.rnnn (RNNoise model) for stronger noise removal")
    ap.add_argument("--image", action="store_true", help="light colour correction, skin smoothing, sharpening")
    a = ap.parse_args()

    words = json.load(open(a.words, encoding="utf-8-sig"))["words"]
    plan = json.load(open(a.plan, encoding="utf-8-sig"))
    new_words = retime(words, plan)
    elements = json.load(open(a.elements, encoding="utf-8-sig")) if a.elements else []
    cuts = []
    t = 0.0
    for s in plan["segments"]:
        d = s["out"] - s["in"]
        cuts.append({"start": round(t, 3), "end": round(t + d, 3)}); t += d

    os.makedirs(a.public, exist_ok=True)
    name = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(a.video)))) + "_" + os.path.basename(a.video)
    fps = probe(a.video)["fps"]
    v = a.speed
    vf = ([IMAGE_FILTER] if a.image else []) + ([f"setpts=PTS/{v}"] if v != 1 else []) + [f"fps={fps}"]
    af = ([audio_filter(a.models)] if a.audio else []) + ([f"atempo={v}"] if v != 1 else []) + ["aresample=async=1"]
    # constant frame rate re-encode: Remotion needs continuous frames
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.video, "-vf", ",".join(vf),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-af", ",".join(af), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
                    os.path.join(a.public, name)], check=True)
    info = probe(os.path.join(a.public, name))
    if v != 1:
        new_words, elements, cuts = rescale(new_words, v), rescale(elements, v), rescale(cuts, v)

    props = {"video": name, "fps": info["fps"], "width": info["width"], "height": info["height"],
             "duration": round(info["duration"], 3), "style": a.style, "color": a.color,
             "pages": paginate(new_words, a.max_words), "elements": elements, "cuts": cuts,
             "zoom": a.zoom, "progress": a.progress}
    with open(a.o, "w", encoding="utf-8") as f:
        json.dump(props, f, ensure_ascii=False, indent=1)
    print(f"OK: {len(new_words)} words in {len(props['pages'])} captions, {info['width']}x{info['height']} "
          f"{info['fps']}fps, {info['duration']:.2f}s -> {a.o}")


if __name__ == "__main__":
    main()
