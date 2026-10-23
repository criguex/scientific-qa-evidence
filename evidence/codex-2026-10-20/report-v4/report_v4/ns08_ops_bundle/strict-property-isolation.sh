OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
OUT="$OPS/results/strict-property-isolation.log"
exec > >(tee "$OUT") 2>&1
set +e
echo "UTC start: $(date -u +%FT%TZ)"
systemd --version | head -n 1
run_probe() {
  name="$1"
  property="$2"
  unit="ns08-parse-${name}-a5ygak"
  echo "=== property=$property unit=$unit ==="
  systemd-run --user --wait --pipe --collect --unit="$unit" --property="$property" /usr/bin/true
  rc=$?
  echo "systemd_run_exit=$rc"
  echo 'journal:'
  journalctl --user -u "$unit" --no-pager -o short-iso-precise 2>&1
  echo "probe_${name}_exit=$rc"
}
run_probe raf RestrictAddressFamilies=none
run_probe arch SystemCallArchitectures=native
run_probe filter 'SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register'
echo "UTC end: $(date -u +%FT%TZ)"
exit 0
