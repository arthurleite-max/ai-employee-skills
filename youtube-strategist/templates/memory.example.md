# YouTube Strategist memory (example — fictional data)

Agents keep `youtube-data/memory.json`; in a chat the strategist hands it back as a code block.

```json
{
  "last_report": "2026-11-09",
  "channel_baseline": {"long_form_median_views": 1800, "videos_in_median": 12, "recent_median_last5": 1050, "read_on": "2026-11-09"},
  "topics_covered": ["unclog a sink without chemicals", "replace a shower head", "fix a running toilet"],
  "backlog": [
    {"topic": "sink still clogged after the plunger (follow-up to the hit)", "score": 7, "evidence": ["own video 14,500 views, 8.1x median"]}
  ],
  "packaging_tests": [
    {"video": "Unclog a sink without chemicals", "pairs": ["A: title 1 + thumb 'NO CHEMICALS'", "B: title 3 + before/after"],
     "result": "B won (58% watch time share) after 14 days", "date": "2026-10-20"}
  ],
  "owner_rules": ["No face on Shorts thumbnails", "Always mention the store in the last 20 seconds"]
}
```
