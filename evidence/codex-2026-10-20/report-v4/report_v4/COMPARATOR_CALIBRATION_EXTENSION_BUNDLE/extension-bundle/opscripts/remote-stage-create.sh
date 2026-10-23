set -eu
ROOT=<WSL_HOME>/ns08_validation_20261020_a5YGak/calibration_20261020T2002Z_ns08extra_5r9k2m
date -u +%FT%TZ
test ! -e "$ROOT"
mkdir -m 700 "$ROOT"
printf 'CREATED_REMOTE_STAGE=%s\n' "$ROOT"
