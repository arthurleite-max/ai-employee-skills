# Credits

The Video Editor is original text and code, inspired by ideas from open community projects. No files
from these projects were copied. Thanks to their authors:

| Project | License | Idea used |
|---|---|---|
| [browser-use/video-use](https://github.com/browser-use/video-use) | MIT | Editing from the transcript; confirm the strategy before touching the cut; captions on the output timeline; 30 ms audio fades at every join; never cut inside a word; check the render against the plan |
| [nateherkai/herk-edit-kit](https://github.com/nateherkai/herk-edit-kit) | not stated | Ideas only: review-gated cutting of stutters, false starts and retakes; the "first 3 seconds" test for short-form; turning owner notes into lasting rules |
| [veedstudio/open-edit](https://github.com/veedstudio/open-edit) | Apache-2.0 | Captions and graphics as part of the edit pipeline |
| [WyattBlue/auto-editor](https://github.com/WyattBlue/auto-editor) | Unlicense | Silence-based cutting with a margin, and exporting a timeline the owner's editor can open |
| [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) | MIT | Small, safe ffmpeg operations with a predictable contract |
| [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) | MIT | Used as a dependency (not bundled) for transcription with word timing |
| [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | Remotion License (free for individuals and companies up to 3 people) | Used as a dependency (not bundled) by the motion template |
| [google-ai-edge/mediapipe](https://github.com/google-ai-edge/mediapipe) | Apache-2.0 | Used as a dependency (not bundled) to cut the person out and track the face |
| [GregorR/rnnoise-models](https://github.com/GregorR/rnnoise-models) · [xiph/rnnoise](https://github.com/xiph/rnnoise) | BSD-3-Clause | Optional voice noise model used through ffmpeg `arnndn` (not bundled) |
| [lobehub/lobe-icons](https://github.com/lobehub/lobe-icons) | MIT | Optional source of product logos when the owner asks (not bundled) |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) · [remotion-dev/skills](https://github.com/remotion-dev/skills) | Apache-2.0 · see repository | Graphics and animated captions as optional add-ons |

The folder follows the open Agent Skills format (`SKILL.md`), documented at
[agentskills.io](https://agentskills.io).
