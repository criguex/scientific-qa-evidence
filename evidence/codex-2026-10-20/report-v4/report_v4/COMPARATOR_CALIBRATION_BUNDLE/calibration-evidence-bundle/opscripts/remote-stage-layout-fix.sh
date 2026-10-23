set -eu
ROOT=<WSL_HOME>/ns08_validation_20261020_a5YGak/calibration_20261020T1953Z_ns08cal_9m2xq1
test ! -e "$ROOT/cases"
mkdir -m 700 "$ROOT/cases"
mv "$ROOT/positive" "$ROOT/mismatch" "$ROOT/axiom" "$ROOT/cases/"
printf 'LAYOUT_FIXED=%s/cases\n' "$ROOT"
