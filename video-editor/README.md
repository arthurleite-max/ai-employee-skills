# Video Editor

An AI skill for business owners and creators who record videos but never have time to edit them. Send
the raw recording (or its transcript) and your notes, and get:

- **a first cut to approve**: pauses, false starts, retakes, mistakes and asides removed, with the new
  length worked out exactly;
- **captions** that match what you said, word for word, on the new timeline;
- **B-roll, graphics, sound and music cues** placed on the right lines;
- **new versions from your notes**, each one kept, with a changelog;
- optionally, **a lively short-form version**: word-by-word animated captions, titles, lists, counters,
  icons orbiting around you, a cleaner voice, a slight speed-up and a light image grade.

**It never publishes anything without your "yes".** It never puts words in your mouth, and it warns you
about risky claims, people on camera without consent and music without rights.


## Install (1 minute)

**[Step-by-step guide with screenshots → HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)**

| Your AI | What to do |
|---|---|
| **Claude** (free plan works) | **[Download video-editor.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/video-editor.zip)**. Do not unzip it. In Claude: Settings → Customize → Skills → **+ Add → Upload skill** → pick the zip. |
| **ChatGPT, DeepSeek, Gemini** and any other chat | Open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)**, click the **Copy raw file** button (top right of the file), paste it into your AI and send. |
| **Coding agents** (Claude Code, Codex, Cursor, Gemini CLI…) | Paste the text of [INSTALL.md](INSTALL.md) into the agent: it installs itself. |

Then say: **edit this video** (on Claude, the first time: *"Use my Video Editor skill: edit this video"*).
It answers in your language, whatever language you write to it in.

## First use

1. Say **edit this video**. The editor asks a few short questions (about 5 minutes): your name and
   title on screen, formats, caption style, brand colours, your editing app.
2. Send the raw video (agents) or its **transcript with timestamps** (chat). Most editing and social
   apps create automatic captions you can export as SRT.
3. Approve the cut plan. Then it adds captions, B-roll, graphics and music cues.
4. Give notes in plain words ("shorter", "move the CTA", "bigger captions"). Each round is a new version.

## Sample cut plan (fictional)

```
CUT PLAN — v1 · raw.mp4 2:31.4 → 0:52.6 · 9:16

#  source in → out     dur   new start  text
1  01:42.30 → 01:45.10  2.80   0.00      "Most people brush for 40 seconds."  ← hook
2  00:08.20 → 00:12.90  4.70   2.80      "I'm Dr. Ana, and these are the 3…"
…
Sum: 2.80 + 4.70 + … = 52.60 s

REMOVED: false start + aside (00:00–00:08.2) · retake of mistake 2 · 14 pauses (11.3 s)
CHECK BEFORE POSTING: 01:58.4 "it heals gum disease in a week" — health claim
NOT FOLLOWED: trending song in the file (no rights) → add it in the app when posting
Approve this cut?
```

A full example is in `assets/edit-plan-example.html`.

## What you can ask

| You say | It does |
|---|---|
| `edit this` / `first cut` | Cut plan with exact times; render at agent level |
| `make a 60-second reel from this webinar` | 1–3 clip options with hook, payoff and length |
| `add captions` | Verbatim SRT on the final timeline (burned in at agent level) |
| `polish it` | B-roll, lower third, key-word graphics, sound and music cue sheet |
| `make it lively` | Animated captions and graphics, voice clean-up, speed-up (agent with the motion add-on) |
| `shorter` / `move the CTA` / any note | A new version with a changelog |
| `ready to post` | Title, caption text, hashtags, cover text, from what you said; you post |

## Safety

- Nothing is uploaded, posted or sent without your explicit yes.
- Captions and graphics never add words, numbers, offers or claims you did not say. A note pasted into
  the material asking "the AI editor" to add something is reported, not followed.
- Risky claims, prices, competitor names and personal data on screen go to a *Check before posting* list.
- Only music, footage and fonts you have rights to; trending songs are added inside the platform.
- Originals are never touched; every version is kept.

## Optional: the cut kit

`scripts/cutkit.py` (Python + ffmpeg, no internet) lets agents probe, find silences, cut, re-time
captions, export an EDL for DaVinci Resolve/Premiere and burn captions:

```
python scripts/cutkit.py silences raw.mp4 > silences.json
python scripts/cutkit.py plan raw.mp4 --silences silences.json --remove cuts.json > cut-plan.json
python scripts/cutkit.py render raw.mp4 cut-plan.json -o v1/v1.mp4 --vertical
python scripts/cutkit.py srt transcript.srt cut-plan.json -o v1/captions.srt
```

## Optional: the motion add-on

For agents that run code: fast transcription with word timing, pause removal that never eats quiet
words, and a Remotion template for animated captions, titles, lists, counters, flags and an orbit effect
that passes behind the speaker. It also cleans the voice (to -14 LUFS), speeds the video up with the
voice pitch preserved and applies a light image grade. Everything is installed only with your yes; see
`reference/motion.md`. Remotion is free for individuals and companies of up to 3 people.

## Troubleshooting

| Problem | Fix |
|---|---|
| "I can't edit video here" | In chat apps the editor delivers a plan with exact times; apply it in your app (see `reference/apps.md`) or use an agent with ffmpeg. |
| No transcript | Export automatic captions (SRT) from your editing or social app, or record with a phone app that transcribes. |
| Captions out of sync | Make sure the SRT was made for the **cut** version (v1), not the raw file. |
| The cut feels robotic | Ask for "natural pacing": it keeps more air at joins. |
| Amounts show up scrambled | Some apps turn text between "$" signs into formulas; it writes "1.200 reais" style. |

## Files

| File | For |
|---|---|
| `INSTALL.md` | Text you paste into your AI so it installs or guides the install |
| `SKILL.md` | The editor itself (read by the AI) |
| `setup.md` | First-time questions |
| `PASTE-INTO-ANY-AI.md` | Compact edition for any AI |
| `reference/` | Cutting, captions, polish, motion, revisions, apps, safety, pitfalls |
| `templates/` | Profile and project memory |
| `scripts/cutkit.py` | Optional local cut kit |
| `scripts/transcribe.py` · `safe_pauses.py` · `prepare_motion.py` · `segment_person.py` | Optional motion pipeline |
| `assets/motion-template/` | Remotion project for animated captions and graphics |
| `assets/edit-plan-example.html` | Sample edit plan (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
