import type React from "react";
import { Composition, Folder } from "remotion";
import generatedMedia from "../generatedMedia.json";
import { LongVisualV2, ShortVisualV2 } from "./Story";

const media = generatedMedia as { fps: number; long_duration_in_frames: number; chapters: { id: string; clip_end_frame: number }[] };
const Short01: React.FC = () => <ShortVisualV2 chapterIndex={0} />;
const Short02: React.FC = () => <ShortVisualV2 chapterIndex={1} />;
const Short03: React.FC = () => <ShortVisualV2 chapterIndex={2} />;
const Short04: React.FC = () => <ShortVisualV2 chapterIndex={3} />;
const Short05: React.FC = () => <ShortVisualV2 chapterIndex={4} />;

export const VisualV2Root = () => (
  <>
    <Folder name="V2-YouTube">
      <Composition id="EN-V2-Long" component={LongVisualV2} durationInFrames={media.long_duration_in_frames} fps={media.fps} width={1920} height={1080} />
      <Composition id="EN-V2-Short-01-Method" component={Short01} durationInFrames={media.chapters[0].clip_end_frame} fps={media.fps} width={1080} height={1920} />
      <Composition id="EN-V2-Short-02-Models" component={Short02} durationInFrames={media.chapters[1].clip_end_frame} fps={media.fps} width={1080} height={1920} />
      <Composition id="EN-V2-Short-03-Formal" component={Short03} durationInFrames={media.chapters[2].clip_end_frame} fps={media.fps} width={1080} height={1920} />
      <Composition id="EN-V2-Short-04-Campaign" component={Short04} durationInFrames={media.chapters[3].clip_end_frame} fps={media.fps} width={1080} height={1920} />
      <Composition id="EN-V2-Short-05-Limits" component={Short05} durationInFrames={media.chapters[4].clip_end_frame} fps={media.fps} width={1080} height={1920} />
    </Folder>
  </>
);
