import type React from "react";
import { Composition, Folder } from "remotion";
import { CanvasScene } from "./CanvasScene";

const Square: React.FC<{ sceneId: "rc" | "chemistry" | "campaign" | "formal" | "cooling" | "snell" }> = ({ sceneId }) => (
  <CanvasScene sceneId={sceneId} />
);

const Vertical: React.FC<{ sceneId: "rc" | "chemistry" | "campaign" | "formal" | "cooling" | "snell" }> = ({ sceneId }) => (
  <CanvasScene sceneId={sceneId} vertical />
);

export const AnimationRoot = () => (
  <>
    <Folder name="Square">
      <Composition id="RC" component={Square} durationInFrames={480} fps={24} width={1080} height={1080} defaultProps={{ sceneId: "rc" }} />
      <Composition id="Chemistry" component={Square} durationInFrames={480} fps={24} width={1080} height={1080} defaultProps={{ sceneId: "chemistry" }} />
      <Composition id="Campaign" component={Square} durationInFrames={480} fps={24} width={1080} height={1080} defaultProps={{ sceneId: "campaign" }} />
      <Composition id="Formal" component={Square} durationInFrames={480} fps={24} width={1080} height={1080} defaultProps={{ sceneId: "formal" }} />
      <Composition id="Cooling" component={Square} durationInFrames={480} fps={24} width={1080} height={1080} defaultProps={{ sceneId: "cooling" }} />
      <Composition id="Snell" component={Square} durationInFrames={480} fps={24} width={1080} height={1080} defaultProps={{ sceneId: "snell" }} />
    </Folder>
    <Folder name="Vertical">
      <Composition id="RCVertical" component={Vertical} durationInFrames={480} fps={24} width={1080} height={1920} defaultProps={{ sceneId: "rc" }} />
      <Composition id="ChemistryVertical" component={Vertical} durationInFrames={480} fps={24} width={1080} height={1920} defaultProps={{ sceneId: "chemistry" }} />
      <Composition id="CampaignVertical" component={Vertical} durationInFrames={480} fps={24} width={1080} height={1920} defaultProps={{ sceneId: "campaign" }} />
      <Composition id="FormalVertical" component={Vertical} durationInFrames={480} fps={24} width={1080} height={1920} defaultProps={{ sceneId: "formal" }} />
      <Composition id="CoolingVertical" component={Vertical} durationInFrames={480} fps={24} width={1080} height={1920} defaultProps={{ sceneId: "cooling" }} />
      <Composition id="SnellVertical" component={Vertical} durationInFrames={480} fps={24} width={1080} height={1920} defaultProps={{ sceneId: "snell" }} />
    </Folder>
  </>
);
