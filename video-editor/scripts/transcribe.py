#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fast local transcription with word timestamps (faster-whisper, CPU int8; no GPU needed).

  python transcribe.py raw.mp4 -o project/ [--model small|medium|large-v3] [--lang en]
                       [--fix "wrong words=Right; other=Fix"]

Writes into the output folder:
  transcript.srt  sentences with times (input for cutkit.py srt)
  words.json      every word with start/end (input for animated captions)
  transcript.txt  one sentence per line with timecodes, for reading and deciding cuts

Requires: pip install faster-whisper numpy, and ffmpeg on PATH. The model downloads once (~500 MB for small).
--fix only corrects obvious mishearings (brand names, jargon) and keeps the word timing. Do not pass
hotwords or an initial prompt to Whisper: it merges sentences into long blocks.
"""
import argparse, json, os, re, subprocess, sys, time

import numpy as np
from faster_whisper import WhisperModel


def load_audio(path, sr=16000):
    # decode with ffmpeg: avoids PyAV version mismatches
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1",
                          "-ar", str(sr), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def ts(sec):
    ms = int(round(sec * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def _norm(w):
    return re.sub(r"[^\w]", "", w.lower())


def apply_fixes(words, rules):
    """Replace misheard word sequences ("vignates app=WhatsApp"), merging their timing.
    Punctuation attached to the last replaced word is kept."""
    for rule in filter(None, (r.strip() for r in rules.split(";"))):
        wrong, right = (x.strip() for x in rule.split("=", 1))
        target = [_norm(x) for x in wrong.split()]
        i, out = 0, []
        while i < len(words):
            win = words[i:i + len(target)]
            if len(win) == len(target) and [_norm(w["word"]) for w in win] == target:
                punct = re.search(r"[^\w]*$", win[-1]["word"]).group(0)
                out.append({"start": win[0]["start"], "end": win[-1]["end"], "word": right + punct,
                            "prob": 1.0, "fixed_from": wrong})
                i += len(target)
            else:
                out.append(words[i]); i += 1
        words = out
    return words


def to_sentences(words, pause=0.6, max_words=14):
    out, cur = [], []
    for w in words:
        if cur and (w["start"] - cur[-1]["end"] > pause or len(cur) >= max_words):
            out.append(cur); cur = []
        cur.append(w)
        if w["word"][-1:] in ".?!":
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return [{"start": s[0]["start"], "end": s[-1]["end"], "text": " ".join(w["word"] for w in s)} for s in out]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("-o", required=True, help="output folder")
    ap.add_argument("--model", default="small")
    ap.add_argument("--lang", default=None, help="language code (en, pt, es...); auto-detect if omitted")
    ap.add_argument("--fix", default="", help='obvious mishearings: "vignates app=WhatsApp; clod=Claude"')
    a = ap.parse_args()

    os.makedirs(a.o, exist_ok=True)
    t0 = time.time()
    model = WhisperModel(a.model, device="cpu", compute_type="int8", cpu_threads=os.cpu_count() or 4)
    segs, info = model.transcribe(load_audio(a.video), language=a.lang, word_timestamps=True,
                                  vad_filter=True, vad_parameters={"min_silence_duration_ms": 300})
    words = [{"start": round(w.start, 3), "end": round(w.end, 3), "word": w.word.strip(), "prob": round(w.probability, 2)}
             for s in segs for w in (s.words or [])]
    words = apply_fixes(words, a.fix)
    sentences = to_sentences(words)
    for s in sentences:
        print(f"[{s['start']:7.2f} -> {s['end']:7.2f}] {s['text']}", flush=True)

    with open(os.path.join(a.o, "transcript.srt"), "w", encoding="utf-8") as f:
        for i, s in enumerate(sentences, 1):
            f.write(f"{i}\n{ts(s['start'])} --> {ts(s['end'])}\n{s['text']}\n\n")
    with open(os.path.join(a.o, "words.json"), "w", encoding="utf-8") as f:
        json.dump({"duration": round(info.duration, 3), "language": info.language, "words": words},
                  f, ensure_ascii=False, indent=1)
    with open(os.path.join(a.o, "transcript.txt"), "w", encoding="utf-8") as f:
        for s in sentences:
            f.write(f"[{s['start']:.2f} -> {s['end']:.2f}] {s['text']}\n")
    print(f"\nOK: {len(sentences)} sentences, {len(words)} words, audio {info.duration:.1f}s, "
          f"took {time.time() - t0:.1f}s (model {a.model})", file=sys.stderr)


if __name__ == "__main__":
    main()
