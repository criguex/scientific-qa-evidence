B4=/home/nse/validacion_cd_20261021/nocache
OPS=/home/nse/ns08_validation_20261020_a5YGak
OLD=/home/nse/nse_audit_20261020/NavierStokesAndEuler
PS=/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe
die() { echo "ABORT: $*" >&2; exit 3; }
expect() { local rc=$1 what=$2 ok; shift 2; for ok in "$@"; do [ "$rc" = "$ok" ] && return 0; done; die "$what exited $rc, expected one of: $*"; }
now() { date -u +%FT%TZ; }
sha() { sha256sum "$1" | cut -c1-64; }
guard() {
  local f
  f=$($PS -NoProfile -Command '[math]::Floor((Get-PSDrive C).Free/1GB)' 2>/dev/null | tr -d '\r')
  [[ "$f" =~ ^[0-9]+$ ]] || die "cannot read the host drive's free space"
  [ "$f" -ge "$1" ] || die "host drive has ${f} GB free, need $1"
}
link_tools() {
  local bin=$1 name want
  mkdir -p "$bin" || die "cannot create $bin"
  ln -sf $OPS/tools/landrun/landrun "$bin/landrun"
  ln -sf $OLD/.lake/packages/lean4export/.lake/build/bin/lean4export "$bin/lean4export"
  ln -sf $OPS/tools/nanoda/target/release/nanoda_bin "$bin/nanoda_bin"
  while read -r name want; do
    [ "$(sha "$bin/$name")" = "$want" ] || die "tool hash mismatch: $name"
  done <<'PINS'
landrun e3d26ebf2f7c786f8d34b7051ad2c655329aeadbb863404e3dd05d3a97b0518a
lean4export 4fa9e14cada304109e85da5048bcd411cf781a03539b3e50953e5c537074bd9e
nanoda_bin ccda52587ef42760dff9bc2de26edca0cb6ad207c8719cfffcd1e7daab22ccfb
PINS
}
copy_tree() {
  local dest=$1
  guard 40
  rm -rf "$dest"
  cp -a $B4/NavierStokesAndEuler-* "$dest" </dev/null || die "copy of the B4 tree failed"
  guard 15
  [ "$(cat "$dest/lean-toolchain")" = "leanprover/lean4:v4.34.0-rc2" ] || die "unexpected lean-toolchain"
  python3 - "$dest/lake-manifest.json" <<'PY' || die "lake-manifest pins differ"
import json, sys
revs = {p["name"]: p.get("rev") for p in json.load(open(sys.argv[1]))["packages"]}
want = {"Comparator": "19e111e2141cf333c7daff0f64c5f24acc91dd2e", "mathlib": "85e3a25e006c35636f0e53b0e9296caca2685bc0", "lean4export": "cacf989bd75f608700820f6afc595f32e7a99a4d"}
sys.exit(0 if all(revs.get(k) == v for k, v in want.items()) else 1)
PY
}
check_comparator_exe() {
  [ "$(sha "$1/.lake/packages/Comparator/.lake/build/bin/comparator")" = "514de8d2acbd6e0102575cd2c575e336b7c4a40daf3ae66abe97cef5e1e6b02a" ] || die "Comparator binary differs from the audited one"
}
record_toolchain() {
  (cd "$1" && { lake --version && lean --version && cat lean-toolchain; } ) > "$2" 2>&1 </dev/null || die "cannot record the toolchain"
}
