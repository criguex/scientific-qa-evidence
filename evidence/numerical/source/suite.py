REFINEMENTS = (64, 128, 256)
OBSERVATION_FRACTIONS = (0.25, 0.5, 0.75, 1.0)
TOLERANCE = 1e-6


def _case(model, index, params, units, scale, horizon=None):
    return {"case_id": f"{model}_{index:02d}", "model": model, "params": params, "units": units, "scale": scale, "horizon": horizon}


CASES = [
    _case("rc", 1, {"vin": 5.0, "v0": 0.0, "r": 1000.0, "c": 0.001}, {"vin": "V", "v0": "V", "r": "ohm", "c": "F", "time": "s"}, 5.0, 3.0),
    _case("rc", 2, {"vin": 12.0, "v0": 2.0, "r": 2200.0, "c": 0.00047}, {"vin": "V", "v0": "V", "r": "ohm", "c": "F", "time": "s"}, 12.0, 3.0 * 2200.0 * 0.00047),
    _case("rc", 3, {"vin": 9.0, "v0": 1.0, "r": 4700.0, "c": 0.00022}, {"vin": "V", "v0": "V", "r": "ohm", "c": "F", "time": "s"}, 9.0, 3.0 * 4700.0 * 0.00022),
    _case("cooling", 1, {"t0": 90.0, "ambient": 20.0, "k": 0.2}, {"t0": "degC", "ambient": "degC", "k": "1/s", "time": "s"}, 70.0, 15.0),
    _case("cooling", 2, {"t0": 15.0, "ambient": 5.0, "k": 0.08}, {"t0": "degC", "ambient": "degC", "k": "1/s", "time": "s"}, 10.0, 37.5),
    _case("cooling", 3, {"t0": 75.0, "ambient": 10.0, "k": 0.4}, {"t0": "degC", "ambient": "degC", "k": "1/s", "time": "s"}, 65.0, 7.5),
    _case("chemical_second_order", 1, {"a0": 1.2, "k": 0.4}, {"a0": "mol/L", "k": "L/(mol s)", "time": "s"}, 1.2, 2.0 / (0.4 * 1.2)),
    _case("chemical_second_order", 2, {"a0": 0.7, "k": 1.3}, {"a0": "mol/L", "k": "L/(mol s)", "time": "s"}, 0.7, 2.0 / (1.3 * 0.7)),
    _case("chemical_second_order", 3, {"a0": 2.0, "k": 0.15}, {"a0": "mol/L", "k": "L/(mol s)", "time": "s"}, 2.0, 2.0 / (0.15 * 2.0)),
    _case("beer_lambert", 1, {"i0": 100.0, "alpha": 0.7, "length": 0.8}, {"i0": "W/m^2", "alpha": "1/m", "length": "m"}, 100.0, 0.8),
    _case("beer_lambert", 2, {"i0": 45.0, "alpha": 0.18, "length": 2.2}, {"i0": "W/m^2", "alpha": "1/m", "length": "m"}, 45.0, 2.2),
    _case("beer_lambert", 3, {"i0": 250.0, "alpha": 0.9, "length": 1.6}, {"i0": "W/m^2", "alpha": "1/m", "length": "m"}, 250.0, 1.6),
    _case("snell", 1, {"n1": 1.0, "n2": 1.5, "theta1": 0.4}, {"n1": "1", "n2": "1", "theta1": "rad", "theta2": "rad"}, 1.0),
    _case("snell", 2, {"n1": 1.33, "n2": 1.5, "theta1": 0.7}, {"n1": "1", "n2": "1", "theta1": "rad", "theta2": "rad"}, 1.0),
    _case("snell", 3, {"n1": 1.4, "n2": 1.6, "theta1": 0.6}, {"n1": "1", "n2": "1", "theta1": "rad", "theta2": "rad"}, 1.0),
    _case("thin_lens", 1, {"f": 0.05, "do": 0.15, "height": 0.01}, {"f": "m", "do": "m", "height": "m", "di": "m"}, 0.05),
    _case("thin_lens", 2, {"f": 0.1, "do": 0.3, "height": 0.02}, {"f": "m", "do": "m", "height": "m", "di": "m"}, 0.1),
    _case("thin_lens", 3, {"f": 0.25, "do": 0.75, "height": 0.04}, {"f": "m", "do": "m", "height": "m", "di": "m"}, 0.25),
    _case("acoustic_interface", 1, {"z1": 1.5e6, "z2": 3.0e6, "pi": 100.0}, {"z1": "Rayl", "z2": "Rayl", "pi": "Pa", "pr": "Pa", "pt": "Pa"}, 100.0),
    _case("acoustic_interface", 2, {"z1": 4.0e5, "z2": 1.5e6, "pi": 20.0}, {"z1": "Rayl", "z2": "Rayl", "pi": "Pa", "pr": "Pa", "pt": "Pa"}, 20.0),
    _case("acoustic_interface", 3, {"z1": 2.0e6, "z2": 1.0e6, "pi": 50.0}, {"z1": "Rayl", "z2": "Rayl", "pi": "Pa", "pr": "Pa", "pt": "Pa"}, 50.0),
    _case("fechner", 1, {"i0": 1e-12, "i1": 2.5e-12, "k": 1.0}, {"i0": "W/m^2", "i1": "W/m^2", "k": "subjective-unit", "s": "subjective-unit"}, 1.0),
    _case("fechner", 2, {"i0": 4e-12, "i1": 16e-12, "k": 2.0}, {"i0": "W/m^2", "i1": "W/m^2", "k": "subjective-unit", "s": "subjective-unit"}, 2.0),
    _case("fechner", 3, {"i0": 2e-11, "i1": 1e-10, "k": 0.5}, {"i0": "W/m^2", "i1": "W/m^2", "k": "subjective-unit", "s": "subjective-unit"}, 0.5),
    _case("logistic", 1, {"p0": 0.1, "capacity": 1.0, "r": 8.0}, {"p0": "probability", "capacity": "probability", "r": "1/normalized-stimulus", "stimulus": "normalized [0,1]"}, 1.0, 1.0),
    _case("logistic", 2, {"p0": 0.05, "capacity": 1.0, "r": 5.0}, {"p0": "probability", "capacity": "probability", "r": "1/normalized-stimulus", "stimulus": "normalized [0,1]"}, 1.0, 1.0),
    _case("logistic", 3, {"p0": 0.25, "capacity": 1.0, "r": 10.0}, {"p0": "probability", "capacity": "probability", "r": "1/normalized-stimulus", "stimulus": "normalized [0,1]"}, 1.0, 1.0),
]


MUTANTS = {
    "rc": ("rhs_sign", "tau_double"),
    "cooling": ("rhs_sign", "rate_half"),
    "chemical_second_order": ("rhs_sign", "rate_double"),
    "beer_lambert": ("exponent_sign", "alpha_half"),
    "snell": ("index_swap", "degrees_as_radians"),
    "thin_lens": ("power_half", "power_sign"),
    "acoustic_interface": ("pressure_boundary_sign", "impedance_swap"),
    "fechner": ("coefficient_double", "shifted_denominator"),
    "logistic": ("rhs_sign", "capacity_half"),
}
