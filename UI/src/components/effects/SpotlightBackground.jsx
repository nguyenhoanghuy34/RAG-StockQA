import { useState } from "react";

export default function SpotlightBackground({ background, children }) {
  const [pos, setPos] = useState({ x: 0, y: 0 });

  return (
    <div
      className="relative flex h-screen items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: `url(${background})` }}
      onMouseMove={(e) => {
        setPos({ x: e.clientX, y: e.clientY });
      }}
    >
      {/* overlay spotlight */}
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background: `radial-gradient(
            200px at ${pos.x}px ${pos.y}px,
            rgba(255,255,255,0.35),
            rgba(0,0,0,0.8)
          )`,
          transition: "background 0.08s linear",
        }}
      />

      {/* nội dung (chat UI) */}
      <div className="relative z-10 w-full h-full flex items-center justify-center">
        {children}
      </div>
    </div>
  );
}
