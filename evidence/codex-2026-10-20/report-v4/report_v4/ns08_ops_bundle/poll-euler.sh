set +e
UNIT=ns08-comparator-euler-20261020-1914
R=<WSL_HOME>/ns08_validation_20261020_a5YGak/results/comparator-euler-20261020-1914
date -u +%FT%TZ
systemctl --user show "$UNIT.service" -p ActiveState -p SubState -p Result -p ExecMainPID -p MemoryPeak -p CPUUsageNSec -p InvocationID
test -f "$R/guard.log" && cat "$R/guard.log"
test -f "$R/status.txt" && cat "$R/status.txt"
cat /proc/sys/kernel/random/boot_id
systemctl --user status "$UNIT.service" --no-pager -n 10
