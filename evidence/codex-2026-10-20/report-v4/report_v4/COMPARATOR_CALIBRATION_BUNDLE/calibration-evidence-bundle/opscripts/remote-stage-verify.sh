set -eu
ROOT=<WSL_HOME>/ns08_validation_20261020_a5YGak/calibration_20261020T1957Z_ns08cal_3p8kza
sha256sum "$ROOT/run-calibration-remote.sh"
test "$(sha256sum "$ROOT/run-calibration-remote.sh" | awk '{print $1}')" = f17f7a69cc7843a59bffc3434f21bab1b723942d2307099a2318d1f29c9f5cf1
sha256sum \
  "$ROOT/cases/positive/lean-toolchain" "$ROOT/cases/positive/lakefile.toml" "$ROOT/cases/positive/config.json" "$ROOT/cases/positive/Challenge.lean" "$ROOT/cases/positive/Solution.lean" \
  "$ROOT/cases/mismatch/lean-toolchain" "$ROOT/cases/mismatch/lakefile.toml" "$ROOT/cases/mismatch/config.json" "$ROOT/cases/mismatch/Challenge.lean" "$ROOT/cases/mismatch/Solution.lean" \
  "$ROOT/cases/axiom/lean-toolchain" "$ROOT/cases/axiom/lakefile.toml" "$ROOT/cases/axiom/config.json" "$ROOT/cases/axiom/Challenge.lean" "$ROOT/cases/axiom/Solution.lean"
test "$(sha256sum "$ROOT/cases/positive/Challenge.lean" | awk '{print $1}')" = 0d4a77ab995c3ebb09c58fb2a82db3eb48b5898907c65df29688694d07aba4d6
test "$(sha256sum "$ROOT/cases/positive/Solution.lean" | awk '{print $1}')" = 0d4a77ab995c3ebb09c58fb2a82db3eb48b5898907c65df29688694d07aba4d6
test "$(sha256sum "$ROOT/cases/mismatch/Solution.lean" | awk '{print $1}')" = 4420c80f4e3248c5e03ebf62e2add2d4d94b620726bcd2bf1e108e65707b98d4
test "$(sha256sum "$ROOT/cases/axiom/Challenge.lean" | awk '{print $1}')" = ad777397fec00027e82304d9b5261e1d75154822b50b4581b5c9e6e0c64f8cf7
test "$(sha256sum "$ROOT/cases/axiom/Solution.lean" | awk '{print $1}')" = d7fbcda73f36af87f525becd5bd8f814fa8ef3d0e1dfb62323f8260e7e30feec
test "$(sha256sum "$ROOT/cases/positive/config.json" | awk '{print $1}')" = 4fff5bf4ebcb5666c718d6a774b392fd6a43cad0c8c5e1ca6c51ea850db082bc
test "$(sha256sum "$ROOT/cases/mismatch/config.json" | awk '{print $1}')" = 4fff5bf4ebcb5666c718d6a774b392fd6a43cad0c8c5e1ca6c51ea850db082bc
test "$(sha256sum "$ROOT/cases/axiom/config.json" | awk '{print $1}')" = 4fff5bf4ebcb5666c718d6a774b392fd6a43cad0c8c5e1ca6c51ea850db082bc
test ! -e "$ROOT/results"
if find "$ROOT" -type d -name .lake -print -quit | grep -q .; then
  echo 'unexpected .lake directory in staging' >&2
  exit 91
fi
echo "REMOTE_STAGE_HASHES_OK=$ROOT"
