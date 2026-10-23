echo "UTC now: $(date -u +%FT%TZ)"
echo "boot_id=$(cat /proc/sys/kernel/random/boot_id)"
echo "uptime=$(cat /proc/uptime)"
uptime -s
who -b || true
echo 'boots:'
journalctl --list-boots --no-pager
echo 'last boot journal around unit:'
journalctl -b --no-pager -o short-iso-precise -n 70
echo 'exact runner and command metadata:'
sha256sum <WSL_HOME>/ns08_validation_20261020_a5YGak/ops/run-comparator-ns-20261020-1901.sh
sed -n '1,160p' <WSL_HOME>/ns08_validation_20261020_a5YGak/ops/run-comparator-ns-20261020-1901.sh
cat <WSL_HOME>/ns08_validation_20261020_a5YGak/results/comparator-ns-20261020-1901/command.txt
echo 'still-live related processes:'
ps -eo pid,ppid,stat,etime,rss,cmd | grep -E 'ns08-comparator-ns-20261020-1901|ComparatorChallenges/NavierStokes.json|lean4export ComparatorChallenges.NavierStokes|lake env' | grep -v grep || true
