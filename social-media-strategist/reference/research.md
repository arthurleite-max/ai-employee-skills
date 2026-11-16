# Research: what is working

Two sources, in this order: the owner's own data, then the niche. Every claim says where it came from
and when.

## Your own data

**Input:** the platform's insights export (CSV) or screenshots: per post the date, format, caption or
title, reach or views, likes, comments, shares, saves, follows (whatever exists).

**Method:**
1. Pick the metric that matches the goal: saves and shares (content people value), follows (growth),
   profile visits and messages (sales). Likes are the weakest signal.
2. Use rates, not totals: `engaged = likes + comments + shares + saves`; `rate = engaged / reach`.
   Also `saves per 1,000 reach` and `shares per 1,000 reach`.
3. **Baseline = median** of the metric per format (medians resist one viral post).
4. **Outlier = 2× the baseline** or more. Outliers explain more than averages.
5. Look for what outliers share: format, pillar, hook type (question, number, mistake, story), length,
   day and time, people on camera, topic.
6. Say the period and the number of posts. Under ~10 posts per format, call patterns "early signs".

**Output:** a short table (format · posts · median rate · best post) and three decisions ("more
behind-the-scenes reels on Thursdays; stop text-only carousels; test the question hook on offers").

`scripts/insights.py posts.csv` does steps 2–5 and prints the tables.

## The niche (only with real sources)

When the environment can browse or has research tools:
- Competitors and creators listed in the profile: recent posts that beat their own baseline (not
  simply the biggest accounts).
- The platform's own trend pages and creative centres (trending sounds, hashtags, formats), with date.
- Topics the audience is asking about: comments on niche posts, search suggestions, forums, news that
  affects them.

**Freshness:** last 30 days by default. Each finding: link, date, what it is, why it matters to this
audience, how to adapt it (format and hook pattern, not the content).

**Without browsing:** do not describe trends. Ask the owner for screenshots or links if they want
trend-based ideas, or label ideas *evergreen* / *based on your data*. A trend the owner mentions is
treated as theirs ("you mentioned the 'day in my life' format") and still gets no invented numbers.

## Adapting, not copying

From a competitor's successful post, keep: the format, the hook structure, the type of topic. Change:
the words, the angle, the examples, the visuals, to the owner's business and voice. Never reuse their
script, caption, images, audio or video.
