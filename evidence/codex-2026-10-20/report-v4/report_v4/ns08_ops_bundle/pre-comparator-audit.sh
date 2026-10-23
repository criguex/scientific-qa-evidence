OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
REPO=<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler
echo "UTC audit: $(date -u +%FT%TZ)"
echo "repo=$REPO"
git -C "$REPO" rev-parse HEAD
git -C "$REPO" status --porcelain=v1
echo 'lake manifest pins:'
rg -n 'Comparator|lean4export' "$REPO/lake-manifest.json"
echo 'dependency commits:'
git -C "$REPO/.lake/packages/Comparator" rev-parse HEAD
git -C "$REPO/.lake/packages/Comparator" status --porcelain=v1
git -C "$REPO/.lake/packages/lean4export" rev-parse HEAD
git -C "$REPO/.lake/packages/lean4export" status --porcelain=v1
git -C "$OPS/tools/nanoda" rev-parse HEAD
git -C "$OPS/tools/nanoda" status --porcelain=v1
git -C "$OPS/tools/landrun" rev-parse HEAD
git -C "$OPS/tools/landrun" status --porcelain=v1
echo 'Challenge JSON files:'
find "$REPO/ComparatorChallenges" -maxdepth 1 -type f -name '*.json' -printf '%f\n' | sort
for f in "$REPO/ComparatorChallenges/NavierStokes.json" "$REPO/ComparatorChallenges/Euler.json"; do
  test -f "$f" || { echo "MISSING $f"; exit 11; }
  sha256sum "$f"
  jq -c '{enable_nanoda,permitted_axioms}' "$f"
done
echo 'Expected comparator and helper binaries:'
for f in \
 "$REPO/.lake/packages/Comparator/.lake/build/bin/comparator" \
 "$REPO/.lake/packages/lean4export/.lake/build/bin/lean4export" \
 "$OPS/tools/nanoda/target/release/nanoda_bin" \
 "$OPS/tools/landrun/landrun"; do
  test -x "$f" || { echo "MISSING_OR_NOT_EXECUTABLE $f"; exit 12; }
  file "$f"
  sha256sum "$f"
done
echo 'Tool versions:'
<WSL_HOME>/.elan/bin/lean --version
<WSL_HOME>/.elan/bin/lake --version
"$OPS/tools/nanoda/target/release/nanoda_bin" --help | head -5
"$OPS/tools/landrun/landrun" --version
echo 'Comparator source command construction:'
rg -n -C 2 -- '--best-effort|COMPARATOR_LANDRUN|COMPARATOR_NANODA|enable_nanoda' "$REPO/.lake/packages/Comparator/Main.lean"
echo 'Current sandbox and unit manager:'
python3 -c 'import ctypes,os; libc=ctypes.CDLL(None); a=libc.syscall(444,0,0,1); print("landlock_abi=%d"%a); print("CapEff="+next(x.split()[1] for x in open("/proc/self/status") if x.startswith("CapEff:")))'
echo 'systemd status and manager:'
systemd --version | head -1
systemctl --user is-system-running
echo "UTC audit end: $(date -u +%FT%TZ)"
