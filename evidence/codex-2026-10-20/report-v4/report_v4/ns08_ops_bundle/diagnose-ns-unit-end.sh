UNIT=ns08-comparator-ns-20261020-1901.service
RUNDIR=<WSL_HOME>/ns08_validation_20261020_a5YGak/results/comparator-ns-20261020-1901
echo "UTC diagnosis: $(date -u +%FT%TZ)"
systemctl --user status "$UNIT" --no-pager -l || true
systemctl --user show "$UNIT" -p ActiveState -p SubState -p Result -p ExecMainCode -p ExecMainStatus -p ExecMainStartTimestamp -p ExecMainExitTimestamp -p MainPID -p ControlGroup -p MemoryPeak -p CPUUsageNSec -p StandardOutput -p StandardError || true
echo 'Journal:'
journalctl --user -u "$UNIT" --no-pager -o short-iso-precise -n 100 || true
echo 'Processes:'
ps -eo pid,ppid,stat,etime,rss,cmd | grep -E 'ns08-comparator-ns-20261020-1901|comparator|lean4export|lean4 --|/lake env' | grep -v grep || true
echo 'Run dir listing:'
find "$RUNDIR" -maxdepth 1 -type f -printf '%f %s bytes\n' | sort
for f in stdout.log stderr.log time.log status.txt start_utc.txt end_utc.txt unit-stdout.log unit-stderr.log; do
  if test -f "$RUNDIR/$f"; then echo "=== $f ==="; tail -c 8000 "$RUNDIR/$f"; echo; fi
done
