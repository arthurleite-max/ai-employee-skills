# Applying the plan in the owner's editing app

When the environment cannot render, the owner (or their editor) applies the cut plan. Make it fast to
follow. Menu names change between versions: describe the action, and if you do not know the exact menu
in the owner's version, say "look for…" instead of inventing it.

## Any app: cut by times

1. Import the raw video.
2. Work through the cut plan **from the end to the start**: removing later parts first keeps earlier
   timecodes valid.
3. For each removed range: put the playhead at the *in* time, split; at the *out* time, split; delete
   the piece between and close the gap (ripple delete).
4. Moved segments (a hook brought to the front): cut it out, drag it to the start.
5. Check the total length against the plan.
6. Import `captions.srt` if the app supports it; otherwise use the app's automatic captions and correct
   them against the plan's caption text.

## DaVinci Resolve and Premiere Pro

- **EDL:** import `edit.edl` (CMX 3600) as a timeline with the raw clip as the source; the cuts arrive
  done. Set the timeline frame rate to the one in the EDL.
- **Captions:** import `captions.srt` into a subtitle track.

## Final Cut Pro

No CMX EDL import by default: use the cut-by-times steps, or a converter to FCPXML if the owner has one.
Captions: import SRT as captions.

## CapCut and phone editors

- Use cut-by-times (split, delete). The plan's times are in the **source** timeline; working from the
  end keeps them valid.
- Auto captions, then correct the words against the plan (verbatim, names spelled right).
- Add music from the app's licensed library; it stays licensed inside the app's export rules.

## Handing off to a human editor

Send: the raw files, the cut plan, `captions.srt`, `edit.edl`, the cue sheet and the *Check before
posting* list. The plan is the brief.
