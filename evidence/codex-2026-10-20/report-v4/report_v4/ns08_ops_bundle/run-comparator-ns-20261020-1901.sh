set -u
OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
REPO=<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler
RUNDIR="$OPS/results/comparator-ns-20261020-1901"
if test ! -d "$RUNDIR" || test ! -f "$RUNDIR/command.txt"; then
  echo "run directory/command metadata missing: $RUNDIR"
  exit 90
fi
date -u +%FT%TZ > "$RUNDIR/start_utc.txt"
echo 'Runner socket descriptors:'
python3 -c 'import os; p="/proc/"+str(os.getpid())+"/fd"; a=[]
for n in os.listdir(p):
 try:
  t=os.readlink(p+"/"+n)
  if t.startswith("socket:"): a.append((n,t))
 except OSError: pass
print(repr(a)); raise SystemExit(bool(a))'
SOCKET_RC=$?
echo "runner_socket_inspection_exit=$SOCKET_RC"
CAP=$(awk '/^CapEff:/ {print $2}' /proc/self/status)
echo "CapEff=$CAP"
if test "$SOCKET_RC" != 0 || test "$CAP" != 0000000000000000; then
  echo "pre-exec guard failed: socket_exit=$SOCKET_RC CapEff=$CAP" > "$RUNDIR/status.txt"
  exit 91
fi
set +e
/usr/bin/time -v -o "$RUNDIR/time.log" \
  <WSL_HOME>/.elan/bin/lake env \
  "$REPO/.lake/packages/Comparator/.lake/build/bin/comparator" \
  ComparatorChallenges/NavierStokes.json \
  > "$RUNDIR/stdout.log" 2> "$RUNDIR/stderr.log"
RUN_RC=$?
set -e
date -u +%FT%TZ > "$RUNDIR/end_utc.txt"
printf 'exit_code=%s\n' "$RUN_RC" > "$RUNDIR/status.txt"
printf 'UTC start: '; cat "$RUNDIR/start_utc.txt"
printf 'UTC end: '; cat "$RUNDIR/end_utc.txt"
echo "comparator_exit=$RUN_RC"
echo "stdout=$RUNDIR/stdout.log"
echo "stderr=$RUNDIR/stderr.log"
echo "time=$RUNDIR/time.log"
exit "$RUN_RC"
