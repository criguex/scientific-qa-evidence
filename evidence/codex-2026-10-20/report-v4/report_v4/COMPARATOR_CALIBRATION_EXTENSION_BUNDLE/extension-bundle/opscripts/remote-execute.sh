set -eu
ROOT=<WSL_HOME>/ns08_validation_20261020_a5YGak/calibration_20261020T2002Z_ns08extra_5r9k2m
cd "$ROOT"
exec /usr/bin/bash "$ROOT/run-calibration-remote.sh" --execute
