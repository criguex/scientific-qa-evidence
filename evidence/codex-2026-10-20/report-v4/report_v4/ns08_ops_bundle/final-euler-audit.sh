set -eu
OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
REPO=<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler
R=$OPS/results/comparator-euler-20261020-1914
date -u +%FT%TZ
cat "$R/start_utc.txt" "$R/end_utc.txt" "$R/status.txt" "$R/guard.log"
cat "$R/time.log"
sha256sum "$R/command.txt" "$R/unit-properties.txt" "$R/inputs.sha256.txt" "$R/runner-payload.txt" "$R/stdout.log" "$R/stderr.log" "$R/time.log" "$R/status.txt"
echo 'final_git_commit:'
git -C "$REPO" rev-parse HEAD
echo 'final_git_status:'
git -C "$REPO" status --porcelain=v1
echo 'final_config_hashes:'
sha256sum "$REPO/ComparatorChallenges/NavierStokes.json" "$REPO/ComparatorChallenges/Euler.json"
echo 'unit journal:'
journalctl --user -u ns08-comparator-euler-20261020-1914.service --no-pager -o short-iso
echo 'boot id:'
cat /proc/sys/kernel/random/boot_id
