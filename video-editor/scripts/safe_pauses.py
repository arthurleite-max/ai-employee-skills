#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Intersect ffmpeg's silence detection with the transcript's words: a stretch only counts as a pause
when it is silent AND falls between two words. Quiet speech (poor audio) is never cut as "silence".

  python cutkit.py silences raw.mp4 --min 0.4 --noise=-32dB > silences.json
  python safe_pauses.py silences.json words.json -o pauses.json [--min 0.3] [--margin 0.05]
  python cutkit.py plan raw.mp4 --silences pauses.json --remove cuts.json > cut-plan.json
"""
import argparse, json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("silences"); ap.add_argument("words"); ap.add_argument("-o", required=True)
    ap.add_argument("--min", type=float, default=0.3, help="shortest pause worth cutting (s)")
    ap.add_argument("--margin", type=float, default=0.05, help="air kept around every word (s)")
    a = ap.parse_args()

    sil = json.load(open(a.silences, encoding="utf-8-sig"))
    data = json.load(open(a.words, encoding="utf-8-sig"))
    # Whisper tends to stretch a word's start back into the pause before it: protect only a plausible
    # duration for the word (by letter count), measured back from its end
    w = [{"start": max(x["start"], x["end"] - (0.08 + 0.065 * len(x["word"]))), "end": x["end"]}
         for x in data["words"]]
    gaps = [(0.0, w[0]["start"] - a.margin)] if w else []
    gaps += [(x["end"] + a.margin, y["start"] - a.margin) for x, y in zip(w, w[1:])]
    if w:
        gaps.append((w[-1]["end"] + a.margin, data.get("duration", w[-1]["end"]) + 1))
    out = []
    for s in sil:
        for ga, gb in gaps:
            lo, hi = max(s["start"], ga), min(s["end"], gb)
            if hi - lo >= a.min:
                out.append({"start": round(lo, 3), "end": round(hi, 3)})
    with open(a.o, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(f"{len(sil)} ffmpeg silences -> {len(out)} safe pauses (none touching a word)")


if __name__ == "__main__":
    main()
