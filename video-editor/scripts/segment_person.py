#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cut the person out of the background (MediaPipe) over a time range and track the face per frame.
Used by "behind me" effects in the motion template (orbit, text behind the head).

  python segment_person.py motion/public/video.mp4 --from 24.0 --to 27.5 --name orbit1 \
      --public motion/public --models models/ [--props v1/props.json]

Writes <public>/<name>/f_<frame>.png (person on a transparent background) and face.json
({fps, from, to, frames: {frame: [cx, cy, width]}}, fractions of the frame, smoothed). With --props,
the face track is injected into the element whose "cutout" equals --name.

Requires: pip install mediapipe pillow numpy, plus two model files in --models (see reference/motion.md):
selfie_multiclass_256x256.tflite and blaze_face_short_range.tflite.
"""
import argparse, json, os, subprocess

import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision
from PIL import Image


def info(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    n, d = s["r_frame_rate"].split("/")
    return s["width"], s["height"], round(float(n) / float(d))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--from", dest="start", type=float, required=True)
    ap.add_argument("--to", dest="end", type=float, required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--public", required=True)
    ap.add_argument("--models", required=True)
    ap.add_argument("--props")
    a = ap.parse_args()

    w, h, fps = info(a.video)
    folder = os.path.join(a.public, a.name)
    os.makedirs(folder, exist_ok=True)
    seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
        base_options=BaseOptions(model_asset_path=os.path.join(a.models, "selfie_multiclass_256x256.tflite")),
        output_confidence_masks=True, output_category_mask=False))
    det = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(
        base_options=BaseOptions(model_asset_path=os.path.join(a.models, "blaze_face_short_range.tflite")),
        min_detection_confidence=0.4))

    f0 = int(round(a.start * fps))
    n = int(round((a.end - a.start) * fps)) + 1
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{f0 / fps:.3f}", "-i", a.video, "-frames:v", str(n),
                             "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    faces, last = {}, None
    for i in range(n):
        buf = proc.stdout.read(w * h * 3)
        if len(buf) < w * h * 3:
            break
        rgb = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        bg = seg.segment(img).confidence_masks[0].numpy_view()  # class 0 = background
        alpha = np.clip((1.0 - bg) * 1.6 - 0.3, 0, 1)  # firmer edge
        Image.fromarray(np.dstack([rgb, (alpha * 255).astype(np.uint8)]), "RGBA").save(
            os.path.join(folder, f"f_{f0 + i}.png"), compress_level=1)
        r = det.detect(img).detections
        if r:
            b = max(r, key=lambda d: d.bounding_box.width).bounding_box
            cur = [(b.origin_x + b.width / 2) / w, (b.origin_y + b.height / 2) / h, b.width / w]
            last = cur if last is None else [0.7 * u + 0.3 * x for u, x in zip(last, cur)]  # smoothing
        if last:
            faces[f0 + i] = [round(x, 4) for x in last]
    proc.wait()
    with open(os.path.join(folder, "face.json"), "w", encoding="utf-8") as f:
        json.dump({"fps": fps, "from": f0, "to": f0 + n - 1, "frames": faces}, f)
    if a.props:
        props = json.load(open(a.props, encoding="utf-8-sig"))
        for el in props.get("elements", []):
            if el.get("cutout") == a.name:
                el["face"] = {str(k): v for k, v in faces.items()}
        with open(a.props, "w", encoding="utf-8") as f:
            json.dump(props, f, ensure_ascii=False, indent=1)
    print(f"OK: {n} frames cut out into {folder}, face found in {len(faces)}")


if __name__ == "__main__":
    main()
