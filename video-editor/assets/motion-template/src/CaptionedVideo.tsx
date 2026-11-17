import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Box, Counter, Element, FONT, List, PALETTE, Stamp } from "./Elements";
import { Orbit, OrbitElement } from "./Orbit";

type Word = { start: number; end: number; word: string };
type Page = { start: number; end: number; words: Word[] };
type Cut = { start: number; end: number };

export type VideoProps = {
  video: string;
  fps: number;
  width: number;
  height: number;
  duration: number;
  style: "highlight" | "karaoke" | "clean";
  color: string; // "multicolor" rotates the palette on every caption
  pages: Page[];
  elements: (Element | OrbitElement)[];
  cuts?: Cut[];
  zoom?: boolean;
  progress?: boolean;
  locale?: string;
};

const Caption: React.FC<{ page: Page; style: VideoProps["style"]; color: string }> = ({ page, style, color }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = frame / fps + page.start; // frame is relative to the page's Sequence
  const vertical = height > width;
  const size = Math.round(width * (vertical ? 0.085 : 0.05));
  const enter = spring({ frame, fps, config: { damping: 14, stiffness: 180 }, durationInFrames: 8 });
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: height * (vertical ? 0.2 : 0.1) }}>
      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", columnGap: size * 0.32, maxWidth: width * 0.86,
        transform: `scale(${interpolate(enter, [0, 1], [0.85, 1])})`, opacity: enter }}>
        {page.words.map((w, i) => {
          const active = t >= w.start && t < w.end + 0.05;
          const said = t >= w.start;
          const c = style === "clean" ? "#FFFFFF" : style === "karaoke" ? (said ? color : "#FFFFFF") : active ? color : "#FFFFFF";
          return (
            <span key={i} style={{
              fontFamily: FONT, fontWeight: 900, fontSize: size, lineHeight: 1.1, textTransform: "uppercase", color: c,
              WebkitTextStroke: `${Math.max(2, size * 0.07)}px #000`, paintOrder: "stroke fill",
              textShadow: "0 6px 18px rgba(0,0,0,.55)", display: "inline-block",
              transform: `translateY(${style === "highlight" && active ? -0.06 : 0}em)`, // a small hop, never into the neighbour
            }}>
              {w.word}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// alternate punch-in at every cut (hides jump cuts) plus a slow push-in inside each segment
const cutScale = (t: number, cuts: Cut[]) => {
  const i = cuts.findIndex((c) => t >= c.start && t < c.end);
  if (i < 0) return 1;
  return (i % 2 ? 1.12 : 1.0) + interpolate(t, [cuts[i].start, cuts[i].end], [0, 0.04], { extrapolateRight: "clamp" });
};

const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames, width } = useVideoConfig();
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", top: 0, left: 0, height: width * 0.012, width: `${(frame / durationInFrames) * 100}%`,
        background: `linear-gradient(90deg, ${PALETTE.join(",")})` }} />
    </AbsoluteFill>
  );
};

const renderElement = (el: Element, color: string, i: number, locale?: string) => {
  const dur = el.end - el.start;
  const c = color === "multicolor" ? PALETTE[i % PALETTE.length] : color;
  switch (el.type) {
    case "title": return <Box text={el.text} color={c} big dur={dur} />;
    case "callout": return <Box text={el.text} color={c} dur={dur} />;
    case "list": return <List el={el} />;
    case "counter": return <Counter el={el} locale={locale} />;
    case "stamp": return <Stamp text={el.text} dur={dur} />;
    default: return null;
  }
};

export const CaptionedVideo: React.FC<VideoProps> = ({ video, style, color, pages, elements, cuts = [], zoom, progress, locale }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const scale = zoom ? cutScale(frame / fps, cuts) : 1;
  const orbits = elements.filter((e): e is OrbitElement => e.type === "orbit");
  const others = elements.filter((e): e is Element => e.type !== "orbit");
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {video ? (
        // the orbit lives inside the zoomed layer so the cut-out person stays aligned with the video
        <AbsoluteFill style={{ transform: `scale(${scale})`, transformOrigin: "50% 40%" }}>
          <OffthreadVideo src={staticFile(video)} />
          {orbits.map((o, i) => (
            <Sequence key={`o${i}`} from={f(o.start)} durationInFrames={Math.max(1, f(o.end - o.start))}>
              <Orbit el={o} />
            </Sequence>
          ))}
        </AbsoluteFill>
      ) : null}
      {others.map((e, i) => (
        <Sequence key={`e${i}`} from={f(e.start)} durationInFrames={Math.max(1, f(e.end - e.start))}>
          {renderElement(e, color, i, locale)}
        </Sequence>
      ))}
      {pages.map((p, i) => (
        <Sequence key={`p${i}`} from={f(p.start)} durationInFrames={Math.max(1, f(p.end - p.start))}>
          <Caption page={p} style={style} color={color === "multicolor" ? PALETTE[i % PALETTE.length] : color} />
        </Sequence>
      ))}
      {progress ? <ProgressBar /> : null}
    </AbsoluteFill>
  );
};
