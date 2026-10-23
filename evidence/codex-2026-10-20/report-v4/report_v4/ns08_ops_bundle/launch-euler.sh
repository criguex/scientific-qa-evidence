set -euo pipefail
OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
REPO=<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler
RUNDIR="$OPS/results/comparator-euler-20261020-1914"
UNIT=ns08-comparator-euler-20261020-1914
COMPARATOR="$REPO/.lake/packages/Comparator/.lake/build/bin/comparator"
LEAN4EXPORT="$REPO/.lake/packages/lean4export/.lake/build/bin/lean4export"
NANODA="$OPS/tools/nanoda/target/release/nanoda_bin"
LANDRUN="$OPS/tools/landrun/landrun"
test ! -e "$RUNDIR"
test "$(git -C "$REPO" rev-parse HEAD)" = f9e8bc5b38b6e212696e8a30e3e91517af887bbd
test -z "$(git -C "$REPO" status --porcelain=v1)"
test "$(git -C "$REPO/.lake/packages/Comparator" rev-parse HEAD)" = 19e111e2141cf333c7daff0f64c5f24acc91dd2e
test -z "$(git -C "$REPO/.lake/packages/Comparator" status --porcelain=v1)"
test "$(git -C "$REPO/.lake/packages/lean4export" rev-parse HEAD)" = cacf989bd75f608700820f6afc595f32e7a99a4d
test -z "$(git -C "$REPO/.lake/packages/lean4export" status --porcelain=v1)"
test "$(git -C "$OPS/tools/nanoda" rev-parse HEAD)" = 9d6964f78d0fa4c93fd22fe956e17afe7e72a441
test -z "$(git -C "$OPS/tools/nanoda" status --porcelain=v1)"
test "$(git -C "$OPS/tools/landrun" rev-parse HEAD)" = ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a
test -z "$(git -C "$OPS/tools/landrun" status --porcelain=v1)"
python3 - "$REPO" <<'PY'
import json,pathlib,sys
r=pathlib.Path(sys.argv[1])
for name in ('NavierStokes.json','Euler.json'):
 d=json.loads((r/'ComparatorChallenges'/name).read_text())
 assert d.get('enable_nanoda') is True and d.get('permitted_axioms') == ['propext','Quot.sound','Classical.choice'], (name,d)
PY
sha256sum "$COMPARATOR" "$LEAN4EXPORT" "$NANODA" "$LANDRUN" "$REPO/ComparatorChallenges/NavierStokes.json" "$REPO/ComparatorChallenges/Euler.json"
date -u +%FT%TZ
python3 -c 'print("CapEff="+next(x.split()[1] for x in open("/proc/self/status") if x.startswith("CapEff:")))'
mkdir -m 700 "$RUNDIR"
cat > "$RUNDIR/command.txt" <<EOF
run=Euler, sequential after NS attempt2 returned accepted solution and exit 0
UTC requested launch: $(date -u +%FT%TZ)
WorkingDirectory=$REPO
PATH=<WSL_HOME>/.elan/bin:/usr/bin:/bin
COMPARATOR_LANDRUN=$LANDRUN
COMPARATOR_LEAN4EXPORT=$LEAN4EXPORT
COMPARATOR_NANODA=$NANODA
/usr/bin/time -v -o $RUNDIR/time.log <WSL_HOME>/.elan/bin/lake env $COMPARATOR ComparatorChallenges/Euler.json > $RUNDIR/stdout.log 2> $RUNDIR/stderr.log
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
cat > "$RUNDIR/runner-payload.txt" <<'EOF'
set -eu
RUNDIR=<WSL_HOME>/ns08_validation_20261020_a5YGak/results/comparator-euler-20261020-1914
date -u +%FT%TZ > "$RUNDIR/start_utc.txt"
if python3 -c 'import os; p="/proc/"+str(os.getpid())+"/fd"; a=[]
for n in os.listdir(p):
 try:
  t=os.readlink(p+"/"+n)
  if t.startswith("socket:"): a.append((n,t))
 except OSError: pass
print("runner_socket_fds="+repr(a)); raise SystemExit(bool(a))' > "$RUNDIR/guard.log" 2>&1; then SOCKET_RC=0; else SOCKET_RC=$?; fi
CAP=$(awk '/^CapEff:/ {print $2}' /proc/self/status)
echo "runner_socket_inspection_exit=$SOCKET_RC CapEff=$CAP" >> "$RUNDIR/guard.log"
if test "$SOCKET_RC" != 0 || test "$CAP" != 0000000000000000; then
 echo "exit_code=91 pre-exec guard failure" > "$RUNDIR/status.txt"
 date -u +%FT%TZ > "$RUNDIR/end_utc.txt"
 exit 91
fi
set +e
/usr/bin/time -v -o "$RUNDIR/time.log" <WSL_HOME>/.elan/bin/lake env <WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler/.lake/packages/Comparator/.lake/build/bin/comparator ComparatorChallenges/Euler.json > "$RUNDIR/stdout.log" 2> "$RUNDIR/stderr.log"
RC=$?
set -e
date -u +%FT%TZ > "$RUNDIR/end_utc.txt"
printf 'exit_code=%s\n' "$RC" > "$RUNDIR/status.txt"
exit "$RC"
EOF
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
printf 'unit=%s requested_start_utc=%s\n' "$UNIT" "$(cat "$RUNDIR/requested_start_utc.txt")"
printf 'systemd-run --user --wait --unit=%q --working-directory=%q ' "$UNIT" "$REPO"
printf '%q ' "${PROPS[@]}"
printf '%q ' -E PATH=<WSL_HOME>/.elan/bin:/usr/bin:/bin -E "COMPARATOR_LANDRUN=$LANDRUN" -E "COMPARATOR_LEAN4EXPORT=$LEAN4EXPORT" -E "COMPARATOR_NANODA=$NANODA"
printf '%q %q %q\n' /usr/bin/bash -c "$(cat "$RUNDIR/runner-payload.txt")"
systemd-run --user --wait --unit="$UNIT" --working-directory="$REPO" "${PROPS[@]}" \
  -E PATH=<WSL_HOME>/.elan/bin:/usr/bin:/bin \
  -E "COMPARATOR_LANDRUN=$LANDRUN" \
  -E "COMPARATOR_LEAN4EXPORT=$LEAN4EXPORT" \
  -E "COMPARATOR_NANODA=$NANODA" \
  /usr/bin/bash -c "$(cat "$RUNDIR/runner-payload.txt")"
RC=$?
printf 'systemd_run_exit=%s\n' "$RC"
exit "$RC"
