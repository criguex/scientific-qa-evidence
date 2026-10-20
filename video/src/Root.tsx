import { Audio, Video } from "@remotion/media";
import type React from "react";
import narration from "../../production/narration.json";
import numerical from "../../evidence/numerical/multidomain_derived.json";
import rcBaseline from "../../evidence/numerical/fixtures/rc-baseline.json";
import rcMutation from "../../evidence/numerical/fixtures/rc-tau-double.json";
import generatedMedia from "./generatedMedia.json";
import {
  AbsoluteFill,
  Composition,
  Folder,
  Loop,
  Series,
  Still,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

type Caption = { text: string; startMs: number; endMs: number };
type ChapterAsset = {
  id: string;
  title: string;
  audio: string;
  duration_in_frames: number;
  clip_end_frame: number;
  from_frame: number;
  captions: Caption[];
};
type MediaManifest = {
  status: string;
  fps: number;
  long_duration_in_frames: number;
  chapters: ChapterAsset[];
};
type ChapterSceneProps = { chapterIndex: number; vertical?: boolean };
type ShortProps = { chapterIndex: number };
type CardProps = { chapterIndex: number };

const media = generatedMedia as MediaManifest;
const stories = narration.chapters.map((chapter) => chapter.en);
const campaign = numerical.per_host;
const resultCounts = campaign.classification_counts;
const modelCount = new Set(["rc", "cooling", "chemical_second_order", "beer_lambert", "snell", "thin_lens", "acoustic_interface", "fechner", "logistic"]).size;
const colors = {
  navy: "#071b2b",
  deep: "#0d2638",
  panel: "#122f42",
  mint: "#55dfbd",
  white: "#f4f7f5",
  muted: "#a9bdc6",
  amber: "#ffc56e",
  coral: "#fb8176",
};

const Surface: React.FC<{ children: React.ReactNode; vertical?: boolean }> = ({ children, vertical }) => (
  <AbsoluteFill
    style={{
      backgroundColor: colors.navy,
      backgroundImage: "radial-gradient(ellipse at 78% 20%, #173b4c 0%, #071b2b 56%)",
      color: colors.white,
      fontFamily: "Inter, Avenir Next, Arial, sans-serif",
      padding: vertical ? "92px 100px 190px" : "92px 128px 120px",
      overflow: "hidden",
    }}
  >
    <div style={{ position: "absolute", inset: 0, opacity: 0.18, backgroundImage: "linear-gradient(#557080 1px, transparent 1px), linear-gradient(90deg, #557080 1px, transparent 1px)", backgroundSize: vertical ? "100px 100px" : "120px 120px", maskImage: "linear-gradient(to bottom, black, transparent 86%)" }} />
    {children}
  </AbsoluteFill>
);

const Eyebrow: React.FC<{ children: React.ReactNode; vertical?: boolean }> = ({ children, vertical }) => (
  <div style={{ color: colors.mint, fontSize: vertical ? 26 : 24, fontWeight: 700, letterSpacing: vertical ? 2 : 4, textTransform: "uppercase" }}>{children}</div>
);

const Panel: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <div style={{ background: "linear-gradient(145deg, #15374a, #0d2638)", border: "1px solid #315264", borderRadius: 28, padding: 32, boxShadow: "0 24px 72px #020b1270", ...style }}>{children}</div>
);

const CaptionLine: React.FC<{ chapterIndex: number; vertical: boolean }> = ({ chapterIndex, vertical }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const caption = media.chapters[chapterIndex]?.captions.find((item) => frame * 1000 / fps >= item.startMs && frame * 1000 / fps <= item.endMs);
  if (!caption) return null;
  return (
    <div style={{ position: "absolute", zIndex: 8, left: 0, right: 0, bottom: vertical ? 32 : 24, display: "flex", justifyContent: "center", padding: vertical ? "0 40px" : "0 12px" }}>
      <div style={{ backgroundColor: "#061723e8", border: "1px solid #4ed6b4", borderRadius: 18, color: colors.white, fontSize: vertical ? 42 : 31, fontWeight: 600, lineHeight: 1.25, textAlign: "center", padding: vertical ? "20px 25px" : "16px 28px", maxWidth: vertical ? 880 : 1520 }}>{caption.text}</div>
    </div>
  );
};

const Metric: React.FC<{ value: string; label: string; color?: string; vertical?: boolean }> = ({ value, label, color = colors.mint, vertical }) => (
  <div style={{ display: "flex", flexDirection: "column", gap: vertical ? 12 : 8 }}>
    <div style={{ color, fontSize: vertical ? 60 : 62, fontWeight: 750, lineHeight: 1 }}>{value}</div>
    <div style={{ color: colors.muted, fontSize: vertical ? 32 : 23, fontWeight: 600 }}>{label}</div>
  </div>
);

const ChapterGraphic: React.FC<{ chapterIndex: number; vertical: boolean }> = ({ chapterIndex, vertical }) => {
  const sizes = vertical ? { heading: 40, body: 31, pad: 26 } : { heading: 28, body: 22, pad: 28 };
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const beat = Math.floor(frame / Math.max(1, fps * 1.8));
  if (chapterIndex === 0) {
    return (
      <div style={{ display: "grid", gridTemplateColumns: vertical ? "1fr" : "repeat(3, 1fr)", gap: vertical ? 18 : 22 }}>
        {["Freeze the contract", "Run known mutations", "Compare to an oracle"].map((label, index) => (
          <Panel key={label} style={{ opacity: beat >= index ? 1 : 0.25, transform: `translateY(${beat >= index ? 0 : 16}px)`, padding: sizes.pad, minHeight: vertical ? 112 : 210, display: "flex", flexDirection: vertical ? "row" : "column", alignItems: "center", gap: 20 }}>
            <div style={{ width: 58, height: 58, flex: "0 0 auto", borderRadius: 18, backgroundColor: index === 1 ? colors.amber : colors.mint, color: colors.navy, display: "grid", placeItems: "center", fontSize: 30, fontWeight: 800 }}>{index + 1}</div>
            <div style={{ fontSize: sizes.heading, fontWeight: 700, lineHeight: 1.2 }}>{label}</div>
          </Panel>
        ))}
      </div>
    );
  }
  if (chapterIndex === 1) {
    return (
      <Panel style={{ display: "grid", gridTemplateColumns: vertical ? "1fr" : "1.2fr 1fr", alignItems: "center", gap: 40, padding: vertical ? 30 : 44 }}>
        <div>
          <div style={{ fontSize: sizes.heading, color: colors.muted, fontWeight: 600 }}>RC circuit · τ = R × C = 1 second</div>
          <div style={{ marginTop: 30, display: "grid", gap: 22 }}>
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: sizes.body, marginBottom: 8 }}><span>Baseline at 3 s</span><strong>{rcBaseline.values["256"][3].toFixed(3)} V</strong></div>
              <div style={{ height: 18, background: "#25485a", borderRadius: 10 }}><div style={{ width: `${beat > 0 ? (rcBaseline.values["256"][3] / 5) * 100 : 0}%`, height: "100%", background: colors.mint, borderRadius: 10 }} /></div>
            </div>
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: sizes.body, marginBottom: 8 }}><span>Double τ mutation</span><strong>{rcMutation.values["256"][3].toFixed(3)} V</strong></div>
              <div style={{ height: 18, background: "#25485a", borderRadius: 10 }}><div style={{ width: `${beat > 1 ? (rcMutation.values["256"][3] / 5) * 100 : 0}%`, height: "100%", background: colors.amber, borderRadius: 10 }} /></div>
            </div>
          </div>
        </div>
        <div style={{ borderLeft: vertical ? "none" : "1px solid #315264", borderTop: vertical ? "1px solid #315264" : "none", padding: vertical ? "28px 0 0" : "12px 0 12px 40px" }}>
          <Metric value={String(modelCount)} label="synthetic models" vertical={vertical} />
          <div style={{ marginTop: 24, color: colors.muted, fontSize: sizes.body, lineHeight: 1.45 }}>Three fixed configurations per model. Calculated values, not laboratory measurements.</div>
        </div>
      </Panel>
    );
  }
  if (chapterIndex === 2) {
    return (
      <div style={{ display: "grid", gridTemplateColumns: vertical ? "1fr" : "1.2fr 1fr", gap: 20 }}>
        <Panel style={{ padding: sizes.pad }}>
          <Eyebrow vertical={vertical}>One declaration · two outcomes</Eyebrow>
          <div style={{ marginTop: 20, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
            <div style={{ opacity: beat > 0 ? 1 : 0.28, background: "#0b2434", borderRadius: 18, padding: 20 }}><div style={{ color: colors.muted, fontSize: sizes.body }}>Baseline</div><div style={{ fontSize: sizes.heading, fontFamily: "ui-monospace, SFMono-Regular, monospace", marginTop: 12 }}>0 = 0 · rfl</div><div style={{ color: colors.mint, fontSize: sizes.body, marginTop: 14 }}>Lean accepts · nanoda accepts</div></div>
            <div style={{ opacity: beat > 1 ? 1 : 0.28, background: "#0b2434", borderRadius: 18, padding: 20 }}><div style={{ color: colors.muted, fontSize: sizes.body }}>Mutated value</div><div style={{ fontSize: sizes.heading, fontFamily: "ui-monospace, SFMono-Regular, monospace", marginTop: 12 }}>0 = 0 · True.intro</div><div style={{ color: colors.coral, fontSize: sizes.body, marginTop: 14 }}>Lean type mismatch</div><div style={{ color: colors.amber, fontSize: sizes.body, marginTop: 8 }}>nanoda assertion · derived reject</div></div>
          </div>
          <div style={{ color: colors.muted, fontSize: vertical ? 18 : 18, marginTop: 15 }}>nanoda outcome is derived from pinned typechecker source; the raw summary retains pending classification.</div>
        </Panel>
        <Panel style={{ display: "flex", flexDirection: "column", justifyContent: "center", gap: 18, padding: sizes.pad }}>
          <Eyebrow vertical={vertical}>Separate positive control</Eyebrow>
          <div style={{ fontSize: sizes.heading, fontWeight: 700 }}>Periodic Navier–Stokes</div>
          <div style={{ color: colors.muted, fontSize: sizes.body, lineHeight: 1.4 }}>Torus · constant field · zero pressure and force · unit viscosity</div>
          <div style={{ color: colors.amber, fontSize: sizes.body, fontWeight: 700 }}>Bounded formal control; no Euclidean transfer</div>
        </Panel>
      </div>
    );
  }
  if (chapterIndex === 3) {
    return (
      <Panel style={{ padding: vertical ? 28 : 40 }}>
        <div style={{ display: "grid", gridTemplateColumns: vertical ? "1fr" : "1fr 1fr", gap: vertical ? 18 : 28 }}>
          {["macOS arm64", "Linux x86_64"].map((host) => (
            <div key={host} style={{ background: "#0b2434", borderRadius: 20, padding: vertical ? 22 : 28 }}>
              <Eyebrow vertical={vertical}>{host}</Eyebrow>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", marginTop: 24, gap: 12 }}>
                <Metric value={String(beat > 0 ? resultCounts.PASS : 0)} label="PASS" vertical={vertical} />
                <Metric value={String(beat > 1 ? resultCounts.KILLED : 0)} label="KILLED" color={colors.coral} vertical={vertical} />
                <Metric value={String(beat > 2 ? resultCounts.SURVIVED : 0)} label="SURVIVED" color={colors.amber} vertical={vertical} />
              </div>
            </div>
          ))}
        </div>
        <div style={{ marginTop: 20, textAlign: "center", color: colors.white, fontSize: vertical ? 24 : 25, fontWeight: 700 }}>84 per host · 84 paired matches · not 168 distinct variants</div>
      </Panel>
    );
  }
  return (
    <div style={{ display: "grid", gridTemplateColumns: vertical ? "1fr" : "1.15fr 0.85fr", gap: 20 }}>
      <Panel style={{ padding: sizes.pad }}>
        <Eyebrow vertical={vertical}>Two separate checks</Eyebrow>
        <div style={{ marginTop: 24, display: "grid", gap: 18 }}>
          <div style={{ opacity: beat > 0 ? 1 : 0.26, borderLeft: `6px solid ${colors.mint}`, padding: "6px 18px" }}><div style={{ fontSize: sizes.heading, fontWeight: 750 }}>Clean source build</div><div style={{ color: colors.muted, fontSize: sizes.body, marginTop: 7 }}>PASS · 11,424 jobs · cached dependencies reused</div></div>
          <div style={{ opacity: beat > 1 ? 1 : 0.26, borderLeft: `6px solid ${colors.amber}`, padding: "6px 18px" }}><div style={{ fontSize: sizes.heading, fontWeight: 750 }}>Comparator rerun</div><div style={{ color: colors.muted, fontSize: sizes.body, marginTop: 7 }}>Navier–Stokes and Euler accepted by Lean and nanoda</div></div>
          <div style={{ color: colors.amber, fontSize: sizes.body, fontWeight: 700 }}>Build success is not a full bootstrap or mathematical proof.</div>
        </div>
      </Panel>
      <Panel style={{ padding: 16, position: "relative", minHeight: vertical ? 280 : 240 }}>
        <Loop durationInFrames={1196}><Video src={staticFile("english/media/flow-illustration.mp4")} premountFor={30} muted style={{ width: "100%", height: "100%", objectFit: "cover", borderRadius: 18 }} /></Loop>
        <div style={{ position: "absolute", left: 28, bottom: 28, right: 28, background: "#061723e8", border: `1px solid ${colors.amber}`, borderRadius: 12, padding: "12px 16px", fontSize: vertical ? 18 : 20, fontWeight: 750, textAlign: "center" }}>ILLUSTRATIVE FLOW · NOT A FORMAL PROOF</div>
      </Panel>
    </div>
  );
};

const ChapterScene: React.FC<ChapterSceneProps> = ({ chapterIndex, vertical = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const chapter = stories[chapterIndex];
  const opacity = interpolate(frame, [0, Math.round(fps * 0.6)], [0, 1], { extrapolateRight: "clamp" });
  const titleSize = vertical ? 84 : 82;
  return (
    <Surface vertical={vertical}>
      <div style={{ opacity, position: "relative", zIndex: 1, height: "100%" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <Eyebrow vertical={vertical}>ADV-050 · QA AUTOMATION</Eyebrow>
          <div style={{ color: colors.muted, fontSize: vertical ? 25 : 22, fontWeight: 700 }}>0{chapterIndex + 1} / 05</div>
        </div>
        <div style={{ fontSize: titleSize, fontWeight: 760, lineHeight: 1.02, letterSpacing: -2, maxWidth: vertical ? 880 : 1420, marginTop: vertical ? 44 : 32 }}>{chapter.title}</div>
        <div style={{ marginTop: vertical ? 44 : 34 }}><ChapterGraphic chapterIndex={chapterIndex} vertical={vertical} /></div>
        <div style={{ position: "absolute", left: 0, bottom: vertical ? 245 : 190, color: colors.muted, fontSize: vertical ? 30 : 20 }}>Synthetic calculations and scoped software controls · no theorem discovery claimed</div>
        <CaptionLine chapterIndex={chapterIndex} vertical={vertical} />
      </div>
    </Surface>
  );
};

const LongVideo: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <Series>
      <Series.Sequence name="01 · Method" durationInFrames={media.chapters[0].duration_in_frames} premountFor={fps}><Audio src={staticFile(media.chapters[0].audio)} premountFor={fps} /><ChapterScene chapterIndex={0} /></Series.Sequence>
      <Series.Sequence name="02 · Synthetic models" durationInFrames={media.chapters[1].duration_in_frames} premountFor={fps}><Audio src={staticFile(media.chapters[1].audio)} premountFor={fps} /><ChapterScene chapterIndex={1} /></Series.Sequence>
      <Series.Sequence name="03 · Formal controls" durationInFrames={media.chapters[2].duration_in_frames} premountFor={fps}><Audio src={staticFile(media.chapters[2].audio)} premountFor={fps} /><ChapterScene chapterIndex={2} /></Series.Sequence>
      <Series.Sequence name="04 · Paired campaign" durationInFrames={media.chapters[3].duration_in_frames} premountFor={fps}><Audio src={staticFile(media.chapters[3].audio)} premountFor={fps} /><ChapterScene chapterIndex={3} /></Series.Sequence>
      <Series.Sequence name="05 · Reproducibility and limits" durationInFrames={media.chapters[4].duration_in_frames} premountFor={fps}><Audio src={staticFile(media.chapters[4].audio)} premountFor={fps} /><ChapterScene chapterIndex={4} /></Series.Sequence>
    </Series>
  );
};

const ShortVideo: React.FC<ShortProps> = ({ chapterIndex }) => (
  <>
    <Audio src={staticFile(media.chapters[chapterIndex].audio)} premountFor={30} />
    <ChapterScene chapterIndex={chapterIndex} vertical />
  </>
);

const CardStill: React.FC<CardProps> = ({ chapterIndex }) => {
  const { width } = useVideoConfig();
  const cover = chapterIndex === 0;
  const storyIndex = cover ? 0 : chapterIndex - 1;
  const title = cover ? "Would your tests catch it?" : stories[storyIndex].title;
  const detail = [
    "Synthetic mutations. Narrow controls. Explicit limits.",
    "Freeze the contract → mutate → compare with an oracle.",
    `${modelCount} synthetic models · 27 fixed configurations.`,
    "One fixture · one incompatible proof-value mutation · bounded result.",
    `${resultCounts.PASS} PASS · ${resultCounts.KILLED} KILLED · ${resultCounts.SURVIVED} SURVIVED per host.`,
    "Build: PASS · 11,424 jobs. Comparator: both configured challenges accepted by both kernels.",
  ][chapterIndex];
  return (
    <Surface>
      <div style={{ position: "relative", zIndex: 1, display: "flex", flexDirection: "column", justifyContent: "space-between", height: "100%" }}>
        <Eyebrow>ADV-050 · Independent QA study</Eyebrow>
        <div style={{ maxWidth: width - 280 }}>
          <div style={{ fontSize: 30, color: colors.mint, fontWeight: 700, marginBottom: 24 }}>{cover ? "EVIDENCE · MUTATIONS · LIMITS" : `CHAPTER 0${storyIndex + 1}`}</div>
          <div style={{ fontSize: cover ? 88 : 76, lineHeight: 1.04, letterSpacing: -2, fontWeight: 760 }}>{title}</div>
          <Panel style={{ marginTop: 30, padding: 26, borderColor: chapterIndex === 5 ? colors.amber : colors.mint }}>
            <div style={{ fontSize: 36, color: colors.white, fontWeight: 700, lineHeight: 1.25 }}>{detail}</div>
            {chapterIndex === 5 && <div style={{ marginTop: 20, color: colors.amber, fontSize: 23, fontWeight: 750 }}>No theorem discovery · no certification · review before release</div>}
          </Panel>
        </div>
        <div style={{ display: "flex", alignItems: "end", justifyContent: "space-between" }}>
          <div style={{ color: colors.muted, fontSize: 25 }}>Cristian Guerra · criguex · Medellín, Colombia</div>
          <div style={{ color: colors.mint, fontSize: 25, fontWeight: 750 }}>CONTROLLED EXAMPLES</div>
        </div>
      </div>
    </Surface>
  );
};

export const RemotionRoot: React.FC = () => (
  <>
    {media.status === "ready" && media.chapters.length === 5 && (
      <Folder name="English-video">
        <Composition id="ENLong1920x1080" component={LongVideo} width={1920} height={1080} fps={media.fps} durationInFrames={media.long_duration_in_frames} />
        <Composition id="ENShort01Method1080x1920" component={ShortVideo} width={1080} height={1920} fps={media.fps} durationInFrames={media.chapters[0].clip_end_frame} defaultProps={{ chapterIndex: 0 }} />
        <Composition id="ENShort02Models1080x1920" component={ShortVideo} width={1080} height={1920} fps={media.fps} durationInFrames={media.chapters[1].clip_end_frame} defaultProps={{ chapterIndex: 1 }} />
        <Composition id="ENShort03Formal1080x1920" component={ShortVideo} width={1080} height={1920} fps={media.fps} durationInFrames={media.chapters[2].clip_end_frame} defaultProps={{ chapterIndex: 2 }} />
        <Composition id="ENShort04Results1080x1920" component={ShortVideo} width={1080} height={1920} fps={media.fps} durationInFrames={media.chapters[3].clip_end_frame} defaultProps={{ chapterIndex: 3 }} />
        <Composition id="ENShort05Limits1080x1920" component={ShortVideo} width={1080} height={1920} fps={media.fps} durationInFrames={media.chapters[4].clip_end_frame} defaultProps={{ chapterIndex: 4 }} />
      </Folder>
    )}
    <Folder name="English-cards">
      <Still id="ENCard01Cover1080" component={CardStill} width={1080} height={1080} defaultProps={{ chapterIndex: 0 }} />
      <Still id="ENCard02Method1080" component={CardStill} width={1080} height={1080} defaultProps={{ chapterIndex: 1 }} />
      <Still id="ENCard03Models1080" component={CardStill} width={1080} height={1080} defaultProps={{ chapterIndex: 2 }} />
      <Still id="ENCard04Formal1080" component={CardStill} width={1080} height={1080} defaultProps={{ chapterIndex: 3 }} />
      <Still id="ENCard05Results1080" component={CardStill} width={1080} height={1080} defaultProps={{ chapterIndex: 4 }} />
      <Still id="ENCard06Limits1080" component={CardStill} width={1080} height={1080} defaultProps={{ chapterIndex: 5 }} />
    </Folder>
  </>
);
