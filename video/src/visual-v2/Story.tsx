import { Audio, Video } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CanvasScene } from "../animations/CanvasScene";
import generatedMedia from "../generatedMedia.json";
import narration from "../../../production/narration.json";
import campaignSummary from "../../../evidence/numerical/multidomain_derived.json";
import rcBaseline from "../../../evidence/numerical/fixtures/rc-baseline.json";
import rcMutation from "../../../evidence/numerical/fixtures/rc-tau-double.json";

type SceneId = "rc" | "chemistry" | "campaign" | "formal" | "cooling" | "snell";
type Chapter = { id: string; title: string; audio: string; duration_in_frames: number; clip_end_frame: number; from_frame: number; captions: { text: string; startMs: number; endMs: number }[] };
type MediaManifest = { status: string; fps: number; width: number; height: number; long_duration_in_frames: number; chapters: Chapter[] };
type Beat = { at: number; scene: SceneId | "flow"; kind: string; title: string; body: string; values?: string[]; video?: boolean; videoStart?: number };

const media = generatedMedia as MediaManifest;
const chapters = narration.chapters;
const counts = campaignSummary.per_host.classification_counts;
const modelNames = ["RC circuit", "Newton cooling", "2nd-order consumption", "Beer–Lambert", "Snell refraction", "Thin lens", "Acoustic interface", "Fechner scale*", "Logistic response"];
const colors = { navy: "#071b2b", deep: "#0d2638", panel: "#123448", mint: "#55dfbd", white: "#f4f7f5", muted: "#abc0c8", coral: "#fb8176", gold: "#ffc56e", blue: "#70b9ff" };

const beats: Beat[][] = [
  [
    { at: 0, scene: "rc", kind: "flow", title: "What can a test actually show?", body: "A green suite is not enough. This footage is illustrative context—not evidence of blow-up or of the campaign.", video: true, videoStart: 0 },
    { at: 5, scene: "rc", kind: "contract", title: "Freeze the contract first", body: "Specify the domain, units, tolerance and invariants before results are known.", values: ["Domain", "Units", "Tolerance", "Invariants"] },
    { at: 12, scene: "rc", kind: "mutation", title: "Run deliberate changes", body: "A baseline is compared with controlled mutations such as a sign reversal or doubled coefficient.", values: ["Baseline", "Sign reversal", "Coefficient ×2"] },
    { at: 18, scene: "rc", kind: "detect", title: "Measure test sensitivity", body: "The test asks whether an independent oracle detects the known change—not whether a theorem was discovered.", values: ["Known change", "Independent oracle", "Classification"] },
    { at: 26, scene: "chemistry", kind: "independent", title: "Avoid shared implementation errors", body: "A program and oracle that share a formula and integrator can share a mistake.", values: ["SUT", "Different formulation", "Multiple observations"] },
    { at: 36, scene: "formal", kind: "contract", title: "Keep success criteria fixed", body: "A failing baseline blocks interpretation of its mutants. A tiny change can survive if it stays below the fixed threshold.", values: ["Baseline must pass", "Mutant evaluated", "Tolerance unchanged"] },
    { at: 45, scene: "rc", kind: "survivor", title: "A survivor is still a result", body: "Small variations can remain inside the contract. They are reported, not silently promoted to equivalence.", values: ["SURVIVED", "Within tolerance", "No equivalence claim"] },
    { at: 55, scene: "campaign", kind: "trace", title: "Preserve the evidence chain", body: "Parameters, source, hashes and outputs stay linked so a reviewer can trace each classification.", values: ["Contract", "Source + parameters", "Outputs + hashes"] },
    { at: 56, scene: "rc", kind: "author", title: "Who made this QA study?", body: "Cristian Guerra · criguex · Colombian QA Automation professional from Medellín · 8+ years of experience (self-reported).", values: ["QA study", "Independent reproduction", "Human review"] },
    { at: 64, scene: "campaign", kind: "contribution", title: "A traceable testing contribution", body: "The contribution is making known failures, test sensitivity and limitations auditable.", values: ["Test strategy", "Mutations", "Validation"] },
    { at: 72, scene: "formal", kind: "ai", title: "AI assistance is disclosed", body: "AI tools assisted analysis and code preparation; they are not coauthors or co-discoverers.", values: ["Human-authored QA study", "AI-assisted preparation", "Disclosure included"] },
    { at: 78, scene: "formal", kind: "openai", title: "Credit for the original proofs", body: "The original proofs are credited to OpenAI. This study claims neither their authorship nor theorem discovery.", values: ["Original proofs · OpenAI", "New QA evidence", "No discovery claim"] },
    { at: 84, scene: "formal", kind: "scope", title: "Scope stays narrow", body: "Synthetic calculations, bounded kernel controls and historical campaigns are distinct evidence categories.", values: ["Synthetic models", "Formal controls", "Historical context"] },
  ],
  [
    { at: 0, scene: "rc", kind: "models", title: "Nine synthetic models", body: "Nine model names; some configurations share mathematical structure after rescaling.", values: modelNames },
    { at: 8, scene: "chemistry", kind: "notlab", title: "Synthetic examples—not experiments", body: "This model list evaluates the QA instrument; it does not represent nine independent physical regimes.", values: ["Synthetic calculations", "No laboratory measurements", "QA sensitivity"] },
    { at: 15, scene: "rc", kind: "circuit", title: "One concrete case: an RC circuit", body: "A one-kiloohm resistor and one-millifarad capacitor give τ = R × C = 1 second.", values: ["R = 1,000 Ω", "C = 0.001 F", "τ = 1 s"] },
    { at: 18, scene: "rc", kind: "circuit", title: "The observed quantity is voltage", body: "At three seconds, the fine-resolution recorded values differ after doubling τ.", values: [`Baseline ${rcBaseline.values["256"][3].toFixed(3)} V`, `Doubled τ ${rcMutation.values["256"][3].toFixed(3)} V`] },
    { at: 23, scene: "rc", kind: "notlab", title: "Calculated—not measured", body: "These values come from reproducible synthetic calculations, not laboratory instruments.", values: ["JSON observations", "Fixed units", "No experiment"] },
    { at: 30, scene: "chemistry", kind: "configurations", title: "Three configurations per model", body: "The fixed contract defines units and observation points; model counts do not imply independent regimes.", values: ["Configuration 1", "Configuration 2", "Configuration 3"] },
    { at: 36, scene: "rc", kind: "resolution", title: "Refine the RC integration", body: "The RC record uses 64, 128 and 256 integration steps over a three-second horizon.", values: ["64 steps", "128 steps", "256 steps"] },
    { at: 44, scene: "rc", kind: "circuit", title: "At 3 seconds: 4.751 vs 3.884 V", body: "The baseline and doubled-time-constant output are the recorded 256-step values.", values: [`Baseline ${rcBaseline.values["256"][3].toFixed(3)} V`, `Mutant ${rcMutation.values["256"][3].toFixed(3)} V`] },
    { at: 52, scene: "rc", kind: "equation", title: "Why the curve changes", body: "The circuit time constant is resistance multiplied by capacitance.", values: ["τ = R × C", "Mutation: τ × 2", "Horizon: 3 s"] },
    { at: 61, scene: "snell", kind: "oracles", title: "Different models, different oracles", body: "The suite avoids one shared oracle strategy for every model.", values: ["ODEs · closed form", "Snell · bisection", "Lens · ray tracing", "Acoustics · boundary system", "Fechner · numerical integral"] },
    { at: 73, scene: "chemistry", kind: "logistic", title: "Illustrative models stay labeled", body: "Logistic response is synthetic; Fechner is illustrative, not a universal law.", values: ["Normalized stimulus", "Response in [0, 1]", "Not human validation"] },
    { at: 81, scene: "campaign", kind: "rescaling", title: "Nine names are not nine regimes", body: "Some configurations share mathematical structure after rescaling.", values: ["Nine synthetic models", "Fixed configurations", "No independence claim"] },
    { at: 89, scene: "rc", kind: "notlab", title: "No experimental measurements", body: "The plots show model calculations and recorded numerical points only.", values: ["Synthetic", "Calculated", "Reproducible"] },
    { at: 94, scene: "rc", kind: "scope", title: "No real-world certification", body: "The suite evaluates detection of known changes in controlled examples.", values: ["Mutation sensitivity", "Not field performance", "Not certification"] },
  ],
  [
    { at: 0, scene: "formal", kind: "baseline-proof", title: "A minimal kernel fixture", body: "The target declaration states 0 = 0 and the exported proof value is rfl.", values: ["target : 0 = 0", "value := rfl"] },
    { at: 5, scene: "formal", kind: "mutated-proof", title: "Change only the proof value", body: "The mutation preserves the declared type but substitutes a proof of True.", values: ["Expected: 0 = 0", "Supplied: True.intro", "Only exported proof value changed"] },
    { at: 10, scene: "formal", kind: "proof-result", title: "Baseline accepted · mutation rejected", body: "Lean records a type mismatch. nanoda reaches a definitional-equality assertion; its classification is derived from pinned source.", values: ["Lean · baseline accepted", "Lean · type mismatch", "nanoda · source-derived rejection"] },
    { at: 18, scene: "formal", kind: "torus", title: "A separate periodic control", body: "Lean accepts a nonzero constant-velocity field on a periodic torus, with zero pressure and force and unit viscosity.", values: ["Periodic domain", "Constant velocity", "ν = 1"] },
    { at: 25, scene: "formal", kind: "scope", title: "Do not transfer the result to ℝ³", body: "A constant velocity field has infinite energy over all of Euclidean space.", values: ["Torus: periodic", "ℝ³: infinite energy", "Different scope"] },
    { at: 27, scene: "formal", kind: "proof-diagnostic", title: "The mismatch is local", body: "Lean reports that True does not match the expected equality type.", values: ["Expected Eq Nat 0 0", "Found True", "One declaration"] },
    { at: 34, scene: "formal", kind: "axioms", title: "Three reported axioms", body: "The periodic fixture's axiom report lists these names.", values: ["propext", "Classical.choice", "Quot.sound"] },
    { at: 41, scene: "formal", kind: "scope", title: "A bounded control, not a theorem audit", body: "The periodic example is intentionally separate from the minimal proof-value mutation.", values: ["Positive control", "Finite fixture", "No broad verification claim"] },
    { at: 47, scene: "formal", kind: "comparator", title: "Fresh Comparator recheck", body: "After the clean-source build, both configured challenges were accepted by both kernels.", values: ["Navier–Stokes · nanoda + Lean", "Euler · nanoda + Lean", "Recorded independent recheck"] },
    { at: 53, scene: "formal", kind: "comparator-runtime", title: "Long, recorded runs", body: "The saved logs show the configured comparison and successful command exits.", values: ["NS · 417.56 s", "Euler · 654.43 s", "Exit code 0"] },
    { at: 59, scene: "formal", kind: "calibration", title: "Harness calibration is separate", body: "Calibration used two positive fixtures accepted and four negative fixtures rejected before kernel calls.", values: ["2 positive accepted", "4 negative rejected", "Before kernel calls"] },
    { at: 62, scene: "formal", kind: "trace", title: "Inspect the preserved records", body: "The fixture, declarations and outputs remain linked for review.", values: ["Source", "Harness", "Sanitized logs"] },
  ],
  [
    { at: 0, scene: "campaign", kind: "hosts", title: "Two environments, one suite", body: "The same campaign ran on macOS arm64 and Linux x86_64.", values: ["macOS arm64", "Linux x86_64"] },
    { at: 4, scene: "campaign", kind: "campaign", title: "84 variants per host", body: "Counts below are per host; the variants are paired across hosts.", values: ["27 PASS", "54 KILLED", "3 SURVIVED"] },
    { at: 12, scene: "campaign", kind: "pairing", title: "84 paired records—not 168 cases", body: "Classifications and parameters match across the two host runs.", values: ["84 macOS", "84 Linux", "84 paired matches"] },
    { at: 19, scene: "campaign", kind: "survivor", title: "Survivors remain visible", body: "Tiny calibration mutations survived under the fixed threshold; they were not forced into rejection.", values: ["3 SURVIVED", "Reported", "Not equivalent by proof"] },
    { at: 22, scene: "campaign", kind: "paired-total", title: "The denominator matters", body: "The suite records counts per host and does not add a second platform as new variants.", values: ["84 / host", "2 paired hosts", "No 168-case claim"] },
    { at: 32, scene: "campaign", kind: "finite", title: "738 finite comparisons + 18 nulls", body: "The nulls come from the known chemical sign-reversal mutant's non-finite outputs.", values: ["738 finite", "18 non-finite", "18 represented as null"] },
    { at: 40, scene: "campaign", kind: "delta", title: "Cross-host difference: 1.11 × 10⁻¹⁶", body: "This is the largest scaled delta across finite paired values.", values: ["738 finite pairs", "Max scaled delta", "1.11 × 10⁻¹⁶"] },
    { at: 46, scene: "campaign", kind: "tolerance", title: "An explicit 10⁻⁶ error threshold", body: "Baselines are compared to an independent oracle using the fixed normalized tolerance.", values: ["Oracle", "Normalized error", "Tolerance 10⁻⁶"] },
    { at: 52, scene: "rc", kind: "resolution", title: "ODEs use applicable refinements", body: "Algebraic models receive no invented refinement levels.", values: ["ODE: refine where applicable", "Algebraic: no fabricated steps"] },
    { at: 57, scene: "campaign", kind: "convergence", title: "Observed order is diagnostic", body: "Across 15 ODE baselines, observed orders were near four; this is not a general error bound.", values: ["15 ODE baselines", "Observed order ≈ 4", "Diagnostic only"] },
    { at: 64, scene: "campaign", kind: "fine-errors", title: "Largest fine errors stayed below tolerance", body: "The largest fine ODE error was logistic; the Fechner result used a trapezoidal oracle.", values: ["Logistic · 1.12 × 10⁻⁹", "Fechner · 7.63 × 10⁻⁸", "Tolerance · 10⁻⁶"] },
    { at: 70, scene: "chemistry", kind: "fechner", title: "Fechner remains illustrative", body: "The logarithmic formula is compared with a trapezoidal numerical integral; this does not validate perception.", values: ["Trapezoidal oracle", "Finite computation", "Not human-subject data"] },
    { at: 76, scene: "rc", kind: "survivor", title: "A tiny RC mutation survived", body: "Survival under this contract does not establish mathematical equivalence.", values: ["Inside threshold", "SURVIVED", "No equivalence inference"] },
    { at: 80, scene: "campaign", kind: "scope", title: "Known changes, controlled examples", body: "The campaign tests detection and paired cross-platform consistency.", values: ["Synthetic QA", "Paired reruns", "No empirical validation"] },
    { at: 85, scene: "campaign", kind: "trace", title: "JSON stayed authoritative", body: "JSON and classifications were preserved when the CSV export was corrected.", values: ["Raw JSON", "Derived CSV", "Classification preserved"] },
  ],
  [
    { at: 0, scene: "campaign", kind: "trace", title: "A reviewable evidence path", body: "The package links source, records and reproducible checks; publication remains a separate review decision.", values: ["Source", "Evidence", "Reproduction"] },
    { at: 8, scene: "formal", kind: "chain", title: "Integrity, rows, paired correspondence", body: "Local checks confirmed artifact integrity, CSV row counts and cross-host correspondence.", values: ["SHA-256", "CSV rows", "Paired host records"] },
    { at: 17, scene: "campaign", kind: "reproduce", title: "Reproducing files is not repeating experiments", body: "A saved-evidence check verifies artifacts; the synthetic suite rerun is a distinct action.", values: ["Verify saved records", "Rerun synthetic suite", "Different from experiment"] },
    { at: 22, scene: "campaign", kind: "build", title: "Clean source build: 11,424 jobs", body: "Clean03 exited successfully and reused dependency and toolchain caches; it was not a full bootstrap.", values: ["PASS · exit 0", "11,424 jobs", "Cache reused"] },
    { at: 27, scene: "campaign", kind: "build", title: "A cached source build—not a bootstrap", body: "The successful source build reused cached dependencies and toolchain artifacts.", values: ["11,424 jobs", "Cache reused", "Bootstrap not claimed"] },
    { at: 36, scene: "formal", kind: "comparator", title: "Comparator rechecked both challenges", body: "The recorded recheck followed the clean-source build; both nanoda and Lean accepted each configured solution.", values: ["Navier–Stokes · accepted", "Euler · accepted", "Not theorem discovery"] },
    { at: 41, scene: "rc", kind: "historical", title: "Earlier ODE runs are separate context", body: "150 recorded runs in groups of 90, 30 and 30—not 150 independent cases.", values: ["90 + 30 + 30", "Earlier campaign", "Separate evidence"] },
    { at: 50, scene: "rc", kind: "ode-errors", title: "Historical maximum error falls with h", body: "The three step-size values come from a separate earlier ODE context.", values: ["h = 0.05 · 1.3023 × 10⁻⁵", "h = 0.025 · 7.24 × 10⁻⁷", "h = 0.0125 · 4.27 × 10⁻⁸"] },
    { at: 59, scene: "rc", kind: "convergence", title: "The finest historical step met the stated tolerance", body: "These historical ODE errors are context, separate from the current 84-variant campaign.", values: ["h = 0.0125", "Max error 4.27 × 10⁻⁸", "Fine tolerance 10⁻⁶"] },
    { at: 65, scene: "flow", kind: "flow", title: "Taylor–Green is visual context", body: "This actual cropped clip illustrates flow only. It is not a formal construction or evidence of blow-up.", video: true, videoStart: 0 },
    { at: 69, scene: "campaign", kind: "contribution", title: "What this QA work contributes", body: "Contracts, known mutations, paired environments and traceable evidence make the testing process auditable.", values: ["Fixed criteria", "Known failures", "Traceability"] },
    { at: 75, scene: "formal", kind: "author", title: "Authorship and AI disclosure", body: "Cristian Guerra receives credit for the QA study and independent reproduction. AI is disclosed as assistance.", values: ["Cristian Guerra · criguex", "QA Automation", "Medellín, Colombia"] },
    { at: 84, scene: "formal", kind: "openai", title: "Original proofs credited to OpenAI", body: "No new theorem, certification or validation of an open mathematical problem is claimed.", values: ["OpenAI · original proofs", "No discovery claim", "No certification claim"] },
    { at: 90, scene: "campaign", kind: "scope", title: "Review scope and limits", body: "We invite review of the evidence, assumptions and limitations before reuse.", values: ["Inspect", "Reproduce", "Challenge the scope"] },
  ],
];

const chapterScene: SceneId[] = ["rc", "rc", "formal", "campaign", "formal"];

const Shell: React.FC<{ vertical: boolean; children: React.ReactNode }> = ({ vertical, children }) => (
  <AbsoluteFill style={{ background: "radial-gradient(ellipse at 75% 10%, #173b4c 0%, #071b2b 58%)", color: colors.white, fontFamily: "Inter, Avenir Next, Arial, sans-serif", overflow: "hidden" }}>
    <div style={{ position: "absolute", inset: 0, opacity: 0.14, backgroundImage: "linear-gradient(#557080 1px, transparent 1px), linear-gradient(90deg, #557080 1px, transparent 1px)", backgroundSize: vertical ? "90px 90px" : "120px 120px", maskImage: "linear-gradient(to bottom, black, transparent 90%)" }} />
    {children}
  </AbsoluteFill>
);

const ModelGrid: React.FC<{ progress: number; vertical: boolean }> = ({ progress, vertical }) => (
  <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: vertical ? 9 : 12, marginTop: 22 }}>
    {modelNames.map((name, index) => {
      const opacity = interpolate(progress * modelNames.length - index, [0, 0.8], [0.18, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      return <div key={name} style={{ opacity, minHeight: vertical ? 74 : 84, padding: vertical ? 12 : 16, borderRadius: 14, background: index === 7 ? "#342f28" : "#102f43", border: `1px solid ${index === 7 ? colors.gold : "#315264"}`, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center", fontSize: vertical ? 19 : 22, fontWeight: 700 }}>{name}</div>;
    })}
  </div>
);

const Matrix: React.FC<{ vertical: boolean; progress: number }> = ({ vertical, progress }) => {
  const cells = Array.from({ length: 84 }, (_, index) => index < counts.PASS ? colors.mint : index < counts.PASS + counts.KILLED ? colors.coral : colors.gold);
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: vertical ? 16 : 24, marginTop: 28 }}>
      {["macOS arm64", "Linux x86_64"].map((host) => <div key={host} style={{ background: "#0b2434", border: "1px solid #315264", borderRadius: 20, padding: vertical ? 16 : 22 }}><div style={{ fontSize: vertical ? 20 : 26, color: colors.mint, fontWeight: 800 }}>{host} · 84</div><div style={{ display: "grid", gridTemplateColumns: "repeat(14,1fr)", gap: 4, marginTop: 14 }}>{cells.map((color, index) => <div key={index} style={{ opacity: interpolate(progress * 84 - index, [0, 1], [0.08, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }), height: vertical ? 13 : 17, borderRadius: 5, background: color }} />)}</div><div style={{ marginTop: 10, fontSize: vertical ? 17 : 21, lineHeight: 1.5 }}>27 PASS · 54 KILLED · 3 SURVIVED</div></div>)}
    </div>
  );
};

const TorusDiagram: React.FC<{ frame: number; vertical: boolean }> = ({ frame, vertical }) => {
  const rotation = frame * 1.4;
  return (
    <div style={{ display: "grid", gridTemplateColumns: vertical ? "1fr" : "1fr 1fr", alignItems: "center", gap: 24, marginTop: 20 }}>
      <svg viewBox="0 0 420 270" style={{ width: "100%", height: vertical ? 220 : 280 }} aria-label="Periodic torus schematic with constant velocity arrows">
        <ellipse cx="210" cy="134" rx="166" ry="72" fill="#0b2434" stroke={colors.mint} strokeWidth="4" />
        <ellipse cx="210" cy="134" rx="92" ry="72" fill="none" stroke="#315264" strokeWidth="3" />
        {[0, 1, 2, 3, 4, 5].map((i) => <g key={i} transform={`rotate(${rotation + i * 60} 210 134)`}><line x1="210" y1="134" x2="350" y2="134" stroke={i % 2 ? colors.gold : colors.mint} strokeWidth="5" /><path d="M350 134l-18 -10v20z" fill={i % 2 ? colors.gold : colors.mint} /></g>)}
        <text x="210" y="252" fill={colors.muted} fontSize="18" textAnchor="middle">Periodic domain · schematic</text>
      </svg>
      <div style={{ display: "grid", gap: 12 }}>{["Constant velocity", "Zero pressure and force", "Unit viscosity"].map((value, i) => <div key={value} style={{ padding: 16, background: "#102f43", borderLeft: `5px solid ${i === 1 ? colors.gold : colors.mint}`, borderRadius: 12, fontSize: vertical ? 22 : 28, fontWeight: 750 }}>{value}</div>)}</div>
    </div>
  );
};

const ODEBars: React.FC<{ vertical: boolean }> = ({ vertical }) => {
  const values = [{ h: "0.05", value: 1.3023e-5, label: "1.3023 × 10⁻⁵" }, { h: "0.025", value: 7.24e-7, label: "7.24 × 10⁻⁷" }, { h: "0.0125", value: 4.27e-8, label: "4.27 × 10⁻⁸" }];
  return <div style={{ display: "grid", gap: vertical ? 12 : 18, marginTop: 24 }}>{values.map((item, index) => <div key={item.h} style={{ display: "grid", gridTemplateColumns: vertical ? "150px 1fr" : "210px 1fr", alignItems: "center", gap: 16 }}><div style={{ fontSize: vertical ? 21 : 27, fontWeight: 700 }}>h = {item.h}</div><div><div style={{ height: vertical ? 32 : 42, width: `${Math.max(12, Math.sqrt(item.value / values[0].value) * 100)}%`, background: index === 0 ? colors.coral : index === 1 ? colors.gold : colors.mint, borderRadius: 9 }} /><div style={{ marginTop: 4, fontSize: vertical ? 20 : 25, fontWeight: 800 }}>{item.label}</div></div></div>)}</div>;
};

const PhaseGraphic: React.FC<{ beat: Beat; progress: number; frame: number; vertical: boolean }> = ({ beat, progress, frame, vertical }) => {
  if (beat.kind === "models") return <ModelGrid progress={progress} vertical={vertical} />;
  if (beat.kind === "campaign") return <Matrix vertical={vertical} progress={progress} />;
  if (beat.kind === "torus") return <TorusDiagram frame={frame} vertical={vertical} />;
  if (beat.kind === "ode-errors") return <ODEBars vertical={vertical} />;
  if (beat.kind === "comparator" || beat.kind === "comparator-runtime") {
    const values = beat.values ?? [];
    return <div style={{ display: "grid", gap: 12, marginTop: 24 }}>{values.map((value, index) => <div key={value} style={{ display: "grid", gridTemplateColumns: vertical ? "1fr" : "1fr auto", alignItems: "center", gap: 14, padding: 17, borderRadius: 14, background: "#102f43", border: "1px solid #315264", fontSize: vertical ? 22 : 27, fontWeight: 750 }}><span>{value}</span><span style={{ color: index < 2 ? colors.mint : colors.gold }}>{index < 2 ? "ACCEPTED" : "RECORDED"}</span></div>)}</div>;
  }
  if (beat.kind === "convergence") return <div style={{ display: "grid", gap: 14, marginTop: 26 }}>{(beat.values ?? []).map((value, index) => <div key={value} style={{ padding: 18, borderRadius: 15, background: "#102f43", borderLeft: `5px solid ${[colors.mint, colors.gold, colors.coral][index % 3]}`, fontSize: vertical ? 22 : 30, fontWeight: 800 }}>{value}</div>)}</div>;
  if (beat.kind === "resolution") {
    const items = beat.values ?? [];
    return <div style={{ display: "grid", gridTemplateColumns: `repeat(${items.length},1fr)`, gap: 12, marginTop: 28, alignItems: "end", minHeight: vertical ? 180 : 230 }}>{items.map((item, index) => <div key={item} style={{ height: `${45 + ((index + 1) / items.length) * 45}%`, borderRadius: "14px 14px 4px 4px", background: [colors.blue, colors.gold, colors.mint][index % 3], display: "flex", alignItems: "flex-end", justifyContent: "center", padding: 12, color: colors.navy, fontSize: vertical ? 17 : 21, fontWeight: 800, opacity: interpolate(progress * 3 - index, [0, 1], [0.25, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>{item}</div>)}</div>;
  }
  if (beat.kind === "axioms") return <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: 14, marginTop: 26 }}>{(beat.values ?? []).map((value, index) => <div key={value} style={{ padding: 20, borderRadius: 16, background: "#102f43", border: `1px solid ${[colors.mint, colors.gold, colors.coral][index]}`, fontFamily: "ui-monospace,Menlo,monospace", fontSize: vertical ? 24 : 34, fontWeight: 800, textAlign: "center" }}>{value}</div>)}</div>;
  if (beat.kind === "flow") return <div style={{ color: colors.gold, fontSize: vertical ? 19 : 24, fontWeight: 850, paddingTop: 22 }}>ILLUSTRATIVE FLOW · NOT CAMPAIGN EVIDENCE</div>;
  if (beat.kind === "baseline-proof" || beat.kind === "mutated-proof" || beat.kind === "proof-result" || beat.kind === "proof-diagnostic") {
    return <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, marginTop: 25 }}><div style={{ border: "1px solid #315264", background: "#0b2434", borderRadius: 18, padding: 22 }}><div style={{ color: colors.mint, fontSize: vertical ? 21 : 26, fontWeight: 800 }}>BASELINE</div><div style={{ marginTop: 16, fontFamily: "ui-monospace,Menlo,monospace", fontSize: vertical ? 27 : 38, fontWeight: 800 }}>0 = 0</div><div style={{ marginTop: 8, fontFamily: "ui-monospace,Menlo,monospace", fontSize: vertical ? 22 : 29 }}>rfl</div><div style={{ color: colors.mint, marginTop: 14, fontSize: vertical ? 19 : 23, fontWeight: 700 }}>accepted</div></div><div style={{ border: "1px solid #315264", background: "#0b2434", borderRadius: 18, padding: 22 }}><div style={{ color: colors.coral, fontSize: vertical ? 21 : 26, fontWeight: 800 }}>MUTATED VALUE</div><div style={{ marginTop: 16, fontFamily: "ui-monospace,Menlo,monospace", fontSize: vertical ? 25 : 34, fontWeight: 800 }}>True.intro</div><div style={{ color: colors.gold, marginTop: 14, fontSize: vertical ? 19 : 23, fontWeight: 700 }}>Type mismatch</div></div></div>;
  }
  if (beat.kind === "hosts") return <Matrix vertical={vertical} progress={progress} />;
  const values = beat.values ?? [];
  const metricSize = values.length < 3 ? (vertical ? 36 : 48) : (vertical ? 25 : 32);
  return (
    <div style={{ display: "grid", gridTemplateColumns: `repeat(${values.length >= 3 ? 2 : values.length || 1},minmax(0,1fr))`, gap: 16, marginTop: 24 }}>
      {values.map((value, index) => <div key={value} style={{ minHeight: vertical ? 88 : 110, padding: vertical ? 16 : 22, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center", borderRadius: 18, border: "1px solid #315264", borderTop: `5px solid ${[colors.mint, colors.gold, colors.coral][index % 3]}`, background: "linear-gradient(140deg,#123448,#0b2434)", fontSize: metricSize, fontWeight: 800, lineHeight: 1.12, opacity: interpolate(progress * 100 - index * 12, [0, 24], [0.35, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>{value}</div>)}
    </div>
  );
};

const StageArt: React.FC<{ beat: Beat; scene: SceneId; sceneTime: number; vertical: boolean; startFrame: number; duration: number; fps: number }> = ({ beat, scene, sceneTime, vertical, startFrame, duration, fps }) => (
  <div style={{ width: vertical ? 792 : 700, height: vertical ? 792 : 700, overflow: "hidden", border: "1px solid #315264", borderRadius: 22, background: colors.navy, position: "relative" }}>
    {beat.video ? (
      <Sequence from={startFrame} durationInFrames={duration} trimBefore={Math.round((beat.videoStart ?? 0) * fps)} premountFor={fps} style={{ position: "absolute", inset: 0 }}>
        <Video src={staticFile("english/media/flow-illustration.mp4")} muted premountFor={fps} objectFit="cover" style={{ position: "absolute", width: 1080, height: 1080, transform: vertical ? "scale(.7333)" : "scale(.6481)", transformOrigin: "top left", opacity: 0.82 }} />
      </Sequence>
    ) : (
      <div style={{ width: 1080, height: 1080, transform: vertical ? "scale(.7333)" : "scale(.6481)", transformOrigin: "top left" }}><CanvasScene sceneId={scene} timeOverrideSeconds={sceneTime} /></div>
    )}
    {beat.video && <div style={{ position: "absolute", left: 18, right: 18, bottom: 16, textAlign: "center", borderRadius: 12, padding: 10, background: "#071b2bd9", color: colors.gold, fontSize: vertical ? 16 : 20, fontWeight: 850 }}>ILLUSTRATIVE FLOW · NOT CAMPAIGN EVIDENCE OR PROOF</div>}
  </div>
);

const StoryVisual: React.FC<{ chapterIndex: number; vertical: boolean }> = ({ chapterIndex, vertical }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const second = frame / fps;
  const list = beats[chapterIndex];
  let beatIndex = 0;
  for (let index = 1; index < list.length; index += 1) if (second >= list[index].at) beatIndex = index;
  const beat = list[beatIndex];
  const elapsed = second - beat.at;
  const nextBeat = list[beatIndex + 1];
  const beatDuration = nextBeat ? nextBeat.at - beat.at : media.chapters[chapterIndex].duration_in_frames / fps - beat.at;
  const progress = interpolate(elapsed / Math.max(0.01, beatDuration), [0, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const sceneTime = Math.min(20, Math.max(0, elapsed));
  const canvasScene = beat.scene === "flow" ? chapterScene[chapterIndex] : beat.scene;
  const startFrame = Math.round(beat.at * fps);
  const duration = Math.max(1, Math.round(beatDuration * fps));
  const title = chapters[chapterIndex].en.title;

  return (
    <Shell vertical={vertical}>
      <div style={{ position: "absolute", top: vertical ? 58 : 48, left: vertical ? 54 : 90, right: vertical ? 54 : 90, display: "flex", justifyContent: "space-between", alignItems: "center", color: colors.mint, fontSize: vertical ? 20 : 22, letterSpacing: vertical ? 2 : 4, fontWeight: 800, textTransform: "uppercase" }}>
        <span>ADV-050 · {String(chapterIndex + 1).padStart(2, "0")} / 05</span><span>Cristian Guerra · QA Automation · Medellín, Colombia · @criguex</span>
      </div>
      {vertical ? (
        <>
          <div style={{ position: "absolute", top: 150, left: 54, right: 54, fontSize: 48, fontWeight: 850, lineHeight: 1.05 }}>{title}</div>
          <div style={{ position: "absolute", top: 280, left: 144 }}><StageArt beat={beat} scene={canvasScene} sceneTime={sceneTime} vertical startFrame={startFrame} duration={duration} fps={fps} /></div>
          <div style={{ position: "absolute", top: 1105, left: 54, right: 54, border: "1px solid #315264", borderRadius: 22, background: "linear-gradient(145deg,#15374a,#0d2638)", padding: 24 }}>
            <div style={{ color: colors.gold, fontSize: 18, fontWeight: 800, letterSpacing: 1.6 }}>{beat.kind.toUpperCase().replace(/-/g, " ")}</div>
            <div style={{ marginTop: 10, fontSize: 34, fontWeight: 850, lineHeight: 1.08 }}>{beat.title}</div>
            <div style={{ marginTop: 12, color: colors.muted, fontSize: 22, lineHeight: 1.28 }}>{beat.body}</div>
            <PhaseGraphic beat={beat} progress={progress} frame={frame} vertical />
          </div>
          <div style={{ position: "absolute", left: 54, right: 54, bottom: 280, height: 8, background: "#25485a", borderRadius: 6 }}><div style={{ width: `${progress * 100}%`, height: "100%", borderRadius: 6, background: colors.mint }} /></div>
        </>
      ) : (
        <>
          <div style={{ position: "absolute", top: 120, left: 90, right: 90, display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 32 }}><div style={{ fontSize: 32, fontWeight: 800 }}>{title}</div><div style={{ color: colors.muted, fontSize: 21 }}>Chapter time {second.toFixed(1)} s</div></div>
          <div style={{ position: "absolute", top: 210, left: 90 }}><StageArt beat={beat} scene={canvasScene} sceneTime={sceneTime} vertical={false} startFrame={startFrame} duration={duration} fps={fps} /></div>
          <div style={{ position: "absolute", top: 210, left: 830, right: 90, height: 700, border: "1px solid #315264", borderRadius: 22, background: "linear-gradient(145deg,#15374a,#0d2638)", padding: 36, overflow: "hidden" }}>
            <div style={{ color: colors.gold, fontSize: 20, fontWeight: 800, letterSpacing: 2 }}>{beat.kind.toUpperCase().replace(/-/g, " ")}</div>
            <div style={{ marginTop: 18, fontSize: 47, fontWeight: 850, lineHeight: 1.04 }}>{beat.title}</div>
            <div style={{ marginTop: 18, color: colors.muted, fontSize: 26, lineHeight: 1.3 }}>{beat.body}</div>
            <PhaseGraphic beat={beat} progress={progress} frame={frame} vertical={false} />
          </div>
          <div style={{ position: "absolute", left: 90, right: 90, bottom: 94, height: 8, background: "#25485a", borderRadius: 6 }}><div style={{ width: `${progress * 100}%`, height: "100%", borderRadius: 6, background: colors.mint }} /></div>
          <div style={{ position: "absolute", right: 90, bottom: 52, color: colors.muted, fontSize: 17 }}>Synthetic / bounded evidence · review scope only</div>
        </>
      )}
    </Shell>
  );
};

const CaptionOverlay: React.FC<{ chapterIndex: number; vertical: boolean }> = ({ chapterIndex, vertical }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentMs = frame * 1000 / fps;
  const caption = media.chapters[chapterIndex].captions.find((item) => currentMs >= item.startMs && currentMs < item.endMs);
  if (!caption) return null;
  return <div style={{ position: "absolute", zIndex: 20, left: vertical ? 66 : 120, right: vertical ? 66 : 120, bottom: vertical ? 164 : 38, display: "flex", justifyContent: "center" }}><div style={{ maxWidth: vertical ? 930 : 1650, textAlign: "center", border: "1px solid #55dfbd", borderRadius: 18, padding: vertical ? "20px 28px" : "16px 30px", background: "#061723ed", color: colors.white, fontSize: vertical ? 40 : 32, fontWeight: 700, lineHeight: 1.18 }}>{caption.text}</div></div>;
};

const ChapterSegment: React.FC<{ chapterIndex: number; vertical: boolean }> = ({ chapterIndex, vertical }) => {
  const chapter = media.chapters[chapterIndex];
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      <Audio src={staticFile(chapter.audio)} premountFor={fps} />
      <StoryVisual chapterIndex={chapterIndex} vertical={vertical} />
      <CaptionOverlay chapterIndex={chapterIndex} vertical={vertical} />
    </AbsoluteFill>
  );
};

export const LongVisualV2: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={media.chapters[0].duration_in_frames} premountFor={fps}><ChapterSegment chapterIndex={0} vertical={false} /></Sequence>
      <Sequence from={2643} durationInFrames={media.chapters[1].duration_in_frames} premountFor={fps}><ChapterSegment chapterIndex={1} vertical={false} /></Sequence>
      <Sequence from={5688} durationInFrames={media.chapters[2].duration_in_frames} premountFor={fps}><ChapterSegment chapterIndex={2} vertical={false} /></Sequence>
      <Sequence from={7790} durationInFrames={media.chapters[3].duration_in_frames} premountFor={fps}><ChapterSegment chapterIndex={3} vertical={false} /></Sequence>
      <Sequence from={10446} durationInFrames={media.chapters[4].duration_in_frames} premountFor={fps}><ChapterSegment chapterIndex={4} vertical={false} /></Sequence>
    </AbsoluteFill>
  );
};

export const ShortVisualV2: React.FC<{ chapterIndex: number }> = ({ chapterIndex }) => <ChapterSegment chapterIndex={chapterIndex} vertical />;
