# Cutting: from raw recording to an approved cut

## Read the transcript like an editor

Work from a transcript with timestamps (phrase level is enough; word level is better). Read **every
line** before deciding anything: automatic detectors miss retakes, and a clean-looking transcript can
hide a false start.

Mark each line as one of:

| Mark | What it is | Default decision |
|---|---|---|
| **Keep** | Content that serves the video | Keep |
| **False start** | An abandoned phrase that restarts ("So today— So today I want…") | Cut the abandoned part |
| **Retake** | The same idea said again ("let me say that again") | Keep the best complete take, usually the last; cut the others **and** the "let me say that again" |
| **Correction** | Speaker fixes themselves ("three minutes, no, sorry, two minutes") | Keep only the corrected version; if it cannot be isolated cleanly, flag it |
| **Stutter / repeat** | "the the", "I- I-" | Cut, unless it is emphasis ("never, never") |
| **Filler** | "uh", "um", "you know", "like" between thoughts | Cut when it sits in a gap; keep when cutting would clip a word |
| **Pause** | Silence | Cut over 0.4 s, leave 0.1–0.2 s of air at joins; keep deliberate pauses after key lines |
| **Aside** | Off-topic ("someone's at the door") | Cut |
| **Risky** | Health, money, legal, guarantee, price, competitor, personal data | Keep as said, add to *Check before posting* |

Emphatic repetition, rhetorical doubling and lists look like stutters. Read the meaning.

## Shape

1. **Hook (first 3 seconds):** the strongest true line: a result, a surprising fact, a question the
   video answers. Moving it to the front is allowed when it still makes sense there; repeating it
   later is fine.
2. **Body:** one idea per beat, in the order that makes sense to a viewer who knows nothing.
3. **Payoff:** what the hook promised must be delivered before the end.
4. **CTA:** what the speaker actually said. If they said two ("comment below" and "link in bio"), keep
   both and suggest dropping one as an option; never drop a spoken CTA silently.

Target length from the notes or profile. If the content does not fit, say what you would drop and
ask; do not speed up speech to fit.

## The cut plan

Present before rendering anything:

```
CUT PLAN — v1 · source: raw.mp4 (2:31.4) → new length 0:52.6

#  | source in → out    | dur   | text
1  | 01:42.30 → 01:45.10 | 2.80 | "Most people brush for 40 seconds."     ← hook, moved to the front
2  | 00:08.20 → 00:12.90 | 4.70 | "I'm Dr. Ana, and these are the 3…"
…
Sum: 2.80 + 4.70 + … = 52.60 s

REMOVED: 00:00.00–00:08.20 false start + aside · 00:31.40–00:39.00 retake of point 2 (kept the
second take) · 14 pauses over 0.4 s (total 11.3 s) · …
CHECK BEFORE POSTING: 00:47.10 "it heals gum disease in a week" — health claim, check before posting.
Approve this cut?
```

Rules for the plan:
- Times as `mm:ss.ss` (or `hh:mm:ss.ss`), all in the **source** timeline.
- Duration of each segment = out − in, two decimals.
- **New length = sum of the durations.** Show the addition. Never round the total before adding.
- Add the padding you will use (default 0.05 s before, 0.08 s after each kept segment) only if you will
  render it; then include it in the durations.
- Every removed range has a reason.

## Timing math (when there is no code)

1. Convert each time to seconds (`01:42.30` = 102.30).
2. Duration = out − in.
3. Add the durations in a visible line; check by adding again in a different order.
4. New-timeline position of a kept segment = sum of the durations of the segments before it.
5. A caption line inside a segment: `new_time = source_time − segment_in + segment_new_start`.

## Rendering (level 3)

`scripts/cutkit.py`:

```
python cutkit.py probe raw.mp4
python cutkit.py silences raw.mp4 --min 0.4 --noise -35dB > silences.json
python cutkit.py plan raw.mp4 --silences silences.json [--remove cuts.json] --pad 0.05 0.08 > cut-plan.json
python cutkit.py render raw.mp4 cut-plan.json -o v1/v1.mp4 [--vertical]
python cutkit.py srt transcript.srt cut-plan.json -o v1/captions.srt --max-chars 32
python cutkit.py edl cut-plan.json -o v1/edit.edl --fps 30
```

`cuts.json` holds the editorial cuts you decided from the transcript (retakes, false starts, asides):
`{"remove": [{"in": 31.4, "out": 39.0, "reason": "retake"}]}`. The render fades audio 30 ms at each
join to avoid clicks, then checks the output duration against the plan. If they differ by more than
0.1 s per segment, say so.

## Before showing the cut

- First 3 seconds: is the reason to keep watching clear even with the sound off?
- Every join: no clipped word, no half breath, no jump that breaks the meaning.
- The payoff is there; every spoken CTA is kept (or its removal was proposed).
- Length matches the plan.
