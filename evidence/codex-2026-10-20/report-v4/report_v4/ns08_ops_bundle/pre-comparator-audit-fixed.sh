set -e
OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
REPO=<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler
LEANBIN=<WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/lean
LAKEBIN=<WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/lake
echo "UTC audit: $(date -u +%FT%TZ)"
echo "repo=$REPO"
test "$(git -C "$REPO" rev-parse HEAD)" = f9e8bc5b38b6e212696e8a30e3e91517af887bbd
test -z "$(git -C "$REPO" status --porcelain=v1)"
echo 'repository pins:'
grep -n -E 'Comparator|lean4export' "$REPO/lake-manifest.json"
test "$(git -C "$REPO/.lake/packages/Comparator" rev-parse HEAD)" = 19e111e2141cf333c7daff0f64c5f24acc91dd2e
test -z "$(git -C "$REPO/.lake/packages/Comparator" status --porcelain=v1)"
test "$(git -C "$REPO/.lake/packages/lean4export" rev-parse HEAD)" = cacf989bd75f608700820f6afc595f32e7a99a4d
test -z "$(git -C "$REPO/.lake/packages/lean4export" status --porcelain=v1)"
test "$(git -C "$OPS/tools/nanoda" rev-parse HEAD)" = 9d6964f78d0fa4c93fd22fe956e17afe7e72a441
test -z "$(git -C "$OPS/tools/nanoda" status --porcelain=v1)"
test "$(git -C "$OPS/tools/landrun" rev-parse HEAD)" = ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a
test -z "$(git -C "$OPS/tools/landrun" status --porcelain=v1)"
echo 'pins_exact_and_worktrees_clean=PASS'
python3 - "$REPO" <<'PY'
import json, pathlib, sys
repo=pathlib.Path(sys.argv[1])
expected={
 'NavierStokes.json': ['propext','Quot.sound','Classical.choice'],
 'Euler.json': ['propext','Quot.sound','Classical.choice'],
}
for name,axioms in expected.items():
 p=repo/'ComparatorChallenges'/name
 data=json.loads(p.read_text())
 got=data.get('permitted_axioms')
 print(f'{p}: enable_nanoda={data.get("enable_nanoda")} permitted_axioms={got}')
 if data.get('enable_nanoda') is not True or got != axioms:
  raise SystemExit(f'FAIL unexpected challenge config: {name}')
PY
sha256sum "$REPO/ComparatorChallenges/NavierStokes.json" "$REPO/ComparatorChallenges/Euler.json"
echo 'expected binary hashes:'
for f in \
 "$REPO/.lake/packages/Comparator/.lake/build/bin/comparator" \
 "$REPO/.lake/packages/lean4export/.lake/build/bin/lean4export" \
 "$OPS/tools/nanoda/target/release/nanoda_bin" \
 "$OPS/tools/landrun/landrun"; do
  test -x "$f"
  file "$f"
  sha256sum "$f"
done
echo 'tool versions:'
"$LEANBIN" --version
"$LAKEBIN" --version
grep -n -E '^(name|version)\s*=' "$OPS/tools/nanoda/Cargo.toml" | head -2
"$OPS/tools/landrun/landrun" --version
echo 'Comparator pinned source command construction:'
grep -n -C 2 -E -- '--best-effort|COMPARATOR_LANDRUN|COMPARATOR_NANODA|enable_nanoda' "$REPO/.lake/packages/Comparator/Main.lean"
echo 'capability/ABI:'
python3 -c 'import ctypes; print("landlock_abi=%d"%ctypes.CDLL(None).syscall(444,0,0,1)); print("CapEff="+next(x.split()[1] for x in open("/proc/self/status") if x.startswith("CapEff:")))'
echo "UTC audit end: $(date -u +%FT%TZ)"
