# Research: what works in the niche

## The input

A list of recent videos from the niche: title, channel, channel subscribers, views, publish date
(duration and format if possible). From the owner (pasted, screenshots), from browsing, or from a
read-only API. Always note when the numbers were collected.

## Outliers, not big numbers

A video with 2 million views on a 5-million-subscriber channel is normal. A video with 400,000 views
on a channel whose videos usually get 20,000 is a signal: **the topic and the packaging** worked, not
the channel's size.

For each video:
- **Channel median**: median views of that channel's recent long-form videos (at least 5 when you
  have them). Without code, write the sorted list first and take the middle value(s) from it.
- **Outlier ratio** = views ÷ channel median. ≥ 3× is a strong signal; 2–3× a signal.
- **Views ÷ subscribers**: a second check (above 1.0 means it reached beyond the channel's audience).
- **Views per day** since publishing: compares old and new videos fairly.

Shorts and long-form are separate: never mix them in one median.

`python scripts/ytlint.py outliers videos.csv --today 2026-11-11` computes all of it.

## What the outliers share

Look across channels: the problem or desire (topic), the angle (fast, cheap, mistake, without a
tool), the promise in the title, the thumbnail composition (object, before/after, face, few words),
the length. A pattern seen on two or more channels is worth more than one hit.

## Comments

Comments on outliers show the questions people still have ("and if the pipe is plastic?"). Each
unanswered question can be a video. Quote short, never copy usernames into reports.

## Freshness and sources

Default window: videos from the last 12 months, with attention to the last 90 days. Each claim with
the video and the date the numbers were read. Without browsing, analyse only the list provided.
