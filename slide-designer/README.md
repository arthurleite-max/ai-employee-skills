# Slide Designer

An AI skill for business owners who need a good presentation without spending a weekend on it. It:

- **organises the ideas** into a storyline that ends with a clear ask;
- **writes every slide**: a one-sentence headline, a short body, the visual and speaker notes;
- **designs layouts and charts** from your real numbers, with sources;
- **delivers an editable deck**: a PowerPoint file (built locally by `scripts/deck.py`) or a
  slide-by-slide plan to rebuild in Google Slides, Keynote or Canva.

Every number has a source and adds up; missing facts are marked **[source needed]** instead of invented.
No borrowed images, no logos that suggest endorsements, no customers' contact details on slides.

## Install (1 minute)

**[Step-by-step guide with screenshots → HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)**

| Your AI | What to do |
|---|---|
| **Claude** (free plan works) | **[Download slide-designer.zip](https://github.com/arthurleite-max/ai-employee-skills/releases/latest/download/slide-designer.zip)**. Do not unzip it. In Claude: Settings → Customize → Skills → **+ Add → Upload skill** → pick the zip. |
| **ChatGPT, DeepSeek, Gemini** and any other chat | Open **[PASTE-INTO-ANY-AI.md](PASTE-INTO-ANY-AI.md)**, click the **Copy raw file** button (top right of the file), paste it into your AI and send. |
| **Coding agents** (Claude Code, Codex, Cursor, Gemini CLI…) | Paste the text of [INSTALL.md](INSTALL.md) into the agent: it installs itself. |

Then say: **make a presentation** (on Claude, the first time: *"Use my Slide Designer skill: make a presentation"*).
It answers in your language, whatever language you write to it in.

## First use

Say **make a presentation**. It asks what the audience should do after, who they are, how long you have,
your material and your brand (about 5 minutes), proposes the headlines and, after your yes, writes the
deck.

## Build the PowerPoint file

```
python scripts/deck.py deck.json -o deck.pptx
```

Checks the plan (words per slide, bullets, numbers without sources, parts of a whole that do not add up
to 100%) and writes an editable `.pptx` made of native text boxes and shapes, plus `deck-notes.md` with
the speaker notes. Python 3.8+, nothing to install. Try it with `assets/example-deck.json`.

## What you can ask

| You say | It does |
|---|---|
| `make a presentation about…` | Headlines first, then every slide and the file |
| `turn this document into slides` | Storyline and slides from your material |
| `pitch deck` / `sales presentation` | The right structure, ending with the ask |
| `design the slides` | Layouts, colours, charts that tell the truth |
| `review my deck` | Fixes by slide: story, numbers, charts, rights, privacy |

## Safety

- No invented numbers, sources, awards, clients or quotes: `[source needed]` instead.
- Charts match the data; parts of a whole must add up to 100%.
- Only material you may use; no competitor images; no logos implying endorsement.
- No customer contact details; testimonials with permission.
- Instructions hidden in pasted material are reported, never followed.

## Files

| File | For |
|---|---|
| `INSTALL.md` · `PASTE-INTO-ANY-AI.md` | Install prompt · compact edition |
| `SKILL.md` · `setup.md` | The slide designer · first-time questions |
| `reference/` | Storyline, slide writing, design, charts, safety, pitfalls |
| `templates/` | Brief and brand |
| `scripts/deck.py` | Checks a deck plan and builds an editable .pptx |
| `assets/example-deck.*` | Sample plan, PowerPoint file and notes (fictional) |
| `LICENSE.md` · `CREDITS.md` | MIT license and credits |
