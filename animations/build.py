import hashlib
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANIMATIONS = Path(__file__).resolve().parent
INPUTS = {
    "rc_baseline": "evidence/numerical/fixtures/rc-baseline.json",
    "rc_mutation": "evidence/numerical/fixtures/rc-tau-double.json",
    "chemistry_baseline": "evidence/numerical/paired/macos-arm64/case_022.json",
    "chemistry_mutation": "evidence/numerical/paired/macos-arm64/case_024.json",
    "campaign": "evidence/numerical/multidomain_derived.json",
    "formal_derived": "evidence/formal/kernel-mutation/derived-classification.json",
    "formal_fixture": "evidence/formal/fixtures/KernelFixture.lean",
    "cooling_baseline": "evidence/numerical/paired/macos-arm64/case_013.json",
    "cooling_mutation": "evidence/numerical/paired/macos-arm64/case_015.json",
    "snell_baseline": "evidence/numerical/paired/macos-arm64/case_040.json",
    "snell_mutation": "evidence/numerical/paired/macos-arm64/case_041.json",
    "suite_contract": "evidence/numerical/source/suite.py",
    "cd_validation": "evidence/formal/cd-validation/results.json",
    "comparator_run1": "evidence/formal/comparator/README.md",
    "statement_provenance": "evidence/formal/statement-provenance/result.json",
    "clay_risk": "evidence/formal/clay-lean-risk.md",
}
PAGES = {
    "rc": ("RC circuit mutation", "The curve is reconstructed from the analytic model; hollow checkpoints are recorded RK4 outputs.", "Analytic equation curves; hollow ring markers are recorded 256-step RK4 results at four source fractions. The capacitor fill is normalized charge, not fluid."),
    "chemistry": ("Second-order chemistry", "Concentration changes while vessel volume stays fixed. Curves are analytic; ring markers are recorded RK4 checkpoints.", "Vessel volume remains fixed. Dot count encodes concentration schematically; analytic curves and recorded 256-step RK4 rings are distinct."),
    "cooling": ("Newton cooling rate mutation", "A lumped synthetic model approaches ambient temperature. The vessel is only a schematic; recorded checkpoints and analytic curves are labeled separately.", "A synthetic lumped cooling model, not a material experiment. Curves are analytic reconstructions; hollow rings are recorded 256-step RK4 values."),
    "snell": ("Snell refraction index swap", "Angles are measured from the normal. Rays are analytic illustrations; ring markers are the four recorded outputs, not literal photons.", "Analytic ray illustration sweeps incidence from 0.10 to 0.40 rad. Hollow markers are four recorded algebraic outputs, not photon trajectories."),
    "campaign": ("Paired 84-variant campaign", "Each host ran the same 84 variants. The two host runs are paired evidence, not 168 distinct variants.", "Dots encode recorded classification totals only. Reveal order is not timing or performance; both hosts ran the same 84 variants."),
    "formal": ("Proof-value typecheck control", "One proof-value mutation is rejected by Lean. nanoda's rejection category is derived from pinned source, not a structured binary result.", "One fixture changes only the exported proof value. Lean records a type mismatch; nanoda's raw status remains pending and rejection is source-derived. No fresh run is implied."),
    "rerun": ("Rebuild and recheck (C) and (D)", "OpenAI's Navier–Stokes and Euler proofs rebuilt from scratch and rechecked by Comparator three times.", "Comparator compiles the official challenge and OpenAI's solution separately, checks that the theorem statements match exactly and use only standard axioms, then has two independent kernels re-check every proof step."),
    "mutants": ("Statement mutants", "Each mutant changes one symbol in the official challenge statement while OpenAI's proof stays untouched. Comparator must refuse every one, and a comment-only control must still pass.", "Original line on top, mutated line below with the change highlighted. A refusal shows the statement check is exact; it does not mean the mutated statement is false, and the f = 0 cases say nothing about (A) or (B)."),
    "replay": ("Fresh kernel replay", "leanchecker --fresh ignores the compiled files and re-checks every declaration, Mathlib included, from an empty environment.", "Bars show the recorded replay time. The kernel panel shows which kernel implementations have actually examined the proofs; lean4lean could not be built for Lean 4.34 and never examined them."),
    "provenance": ("Where the statement comes from", "OpenAI's challenge statement compared with Google DeepMind's public Formal Conjectures statement, declaration by declaration.", "Identical declarations light up one by one; the remaining differences are listed below them. The last panel summarizes the clause-by-clause Clay ↔ Lean risk review, which is reading-based and not yet reviewed by a mathematician."),
}
AUTHOR = "Cristian Guerra · QA Automation · Medellín, Colombia · @criguex"


def read_json(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_package():
    rc_base = read_json(INPUTS["rc_baseline"])
    rc_mutation = read_json(INPUTS["rc_mutation"])
    chem_base = read_json(INPUTS["chemistry_baseline"])
    chem_mutation = read_json(INPUTS["chemistry_mutation"])
    campaign = read_json(INPUTS["campaign"])
    formal = read_json(INPUTS["formal_derived"])
    cooling_base = read_json(INPUTS["cooling_baseline"])
    cooling_mutation = read_json(INPUTS["cooling_mutation"])
    snell_base = read_json(INPUTS["snell_baseline"])
    snell_mutation = read_json(INPUTS["snell_mutation"])
    validation = read_json(INPUTS["cd_validation"])
    provenance = read_json(INPUTS["statement_provenance"])
    run1_text = (ROOT / INPUTS["comparator_run1"]).read_text(encoding="utf-8")
    risk_text = (ROOT / INPUTS["clay_risk"]).read_text(encoding="utf-8")
    suite_source = (ROOT / INPUTS["suite_contract"]).read_text(encoding="utf-8")
    tolerance_match = re.search(r"^TOLERANCE\s*=\s*([0-9.eE+-]+)", suite_source, flags=re.M)
    if not tolerance_match:
        raise ValueError("Numerical suite tolerance is not declared in suite.py")
    formal_text = (ROOT / INPUTS["formal_fixture"]).read_text(encoding="utf-8")
    host = campaign["per_host"]
    rc_tau = rc_base["params"]["r"] * rc_base["params"]["c"]
    chem_rate = chem_base["params"]["k"]
    return {
        "schema_version": 1,
        "fps": 24,
        "duration_seconds": 20,
        "width": 1080,
        "height": 1080,
        "source_hashes": {key: {"path": value, "sha256": sha256(ROOT / value)} for key, value in INPUTS.items()},
        "animations": {
            "rc": {
                "parameters": {
                    "vin": rc_base["params"]["vin"],
                    "v0": rc_base["params"]["v0"],
                    "r_ohm": rc_base["params"]["r"],
                    "c_f": rc_base["params"]["c"],
                    "tau_s": rc_tau,
                },
                "horizon_s": rc_base["horizon"],
                "sample_fractions": rc_base["observations"],
                "sample_times_s": [round(rc_base["horizon"] * value, 12) for value in rc_base["observations"]],
                "baseline": {"status": rc_base["status"], "recorded_rk4_v": rc_base["values"]["256"]},
                "mutation": {
                    "status": rc_mutation["status"],
                    "tau_s": rc_tau * 2,
                    "recorded_rk4_v": rc_mutation["values"]["256"],
                    "variant": rc_mutation["variant"],
                },
            },
            "chemistry": {
                "parameters": {"a0_mol_l": chem_base["params"]["a0"], "k_l_mol_s": chem_rate},
                "horizon_s": chem_base["horizon"],
                "sample_fractions": chem_base["observations"],
                "sample_times_s": [round(chem_base["horizon"] * value, 12) for value in chem_base["observations"]],
                "baseline": {"status": chem_base["status"], "recorded_rk4_mol_l": chem_base["values"]["256"]},
                "mutation": {
                    "status": chem_mutation["status"],
                    "k_l_mol_s": chem_rate * 2,
                    "recorded_rk4_mol_l": chem_mutation["values"]["256"],
                    "variant": chem_mutation["variant"],
                },
            },
            "campaign": {
                "per_host": {
                    "variant_evaluations": host["variant_evaluations"],
                    "classification_counts": host["classification_counts"],
                    "hosts": [entry["host_label"] for entry in campaign["campaigns"]],
                },
                "paired_variant_records": campaign["paired_host_comparison"]["classification_and_parameter_records_equal"],
            },
            "formal": {
                "record_count_each": formal["fixture"]["record_count_each"],
                "only_semantic_change": formal["fixture"]["only_semantic_change"],
                "lean_baseline": formal["results"][0]["baseline"],
                "lean_mutant": formal["results"][0]["mutant"],
                "lean_diagnostic": formal["results"][0]["mutant_diagnostic"],
                "nanoda_baseline": formal["results"][1]["baseline"],
                "nanoda_mutant_raw": "COLLECTED_PENDING_CLASSIFICATION",
                "nanoda_mutant_derived": formal["results"][1]["mutant"],
                "nanoda_basis": formal["results"][1]["classification_basis"],
                "fixture_text": formal_text,
            },
            "cooling": {
                "parameters": {"t0_c": cooling_base["params"]["t0"], "ambient_c": cooling_base["params"]["ambient"], "k_per_s": cooling_base["params"]["k"]},
                "horizon_s": cooling_base["horizon"],
                "sample_fractions": cooling_base["observations"],
                "sample_times_s": [round(cooling_base["horizon"] * value, 12) for value in cooling_base["observations"]],
                "baseline": {"status": cooling_base["status"], "recorded_rk4_c": cooling_base["values"]["256"], "normalized_error": cooling_base["normalized_error"]["256"]},
                "mutation": {
                    "status": cooling_mutation["status"],
                    "k_per_s": cooling_base["params"]["k"] / 2,
                    "recorded_rk4_c": cooling_mutation["values"]["256"],
                    "normalized_error": cooling_mutation["normalized_error"]["256"],
                    "invariants": cooling_mutation["invariants"]["256"],
                    "variant": cooling_mutation["variant"],
                },
                "tolerance": float(tolerance_match.group(1)),
            },
            "snell": {
                "parameters": {"n1": snell_base["params"]["n1"], "n2": snell_base["params"]["n2"], "max_incidence_rad": snell_base["params"]["theta1"]},
                "sample_fractions": snell_base["observations"],
                "sample_incidence_rad": [round(snell_base["params"]["theta1"] * value, 12) for value in snell_base["observations"]],
                "baseline": {"status": snell_base["status"], "recorded_refracted_rad": snell_base["values"]["N/A"], "normalized_error": snell_base["normalized_error"]["N/A"]},
                "mutation": {
                    "status": snell_mutation["status"],
                    "recorded_refracted_rad": snell_mutation["values"]["N/A"],
                    "normalized_error": snell_mutation["normalized_error"]["N/A"],
                    "invariants": snell_mutation["invariants"]["N/A"],
                    "variant": snell_mutation["variant"],
                },
                "tolerance": float(tolerance_match.group(1)),
            },
            "rerun": rerun_data(validation, run1_text),
            "mutants": mutant_data(validation),
            "replay": replay_data(validation),
            "provenance": provenance_data(provenance, risk_text),
        },
    }


def check(validation, check_id):
    return next(item for item in validation["checks"] if item["id"] == check_id)


def rerun_data(validation, run1_text):
    run1 = {name: float(re.search(rf"\| {name} \|.*?\| ([0-9.]+) s \|", run1_text).group(1)) for name in ("Navier–Stokes", "Euler")}
    fresh = check(validation, "clean_build")
    nocache = check(validation, "nocache_build")
    oleans = fresh.get("facts", {}).get("oleans", [])

    def run(label, ns_id, euler_id):
        return {"label": label, "runs": [{"verdict": check(validation, item)["verdict"], "elapsed_s": check(validation, item).get("elapsed_s")} for item in (ns_id, euler_id)]}

    return {
        "source_commit": validation["source_commit"][:7],
        "build": {
            "fresh_local": sum(int(o["total"]) for o in oleans if o["older_than_build_start"] == "0"),
            "fresh_prebuilt": sum(int(o["older_than_build_start"]) for o in oleans),
            "fresh_prebuilt_packages": sum(1 for o in oleans if o["older_than_build_start"] != "0"),
            "fresh_elapsed_s": fresh.get("elapsed_s"),
            "nocache_verdict": nocache["verdict"],
            "nocache_elapsed_s": nocache.get("elapsed_s"),
        },
        "rows": [
            {"label": "Run 1 · B1 · 2026-10-20 record", "runs": [{"verdict": "ACCEPTED", "elapsed_s": run1["Navier–Stokes"]}, {"verdict": "ACCEPTED", "elapsed_s": run1["Euler"]}]},
            run("Run 2 · B2 · Mathlib from prebuilt cache", "comparator2_NavierStokes", "comparator2_Euler"),
            run("Run 3 · B3 · Mathlib compiled here", "comparator3_clean_NavierStokes", "comparator3_clean_Euler"),
            run("Run 4 · B4 · --no-cache, all compiled here", "comparator4_nocache_NavierStokes", "comparator4_nocache_Euler"),
        ],
    }


def mutant_data(validation):
    items = []
    for item in validation["checks"]:
        if item["group"] != "mutant":
            continue
        diff = (ROOT / "evidence/formal/cd-validation" / item["diff"]).read_text(encoding="utf-8").splitlines()
        removed = [line[1:].strip() for line in diff if line.startswith("-") and not line.startswith("---")]
        added = [line[1:].strip() for line in diff if line.startswith("+") and not line.startswith("+++")]
        theorem = re.search(r"'([^']+)'", item.get("decision") or "")
        items.append({
            "title": item["title"],
            "theorem": theorem.group(1).split(".")[-1] if theorem else "end of challenge file",
            "before": removed[0] if removed else "",
            "after": added[0],
            "expected": item["expected"],
            "verdict": item["verdict"],
            "elapsed_s": item["elapsed_s"],
        })
    return {"items": items}


def replay_data(validation):
    replays = [item for item in validation["checks"] if item["group"] == "replay"]
    return {"checks": [{key: item.get(key) for key in ("id", "title", "verdict", "elapsed_s")} for item in replays]}


def provenance_data(provenance, risk_text):
    count = re.search(r"\*\*Count:\*\* (\d+) rows\. (\d+) direct, (\d+) equal by a standard fact, (\d+) needing attention", risk_text)
    removed = [line for line in provenance["only_in_reference"]]
    added = [line for line in provenance["only_in_candidate"]]
    return {
        "identical": provenance["identical_declarations"],
        "names": provenance["identical_names"],
        "removed": [line[:60] for line in removed],
        "added": [line[:60] for line in added],
        "risk": {"rows": int(count.group(1)), "direct": int(count.group(2)), "standard": int(count.group(3)), "attention": int(count.group(4))},
    }


def inline_renderer():
    math_source = (ANIMATIONS / "src" / "math.js").read_text(encoding="utf-8")
    scene_source = (ANIMATIONS / "src" / "scene.js").read_text(encoding="utf-8")
    math_source = re.sub(r"\bexport\s+(?=function\s)", "", math_source)
    scene_source = re.sub(r"^import\s+.*?;\s*$", "", scene_source, flags=re.M)
    scene_source = re.sub(r"\bexport\s+(?=function\s)", "", scene_source)
    return math_source.strip() + "\n\n" + scene_source.strip()


def page_html(animation_id, package):
    title, description, source_note = PAGES[animation_id]
    inline_data = json.dumps(package, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    renderer = inline_renderer()
    description_html = html.escape(description)
    title_html = html.escape(title)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark">
<title>ADV-050 · {title_html}</title>
<style>
:root{{color-scheme:dark;font:16px/1.5 Inter,"Avenir Next",Arial,sans-serif;background:#071b2b;color:#f4f7f5}}
*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 50% 0,#173b4c,#071b2b 58%);min-height:100vh}}
main{{max-width:1100px;margin:auto;padding:28px 22px 56px}}h1{{font-size:clamp(1.8rem,5vw,3.4rem);line-height:1.04;margin:.25em 0}}
.eyebrow{{color:#55dfbd;text-transform:uppercase;letter-spacing:.15em;font-weight:800;font-size:.78rem}}
.stage{{width:min(100%,860px);margin:24px auto 0;border:1px solid #315264;border-radius:20px;overflow:hidden;box-shadow:0 25px 80px #020b1280;background:#071b2b}}
canvas{{display:block;width:100%;height:auto;aspect-ratio:1;touch-action:none}}
.controls{{display:flex;align-items:center;gap:12px;max-width:860px;margin:14px auto;flex-wrap:wrap}}
button{{font:inherit;font-weight:750;color:#071b2b;background:#55dfbd;border:0;border-radius:10px;padding:11px 16px;cursor:pointer}}
button.secondary{{background:#173b4c;color:#f4f7f5;border:1px solid #315264}}button:focus-visible,input:focus-visible{{outline:3px solid #ffc56e;outline-offset:3px}}
input[type=range]{{flex:1;min-width:160px;accent-color:#55dfbd}}.time{{font-variant-numeric:tabular-nums;color:#abc0c8;min-width:92px;text-align:right}}
.note{{max-width:860px;margin:16px auto;color:#bfd0d5}}.data{{max-width:860px;margin:20px auto;padding:18px 20px;border:1px solid #315264;border-radius:14px;background:#0d2638}}
summary{{cursor:pointer;color:#55dfbd;font-weight:750}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;color:#abc0c8;font-size:.78rem}}
a{{color:#55dfbd}}@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}}}
</style>
</head>
<body>
<main>
<div class="eyebrow">ADV-050 · evidence animation · {animation_id}</div>
<p class="note"><strong>{html.escape(AUTHOR)}</strong></p>
<h1>{title_html}</h1>
<p class="note">{description_html}</p>
<div class="stage"><canvas id="scene" width="1080" height="1080" role="img" aria-label="Animated evidence diagram. Read the accompanying description and evidence data below."></canvas></div>
<div class="controls" aria-label="Animation controls">
<button id="toggle" type="button" aria-pressed="true">Pause</button>
<button id="replay" class="secondary" type="button">Replay</button>
<label for="scrub">Seek</label><input id="scrub" type="range" min="0" max="20" step="0.01" value="0" aria-label="Seek animation time">
<output class="time" id="time" for="scrub">0.0 / 20.0 s</output>
</div>
<p class="note"><strong>How to read this animation:</strong> {html.escape(source_note)}</p>
<details class="data"><summary>Accessible explanation, equations, and source records</summary><pre id="accessible"></pre></details>
<p class="note"><a href="./index.html">Open the evidence animation gallery</a> · <a href="{animation_id}.html" download>Download standalone HTML</a></p>
</main>
<script id="evidence-data" type="application/json">{inline_data}</script>
<script>
{renderer}
const PACKAGE=JSON.parse(document.getElementById("evidence-data").textContent);
const ID={json.dumps(animation_id)};const DURATION=20;const FPS=24;
const canvas=document.getElementById("scene");const context=canvas.getContext("2d",{{alpha:false}});
const seek=document.getElementById("scrub");const timeOutput=document.getElementById("time");const toggle=document.getElementById("toggle");
const reduced=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
let elapsed=0;let playing=!reduced;let previous=0;let raf=0;
function renderAt(seconds){{elapsed=clamp(seconds,0,DURATION);drawAnimation(context,PACKAGE,ID,elapsed);seek.value=String(elapsed);timeOutput.value=elapsed.toFixed(1)+" / 20.0 s";timeOutput.textContent=timeOutput.value;}}
function tick(now){{if(playing&&previous){{elapsed=Math.min(DURATION,elapsed+(now-previous)/1000);if(elapsed>=DURATION)playing=false;}}previous=now;renderAt(elapsed);toggle.textContent=playing?"Pause":"Play";toggle.setAttribute("aria-pressed",String(playing));raf=requestAnimationFrame(tick);}}
toggle.addEventListener("click",()=>{{playing=!playing;if(playing&&elapsed>=DURATION)elapsed=0;previous=0;}});
document.getElementById("replay").addEventListener("click",()=>{{elapsed=0;playing=true;previous=0;}});
seek.addEventListener("input",()=>{{elapsed=Number(seek.value);playing=false;previous=0;renderAt(elapsed);toggle.textContent="Play";toggle.setAttribute("aria-pressed","false");}});
document.getElementById("accessible").textContent=JSON.stringify({{animation:ID,data:PACKAGE.animations[ID],source_hashes:PACKAGE.source_hashes}},null,2);
window.renderAt=renderAt;renderAt(0);raf=requestAnimationFrame(tick);
</script>
</body>
</html>
'''


EXPECTED_VERDICTS = {"accept": {"ACCEPTED", "CONTROL_ACCEPTED"}, "reject": {"KILLED"}, "ok": {"OK"}}


def validation_summary(validation):
    done = [check for check in validation["checks"] if check["verdict"] != "PENDING"]
    inconclusive = [check for check in done if check["verdict"].startswith("FAILED_TOOLCHAIN")]
    unexpected = [check for check in done if check["verdict"] not in EXPECTED_VERDICTS[check["expected"]] and check not in inconclusive]
    killed = sum(check["verdict"] == "KILLED" for check in done)
    return f"{len(done)}/{len(validation['checks'])} checks recorded, {len(unexpected)} unexpected, {len(inconclusive)} not run because of a toolchain mismatch. {killed} statement mutants KILLED by Comparator. State: {validation['state'].replace('_', ' ')}."


def gallery_html(package):
    buttons = []
    for animation_id, (title, description, source_note) in PAGES.items():
        buttons.append(f'<button type="button" class="selector" data-id="{animation_id}" aria-pressed="false"><strong>{html.escape(title)}</strong><span>{html.escape(description)}</span></button>')
    rc = package["animations"]["rc"]
    chem = package["animations"]["chemistry"]
    campaign = package["animations"]["campaign"]
    cooling = package["animations"]["cooling"]
    snell = package["animations"]["snell"]
    rc_summary = f"R={rc['parameters']['r_ohm']:g} Ω; C={rc['parameters']['c_f']:g} F; τ={rc['parameters']['tau_s']:g} s. At 3 s: {rc['baseline']['recorded_rk4_v'][-1]:.3f} V baseline vs {rc['mutation']['recorded_rk4_v'][-1]:.3f} V with doubled τ."
    chem_summary = f"A₀={chem['parameters']['a0_mol_l']:g} mol/L; k={chem['parameters']['k_l_mol_s']:g} L/(mol·s). At the {chem['horizon_s']:.2f} s horizon: {chem['baseline']['recorded_rk4_mol_l'][-1]:.3f} vs {chem['mutation']['recorded_rk4_mol_l'][-1]:.3f} mol/L after doubling k."
    cooling_summary = f"T₀={cooling['parameters']['t0_c']:g}°C; ambient={cooling['parameters']['ambient_c']:g}°C. At {cooling['horizon_s']:g} s: {cooling['baseline']['recorded_rk4_c'][-1]:.2f}°C baseline vs {cooling['mutation']['recorded_rk4_c'][-1]:.2f}°C after halving k. Invariant {cooling['mutation']['invariants']} holds, but error {cooling['mutation']['normalized_error']:.3f} exceeds {cooling['tolerance']}."
    snell_summary = f"n₁={snell['parameters']['n1']:g}; n₂={snell['parameters']['n2']:g}. At θ₁={snell['parameters']['max_incidence_rad']:.1f} rad, recorded θ₂ is {snell['baseline']['recorded_refracted_rad'][-1]:.3f} rad baseline vs {snell['mutation']['recorded_refracted_rad'][-1]:.3f} rad for the index swap."
    counts = campaign["per_host"]["classification_counts"]
    manifest_text = json.dumps(package["source_hashes"], indent=2, ensure_ascii=False)
    facts = ''.join(f'<div class="fact"><strong>{title}</strong>{html.escape(text)}</div>' for title, text in [
        ("RC circuit", rc_summary),
        ("Second-order chemistry", chem_summary + " Liquid volume stays fixed."),
        ("Newton cooling", cooling_summary),
        ("Snell refraction", snell_summary + " Angles are measured from the normal."),
        ("C/D revalidation", validation_summary(read_json(INPUTS["cd_validation"]))),
        ("Paired campaign", f"{campaign['per_host']['variant_evaluations']} per host: {counts['PASS']} PASS · {counts['KILLED']} KILLED · {counts['SURVIVED']} SURVIVED. Same variants on both hosts, not 168 distinct cases."),
    ])
    source_text = html.escape(manifest_text)
    page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>ADV-050 · Animated evidence</title>
<style>
:root{color-scheme:dark;font:16px/1.55 Inter,"Avenir Next",Arial,sans-serif;background:#071b2b;color:#f4f7f5}*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 78% 0,#173b4c,#071b2b 55%)}main{max-width:1180px;margin:auto;padding:42px 24px 88px}h1{font-size:clamp(2.4rem,6vw,4.6rem);line-height:1.02;margin:.25em 0}h2{color:#55dfbd;font-size:1.6rem;margin:0 0 10px}p{color:#bfd0d5}a{color:#55dfbd}.eyebrow{color:#55dfbd;text-transform:uppercase;letter-spacing:.17em;font-weight:800;font-size:.8rem}.lead,.context,.sources{border:1px solid #315264;border-radius:20px;background:#0d2638;padding:22px;margin:20px 0}.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}.fact{padding:16px;border-radius:14px;background:#102f43;border-left:4px solid #55dfbd}.fact strong{display:block;color:#f4f7f5;margin-bottom:8px}.fact:nth-child(2n){border-color:#ffc56e}.selectors{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:20px 0}.selector{text-align:left;display:flex;flex-direction:column;gap:6px;min-height:104px;padding:16px;border:1px solid #315264;border-radius:14px;background:#102f43;color:#f4f7f5;cursor:pointer;font:inherit}.selector strong{font-size:1rem}.selector span{color:#abc0c8;font-size:.87rem}.selector[aria-pressed=true]{border-color:#55dfbd;box-shadow:0 0 0 2px #55dfbd55}.selector:focus-visible,a:focus-visible{outline:3px solid #ffc56e;outline-offset:3px}.active{border:1px solid #315264;border-radius:20px;background:#0d2638;padding:18px}.active-head{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;flex-wrap:wrap}.actions{display:flex;gap:12px;flex-wrap:wrap}iframe{display:block;width:100%;aspect-ratio:1;border:1px solid #315264;border-radius:14px;background:#071b2b;margin-top:14px}.badge{display:inline-block;border:1px solid #ffc56e;color:#ffc56e;padding:4px 10px;border-radius:999px;font-size:.78rem;font-weight:800}.context img{display:block;width:min(100%,960px);border-radius:14px;background:#071b2b}summary{cursor:pointer;color:#55dfbd;font-weight:800}pre{white-space:pre-wrap;overflow-wrap:anywhere;color:#abc0c8;font-size:.82rem}code{color:#ffc56e}@media(max-width:600px){main{padding:28px 14px 64px}}
</style></head><body><main>
<div class="eyebrow">Evidence, in motion · local and offline</div><h1>What changed?<br>What did the checks see?</h1>
<section class="lead"><p><strong>__AUTHOR__</strong></p><p>Ten supporting animation scenes turn recorded evidence into comparisons. Choose a scene, play or scrub its embedded HTML, then download the standalone file. The standalone HTML embeds its data and renderer; it does not fetch remote code.</p><div class="facts">__FACTS__</div></section>
<nav class="selectors" aria-label="Choose an evidence animation">__BUTTONS__</nav>
<section class="active"><div class="active-head"><div><h2 id="active-title">RC circuit mutation</h2><p id="active-description"></p><p id="active-note"></p><p><strong>__AUTHOR__</strong></p></div><div class="actions"><a id="html-link" download>Download standalone HTML</a></div></div><iframe id="active-frame" title="Selected evidence animation" src="rc.html"></iframe></section>
<section class="context"><span class="badge">ILLUSTRATIVE CONTEXT · NOT CAMPAIGN DATA</span><h2 style="margin-top:14px">A separate 3D flow visualization</h2><p>This Taylor–Green visualization is only visual context. It is not the 84-variant campaign, evidence of blow-up, or a formal solution. No synthetic physics scene is generated here.</p><img src="../docs/assets/flow-preview.gif" alt="Illustrative Taylor–Green flow clip"></section>
<section class="sources"><details><summary>Input evidence and SHA-256 provenance</summary><pre>__SOURCES__</pre></details><p><a href="../index.html">Back to the English review package</a></p></section>
</main><script>
const scenes=__SCENES__;const buttons=[...document.querySelectorAll(".selector")];const frame=document.getElementById("active-frame");
function selectScene(id){const scene=scenes[id];if(!scene)return;frame.src=scene.id+".html";frame.title=scene.title+" animated evidence";document.getElementById("active-title").textContent=scene.title;document.getElementById("active-description").textContent=scene.description;document.getElementById("active-note").textContent=scene.note;document.getElementById("html-link").href=scene.id+".html";for(const button of buttons)button.setAttribute("aria-pressed",String(button.dataset.id===id));}
for(const button of buttons)button.addEventListener("click",()=>selectScene(button.dataset.id));selectScene("rc");
</script></body></html>'''
    scenes = {key: {"id": key, "title": value[0], "description": value[1], "note": value[2]} for key, value in PAGES.items()}
    return page.replace("__AUTHOR__", html.escape(AUTHOR)).replace("__FACTS__", facts).replace("__BUTTONS__", "".join(buttons)).replace("__SOURCES__", source_text).replace("__SCENES__", json.dumps(scenes, ensure_ascii=False).replace("<", "\\u003c"))


def generate(destination=ANIMATIONS):
    package = load_package()
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "manifest.json").write_text(json.dumps(package, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for animation_id in PAGES:
        (destination / f"{animation_id}.html").write_text(page_html(animation_id, package), encoding="utf-8")
    (destination / "index.html").write_text(gallery_html(package), encoding="utf-8")
    return package


if __name__ == "__main__":
    generate()
