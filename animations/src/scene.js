import { clamp, coolingTemperature, mix, rcVoltage, secondOrderConcentration, smooth, snellAngle, visiblePointCount } from "./math.js";

const C = { navy: "#071b2b", deep: "#0d2638", panel: "#123448", mint: "#55dfbd", white: "#f4f7f5", muted: "#abc0c8", coral: "#fb8176", gold: "#ffc56e", grid: "#214456", blue: "#70b9ff" };
const W = 1080;
const H = 1080;

function rounded(ctx, x, y, w, h, radius, fill, stroke) {
  ctx.beginPath();
  ctx.roundRect(x, y, w, h, radius);
  ctx.fillStyle = fill;
  ctx.fill();
  if (stroke) {
    ctx.strokeStyle = stroke;
    ctx.lineWidth = 2;
    ctx.stroke();
  }
}

function label(ctx, value, x, y, size, color = C.white, weight = 600, align = "left", family = "Inter, Avenir Next, Arial, sans-serif") {
  ctx.font = `${weight} ${size}px ${family}`;
  ctx.fillStyle = color;
  ctx.textAlign = align;
  ctx.textBaseline = "middle";
  ctx.fillText(String(value), x, y, 920);
}

function line(ctx, x1, y1, x2, y2, color, width = 3, dash = []) {
  ctx.beginPath();
  ctx.setLineDash(dash);
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.stroke();
  ctx.setLineDash([]);
}

function circle(ctx, x, y, radius, fill, stroke = null) {
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.fillStyle = fill;
  ctx.fill();
  if (stroke) {
    ctx.strokeStyle = stroke;
    ctx.lineWidth = 4;
    ctx.stroke();
  }
}

function base(ctx, title, eyebrow, t, color) {
  const background = ctx.createLinearGradient(0, 0, W, H);
  background.addColorStop(0, C.deep);
  background.addColorStop(0.55, C.navy);
  background.addColorStop(1, "#102d3b");
  ctx.fillStyle = background;
  ctx.fillRect(0, 0, W, H);
  ctx.save();
  ctx.globalAlpha = 0.18;
  for (let x = 26; x < W; x += 48) line(ctx, x, 0, x, H, C.grid, 1);
  for (let y = 24; y < H; y += 48) line(ctx, 0, y, W, y, C.grid, 1);
  ctx.restore();
  label(ctx, eyebrow.toUpperCase(), 66, 61, 19, color, 800);
  label(ctx, "Cristian Guerra · QA Automation · Medellín, Colombia · @criguex", 66, 94, 17, C.muted, 650);
  label(ctx, title, 66, 124, 48, C.white, 800);
  rounded(ctx, 66, 170, 948, 5, 3, "#2c4a59");
  rounded(ctx, 66, 170, 948 * clamp(t / 20, 0, 1), 5, 3, color);
  label(ctx, `CLIP ${Math.min(20, Math.max(0, t)).toFixed(1)} s`, 1010, 62, 18, C.muted, 700, "right");
}

function chartFrame(ctx, x, y, w, h, xLabel, yLabel, yMax, xMax) {
  rounded(ctx, x, y, w, h, 22, "#0b2434", "#315264");
  const left = x + 68;
  const right = x + w - 28;
  const top = y + 34;
  const bottom = y + h - 88;
  for (let i = 0; i <= 4; i += 1) {
    const py = mix(bottom, top, i / 4);
    line(ctx, left, py, right, py, "#274859", 1);
    label(ctx, (yMax * i / 4).toFixed(1), left - 13, py, 15, C.muted, 500, "right");
  }
  line(ctx, left, top, left, bottom, C.muted, 2);
  line(ctx, left, bottom, right, bottom, C.muted, 2);
  ctx.save();
  ctx.translate(x + 22, y + h / 2);
  ctx.rotate(-Math.PI / 2);
  label(ctx, yLabel, 0, 0, 16, C.muted, 700, "center");
  ctx.restore();
  for (let i = 0; i <= 4; i += 1) {
    const px = left + (i / 4) * (right - left);
    line(ctx, px, bottom, px, bottom + 6, C.muted, 2);
    label(ctx, (xMax * i / 4).toFixed(2), px, bottom + 21, 14, C.muted, 600, "center");
  }
  label(ctx, xLabel, (left + right) / 2, y + h - 27, 17, C.muted, 600, "center");
  return { left, right, top, bottom, plotWidth: right - left, plotHeight: bottom - top };
}

function plotCurve(ctx, frame, fn, domain, maxValue, color, progress, dash = []) {
  const end = clamp(progress, 0, 1);
  if (end <= 0) return;
  const points = Math.max(2, Math.floor(160 * end));
  ctx.beginPath();
  ctx.setLineDash(dash);
  for (let i = 0; i <= points; i += 1) {
    const ratio = i / 160;
    const x = frame.left + ratio * frame.plotWidth;
    const time = domain * ratio;
    const y = frame.bottom - (fn(time) / maxValue) * frame.plotHeight;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.strokeStyle = color;
  ctx.lineWidth = 6;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  ctx.stroke();
  ctx.setLineDash([]);
}

function drawRc(ctx, data, t) {
  const d = data.animations.rc;
  base(ctx, "One mutation. A measured difference.", "01 / Numerical evidence", t, C.mint);
  label(ctx, "C V′ = (Vᵢₙ − V) / R", 70, 220, 26, C.white, 700, "left", "ui-monospace, SFMono-Regular, Menlo, monospace");
  label(ctx, `R = ${d.parameters.r_ohm} Ω · C = ${d.parameters.c_f} F · τ = ${d.parameters.tau_s.toFixed(1)} s`, 70, 258, 19, C.muted);
  const frame = chartFrame(ctx, 66, 295, 620, 500, "time (s)", "volts", d.parameters.vin, d.horizon_s);
  const revealBase = smooth((t - 0.8) / 5.2);
  const revealMutant = smooth((t - 5.8) / 5.2);
  const curve = (tau) => (time) => rcVoltage(time, d.parameters.vin, d.parameters.v0, tau);
  plotCurve(ctx, frame, curve(d.parameters.tau_s), d.horizon_s, d.parameters.vin, C.mint, revealBase);
  plotCurve(ctx, frame, curve(d.mutation.tau_s), d.horizon_s, d.parameters.vin, C.coral, revealMutant);
  const modelTime = d.horizon_s * clamp((t - 0.8) / 15.2, 0, 1);
  const cursorX = frame.left + (modelTime / d.horizon_s) * frame.plotWidth;
  line(ctx, cursorX, frame.top, cursorX, frame.bottom, C.gold, 2, [7, 8]);
  const liveVoltage = rcVoltage(modelTime, d.parameters.vin, d.parameters.v0, d.parameters.tau_s);
  const liveY = frame.bottom - (liveVoltage / d.parameters.vin) * frame.plotHeight;
  circle(ctx, cursorX, liveY, 12, C.gold, C.navy);
  const times = d.sample_times_s;
  const baseValues = d.baseline.recorded_rk4_v;
  const mutantValues = d.mutation.recorded_rk4_v;
  const markerCount = visiblePointCount(smooth((t - 8) / 5), times.length);
  for (let i = 0; i < markerCount; i += 1) {
    const px = frame.left + (times[i] / d.horizon_s) * frame.plotWidth;
    const pyBase = frame.bottom - (baseValues[i] / d.parameters.vin) * frame.plotHeight;
    const pyMutant = frame.bottom - (mutantValues[i] / d.parameters.vin) * frame.plotHeight;
    circle(ctx, px, pyBase, 9, C.navy, C.mint);
    if (t > 9) circle(ctx, px, pyMutant, 8, C.navy, C.coral);
  }
  rounded(ctx, 716, 295, 298, 500, 22, "#0b2434", "#315264");
  label(ctx, "MODEL vs RECORDED", 744, 332, 16, C.muted, 800);
  line(ctx, 744, 370, 784, 370, C.mint, 5);
  label(ctx, "analytic oracle", 797, 370, 18, C.white);
  circle(ctx, 764, 410, 7, C.navy, C.mint);
  label(ctx, "RK4 checkpoints", 797, 410, 18, C.white);
  line(ctx, 744, 446, 784, 446, C.coral, 5);
  label(ctx, "doubled-τ mutation", 797, 446, 17, C.white);
  label(ctx, `Live model time ${modelTime.toFixed(2)} s`, 744, 480, 17, C.gold, 700);
  label(ctx, "Schematic charge · V / Vᵢₙ · not a fluid", 744, 514, 14, C.muted, 600);
  rounded(ctx, 744, 533, 248, 13, 7, "#274859");
  rounded(ctx, 744, 533, 248 * (liveVoltage / d.parameters.vin), 13, 7, C.mint);
  const endpointAlpha = smooth((t - 11) / 2.5);
  ctx.globalAlpha = endpointAlpha;
  rounded(ctx, 736, 568, 256, 62, 15, "#123448");
  label(ctx, `Baseline  ${d.baseline.recorded_rk4_v[3].toFixed(3)} V  ·  PASS`, 752, 599, 18, C.mint, 800);
  rounded(ctx, 736, 638, 256, 62, 15, "#3b2a32");
  label(ctx, `Doubled τ  ${d.mutation.recorded_rk4_v[3].toFixed(3)} V  ·  KILLED`, 752, 669, 16, C.coral, 800);
  ctx.globalAlpha = 1;
  const verdict = t > 15 ? smooth((t - 15) / 1.2) : 0;
  ctx.globalAlpha = verdict;
  rounded(ctx, 716, 720, 298, 56, 14, "#183d3c", "#55dfbd");
  label(ctx, `${d.baseline.status}  →  ${d.mutation.status}`, 865, 748, 22, C.mint, 800, "center");
  ctx.globalAlpha = 1;
  label(ctx, "Curve = analytic reconstruction · hollow markers = recorded RK4 values at four checkpoints", 70, 850, 18, C.muted, 600);
  label(ctx, "Synthetic circuit calculation · not a laboratory measurement", 70, 1005, 17, C.gold, 700);
}

function vessel(ctx, x, y, width, height, concentration, maximum, color, reveal, name, seconds) {
  label(ctx, name, x + width / 2, y - 44, 18, C.white, 700, "center");
  label(ctx, `${concentration.toFixed(3)} mol/L`, x + width / 2, y - 15, 18, color, 800, "center");
  ctx.save();
  ctx.beginPath();
  ctx.roundRect(x, y, width, height, [18, 18, 32, 32]);
  ctx.clip();
  ctx.fillStyle = "#112f42";
  ctx.fillRect(x, y, width, height);
  ctx.fillStyle = "#326078";
  ctx.fillRect(x, y + height * 0.22, width, height * 0.78);
  const dotCount = Math.max(0, Math.round(24 * concentration / maximum));
  for (let i = 0; i < dotCount; i += 1) {
    const col = i % 6;
    const row = Math.floor(i / 6);
    const drift = Math.sin(seconds * 1.4 + i * 1.73) * 7;
    const dx = x + 26 + col * ((width - 52) / 5) + drift;
    const dy = y + height - 38 - row * 28 + Math.cos(seconds * 1.1 + i) * 5;
    ctx.globalAlpha = reveal;
    circle(ctx, dx, dy, 8, color);
  }
  ctx.restore();
  ctx.globalAlpha = reveal;
  ctx.strokeStyle = color;
  ctx.lineWidth = 5;
  ctx.beginPath();
  ctx.roundRect(x, y, width, height, [18, 18, 32, 32]);
  ctx.stroke();
  ctx.globalAlpha = 1;
}

function drawChemistry(ctx, data, t) {
  const d = data.animations.chemistry;
  base(ctx, "Rate mutation changes concentration.", "02 / Numerical evidence", t, C.gold);
  label(ctx, "A′ = −k A²  ·  A(t) = A₀ / (1 + k A₀ t)", 70, 220, 25, C.white, 700, "left", "ui-monospace, SFMono-Regular, Menlo, monospace");
  label(ctx, `A₀ = ${d.parameters.a0_mol_l} mol/L · k = ${d.parameters.k_l_mol_s} L/(mol·s) · t = ${d.horizon_s.toFixed(2)} s`, 70, 258, 18, C.muted);
  rounded(ctx, 66, 298, 948, 365, 22, "#0b2434", "#315264");
  const modelTime = d.horizon_s * clamp((t - 1) / 16, 0, 1);
  const baselineAtTime = secondOrderConcentration(modelTime, d.parameters.a0_mol_l, d.parameters.k_l_mol_s);
  const mutationAtTime = secondOrderConcentration(modelTime, d.parameters.a0_mol_l, d.mutation.k_l_mol_s);
  const appearBase = smooth((t - 1) / 2.5);
  const appearMutant = smooth((t - 4.5) / 2.5);
  label(ctx, "SAME VESSEL VOLUME · SOLUTE MARKERS ARE SCHEMATIC", 90, 333, 15, C.muted, 800);
  label(ctx, `t = ${modelTime.toFixed(2)} s`, 986, 333, 16, C.gold, 700, "right");
  vessel(ctx, 300, 392, 180, 190, baselineAtTime, d.parameters.a0_mol_l, C.mint, appearBase, "Baseline · k", modelTime);
  vessel(ctx, 600, 392, 180, 190, mutationAtTime, d.parameters.a0_mol_l, C.coral, appearMutant, "Mutation · 2k", modelTime);
  const frame = chartFrame(ctx, 66, 690, 948, 280, "time (s)", "mol/L", d.parameters.a0_mol_l, d.horizon_s);
  const curveBase = (time) => secondOrderConcentration(time, d.parameters.a0_mol_l, d.parameters.k_l_mol_s);
  const curveMutant = (time) => secondOrderConcentration(time, d.parameters.a0_mol_l, d.mutation.k_l_mol_s);
  plotCurve(ctx, frame, curveBase, d.horizon_s, d.parameters.a0_mol_l, C.mint, smooth((t - 6) / 5));
  plotCurve(ctx, frame, curveMutant, d.horizon_s, d.parameters.a0_mol_l, C.coral, smooth((t - 9) / 5));
  const cursorX = frame.left + clamp(modelTime / d.horizon_s, 0, 1) * frame.plotWidth;
  line(ctx, cursorX, frame.top, cursorX, frame.bottom, C.gold, 2, [7, 8]);
  circle(ctx, cursorX, frame.bottom - (baselineAtTime / d.parameters.a0_mol_l) * frame.plotHeight, 10, C.gold, C.navy);
  const count = visiblePointCount(smooth((t - 12) / 2.5), d.sample_times_s.length);
  for (let i = 0; i < count; i += 1) {
    const px = frame.left + ((d.sample_times_s[i] / d.horizon_s)) * frame.plotWidth;
    const y0 = frame.bottom - (d.baseline.recorded_rk4_mol_l[i] / d.parameters.a0_mol_l) * frame.plotHeight;
    const y1 = frame.bottom - (d.mutation.recorded_rk4_mol_l[i] / d.parameters.a0_mol_l) * frame.plotHeight;
    circle(ctx, px, y0, 6, C.navy, C.mint);
    if (t > 12.5) circle(ctx, px, y1, 6, C.navy, C.coral);
  }
  label(ctx, "Analytic curves · hollow rings are recorded RK4 checkpoints", 70, 1004, 17, C.muted, 600);
  const verdict = smooth((t - 16.2) / 1.2);
  ctx.globalAlpha = verdict;
  rounded(ctx, 66, 610, 948, 44, 12, "#15384a", "#315264");
  label(ctx, `Horizon values · baseline ${d.baseline.recorded_rk4_mol_l[3].toFixed(3)} PASS  →  2× rate ${d.mutation.recorded_rk4_mol_l[3].toFixed(3)} KILLED`, 540, 632, 17, C.white, 750, "center");
  ctx.globalAlpha = 1;
}

function dotPosition(index, columns, x, y, size, gap) {
  return { x: x + (index % columns) * gap, y: y + Math.floor(index / columns) * gap };
}

function drawHost(ctx, x, y, host, revealed, counts, labelText) {
  rounded(ctx, x, y, 434, 548, 26, "#0b2434", "#315264");
  label(ctx, labelText, x + 28, y + 38, 22, C.white, 800);
  const px = x + 32;
  const py = y + 95;
  const categories = [
    { key: "PASS", count: counts.PASS, color: C.mint },
    { key: "KILLED", count: counts.KILLED, color: C.coral },
    { key: "SURVIVED", count: counts.SURVIVED, color: C.gold },
  ];
  let index = 0;
  for (const category of categories) {
    for (let j = 0; j < category.count; j += 1) {
      const point = dotPosition(index, 12, px, py, 7, 31);
      if (index < revealed) circle(ctx, point.x, point.y, 8, category.color);
      index += 1;
    }
  }
  categories.forEach((category, i) => {
    const yy = y + 468 + i * 26;
    circle(ctx, x + 46, yy, 7, category.color);
    label(ctx, `${category.key}  ${category.count}`, x + 68, yy, 16, C.muted, 700);
  });
  label(ctx, `${Math.min(revealed, host.variant_evaluations)} / ${host.variant_evaluations} variants`, x + 400, y + 38, 16, C.muted, 700, "right");
}

function drawCampaign(ctx, data, t) {
  const d = data.animations.campaign;
  base(ctx, "The same 84 variants on two hosts.", "03 / Paired campaign", t, C.coral);
  const revealA = visiblePointCount(smooth((t - 1.1) / 8.5), d.per_host.variant_evaluations);
  const revealB = visiblePointCount(smooth((t - 6.2) / 8.5), d.per_host.variant_evaluations);
  drawHost(ctx, 66, 258, d.per_host, revealA, d.per_host.classification_counts, "macOS arm64");
  drawHost(ctx, 580, 258, d.per_host, revealB, d.per_host.classification_counts, "Linux x86_64");
  const linkAlpha = smooth((t - 12) / 1.2);
  ctx.globalAlpha = linkAlpha;
  line(ctx, 494, 520, 586, 520, C.gold, 5, [8, 8]);
  circle(ctx, 540, 520, 13, C.gold);
  ctx.globalAlpha = 1;
  rounded(ctx, 66, 844, 948, 114, 22, "#123448", "#ffc56e");
  label(ctx, `${d.per_host.variant_evaluations} paired variants`, 102, 888, 31, C.white, 800);
  label(ctx, "84 per host · same variant set · not 168 distinct cases", 102, 928, 20, C.gold, 700);
  label(ctx, "Color shows classification only; reveal order is a visual sequence, not runtime performance.", 70, 1005, 17, C.muted, 600);
}

function proofCard(ctx, x, y, title, value, type, status, color, alpha) {
  ctx.globalAlpha = alpha;
  rounded(ctx, x, y, 438, 340, 24, "#0b2434", color);
  label(ctx, title, x + 30, y + 40, 21, color, 800);
  label(ctx, "target : 0 = 0", x + 30, y + 104, 22, C.white, 700, "left", "ui-monospace, SFMono-Regular, Menlo, monospace");
  line(ctx, x + 30, y + 145, x + 400, y + 145, "#315264", 2);
  label(ctx, "proof value", x + 30, y + 180, 17, C.muted, 600);
  label(ctx, value, x + 30, y + 222, 26, C.white, 750, "left", "ui-monospace, SFMono-Regular, Menlo, monospace");
  label(ctx, `value type: ${type}`, x + 30, y + 267, 17, color, 700, "left", "ui-monospace, SFMono-Regular, Menlo, monospace");
  rounded(ctx, x + 30, y + 292, 374, 34, 10, color);
  label(ctx, status, x + 217, y + 309, 15, C.navy, 900, "center");
  ctx.globalAlpha = 1;
}

function drawFormal(ctx, data, t) {
  const d = data.animations.formal;
  base(ctx, "Change the proof value—not the theorem.", "04 / Bounded formal control", t, C.blue);
  label(ctx, "One fixture · one incompatible value mutation", 70, 220, 20, C.muted, 600);
  const baselineAlpha = smooth((t - 0.8) / 2.2);
  const mutantAlpha = smooth((t - 6.5) / 2.8);
  proofCard(ctx, 66, 285, "BASELINE", "rfl", "0 = 0", "LEAN + NANODA ACCEPT", C.mint, baselineAlpha);
  proofCard(ctx, 576, 285, "MUTANT", "True.intro", "True", "TYPE MISMATCH", C.coral, mutantAlpha);
  const check = smooth((t - 10) / 2.2);
  ctx.globalAlpha = check;
  rounded(ctx, 66, 682, 948, 142, 22, "#152f40", "#315264");
  label(ctx, "Lean diagnostic", 96, 721, 18, C.muted, 800);
  label(ctx, "target has type True; expected 0 = 0", 96, 768, 24, C.coral, 800, "left", "ui-monospace, SFMono-Regular, Menlo, monospace");
  ctx.globalAlpha = 1;
  const derived = smooth((t - 13.2) / 1.5);
  ctx.globalAlpha = derived;
  rounded(ctx, 66, 858, 948, 116, 22, "#332d25", "#ffc56e");
  label(ctx, "nanoda emitted an internal typechecking assertion; rejection is derived from pinned source", 96, 904, 19, C.gold, 700);
  label(ctx, "The raw result remains pending classification · no fresh kernel run is implied", 96, 944, 17, C.muted, 600);
  ctx.globalAlpha = 1;
  label(ctx, `Recorded scope: ${d.record_count_each} exported records per fixture; only target.thm.value changed.`, 70, 1010, 16, C.muted, 600);
}

function drawThermometer(ctx, x, y, height, value, min, max, color, title) {
  label(ctx, title, x + 12, y - 28, 17, color, 700, "center");
  rounded(ctx, x, y, 24, height, 12, "#183849", "#abc0c8");
  const ratio = clamp((value - min) / (max - min), 0, 1);
  rounded(ctx, x + 6, y + height * (1 - ratio) + 6, 12, Math.max(8, height * ratio - 12), 6, color);
  circle(ctx, x + 12, y + height + 10, 23, color);
  label(ctx, `${value.toFixed(1)}°`, x + 12, y + height + 49, 17, C.white, 700, "center");
}

function drawCooling(ctx, data, t) {
  const d = data.animations.cooling;
  base(ctx, "A rate change slows the approach to ambient.", "05 / Numerical evidence", t, C.coral);
  label(ctx, "T′ = −k(T − Tₐ)  ·  T(t) = Tₐ + (T₀ − Tₐ)e⁻ᵏᵗ", 70, 220, 24, C.white, 700, "left", "ui-monospace, SFMono-Regular, Menlo, monospace");
  label(ctx, `T₀ = ${d.parameters.t0_c}°C · Tₐ = ${d.parameters.ambient_c}°C · k = ${d.parameters.k_per_s} s⁻¹ · horizon ${d.horizon_s} s`, 70, 258, 18, C.muted);
  const modelTime = d.horizon_s * clamp((t - 0.8) / 16.2, 0, 1);
  const baselineTemp = coolingTemperature(modelTime, d.parameters.ambient_c, d.parameters.t0_c, d.parameters.k_per_s);
  const mutationTemp = coolingTemperature(modelTime, d.parameters.ambient_c, d.parameters.t0_c, d.mutation.k_per_s);
  rounded(ctx, 66, 298, 350, 470, 24, "#0b2434", "#315264");
  label(ctx, `Ambient ${d.parameters.ambient_c}°C · model time ${modelTime.toFixed(2)} s`, 90, 336, 17, C.blue, 700);
  const glow = ctx.createRadialGradient(235, 465, 18, 235, 465, 188);
  const intensity = clamp((baselineTemp - d.parameters.ambient_c) / (d.parameters.t0_c - d.parameters.ambient_c), 0, 1);
  glow.addColorStop(0, `rgba(251,129,118,${0.5 * intensity})`);
  glow.addColorStop(1, "rgba(251,129,118,0)");
  ctx.fillStyle = glow;
  ctx.fillRect(72, 312, 338, 354);
  const blockSize = 108;
  const shift = Math.sin(t * 1.2) * 2;
  rounded(ctx, 182 + shift, 424, blockSize, blockSize, 20, `rgb(${Math.round(105 + 130 * intensity)},${Math.round(82 - 18 * intensity)},${Math.round(55 - 9 * intensity)})`, C.coral);
  label(ctx, `${baselineTemp.toFixed(1)}°C`, 236 + shift, 478, 22, C.white, 800, "center");
  drawThermometer(ctx, 130, 620, 65, baselineTemp, d.parameters.ambient_c, d.parameters.t0_c, C.mint, "BASELINE");
  drawThermometer(ctx, 270, 620, 65, mutationTemp, d.parameters.ambient_c, d.parameters.t0_c, C.coral, "½-RATE");
  const chart = chartFrame(ctx, 442, 298, 572, 470, "time (s)", "temperature °C", d.parameters.t0_c, d.horizon_s);
  plotCurve(ctx, chart, (time) => coolingTemperature(time, d.parameters.ambient_c, d.parameters.t0_c, d.parameters.k_per_s), d.horizon_s, d.parameters.t0_c, C.mint, smooth((t - 1) / 14));
  plotCurve(ctx, chart, (time) => coolingTemperature(time, d.parameters.ambient_c, d.parameters.t0_c, d.mutation.k_per_s), d.horizon_s, d.parameters.t0_c, C.coral, smooth((t - 4.5) / 12));
  const cursorX = chart.left + (modelTime / d.horizon_s) * chart.plotWidth;
  line(ctx, cursorX, chart.top, cursorX, chart.bottom, C.gold, 2, [7, 8]);
  circle(ctx, cursorX, chart.bottom - (baselineTemp / d.parameters.t0_c) * chart.plotHeight, 10, C.gold, C.navy);
  const count = visiblePointCount(smooth((t - 11) / 3), d.sample_times_s.length);
  for (let i = 0; i < count; i += 1) {
    const px = chart.left + (d.sample_times_s[i] / d.horizon_s) * chart.plotWidth;
    circle(ctx, px, chart.bottom - (d.baseline.recorded_rk4_c[i] / d.parameters.t0_c) * chart.plotHeight, 7, C.navy, C.mint);
    if (t > 12) circle(ctx, px, chart.bottom - (d.mutation.recorded_rk4_c[i] / d.parameters.t0_c) * chart.plotHeight, 7, C.navy, C.coral);
  }
  const alpha = smooth((t - 16) / 1.2);
  ctx.globalAlpha = alpha;
  rounded(ctx, 66, 820, 948, 130, 22, "#122f42", "#315264");
  label(ctx, `Recorded at 15 s: ${d.baseline.recorded_rk4_c[3].toFixed(2)}°C baseline  →  ${d.mutation.recorded_rk4_c[3].toFixed(2)}°C mutant`, 96, 864, 21, C.white, 800);
  label(ctx, `Mutation invariants: ${d.mutation.invariants} · normalized oracle error ${d.mutation.normalized_error.toFixed(3)} > tolerance ${d.tolerance}`, 96, 912, 18, C.gold, 700);
  ctx.globalAlpha = 1;
  label(ctx, "Lumped synthetic cooling model · not an experiment or material measurement", 70, 1008, 16, C.muted, 600);
}

function drawAngleArc(ctx, x, y, radius, start, end, color, text, tx, ty) {
  ctx.beginPath();
  ctx.arc(x, y, radius, start, end);
  ctx.strokeStyle = color;
  ctx.lineWidth = 4;
  ctx.stroke();
  label(ctx, text, tx, ty, 18, color, 800, "center");
}

function drawSnell(ctx, data, t) {
  const d = data.animations.snell;
  base(ctx, "Swapping refractive indices bends the ray too far.", "06 / Numerical evidence", t, C.blue);
  label(ctx, "n₁ sin θ₁ = n₂ sin θ₂  ·  θ₂ = asin((n₁ / n₂) sin θ₁)", 70, 220, 23, C.white, 700, "left", "ui-monospace, SFMono-Regular, Menlo, monospace");
  label(ctx, `n₁ = ${d.parameters.n1.toFixed(1)} · n₂ = ${d.parameters.n2.toFixed(1)} · incidence sweep 0.10–${d.parameters.max_incidence_rad.toFixed(1)} rad`, 70, 258, 18, C.muted);
  const panelY = 294;
  const interfaceY = 548;
  rounded(ctx, 66, panelY, 948, 390, 24, "#0b2434", "#315264");
  ctx.fillStyle = "#16384a";
  ctx.fillRect(68, panelY + 2, 944, interfaceY - panelY - 2);
  ctx.fillStyle = "#102c3d";
  ctx.fillRect(68, interfaceY, 944, 134);
  line(ctx, 68, interfaceY, 1012, interfaceY, C.white, 4);
  const centerX = 540;
  line(ctx, centerX, panelY + 20, centerX, panelY + 220, C.muted, 3, [8, 8]);
  label(ctx, `n₂ = ${d.parameters.n2.toFixed(1)}`, 94, panelY + 36, 22, C.muted, 800);
  label(ctx, `n₁ = ${d.parameters.n1.toFixed(1)}`, 94, interfaceY + 66, 22, C.muted, 800);
  label(ctx, "normal", centerX + 18, panelY + 52, 15, C.muted, 700);
  label(ctx, "interface", 910, interfaceY - 18, 15, C.white, 700);
  const incidence = d.parameters.max_incidence_rad * clamp((t - 0.8) / 16.2, 0, 1);
  const baselineAngle = snellAngle(incidence, d.parameters.n1, d.parameters.n2);
  const mutantAngle = snellAngle(incidence, d.parameters.n2, d.parameters.n1);
  const rayLength = 235;
  const sourceX = centerX - rayLength * Math.sin(incidence);
  const sourceY = interfaceY + rayLength * Math.cos(incidence);
  line(ctx, sourceX, sourceY, centerX, interfaceY, C.gold, 8);
  circle(ctx, centerX, interfaceY, 10, C.white);
  line(ctx, centerX, interfaceY, centerX + rayLength * Math.sin(baselineAngle), interfaceY - rayLength * Math.cos(baselineAngle), C.mint, 8);
  const mutationAlpha = smooth((t - 7.5) / 2);
  ctx.globalAlpha = mutationAlpha;
  line(ctx, centerX, interfaceY, centerX + rayLength * Math.sin(mutantAngle), interfaceY - rayLength * Math.cos(mutantAngle), C.coral, 7, [12, 8]);
  ctx.globalAlpha = 1;
  drawAngleArc(ctx, centerX, interfaceY, 62, Math.PI / 2, Math.PI / 2 + incidence, C.gold, `θ₁ ${incidence.toFixed(2)} rad`, centerX - 98, interfaceY + 88);
  drawAngleArc(ctx, centerX, interfaceY, 66, -Math.PI / 2, -Math.PI / 2 + baselineAngle, C.mint, `θ₂ ${baselineAngle.toFixed(2)}`, centerX + 104, interfaceY - 85);
  if (t > 9) label(ctx, `index swap · ${mutantAngle.toFixed(2)} rad`, centerX + 190, interfaceY - 178, 16, C.coral, 800, "center");
  const chart = chartFrame(ctx, 66, 704, 948, 268, "incidence angle θ₁ (rad)", "refracted θ₂ (rad)", 0.7, d.parameters.max_incidence_rad);
  plotCurve(ctx, chart, (angle) => snellAngle(angle, d.parameters.n1, d.parameters.n2), d.parameters.max_incidence_rad, 0.7, C.mint, smooth((t - 1) / 13));
  plotCurve(ctx, chart, (angle) => snellAngle(angle, d.parameters.n2, d.parameters.n1), d.parameters.max_incidence_rad, 0.7, C.coral, smooth((t - 7) / 10), [9, 6]);
  const points = visiblePointCount(smooth((t - 12) / 3), d.sample_incidence_rad.length);
  for (let i = 0; i < points; i += 1) {
    const px = chart.left + (d.sample_incidence_rad[i] / d.parameters.max_incidence_rad) * chart.plotWidth;
    circle(ctx, px, chart.bottom - (d.baseline.recorded_refracted_rad[i] / 0.7) * chart.plotHeight, 7, C.navy, C.mint);
    if (t > 13) circle(ctx, px, chart.bottom - (d.mutation.recorded_refracted_rad[i] / 0.7) * chart.plotHeight, 7, C.navy, C.coral);
  }
  const alpha = smooth((t - 16) / 1.2);
  ctx.globalAlpha = alpha;
  rounded(ctx, 66, 986, 948, 50, 14, "#332d25", "#ffc56e");
  label(ctx, `Recorded endpoints: ${d.baseline.recorded_refracted_rad[3].toFixed(3)} rad → ${d.mutation.recorded_refracted_rad[3].toFixed(3)} rad · mutation error ${d.mutation.normalized_error.toFixed(3)} > ${d.tolerance}`, 540, 1011, 16, C.gold, 750, "center");
  ctx.globalAlpha = 1;
  label(ctx, "Ray paths are analytic illustrations; hollow rings are recorded outputs. Angles are measured from the normal.", 70, 1058, 15, C.muted, 600);
}

export function drawAnimation(ctx, data, id, seconds) {
  const t = clamp(seconds, 0, 20);
  ctx.clearRect(0, 0, W, H);
  if (id === "rc") drawRc(ctx, data, t);
  else if (id === "chemistry") drawChemistry(ctx, data, t);
  else if (id === "campaign") drawCampaign(ctx, data, t);
  else if (id === "formal") drawFormal(ctx, data, t);
  else if (id === "cooling") drawCooling(ctx, data, t);
  else if (id === "snell") drawSnell(ctx, data, t);
  else throw new Error(`Unknown animation: ${id}`);
}
