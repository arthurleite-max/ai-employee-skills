# Setup: the first conversation

Goal: in about 5 minutes, a profile the editor can use on every video. Talk to the owner in their
language. Accept "skip" for any question; defaults are in `templates/profile.example.md`.

## 1. What the editor can do here

Say in one line which level you are at (see `SKILL.md`): "I can give you a timed cut plan and
captions to apply in your app" (chat), or "I can cut and render the video here" (agent with ffmpeg).
If ffmpeg or a transcription tool is missing at level 3, say what it would add; do not install
anything without the owner's yes. If the owner wants animated captions and graphics ("make it lively"),
offer the motion add-on and its installs from `reference/motion.md` (Python packages, Node.js, the
Remotion template, optional model files), including the Remotion licence note for companies.

## 2. The questions

1. Your name and title as they should appear on screen; the business in one line.
2. Where do you post, and which formats (vertical 9:16, horizontal 16:9, square)? Usual length?
3. Pacing: natural, tight or cinematic? Should I cut every pause or leave some air?
4. Captions: yes/no, and the look (clean, bold short-form, lower band). Brand colours and font?
5. Logo, end card, standard CTA you say at the end?
6. Music: do you have a licensed library? Otherwise I leave room and you add music in the app.
7. Words or topics that need care on screen (prices, health or money claims, competitors)?
8. Which app do you or your editor use (CapCut, DaVinci Resolve, Premiere, Final Cut, other)?
9. Who else appears in your videos, and do they have consent?

## 3. First video

Ask for the raw file (level 3) or its transcript with timestamps (levels 1–2). Run Mode 1. After the
owner's first round of notes, record the lasting preferences in the profile.

## 4. Save

Level 3: `video-editor-data/profile.md` and one folder per project. Levels 1–2: hand back the profile
in a code block: "Keep this text and paste it with your next video."
