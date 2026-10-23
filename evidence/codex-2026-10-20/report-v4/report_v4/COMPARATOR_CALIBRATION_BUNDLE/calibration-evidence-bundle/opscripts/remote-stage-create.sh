set -eu
ROOT=<WSL_HOME>/ns08_validation_20261020_a5YGak/calibration_20261020T1957Z_ns08cal_3p8kza
date -u +%FT%TZ
test ! -e "$ROOT"
mkdir -m 700 "$ROOT"
printf 'CREATED_REMOTE_STAGE=%s\n' "$ROOT"
