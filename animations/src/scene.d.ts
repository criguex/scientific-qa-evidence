export type AnimationId = "rc" | "chemistry" | "campaign" | "formal" | "cooling" | "snell";

export function drawAnimation(
  context: CanvasRenderingContext2D,
  packageData: unknown,
  animationId: AnimationId,
  seconds: number,
): void;
