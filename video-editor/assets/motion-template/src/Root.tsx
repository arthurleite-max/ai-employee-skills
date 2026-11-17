import React from "react";
import { Composition } from "remotion";
import { CaptionedVideo, VideoProps } from "./CaptionedVideo";

const sample: VideoProps = {
  video: "",
  fps: 30,
  width: 1080,
  height: 1920,
  duration: 5,
  style: "highlight",
  color: "#FFD400",
  pages: [
    {
      start: 0.3,
      end: 2.2,
      words: [
        { start: 0.3, end: 0.7, word: "Animated" },
        { start: 0.7, end: 1.2, word: "captions" },
        { start: 1.2, end: 2.0, word: "here" },
      ],
    },
  ],
  elements: [{ type: "title", start: 0, end: 2.5, text: "VIDEO TITLE" }],
};

// Size, frame rate and length come from props.json (scripts/prepare_motion.py).
export const RemotionRoot: React.FC = () => (
  <Composition
    id="CaptionedVideo"
    component={CaptionedVideo}
    defaultProps={sample}
    fps={30}
    width={1080}
    height={1920}
    durationInFrames={150}
    calculateMetadata={({ props }) => ({
      fps: props.fps,
      width: props.width,
      height: props.height,
      durationInFrames: Math.max(1, Math.floor(props.duration * props.fps) - 1),
    })}
  />
);
