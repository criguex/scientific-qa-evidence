set +e
ROOT=<WSL_HOME>/ns08_validation_20261020_a5YGak/calibration_20261020T1957Z_ns08cal_3p8kza
echo "UTC=$(date -u +%FT%TZ)"
echo "ROOT=$ROOT"
if test -d "$ROOT/results"; then
  echo '===== pins-and-versions ====='
  sed -n '1,160p' "$ROOT/results/pins-and-versions.txt"
  echo '===== launcher and tool hashes ====='
  sed -n '1,80p' "$ROOT/results/launcher-source.sha256" "$ROOT/results/tool-binaries.sha256"
  find "$ROOT/results" -maxdepth 3 -type f -printf '%P\n' | sort
  for CASE in positive mismatch axiom; do
    D="$ROOT/results/$CASE"
    if test -d "$D"; then
      echo "===== $CASE classification/status ====="
      for F in classification.txt systemd-run-status.txt unit-properties.txt journal.log unit-query.stderr.log journal.stderr.log; do
        if test -f "$D/$F"; then echo "--- $F"; sed -n '1,180p' "$D/$F"; fi
      done
      for F in comparator.stdout.log comparator.stderr.log time.log guard.txt cgroup.txt process-status.txt launcher.stdout.log launcher.stderr.log validation.log unit-profile-active.txt unit-profile-poll.stderr.log; do
        if test -f "$D/$F"; then echo "--- $F"; sed -n '1,180p' "$D/$F"; fi
      done
    fi
  done
else
  echo "NO_RESULTS_DIRECTORY"
  find "$ROOT" -maxdepth 2 -type f -printf '%P\n' | sort
fi
echo '===== matching processes ====='
pgrep -af 'comparator|nanoda_bin|lean4export|run-calibration-remote' || true
echo '===== matching units ====='
systemctl --user list-units --all 'ns08-cal-*' --no-pager || true
