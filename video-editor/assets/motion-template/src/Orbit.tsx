import React from "react";
import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { EMOJI_FONT, FONT, PALETTE } from "./Elements";

export type OrbitItem = { text: string; at: number; logo?: string; emoji?: string };
export type OrbitElement = {
  type: "orbit";
  start: number;
  end: number;
  cutout: string; // folder in public/ written by scripts/segment_person.py
  items: OrbitItem[];
  face?: Record<string, [number, number, number]>; // frame -> [cx, cy, width] as fractions of the frame
  turns?: number; // full turns during the effect
};

// Icons circling the head on a tilted ellipse. The back half passes behind the cut-out person,
// so the icons really go "around" the speaker. Each item is born at the front-left, on the frame
// its name is spoken; its label shows for ~1.3 s, then only the icon keeps orbiting.
export const Orbit: React.FC<{ el: OrbitElement }> = ({ el }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const abs = frame + Math.round(el.start * fps);
  const t = frame / fps + el.start;
  const dur = el.end - el.start;

  const f = el.face?.[String(abs)] ?? Object.values(el.face ?? {})[0] ?? [0.5, 0.4, 0.3];
  const [cx, cy, fw] = [f[0] * width, f[1] * height, f[2] * width];
  const rx = Math.max(fw * 1.15, width * 0.29);
  const ry = rx * 0.72; // tilted: behind = above the head, front = at the chin
  const oy = cy - fw * 0.15;
  const size = width * 0.155;
  const speed = ((el.turns ?? 1.3) * Math.PI * 2) / dur; // rad/s
  const SPAWN = Math.PI * 0.8; // front-left
  const exit = interpolate(frame, [dur * fps - 10, dur * fps], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ring = spring({ frame, fps, config: { damping: 20 } });

  const items = el.items.map((it, i) => {
    const th = (t - el.start) * speed + SPAWN - (it.at - el.start) * speed;
    const depth = Math.sin(th); // > 0 = in front of the person
    const fr = Math.round((t - it.at) * fps);
    const s = fr < 0 ? 0 : spring({ frame: fr, fps, config: { damping: 9, stiffness: 180 } });
    const label = interpolate(t - it.at, [1.1, 1.4], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    return { it, i, depth, label, x: cx + rx * Math.cos(th), y: oy + ry * depth, s: s * exit * (0.78 + 0.14 * (depth + 1)) };
  });

  const draw = (list: typeof items) =>
    list.map(({ it, i, x, y, s, depth, label }) => (
      <div key={i} style={{ position: "absolute", left: x, top: y, transform: `translate(-50%,-50%) scale(${s})`,
        filter: depth < 0 ? "brightness(0.8)" : undefined, display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{ width: size, height: size, borderRadius: size * 0.28, background: "#fff", display: "flex",
          alignItems: "center", justifyContent: "center",
          boxShadow: `0 0 0 ${size * 0.05}px ${PALETTE[i % PALETTE.length]}, 0 12px 30px rgba(0,0,0,.5)` }}>
          {it.logo ? <Img src={staticFile(`icons/${it.logo}`)} style={{ width: size * 0.68, height: size * 0.68 }} />
            : <span style={{ fontSize: size * 0.6, fontFamily: EMOJI_FONT }}>{it.emoji}</span>}
        </div>
        <div style={{ opacity: label, marginTop: size * 0.1, fontFamily: FONT, fontWeight: 900, fontSize: size * 0.3,
          color: "#000", background: PALETTE[i % PALETTE.length], padding: "0.1em 0.45em", borderRadius: 999, whiteSpace: "nowrap" }}>
          {it.text}
        </div>
      </div>
    ));

  return (
    <AbsoluteFill>
      <svg width={width} height={height} style={{ position: "absolute", opacity: ring * exit * 0.8 }}>
        <defs><linearGradient id="orbitRing"><stop offset="0" stopColor={PALETTE[1]} /><stop offset="1" stopColor={PALETTE[2]} /></linearGradient></defs>
        <ellipse cx={cx} cy={oy} rx={rx} ry={ry} fill="none" stroke="url(#orbitRing)" strokeWidth={width * 0.008}
          strokeDasharray={`${width * 0.02} ${width * 0.015}`} strokeDashoffset={-frame * 4} />
      </svg>
      {draw(items.filter((x) => x.depth < 0))}
      <Img src={staticFile(`${el.cutout}/f_${abs}.png`)} style={{ position: "absolute", width, height }} />
      {draw(items.filter((x) => x.depth >= 0))}
    </AbsoluteFill>
  );
};
