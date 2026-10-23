OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
UNIT=ns08-strict-correction-20261020-a5ygak
TESTSCRIPT="$OPS/ops/strict-correction-controls-20261020.sh"
OUT="$OPS/results/strict-correction-controls.log"
echo "UTC runner start: $(date -u +%FT%TZ)"
echo 'Runner inherited sockets:'
python3 -c 'import os; p="/proc/"+str(os.getppid())+"/fd"; a=[]
for n in os.listdir(p):
 try:
  t=os.readlink(p+"/"+n)
  if t.startswith("socket:"): a.append((n,t))
 except OSError: pass
print(repr(a)); raise SystemExit(bool(a))'
HOST_SOCKET_RC=$?
echo "runner_socket_inspection_exit=$HOST_SOCKET_RC"
test "$HOST_SOCKET_RC" = 0 || exit 50
PROPS=(
  --property=RestrictAddressFamilies=~AF_UNIX
  --property=SystemCallArchitectures=native
  --property='SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register'
  --property=NoNewPrivileges=yes
  --property=SystemCallErrorNumber=EPERM
  --property=MemoryMax=28991029248
  --property=CPUQuota=800%
  --property=RuntimeMaxSec=8h
)
echo 'Exact transient command properties:'
printf '%q ' "${PROPS[@]}"
printf '\n'
set +e
systemd-run --user --wait --pipe --collect --unit="$UNIT" "${PROPS[@]}" /usr/bin/bash "$TESTSCRIPT"
RUN_RC=$?
set -e
echo "systemd_run_exit=$RUN_RC"
echo 'Unit journal:'
journalctl --user -u "$UNIT" --no-pager -o short-iso-precise 2>&1
echo "UTC runner end: $(date -u +%FT%TZ)"
exit "$RUN_RC"
