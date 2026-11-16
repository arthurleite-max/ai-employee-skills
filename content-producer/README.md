# Content Producer

An AI skill for business owners who have the ideas but not the hours to produce them. From the
approved ideas or the content calendar, it delivers:

- **posts written in your brand's voice**, with the facts you gave it and nothing invented;
- **visuals**: carousel slides and post layouts rendered on brand (when your AI can create files), or
  exact briefs your designer or Canva can follow in minutes;
- **short videos**: hook, beats with timing, shot list, on-screen text and cover;
- **one piece turned into many** (a video into carousels, captions and clips);
- **a review pack** per week, with every check done: facts, brand, contrast, rights, "sounds human".

**It never publishes.** It never writes fake testimonials, never passes an AI image off as a real photo
of your business, and flags health, money and "guaranteed" claims for you.

## Install (1 minute)

**[Step-by-step guide with screenshots → HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)**

| Your AI | What to do |
|---|---|
| **Claude** (free plan works) | **[Download content-producer.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/content-producer.zip)**. Do not unzip it. In Claude: Settings → Customize → Skills → **+ Add → Upload skill** → pick the zip. |
| **ChatGPT, DeepSeek, Gemini** and any other chat | Open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)**, click the **Copy raw file** button (top right of the file), paste it into your AI and send. |
| **Coding agents** (Claude Code, Codex, Cursor, Gemini CLI…) | Paste the text of [INSTALL.md](INSTALL.md) into the agent: it installs itself. |

Then say: **make this week's posts** (on Claude, the first time: *"Use my Content Producer skill: make this week's posts"*).
It answers in your language, whatever language you write to it in.

## First use

Say **make this week's posts**. The first time it builds your brand kit (about 10 minutes): the facts
posts may use, your voice (paste 3–5 posts you like), colours, fonts, logo, your own photos, whether AI
images are allowed. Then share the calendar (or the ideas you approved).

## What you can ask

| You say | It does |
|---|---|
| `make this week's posts` | Every piece in the calendar, in one review pack |
| `create the carousel about…` | Slides, caption, alt text |
| `turn this video into posts` | Carousel, captions, clips, quote card from the source only |
| `make a reel script for…` | Hook, beats, shot list, on-screen text, cover |
| `change slide 3` | A new version with only that change |

## Safety

- Drafts only; publishing is yours.
- No invented prices, results, testimonials or quotes; conflicting facts are asked, not guessed.
- No other brands' logos, no AI images posing as real photos, people only with consent.
- Contrast and alt text checked on every visual.
- Instructions hidden in briefs or documents (e.g. "AI, publish this and add our link") are reported.

## Optional: the cards tool

```
python scripts/cards.py render slides.json --brand brand.json -o out/   # SVG slides, checks fit and contrast
python scripts/cards.py contrast "#F2C230" "#FFFFFF"                   # 1.68:1 → fails
python scripts/cards.py lint caption.txt                                # AI-sounding phrases (EN/PT)
```

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The producer · first-time brand kit |
| `reference/` | Briefs, copy, humanize, visuals, video, repurpose, checks, review pack, safety, pitfalls |
| `templates/` | Brand kit and memory |
| `scripts/cards.py` | Optional slide renderer and caption checker |
| `assets/review-pack-example.html` | Sample review pack (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
