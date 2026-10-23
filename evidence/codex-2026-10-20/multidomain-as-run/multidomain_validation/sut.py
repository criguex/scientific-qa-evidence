import math


def _rk4(rhs, y0, end, steps):
    h = end / steps
    y = y0
    values = []
    targets = {round(steps * f): f for f in (0.25, 0.5, 0.75, 1.0)}
    for i in range(1, steps + 1):
        t = (i - 1) * h
        a = rhs(t, y)
        b = rhs(t + h / 2, y + h * a / 2)
        c = rhs(t + h / 2, y + h * b / 2)
        d = rhs(t + h, y + h * c)
        y += h * (a + 2 * b + 2 * c + d) / 6
        if i in targets:
            values.append(y)
    return values


def evaluate(case, variant, steps):
    m, p, end = case["model"], case["params"], case["horizon"]
    if m in {"rc", "cooling", "chemical_second_order", "beer_lambert", "logistic"}:
        if m == "rc":
            tau = p["r"] * p["c"] * (2 if variant == "tau_double" else 1 + 5e-8 if variant == "tau_tiny" else 1)
            sign = -1 if variant == "rhs_sign" else 1
            rhs = lambda t, y: sign * (p["vin"] - y) / tau
            y0 = p["v0"]
        elif m == "cooling":
            k = p["k"] * (0.5 if variant == "rate_half" else 1)
            rhs = lambda t, y: (1 if variant == "rhs_sign" else -1) * k * (y - p["ambient"])
            y0 = p["t0"]
        elif m == "chemical_second_order":
            k = p["k"] * (2 if variant == "rate_double" else 1)
            rhs = lambda t, y: (1 if variant == "rhs_sign" else -1) * k * y * y
            y0 = p["a0"]
        elif m == "beer_lambert":
            alpha = p["alpha"] * (0.5 if variant == "alpha_half" else 1)
            sign = 1 if variant == "exponent_sign" else -1
            rhs = lambda t, y: sign * alpha * y
            y0 = p["i0"]
        else:
            cap = p["capacity"] * (0.5 if variant == "capacity_half" else 1)
            sign = -1 if variant == "rhs_sign" else 1
            rhs = lambda t, y: sign * p["r"] * y * (1 - y / cap)
            y0 = p["p0"]
        return _rk4(rhs, y0, end, steps)
    fractions = (0.25, 0.5, 0.75, 1.0)
    if m == "snell":
        n1, n2 = (p["n2"], p["n1"]) if variant == "index_swap" else (p["n1"], p["n2"])
        theta = math.degrees(p["theta1"]) if variant == "degrees_as_radians" else p["theta1"]
        return [math.asin(max(-1, min(1, n1 * math.sin(theta * f) / n2))) for f in fractions]
    if m == "thin_lens":
        f, do = p["f"], p["do"]
        if variant == "power_sign":
            f = -f
        elif variant == "power_half":
            f *= 2
        di = 1 / (1 / f - 1 / do)
        return [-p["height"] * di / do * x for x in fractions]
    if m == "acoustic_interface":
        z1, z2 = p["z1"], p["z2"]
        if variant == "impedance_swap":
            z1, z2 = z2, z1
        pr = p["pi"] * ((z2 - z1) / (z1 + z2))
        if variant == "pressure_boundary_sign":
            pr = -pr
        pt = p["pi"] + pr
        return [v for _ in fractions for v in (pr, pt)]
    if m == "fechner":
        i0, i1, k = p["i0"], p["i1"], p["k"]
        if variant == "coefficient_double":
            k *= 2
        return [k * math.log((i0 + (i1-i0)*f) / (2*i0 if variant == "shifted_denominator" else i0)) for f in fractions]
    raise ValueError(m)
