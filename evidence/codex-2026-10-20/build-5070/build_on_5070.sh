#!/usr/bin/env bash
# Build and check github.com/openai/NavierStokesAndEuler on a Linux machine with open internet.
# Produces ./nse_results/ with logs and summary.json for the ADV-050 audit (NS-05..NS-09, EU-05).
#
# Usage (inside tmux or screen, it can take hours):
#   bash build_on_5070.sh            # build + axioms + statement mutation
#   RUN_COMPARATOR=1 bash build_on_5070.sh   # also try Comparator + nanoda (needs Go and Rust)
set -uo pipefail

COMMIT=f9e8bc5b38b6e212696e8a30e3e91517af887bbd
WORK="${WORK:-$HOME/nse_audit}"
OUT="$WORK/nse_results"
mkdir -p "$OUT"
LOG="$OUT/run.log"
exec > >(tee -a "$LOG") 2>&1
stamp() { date -u +%Y-%m-%dT%H:%M:%SZ; }
step() { echo; echo "== $(stamp) $*"; }
declare -A STATUS

step "environment"
uname -a; nproc; free -g | head -2; df -h "$HOME" | tail -1
command -v git curl >/dev/null || { echo "git and curl are required"; exit 1; }

step "install elan + Lean"
if ! command -v elan >/dev/null 2>&1; then
  curl -sSfL https://elan.lean-lang.org/elan-init.sh -o /tmp/elan-init.sh && sh /tmp/elan-init.sh -y --default-toolchain none
fi
export PATH="$HOME/.elan/bin:$PATH"
elan --version

step "clone at fixed commit"
cd "$WORK"
[ -d NavierStokesAndEuler ] || git clone https://github.com/openai/NavierStokesAndEuler.git
cd NavierStokesAndEuler
git fetch --quiet origin
git checkout --quiet "$COMMIT"
HEAD=$(git rev-parse HEAD)
echo "HEAD=$HEAD"
[ "$HEAD" = "$COMMIT" ] && STATUS[commit]=OK || STATUS[commit]=MISMATCH
sha256sum ComparatorChallenges/NavierStokes.lean ComparatorChallenges/Euler.lean \
  NavierStokes/ComparatorDefinitions.lean NavierStokes/ComparatorSolution.lean Euler/Solution.lean \
  lean-toolchain lakefile.toml lake-manifest.json | tee "$OUT/sha256.txt"
lean --version

step "mathlib cache"
if lake exe cache get; then STATUS[cache]=OK; else STATUS[cache]=FAILED; fi

step "lake build (full project)"
START=$(date +%s)
if lake build 2>&1 | tee "$OUT/lake_build.log"; then STATUS[build]=OK; else STATUS[build]=FAILED; fi
STATUS[build_seconds]=$(( $(date +%s) - START ))

step "print axioms (NS-07, EU-05)"
cat > /tmp/AxiomsCheck.lean <<'EOF'
import NavierStokes.ComparatorSolution
import Euler.Solution
#print axioms NavierStokes.Comparator.navier_stokes_breakdown_R3
#print axioms NavierStokes.Comparator.navier_stokes_breakdown_periodic
#print axioms Euler.euler_breakdown_R3
#print axioms Euler.exists_compact_smooth_euler_singularity
EOF
lake env lean /tmp/AxiomsCheck.lean 2>&1 | tee "$OUT/axioms.txt"
if grep -q "sorryAx" "$OUT/axioms.txt"; then STATUS[axioms]=SORRY_FOUND
elif [ "$(grep -c "depends on axioms: \[propext, Classical.choice, Quot.sound\]" "$OUT/axioms.txt")" = "4" ]; then STATUS[axioms]=STANDARD_ONLY
else STATUS[axioms]=CHECK_MANUALLY; fi

step "statement mutation NS-09: force must be identically zero"
# Adds a field `zero : f = 0` to ForceConditionDecay in the solution's copy of the definitions.
# A correct proof that really needs a non-zero force must stop compiling.
MUT="$WORK/mutant_force_zero"
rm -rf "$MUT"; cp -r "$WORK/NavierStokesAndEuler" "$MUT"; cd "$MUT"
python3 - <<'EOF'
import re, pathlib
p = pathlib.Path("NavierStokes/ComparatorDefinitions.lean")
s = p.read_text()
old = "structure ForceConditionDecay (f : ℝ^n → ℝ → ℝ^n) : Prop extends ForceCondition f where"
assert s.count(old) == 1, "target not found"
s = s.replace(old, old + "\n  /-- MUTANT: the force must vanish identically. -/\n  zero : f = 0")
p.write_text(s)
print("mutant applied")
EOF
if lake build NavierStokes.ComparatorSolution > "$OUT/mutant_force_zero.log" 2>&1; then
  STATUS[mutant_force_zero]=SURVIVED
else
  STATUS[mutant_force_zero]=KILLED
fi
grep -m 5 -E "error" "$OUT/mutant_force_zero.log" || true
cd "$WORK/NavierStokesAndEuler"

if [ "${RUN_COMPARATOR:-0}" = "1" ]; then
  step "Comparator + nanoda (NS-08)"
  command -v go >/dev/null && go install github.com/zouuup/landrun/cmd/landrun@latest
  command -v cargo >/dev/null && cargo install --git https://github.com/ammkrn/nanoda_lib nanoda_bin || true
  export PATH="$HOME/go/bin:$HOME/.cargo/bin:$PATH"
  lake build lean4export || true
  export PATH="$PWD/.lake/packages/lean4export/.lake/build/bin:$PATH"
  if lake exe comparator ComparatorChallenges/NavierStokes.json > "$OUT/comparator_ns.log" 2>&1; then STATUS[comparator_ns]=OK; else STATUS[comparator_ns]=FAILED; fi
  if lake exe comparator ComparatorChallenges/Euler.json > "$OUT/comparator_euler.log" 2>&1; then STATUS[comparator_euler]=OK; else STATUS[comparator_euler]=FAILED; fi
else
  STATUS[comparator_ns]=SKIPPED; STATUS[comparator_euler]=SKIPPED
fi

step "summary"
{
  echo "{"
  echo "  \"finished_utc\": \"$(stamp)\","
  echo "  \"commit\": \"$HEAD\","
  echo "  \"host_cores\": $(nproc),"
  first=1
  for k in "${!STATUS[@]}"; do
    [ $first = 1 ] && first=0 || echo ","
    printf '  "%s": "%s"' "$k" "${STATUS[$k]}"
  done
  echo; echo "}"
} | tee "$OUT/summary.json"
echo "Results in $OUT — copy that folder back to ~/Desktop/ADV-050_Auditoria/06_auditoria_navier_stokes/resultados_5070/"
