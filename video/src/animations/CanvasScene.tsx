import { useLayoutEffect, useRef } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import packageData from "../../../animations/manifest.json";
import { drawAnimation } from "../../../animations/src/scene.js";

type AnimationId = "rc" | "chemistry" | "campaign" | "formal" | "cooling" | "snell";
type Props = { sceneId: AnimationId; vertical?: boolean; timeOverrideSeconds?: number };

const titles: Record<AnimationId, string> = {
  rc: "One mutation. A measured difference.",
  chemistry: "Rate mutation changes concentration.",
  campaign: "The same 84 variants on two hosts.",
  formal: "Change the proof value—not the theorem.",
  cooling: "A rate change slows the approach to ambient.",
  snell: "Swapping indices bends the ray too far.",
};

const notes: Record<AnimationId, string> = {
  rc: "Fixed RC inputs · analytic curve vs recorded RK4",
  chemistry: "Concentration changes; vessel volume stays fixed",
  campaign: "84 paired variants per host · not 168 unique",
  formal: "One proof-value mutation · bounded fixture only",
  cooling: "Lumped synthetic model · not a material experiment",
  snell: "Angles from normal · rays are schematic",
};

export const CanvasScene: React.FC<Props> = ({ sceneId, vertical = false, timeOverrideSeconds }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const size = vertical ? 960 : 1080;

  useLayoutEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas?.getContext("2d", { alpha: false });
    if (!canvas || !context) throw new Error("Could not acquire the 2D animation canvas");
    const scale = size / 1080;
    context.setTransform(scale, 0, 0, scale, 0, 0);
    drawAnimation(context, packageData, sceneId, timeOverrideSeconds ?? frame / fps);
  }, [frame, fps, sceneId, size, timeOverrideSeconds]);

  if (!vertical) {
    return <canvas ref={canvasRef} width={1080} height={1080} style={{ width: 1080, height: 1080, display: "block" }} />;
  }

  return (
    <AbsoluteFill style={{ background: "#071b2b", color: "#f4f7f5", fontFamily: "Inter, Avenir Next, Arial, sans-serif" }}>
      <div style={{ position: "absolute", top: 72, left: 72, right: 72, height: 82, display: "flex", alignItems: "center", justifyContent: "space-between", color: "#55dfbd", fontSize: 24, fontWeight: 800, letterSpacing: 3 }}>
        <span>ADV-050 · QA EVIDENCE</span><span>ANIMATED STUDY</span>
      </div>
      <div style={{ position: "absolute", top: 170, left: 60, width: 960, height: 960 }}>
        <canvas ref={canvasRef} width={960} height={960} style={{ width: 960, height: 960, display: "block" }} />
      </div>
      <div style={{ position: "absolute", left: 72, right: 72, bottom: 100, minHeight: 168, borderTop: "2px solid #315264", paddingTop: 26 }}>
        <div style={{ fontSize: 32, fontWeight: 800, lineHeight: 1.16 }}>{titles[sceneId]}</div>
        <div style={{ marginTop: 18, color: "#abc0c8", fontSize: 23, lineHeight: 1.3 }}>{notes[sceneId]}</div>
        <div style={{ marginTop: 12, color: "#55dfbd", fontSize: 19, fontWeight: 750 }}>Cristian Guerra · QA Automation · Medellín, Colombia · @criguex</div>
      </div>
    </AbsoluteFill>
  );
};
