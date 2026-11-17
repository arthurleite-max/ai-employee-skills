# Motion: animated captions, graphics, effects, voice and image clean-up

Optional add-on for level 3 (an agent that runs code). It turns the approved cut into a short-form
video with word-by-word captions, animated graphics, "around me" effects, a cleaner voice and a light
image grade. Everything here happens **after** the cut is approved (rule 2) and uses only words that
were spoken (rule 3).

## What it adds

| Feature | How |
|---|---|
| Fast transcription with word timing | `scripts/transcribe.py` (faster-whisper, CPU) |
| Pause removal that never eats quiet words | `scripts/safe_pauses.py` between `cutkit.py silences` and `plan` |
| Speed-up without a chipmunk voice | `prepare_motion.py --speed 1.1` (1.05 to 1.15 sounds natural) |
| Voice clean-up and level (-14 LUFS) | `prepare_motion.py --audio [--models folder]` |
| Light image grade (colour cast, skin, sharpness) | `prepare_motion.py --image` |
| Captions, titles, lists, counters, flags, stamps, punch-in zoom, progress bar | `assets/motion-template` (Remotion) |
| Icons orbiting behind and in front of the speaker | `scripts/segment_person.py` + the `orbit` element |

## Install (ask the owner first; nothing is installed without a yes)

- Python packages: `pip install faster-whisper numpy mediapipe pillow`
- Node.js 18+; then copy `assets/motion-template` to the project's working folder and run `npm install` there.
- Optional model files, in one `models/` folder next to the project:
  - `sh.rnnn` (RNNoise voice model, BSD): https://github.com/GregorR/rnnoise-models (somnolent-hogwash)
  - `selfie_multiclass_256x256.tflite` and `blaze_face_short_range.tflite` (MediaPipe, Apache 2.0):
    https://ai.google.dev/edge/mediapipe/solutions/vision/image_segmenter and .../face_detector
- **Remotion licence:** free for individuals and companies of up to 3 people; larger companies need a
  company licence (https://www.remotion.dev/docs/license). Tell the owner before using it for a business.
- Remotion publishes its own agent skills (`npx remotion skills add` inside the template folder): load
  `remotion-best-practices` before writing new animations.

## The pipeline

```
python transcribe.py raw.mp4 -o . --lang en [--fix "misheard=Right"]
python cutkit.py silences raw.mp4 --min 0.4 --noise=-32dB > silences.json
python safe_pauses.py silences.json words.json -o pauses.json
python cutkit.py plan raw.mp4 --silences pauses.json --remove cuts.json > cut-plan.json
   -> show the cut plan, wait for the owner's yes
python cutkit.py render raw.mp4 cut-plan.json -o v1/v1.mp4
python prepare_motion.py v1/v1.mp4 words.json cut-plan.json -o v1/props.json --public motion/public \
       --elements elements.json --color multicolor --zoom --progress [--speed 1.1 --audio --image]
python segment_person.py motion/public/<project>_v1.mp4 --from A --to B --name <cutout> \
       --public motion/public --models models --props v1/props.json        (only for an orbit)
cd motion && npx remotion render src/index.ts CaptionedVideo ../v1/v1_final.mp4 --props=../v1/props.json
```

Before the full render, render 3 to 6 stills (`npx remotion still ... --frame=N --scale=0.3`) at the
moments that matter and look at them. A full render takes about 3 to 4 seconds per second of 1080×1920
video on an ordinary laptop.

## Elements (`elements.json`, times on the cut timeline in seconds)

| type | fields | use |
|---|---|---|
| `title` | start, end, text | opening hook, top band |
| `callout` | start, end, text | a key phrase that was spoken |
| `list` | start, end, heading?, items[{text, at, emoji?, flag?}] | items pop in at the second each is spoken |
| `counter` | start, end, values[{value, at, label?}] | numbers rolling from one spoken value to the next |
| `stamp` | start, end, text | closing line |
| `orbit` | start, end, cutout, items[{text, at, logo? or emoji?}], turns? | icons circling the head, passing behind |

`at` is the start time of the word in the cut timeline (read it from the retimed words). Graphics
live in the top band so the face stays clear; captions sit low. Flags: `br`, `us`, `in`, `jp` are
drawn in `Flags.tsx` (Chrome on Windows has no flag emoji); add others the same way.

## Brand logos

Real product logos (for example the AI tools the speaker names) come from the MIT-licensed
`@lobehub/icons-static-svg` package: copy the `*-color.svg` file into `motion/public/icons/` and set
`logo`. Use a logo only when the owner asks, only for a product actually named in the video, never in a
way that suggests endorsement or partnership, and list it under *Check before posting* (rule 5).

## Voice and image

- `--audio`: 80 Hz high-pass, RNNoise (when `sh.rnnn` is available), light FFT denoise, -2.5 dB at
  250 Hz (boxiness), +3 dB at 3.5 kHz (presence), de-esser, 3:1 compressor, loudness -14 LUFS. Measure
  before and after with `ffmpeg -i file -af ebur128 -f null -` and report the numbers.
- `--image`: removes a pink/orange LED cast, smooths compression blocks and skin a little, adds
  sharpness. It does not change the face's shape. Show a before/after still. Stronger "face
  restoration" models (GFPGAN, CodeFormer) invent detail and can change how a person looks: only with the
  owner's explicit yes, and say so.
- A video sent through a messaging app arrives small (often 480×850) with a broken frame rate.
  Normalise first (`scale=1080:1920:flags=lanczos,fps=30`) and ask for the original file next time.

## Known pitfalls (already solved in the scripts)

- Silence detection alone cuts words said quietly: always pass through `safe_pauses.py`.
- Joining segments with stream copy leaves timestamp gaps that crash Remotion ("No frame found") and
  drifts captions by ~20 ms per join: `cutkit.py render` now cuts in one pass.
- RNNoise can output NaN on digital silence: the audio chain zeroes those samples.
- Whisper hotwords / initial prompt merge sentences into long blocks: fix names with `--fix` instead.
- Windows: JSON written by PowerShell 5 has a BOM (scripts read `utf-8-sig`); set
  `PYTHONIOENCODING=utf-8` when redirecting script output to a file.
