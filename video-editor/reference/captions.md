# Captions

Most short videos are watched without sound. Captions are part of the edit, not an extra.

## Rules

1. **Verbatim.** The words spoken, in the order spoken. Fix only transcription errors (a misheard brand,
   a wrong homophone). When unsure, mark `[?]` and list it for the owner.
2. **Filler removed** if it was cut from the audio; never caption words that are no longer heard.
3. **On the final timeline.** Re-time every line after cutting; never reuse source times. Method without
   code: take each kept segment's window from the cut plan (new start → new start + duration) and split
   that segment's words inside it. Windows touch end to end; the last caption ends at the new length.
   Check before delivering: each segment's captions, read together, equal its full text word for word.
   Fix mistakes before you answer and deliver one final SRT, not drafts.
4. **Split by meaning**, not by character count alone: do not end a line on "the", "a", "of", "and".
5. **Length:** defaults 32 characters per line, 2 lines, for vertical video; 42 × 2 for horizontal.
   Profile wins.
6. **Duration:** each caption at least ~0.8 s and at most ~6 s; no gap under 0.1 s between captions
   (merge instead).
7. **Numbers as spoken** ("two minutes" may be shown as "2 minutes"; never change the number).
8. **Names and terms** spelled as in the profile (people, products, places).
9. **Safe area:** on vertical video keep captions out of the bottom ~20% and the right edge, where
   platform buttons sit.

## SRT format

```
1
00:00:00,000 --> 00:00:02,780
Most people brush
for 40 seconds.

2
00:00:02,780 --> 00:00:05,100
I'm Dr. Ana, and these are
the 3 mistakes I see every day.
```

Index from 1, `hh:mm:ss,mmm` with a comma, blank line between blocks, UTF-8.

## Styles (pick from the profile)

| Style | Look | Good for |
|---|---|---|
| Clean | White text, soft shadow or semi-transparent box, sentence case | Talking head, professional |
| Bold short-form | Large, 1–4 words at a time, one highlighted word in the brand colour | Reels, Shorts, TikTok |
| Lower band | Two lines at the bottom, smaller | Interviews, webinars, horizontal |

Highlighted words should be the meaningful ones (the number, the result, the mistake), not every noun.

## Burn-in vs separate file

- **Separate SRT**: platforms like YouTube and LinkedIn accept it; editable; accessible.
- **Burned in**: needed for Reels/Shorts/TikTok styles. At level 3: `cutkit.py burn v1.mp4
  captions.srt -o v1_captions.mp4 --style bold`.
Deliver both when unsure.

## Translations

Only when asked. Label the file with the language (`captions.es.srt`). Keep the timing; shorten
wording only if a line would exceed the limits, and keep the meaning exact. Mark it as a translation.
