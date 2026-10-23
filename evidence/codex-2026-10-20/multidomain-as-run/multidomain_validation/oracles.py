import math


def _independent_rk(rhs, initial, duration, count):
    step = duration / count
    state = initial
    result = []
    checkpoint = {round(count * q) for q in (0.25, 0.5, 0.75, 1.0)}
    for j in range(count):
        now = j * step
        k1 = rhs(now, state)
        k2 = rhs(now + step / 2, state + step * k1 / 2)
        k3 = rhs(now + step / 2, state + step * k2 / 2)
        k4 = rhs(now + step, state + step * k3)
        state = state + step * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        if j + 1 in checkpoint:
            result.append(state)
    return result


def evaluate(case, steps):
    m, p, end = case["model"], case["params"], case["horizon"]
    if m == "rc":
        tau = p["r"] * p["c"]
        return [p["vin"] + (p["v0"] - p["vin"]) * math.exp(-end * q / tau) for q in (0.25, 0.5, 0.75, 1.0)]
    if m == "cooling":
        return [p["ambient"] + (p["t0"] - p["ambient"]) * math.exp(-p["k"] * end * q) for q in (0.25, 0.5, 0.75, 1.0)]
    if m == "chemical_second_order":
        return [p["a0"] / (1 + p["k"] * p["a0"] * end * q) for q in (0.25, 0.5, 0.75, 1.0)]
    if m == "beer_lambert":
        return [p["i0"] * math.exp(-p["alpha"] * end * q) for q in (0.25, 0.5, 0.75, 1.0)]
    if m == "logistic":
        ratio = (p["capacity"] - p["p0"]) / p["p0"]
        return [p["capacity"] / (1 + ratio * math.exp(-p["r"] * end * q)) for q in (0.25, 0.5, 0.75, 1.0)]
    if m == "snell":
        answers = []
        for q in (0.25, 0.5, 0.75, 1.0):
            target = p["n1"] * math.sin(p["theta1"] * q) / p["n2"]
            low, high = 0.0, math.pi / 2
            for _ in range(80):
                middle = (low + high) / 2
                if math.sin(middle) < target:
                    low = middle
                else:
                    high = middle
            answers.append((low + high) / 2)
        return answers
    if m == "thin_lens":
        answers = []
        for q in (0.25, 0.5, 0.75, 1.0):
            object_height = p["height"] * q
            parallel_ray_slope = -object_height / p["f"]
            center_ray_slope = -object_height / p["do"]
            image_distance = -object_height / (parallel_ray_slope - center_ray_slope)
            answers.append(center_ray_slope * image_distance)
        return answers
    if m == "acoustic_interface":
        a, b = 1.0, -1.0
        c, d = 1 / p["z1"], 1 / p["z2"]
        determinant = a * d - b * c
        reflected = (-p["pi"] * d - b * p["pi"] / p["z1"]) / determinant
        transmitted = (a * p["pi"] / p["z1"] - c * (-p["pi"])) / determinant
        return [value for _ in range(4) for value in (reflected, transmitted)]
    if m == "fechner":
        answers = []
        for fraction in (0.25, 0.5, 0.75, 1.0):
            upper = p["i0"] + (p["i1"] - p["i0"]) * fraction
            panels = 4096
            width = (upper - p["i0"]) / panels
            area = 0.0
            for n in range(panels):
                left = p["i0"] + n * width
                right = left + width
                area += width * (1 / left + 1 / right) / 2
            answers.append(p["k"] * area)
        return answers
    raise ValueError(m)
