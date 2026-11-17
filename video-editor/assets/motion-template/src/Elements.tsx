import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Flag } from "./Flags";

export const FONT = "'Montserrat', 'Arial Black', 'Segoe UI', sans-serif";
export const EMOJI_FONT = "'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji', sans-serif";
// Replace with the brand colours from the owner's profile.
export const PALETTE = ["#FFD400", "#00E5FF", "#FF3D7F", "#7CFF4F", "#B388FF"];

export type Item = { text: string; at: number; emoji?: string; flag?: string };
export type Element =
  | { type: "title" | "callout"; start: number; end: number; text: string }
  | { type: "list"; start: number; end: number; heading?: string; items: Item[] }
  | { type: "counter"; start: number; end: number; values: { value: number; at: number; label?: string }[] }
  | { type: "stamp"; start: number; end: number; text: string };

// shared exit: fade out over the last 8 frames
const useExit = (dur: number) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return interpolate(frame, [dur * fps - 8, dur * fps], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
};

// graphics live in the top band so they never cover the speaker's face
const Top: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { height } = useVideoConfig();
  return (
    <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: height * 0.08 }}>
      {children}
    </AbsoluteFill>
  );
};

export const Box: React.FC<{ text: string; color: string; big?: boolean; dur: number }> = ({ text, color, big, dur }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 11, stiffness: 160 } });
  const exit = useExit(dur);
  const size = width * (big ? 0.095 : 0.072);
  return (
    <Top>
      <div style={{
        fontFamily: FONT, fontWeight: 900, fontSize: size, textAlign: "center", maxWidth: width * 0.88, color: "#000",
        background: color, padding: "0.15em 0.45em", borderRadius: size * 0.2, lineHeight: 1.05,
        transform: `scale(${enter * exit}) rotate(${interpolate(enter, [0, 1], [-10, -2.5])}deg)`,
        boxShadow: `0 0 0 ${size * 0.08}px #000, 0 16px 50px rgba(0,0,0,.5)`,
      }}>
        {text}
      </div>
    </Top>
  );
};

export const List: React.FC<{ el: Extract<Element, { type: "list" }> }> = ({ el }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const t = frame / fps + el.start;
  const exit = useExit(el.end - el.start);
  const size = width * 0.058;
  const head = spring({ frame, fps, config: { damping: 12 } });
  return (
    <Top>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: size * 0.35, opacity: exit, maxWidth: width * 0.92 }}>
        {el.heading && (
          <div style={{
            fontFamily: FONT, fontWeight: 900, fontSize: size * 0.8, color: "#fff", letterSpacing: "0.08em",
            background: "#000", padding: "0.2em 0.6em", borderRadius: 999,
            transform: `translateY(${interpolate(head, [0, 1], [-60, 0])}px)`, opacity: head,
          }}>
            {el.heading}
          </div>
        )}
        <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: size * 0.3 }}>
          {el.items.map((it, i) => {
            const f = Math.round((t - it.at) * fps);
            if (f < 0) return null; // each item pops in on the frame its word is spoken
            const s = spring({ frame: f, fps, config: { damping: 9, stiffness: 200 } });
            return (
              <div key={i} style={{
                display: "flex", alignItems: "center", gap: size * 0.3, fontFamily: FONT, fontWeight: 900,
                fontSize: size, color: "#000", background: PALETTE[i % PALETTE.length], padding: "0.18em 0.5em",
                borderRadius: size * 0.25, boxShadow: `0 0 0 ${size * 0.07}px #000, 0 10px 30px rgba(0,0,0,.45)`,
                transform: `scale(${s}) rotate(${interpolate(s, [0, 1], [i % 2 ? 14 : -14, i % 2 ? 2 : -2])}deg)`,
              }}>
                {it.flag && <Flag country={it.flag} size={size * 0.95} />}
                {it.emoji && <span style={{ fontFamily: EMOJI_FONT }}>{it.emoji}</span>}
                {it.text}
              </div>
            );
          })}
        </div>
      </div>
    </Top>
  );
};

export const Counter: React.FC<{ el: Extract<Element, { type: "counter" }>; locale?: string }> = ({ el, locale }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const t = frame / fps + el.start;
  const exit = useExit(el.end - el.start);
  const vs = el.values;
  let idx = 0;
  vs.forEach((v, i) => { if (t >= v.at) idx = i; });
  const cur = vs[idx];
  const prev = idx > 0 ? vs[idx - 1].value : 0;
  const prog = interpolate(t, [cur.at, cur.at + 0.45], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const value = prev + (cur.value - prev) * (1 - Math.pow(1 - prog, 3));
  const pop = spring({ frame: Math.round((t - cur.at) * fps), fps, config: { damping: 8, stiffness: 220 } });
  const color = PALETTE[idx % PALETTE.length];
  const showLabel = prog >= 1 && cur.label; // e.g. "1 MILLION", exactly as spoken
  const size = width * (showLabel ? 0.16 : 0.2);
  return (
    <Top>
      <div style={{ opacity: exit, display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{
          fontFamily: FONT, fontWeight: 900, fontSize: size, color, lineHeight: 1,
          WebkitTextStroke: `${size * 0.05}px #000`, paintOrder: "stroke fill",
          textShadow: `0 0 ${size * 0.4}px ${color}88, 0 12px 30px rgba(0,0,0,.6)`,
          transform: `scale(${interpolate(pop, [0, 1], [1.35, 1])})`, fontVariantNumeric: "tabular-nums",
        }}>
          {showLabel ? cur.label : Math.round(value).toLocaleString(locale)}
        </div>
        <div style={{ display: "flex", gap: width * 0.02, marginTop: width * 0.03 }}>
          {vs.map((_, i) => (
            <div key={i} style={{ width: width * 0.035, height: width * 0.035, borderRadius: 999, border: "3px solid #000",
              background: i <= idx ? PALETTE[i % PALETTE.length] : "rgba(255,255,255,.35)" }} />
          ))}
        </div>
      </div>
    </Top>
  );
};

export const Stamp: React.FC<{ text: string; dur: number }> = ({ text, dur }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 7, stiffness: 140 } });
  const exit = useExit(dur);
  const size = width * 0.085;
  return (
    <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: height * 0.14 }}>
      <div style={{
        fontFamily: FONT, fontWeight: 900, fontSize: size, color: PALETTE[2], textAlign: "center", lineHeight: 1.05,
        border: `${size * 0.1}px solid ${PALETTE[2]}`, padding: "0.25em 0.5em", borderRadius: size * 0.25,
        background: "rgba(0,0,0,.55)", opacity: exit, transform: `scale(${interpolate(s, [0, 1], [2.6, 1])}) rotate(-8deg)`,
      }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};
