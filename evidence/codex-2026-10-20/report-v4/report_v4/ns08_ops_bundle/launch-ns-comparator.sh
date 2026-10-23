set -euo pipefail
OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
REPO=<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler
RUNDIR="$OPS/results/comparator-ns-20261020-1901"
RUNNER="$OPS/ops/run-comparator-ns-20261020-1901.sh"
UNIT=ns08-comparator-ns-20261020-1901
COMPARATOR="$REPO/.lake/packages/Comparator/.lake/build/bin/comparator"
LEAN4EXPORT="$REPO/.lake/packages/lean4export/.lake/build/bin/lean4export"
NANODA="$OPS/tools/nanoda/target/release/nanoda_bin"
LANDRUN="$OPS/tools/landrun/landrun"
test -f "$RUNNER"
test "$(git -C "$REPO" rev-parse HEAD)" = f9e8bc5b38b6e212696e8a30e3e91517af887bbd
test -z "$(git -C "$REPO" status --porcelain=v1)"
test "$(git -C "$REPO/.lake/packages/Comparator" rev-parse HEAD)" = 19e111e2141cf333c7daff0f64c5f24acc91dd2e
test "$(git -C "$REPO/.lake/packages/lean4export" rev-parse HEAD)" = cacf989bd75f608700820f6afc595f32e7a99a4d
test "$(git -C "$OPS/tools/nanoda" rev-parse HEAD)" = 9d6964f78d0fa4c93fd22fe956e17afe7e72a441
test "$(git -C "$OPS/tools/landrun" rev-parse HEAD)" = ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a
python3 - "$REPO" <<'PY'
import json,pathlib,sys
r=pathlib.Path(sys.argv[1])
for name in ('NavierStokes.json','Euler.json'):
 d=json.loads((r/'ComparatorChallenges'/name).read_text())
 assert d.get('enable_nanoda') is True and d.get('permitted_axioms') == ['propext','Quot.sound','Classical.choice'], (name,d)
PY
printf 'prelaunch_utc=%s\n' "$(date -u +%FT%TZ)"
python3 -c 'import os; print("CapEff="+next(x.split()[1] for x in open("/proc/self/status") if x.startswith("CapEff:")))'
if test -e "$RUNDIR"; then echo "refusing existing run path $RUNDIR"; exit 95; fi
mkdir -m 700 "$RUNDIR"
cat > "$RUNDIR/command.txt" <<EOF
UTC run id: $UNIT
WorkingDirectory=$REPO
PATH=<WSL_HOME>/.elan/bin:/usr/bin:/bin
COMPARATOR_LANDRUN=$LANDRUN
COMPARATOR_LEAN4EXPORT=$LEAN4EXPORT
COMPARATOR_NANODA=$NANODA
/usr/bin/time -v -o $RUNDIR/time.log <WSL_HOME>/.elan/bin/lake env $COMPARATOR ComparatorChallenges/NavierStokes.json > $RUNDIR/stdout.log 2> $RUNDIR/stderr.log
EOF
cat > "$RUNDIR/unit-properties.txt" <<EOF
RestrictAddressFamilies=~AF_UNIX
SystemCallArchitectures=native
SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register
NoNewPrivileges=yes
SystemCallErrorNumber=EPERM
MemoryMax=28991029248
CPUQuota=800%
RuntimeMaxSec=8h
StandardInput=null
StandardOutput=append:$RUNDIR/unit-stdout.log
StandardError=append:$RUNDIR/unit-stderr.log
EOF
sha256sum "$COMPARATOR" "$LEAN4EXPORT" "$NANODA" "$LANDRUN" "$REPO/ComparatorChallenges/NavierStokes.json" "$REPO/ComparatorChallenges/Euler.json" > "$RUNDIR/inputs.sha256.txt"
date -u +%FT%TZ > "$RUNDIR/requested_start_utc.txt"
PROPS=(
  --property=RestrictAddressFamilies=~AF_UNIX
  --property=SystemCallArchitectures=native
  --property='SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register'
  --property=NoNewPrivileges=yes
  --property=SystemCallErrorNumber=EPERM
  --property=MemoryMax=28991029248
  --property=CPUQuota=800%
  --property=RuntimeMaxSec=8h
  --property=StandardInput=null
  --property="StandardOutput=append:$RUNDIR/unit-stdout.log"
  --property="StandardError=append:$RUNDIR/unit-stderr.log"
)
echo "unit=$UNIT"
echo "requested_start_utc=$(cat "$RUNDIR/requested_start_utc.txt")"
printf 'systemd-run --user --unit=%q --working-directory=%q ' "$UNIT" "$REPO"
printf '%q ' "${PROPS[@]}"
printf '%q ' -E PATH=<WSL_HOME>/.elan/bin:/usr/bin:/bin -E "COMPARATOR_LANDRUN=$LANDRUN" -E "COMPARATOR_LEAN4EXPORT=$LEAN4EXPORT" -E "COMPARATOR_NANODA=$NANODA"
printf '%q %q\n' /usr/bin/bash "$RUNNER"
systemd-run --user --unit="$UNIT" --working-directory="$REPO" "${PROPS[@]}" \
  -E PATH=<WSL_HOME>/.elan/bin:/usr/bin:/bin \
  -E "COMPARATOR_LANDRUN=$LANDRUN" \
  -E "COMPARATOR_LEAN4EXPORT=$LEAN4EXPORT" \
  -E "COMPARATOR_NANODA=$NANODA" \
  /usr/bin/bash "$RUNNER"
echo "systemd_run_launch_exit=$?"
