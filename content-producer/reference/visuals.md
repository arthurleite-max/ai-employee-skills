# Visuals

## Sizes

| Format | Size (px) |
|---|---|
| Instagram feed / carousel | 1080×1350 (4:5) or 1080×1080 |
| Stories, Reels cover, TikTok | 1080×1920 (9:16) |
| YouTube thumbnail | 1280×720 |
| LinkedIn post | 1200×1200 or 1080×1350 |
| Facebook link | 1200×630 |

## Brand

Colours as hex from the brand kit; at most one accent per piece. Fonts the owner has licensed (or free
licences). Logo small, in a corner, never distorted, never on every slide unless the kit says so.
Photos: the real business first (owner's photos); stock only licensed; AI images only with a yes.

## Layout rules

- One focal point per slide; headline ≤ 8 words; body ≤ 25 words.
- Text contrast ≥ 4.5:1 (large text ≥ 3:1). No text over busy photos without a solid or dark overlay.
- Safe margins: 80 px on feed posts; keep the bottom 20% of 9:16 free of key text (buttons).
- Same structure across a carousel (title position, colours, numbering only if it is a sequence).

## Rendering with the script (level 2–3)

```
python scripts/cards.py render slides.json --brand brand.json -o out/
```

`slides.json`: `{"size": "1080x1350", "slides": [{"title": "...", "body": "...", "style": "dark"}]}`.
It writes one SVG per slide, wraps text, and **fails** the slide if the text does not fit or the
contrast is below 4.5:1. SVGs open in any browser and import into Canva, Figma or Illustrator.

## Image prompts (when the AI has an image tool and the owner said yes)

Structure: subject · setting · composition (framing, angle) · light · style · colour palette (brand
hex) · aspect ratio · what must NOT appear (text, logos, people's faces, hands with wrong fingers).
Generate without text and add the text in the layout (AI image text is unreliable). Label every
generated image "AI-generated" in the review pack. Never generate: real people, the owner's actual
products as if photographed, before/after results, other brands.

## Briefs for the owner's designer or Canva (level 1)

Per slide: size, background colour, text (exact), font and size, text position, image (which photo or
description), logo yes/no. Specific enough to build without questions.
