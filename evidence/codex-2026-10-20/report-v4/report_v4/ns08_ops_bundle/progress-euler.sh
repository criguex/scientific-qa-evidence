set -eu
R=<WSL_HOME>/ns08_validation_20261020_a5YGak/results/comparator-euler-20261020-1914
date -u +%FT%TZ
for n in stdout.log stderr.log time.log status.txt end_utc.txt; do
 if test -f "$R/$n"; then
  printf '\n--- %s (%s bytes) ---\n' "$n" "$(wc -c < "$R/$n")"
  tail -n 12 "$R/$n"
 else printf '\n--- %s missing ---\n' "$n"; fi
done
systemctl --user show ns08-comparator-euler-20261020-1914.service -p ActiveState -p SubState -p Result -p MemoryPeak -p CPUUsageNSec
