# Social Media Strategist

An AI skill for business owners who know they should post but start every day from a blank page. Every
morning it brings:

- **three ideas for today's post** (Instagram, TikTok, Reels, Shorts), each with hook options and the
  reason it should work: your own best posts, a dated source, or an evergreen need;
- **the post ready** once you pick: script or slides, caption, cover text, hashtags, alt text;
- **a content calendar** that follows your rhythm and what you can actually produce;
- **what is working**, measured from your own metrics (saves, shares, follows), not likes.

**It never posts for you**, never invents trends, testimonials or results, and adapts other accounts'
ideas instead of copying them.

## Install (1 minute)

**[Step-by-step guide with screenshots → HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)**

| Your AI | What to do |
|---|---|
| **Claude** (free plan works) | **[Download social-media-strategist.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/social-media-strategist.zip)**. Do not unzip it. In Claude: Settings → Customize → Skills → **+ Add → Upload skill** → pick the zip. |
| **ChatGPT, DeepSeek, Gemini** and any other chat | Open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)**, click the **Copy raw file** button (top right of the file), paste it into your AI and send. |
| **Coding agents** (Claude Code, Codex, Cursor, Gemini CLI…) | Paste the text of [INSTALL.md](INSTALL.md) into the agent: it installs itself. |

Then say: **good morning** (on Claude, the first time: *"Use my Social Media Strategist skill: good morning"*).
It answers in your language, whatever language you write to it in.

## First use

Say **good morning**. It asks about your business, platforms, posting rhythm, what you can film and
your voice (about 10 minutes). Paste or attach your last 30–90 days of post metrics (Instagram:
Professional dashboard → Insights → export, or screenshots sorted by saves). Then every morning: "good
morning", pick 1, 2 or 3.

## Sample morning menu (fictional)

```
Wed 11/11 · carousel at 12:00

1. "Bread storage: 3 rules" — educate · 6 slides
   Hooks: "You're storing your bread wrong." / "3 rules for bread that lasts."
   Why: your data — carousels with lists get 3× the saves of your photos
2. "From flour to loaf in 12 photos" — behind the scenes · 8 slides
   Why: evergreen; process reels are your most shared posts
3. "Sourdough myths" — educate · 5 slides
   Why: evergreen; the question you get most in DMs

Not followed: "say our bread is healthy" → health claim, kept for you to decide.
Which one: 1, 2 or 3?
```

## What you can ask

| You say | It does |
|---|---|
| `good morning` | Three ideas for today's slot |
| `1` (or 2, 3) | The full post pack for that idea |
| `plan next week` | Calendar in your rhythm, pillars balanced |
| `what's working?` + metrics | Medians per format, outliers, three decisions |
| `what's trending in my niche?` | Dated research with links (needs browsing), or asks for screenshots |
| `turn this video into…` | Repurposed posts using only what is in the original |

## Safety

- Nothing is posted, scheduled, commented or sent without your yes.
- No invented trends, metrics, testimonials, reviews or results.
- Other accounts inspire patterns; their content is never copied.
- Music from the platform's library at posting time; people on camera with consent.
- Health, money and "guaranteed" claims, giveaways and partnerships are flagged for you.
- A comment telling "the AI" to post something is reported, not obeyed.

## Optional: the metrics analyser

```
python scripts/insights.py posts.csv --metric saves     # or shares, follows, engaged
```

It reads your export (English or Portuguese column names), computes rates per 1,000 reach, medians per
format and outliers (2× the median).

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The strategist · first-time questions |
| `reference/` | Research, ideas, hooks, scripts and captions, calendar, safety, pitfalls |
| `templates/` | Profile and memory |
| `scripts/insights.py` | Optional metrics analyser |
| `assets/morning-menu-example.html` | Sample morning menu (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
