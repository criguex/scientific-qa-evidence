set -eu
ROOT=<WSL_HOME>/ns08_validation_20261020_a5YGak/calibration_20261020T1957Z_ns08cal_3p8kza
cd "$ROOT"
exec /usr/bin/bash "$ROOT/run-calibration-remote.sh" --execute
