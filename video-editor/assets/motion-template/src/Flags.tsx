import React from "react";

// Flags drawn in SVG (Chrome on Windows has no flag emoji). Add more by following the same pattern.
const W = 60;
const H = 42;

const Brazil = () => (
  <>
    <rect width={W} height={H} fill="#009C3B" />
    <polygon points={`${W / 2},4 ${W - 5},${H / 2} ${W / 2},${H - 4} 5,${H / 2}`} fill="#FFDF00" />
    <circle cx={W / 2} cy={H / 2} r={9.5} fill="#002776" />
    <path d={`M${W / 2 - 9.3},${H / 2 - 1.5} Q${W / 2},${H / 2 - 5} ${W / 2 + 9.3},${H / 2 + 2}`} stroke="#fff" strokeWidth={1.6} fill="none" />
  </>
);

const USA = () => (
  <>
    {Array.from({ length: 13 }).map((_, i) => (
      <rect key={i} y={(i * H) / 13} width={W} height={H / 13 + 0.2} fill={i % 2 ? "#fff" : "#B22234"} />
    ))}
    <rect width={W * 0.42} height={(H * 7) / 13} fill="#3C3B6E" />
    {Array.from({ length: 12 }).map((_, i) => (
      <circle key={i} cx={3.5 + (i % 4) * 6.3} cy={3.5 + Math.floor(i / 4) * 6.8} r={1.3} fill="#fff" />
    ))}
  </>
);

const India = () => (
  <>
    <rect width={W} height={H / 3} fill="#FF9933" />
    <rect y={H / 3} width={W} height={H / 3} fill="#fff" />
    <rect y={(2 * H) / 3} width={W} height={H / 3} fill="#138808" />
    <circle cx={W / 2} cy={H / 2} r={5.5} fill="none" stroke="#000080" strokeWidth={1.3} />
    <circle cx={W / 2} cy={H / 2} r={1.2} fill="#000080" />
  </>
);

const Japan = () => (
  <>
    <rect width={W} height={H} fill="#fff" />
    <circle cx={W / 2} cy={H / 2} r={H * 0.3} fill="#BC002D" />
  </>
);

const FLAGS: Record<string, React.FC> = { br: Brazil, us: USA, in: India, jp: Japan };

export const Flag: React.FC<{ country: string; size: number }> = ({ country, size }) => {
  const C = FLAGS[country];
  if (!C) return null;
  return (
    <svg viewBox={`0 0 ${W} ${H}`} height={size} width={(size * W) / H}
      style={{ borderRadius: size * 0.12, boxShadow: "0 4px 14px rgba(0,0,0,.4)", flexShrink: 0 }}>
      <C />
    </svg>
  );
};
