set -eu
ROOT=<WSL_HOME>/ns08_validation_20261020_a5YGak/calibration_20261020T2002Z_ns08extra_5r9k2m
sha256sum "$ROOT/run-calibration-remote.sh"
test "$(sha256sum "$ROOT/run-calibration-remote.sh" | awk '{print $1}')" = dad31e650b6aed7b80ce6844a399652ce07e86198a111990df8902d72f83ca39
test "$(sha256sum "$ROOT/SHA256SUMS" | awk '{print $1}')" = 888aa438d89b5d4c9cf53c940894bc19313569dbfb4a65d5b62786cdf965ff99
sha256sum \
  "$ROOT/cases/alpha/Challenge.lean" "$ROOT/cases/alpha/Solution.lean" "$ROOT/cases/alpha/config.json" "$ROOT/cases/alpha/lakefile.toml" "$ROOT/cases/alpha/lean-toolchain" \
  "$ROOT/cases/hidden_axiom/Challenge.lean" "$ROOT/cases/hidden_axiom/Solution.lean" "$ROOT/cases/hidden_axiom/config.json" "$ROOT/cases/hidden_axiom/lakefile.toml" "$ROOT/cases/hidden_axiom/lean-toolchain" \
  "$ROOT/cases/weakened_condition/Challenge.lean" "$ROOT/cases/weakened_condition/Solution.lean" "$ROOT/cases/weakened_condition/config.json" "$ROOT/cases/weakened_condition/lakefile.toml" "$ROOT/cases/weakened_condition/lean-toolchain"
test "$(sha256sum "$ROOT/cases/alpha/Challenge.lean" | awk '{print $1}')" = 5fe9c19b704c80e11ca9e7eabfc87bb79bb4febd804daa9e12d8376dd1015378
test "$(sha256sum "$ROOT/cases/alpha/Solution.lean" | awk '{print $1}')" = c031af40a580ebd3a2175e7a33a3895848d14f42e5e6b15dbece62a6df8dc0c3
test "$(sha256sum "$ROOT/cases/hidden_axiom/Solution.lean" | awk '{print $1}')" = 1f35b78a32fe876d8fb5bce06badbae98a2dd8a9f1047789f9e584598abddc6a
test "$(sha256sum "$ROOT/cases/weakened_condition/Challenge.lean" | awk '{print $1}')" = 7575be4c4e052916e34aa9c07360efe8f488bf02c65a1df9850db6e9f3e88ed5
test "$(sha256sum "$ROOT/cases/weakened_condition/Solution.lean" | awk '{print $1}')" = c4ad1a3264af21a197987e02c16b0b34fc2805314ef365f8e2b1d2156f947593
test ! -e "$ROOT/results"
if find "$ROOT" -type d -name .lake -print -quit | grep -q .; then
  echo "unexpected .lake directory in staging" >&2
  exit 91
fi
printf 'REMOTE_STAGE_HASHES_OK=%s\n' "$ROOT"
