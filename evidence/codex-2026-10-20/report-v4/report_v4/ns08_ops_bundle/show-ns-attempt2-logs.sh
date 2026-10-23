set -eu
R=<WSL_HOME>/ns08_validation_20261020_a5YGak/results/comparator-ns-attempt2-20261020-1905
for n in stdout.log stderr.log status.txt time.log start_utc.txt end_utc.txt guard.log command.txt unit-properties.txt inputs.sha256.txt; do
 printf '\n===== BEGIN %s =====\n' "$n"
 cat "$R/$n"
 printf '\n===== END %s =====\n' "$n"
done
