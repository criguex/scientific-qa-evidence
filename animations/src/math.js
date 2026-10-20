export function clamp(value, low, high) {
  return Math.max(low, Math.min(high, value));
}

export function smooth(value) {
  const x = clamp(value, 0, 1);
  return x * x * (3 - 2 * x);
}

export function mix(start, end, amount) {
  return start + (end - start) * clamp(amount, 0, 1);
}

export function rcVoltage(time, inputVoltage, initialVoltage, tau) {
  return inputVoltage + (initialVoltage - inputVoltage) * Math.exp(-time / tau);
}

export function secondOrderConcentration(time, initialConcentration, rate) {
  return initialConcentration / (1 + rate * initialConcentration * time);
}

export function coolingTemperature(time, ambient, initialTemperature, rate) {
  return ambient + (initialTemperature - ambient) * Math.exp(-rate * time);
}

export function snellAngle(incidence, n1, n2) {
  return Math.asin((n1 / n2) * Math.sin(incidence));
}

export function visiblePointCount(progress, total) {
  return Math.floor(clamp(progress, 0, 1) * total + 0.000001);
}
