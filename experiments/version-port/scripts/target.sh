# Uso: STEPS="1 2 3 4 5 6 9 10 7 8" bash target.sh RID   (RID = R0 | R1 | R2)
RID=$1; STEPS=${STEPS:-1 2 3 4 5 6 9 10 7 8}
want(){ [[ " $STEPS " == *" $1 "* ]]; }
R=<path>/$RID; source <path>/scripts/lib.sh
mkdir -p $R/receipts $R/logs $R/work $R/diffs
P=$R/NavierStokesAndEuler; IN=<path>/inputs; SRC=f9e8bc5b38b6e212696e8a30e3e91517af887bbd
case $RID in
  R0) TAG=v4.34.0-rc2; TC=leanprover/lean4:v4.34.0-rc2; EXP_ML=85e3a25; EXP_CMP=19e111e; L4L=;;
  R1) TAG=v4.34.0;     TC=leanprover/lean4:v4.34.0;     EXP_ML=5ed2965; EXP_CMP=d03acab; L4L=0048ed7;;
  R2) TAG=v4.35.0;     TC=leanprover/lean4:v4.35.0;     EXP_ML=56a0058; EXP_CMP=e3dcf30; L4L=b73a4e7;;
esac
export PATH=$HOME/lean/port/tools/bin-$TAG:$PATH
CHK=$R/receipts/checks.tsv
[ -s $CHK ] || printf 'step\texpected\tobserved\tverdict\n' > $CHK
check(){ printf '%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" >> $CHK; log "CHECK $1: esperado=[$2] obtenido=[$3] => $4"; }
alert(){ echo "[$(date -u +%FT%TZ)] $*" >> $R/ALERT; log "ALERTA: $*"; }
waitmem(){ local need=$1; while :; do local a=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo); [ "$a" -ge "$need" ] && return; log "esperando memoria: $a GB < $need GB"; sleep 120; done; }
stmt_check(){ git diff --exit-code $SRC -- ComparatorChallenges/ NavierStokes/ComparatorSolution.lean Euler/Solution.lean && git status --porcelain -- ComparatorChallenges/ NavierStokes/ComparatorSolution.lean Euler/Solution.lean | (! grep .) && sha256sum ComparatorChallenges/* NavierStokes/ComparatorSolution.lean Euler/Solution.lean; }
manifest(){ (LC_ALL=C find . -path ./.git -prune -o -type f -print | LC_ALL=C sort | while IFS= read -r f; do sha256sum "$f"; done) | sha256sum; }
export -f stmt_check manifest; export SRC
MODS="NavierStokes.ComparatorSolution Euler.Solution"
FINAL="NavierStokes.Comparator.navier_stokes_breakdown_R3 NavierStokes.Comparator.navier_stokes_breakdown_periodic Euler.euler_breakdown_R3 Euler.exists_compact_smooth_euler_singularity"
axiom_eval(){ python3 <path>/scripts/axiom_eval.py "$1" $2; }

log "=== $RID ($TAG) pasos: $STEPS"
# ---- 1. clon limpio
if want 1; then
  rm -rf $P; cd $R
  step s1_clone git clone -q https://github.com/openai/NavierStokesAndEuler.git || { alert "clone falló"; exit 1; }
  cd $P && git checkout -q $SRC && git rev-parse HEAD > $R/receipts/source_commit.txt
  step s1_manifest bash -c manifest
  M=$(cut -d' ' -f1 $R/logs/s1_manifest.log)
  [ "$M" = 95bb21c93e834581e1400e31e33a9fb7943db2f64f11425b034f97b9b52e95fc ] && v=OK || v=UNEXPECTED
  check s1_manifest 95bb21c9…52e95fc "$M" $v
fi
cd $P
# ---- 2. versiones (R1, R2)
if want 2 && [ $RID != R0 ]; then
  echo "$TC" > lean-toolchain
  sed -i "s/^rev = \"v4.34.0-rc2\"/rev = \"$TAG\"/" lakefile.toml
  MATHLIB_NO_CACHE_ON_UPDATE=1 step s2_lake_update lake update || { alert "lake update falló"; exit 1; }
  git diff $SRC -- lean-toolchain lakefile.toml lake-manifest.json > $R/diffs/versions.diff
fi
python3 - > $R/receipts/manifest_revs.tsv <<'PY'
import json; m=json.load(open("lake-manifest.json"))
for p in m["packages"]: print(f'{p["name"]}\t{p["rev"]}\t{p.get("inputRev")}')
PY
ML=$(awk '$1=="mathlib"{print $2}' $R/receipts/manifest_revs.tsv); CM=$(awk '$1=="Comparator"{print $2}' $R/receipts/manifest_revs.tsv)
[[ $ML == $EXP_ML* && $CM == $EXP_CMP* ]] && v=OK || v=UNEXPECTED
want 2 && check s2_versions "toolchain $TC, mathlib $EXP_ML, Comparator $EXP_CMP" "toolchain $(cat lean-toolchain), mathlib ${ML:0:7}, Comparator ${CM:0:7}" $v
# ---- 3. enunciados
if want 3; then
  step s3_statements bash -c stmt_check && v=OK || v=UNEXPECTED
  check s3_statements "empty diff vs f9e8bc5 (ComparatorChallenges/, solution files)" "exit $(tail -1 $R/receipts/steps.tsv | cut -f6)" $v
  [ $v = OK ] || { alert "enunciados distintos"; exit 1; }
fi
# ---- 4. build
if want 4; then
  if [ $RID = R0 ]; then
    log "R0: espero la compilación original (~/lean/pasos.tsv build 0)"
    until grep -qP '^build\t0\t' ~/lean/pasos.tsv; do grep -qP '^build\t[1-9]' ~/lean/pasos.tsv && { alert "build original falló"; exit 1; }; sleep 60; done
    cp ~/lean/pasos.tsv $R/receipts/original_build_pasos.tsv; cp ~/lean/setup.log $R/logs/original_setup.log 2>/dev/null
    step s4_copy_lake cp -a ~/lean/NavierStokesAndEuler/.lake $P/.lake || { alert "copia .lake falló"; exit 1; }
    waitmem 12
    step s4_build lake build
  else
    step s4_cache_get lake exe cache get || { alert "cache get falló"; exit 1; }
    waitmem 20
    step s4_build lake build
  fi
  rc=$(tail -1 $R/receipts/steps.tsv | cut -f6); nb=$(grep -c '\] Built ' $R/logs/s4_build.log); last=$(grep -E 'Build completed|error' $R/logs/s4_build.log | tail -1)
  [ $rc = 0 ] && v=OK || v=UNEXPECTED
  check s4_build "exit 0" "exit $rc; $nb modules built here; $last" $v
  [ $rc = 0 ] || { alert "build falló (ver logs/s4_build.log)"; exit 2; }
  step s3b_statements_after_build bash -c stmt_check && v=OK || v=UNEXPECTED
  check s3b_statements_after_build "empty diff" "exit $(tail -1 $R/receipts/steps.tsv | cut -f6)" $v
fi
# versiones
{ echo "lean-toolchain: $(cat lean-toolchain)"; lean --version; lake --version; uname -a
  PFX=$(lean --print-prefix); for b in $PFX/bin/lean $PFX/bin/lake $PFX/bin/leanchecker; do sha256sum $b; done
  for b in landrun nanoda_bin lean4export; do sha256sum $(command -v $b); done; } > $R/receipts/versions.txt 2>&1
# ---- 5. axiomas finales
if want 5; then
  { echo "import NavierStokes.ComparatorSolution"; echo "import Euler.Solution"; for t in $FINAL; do echo "#print axioms $t"; done; } > $R/work/FinalAxioms.lean
  step s5_axioms lake env lean $R/work/FinalAxioms.lean
  out=$(axiom_eval $R/logs/s5_axioms.log 4); v=${out%%|*}
  check s5_axioms "4 theorems, only propext/Classical.choice/Quot.sound" "exit $(tail -1 $R/receipts/steps.tsv | cut -f6); ${out#*|}" $v
fi
# ---- 6. Comparator
if want 6; then
  until [ -s <path>/tools/receipts/tools.tsv ]; do log "esperando herramientas"; sleep 60; done
  for b in landrun nanoda_bin lean4export; do command -v $b >/dev/null || { alert "falta $b en PATH"; exit 7; }; done
  step s6_comparator_prebuild bash -c 'lake build Comparator/comparator 2>&1 || lake exe comparator 2>&1 | tail -3; true'
  sha256sum .lake/packages/Comparator/.lake/build/bin/comparator >> $R/receipts/versions.txt
  for J in NavierStokes Euler; do
    waitmem 12
    step s6_comparator_$J lake exe comparator ComparatorChallenges/$J.json; rc=$?
    ok=$(grep -c 'Your solution is okay!' $R/logs/s6_comparator_$J.log); kern=$(grep -E 'kernel accepts|kernel rejects|nanoda' $R/logs/s6_comparator_$J.log | tr '\n' ';')
    [ $rc = 0 ] && [ $ok -ge 1 ] && v=OK || v=UNEXPECTED
    check s6_comparator_$J "exit 0, Your solution is okay!" "exit $rc; okay-lines=$ok; $kern $(tail -1 $R/logs/s6_comparator_$J.log)" $v
    [ $v = OK ] || { alert "COMPARATOR NO ACEPTÓ $J (rc=$rc)"; exit 3; }
  done
fi
# ---- 9. mutantes
if want 9; then
  for D in ${MUTS:-$IN/mutants/*.diff}; do
    n=$(basename $D .diff); J=NavierStokes; [[ $n == euler* ]] && J=Euler
    MD=$R/mut/$n; rm -rf $MD; mkdir -p $R/mut; cp -a $P $MD
    (cd $MD && git apply $D) || { check s9_$n "diff applies" "git apply failed" UNEXPECTED; rm -rf $MD; continue; }
    (cd $MD && git diff > $R/diffs/mutant_$n.applied.diff)
    waitmem 12
    cd $MD; step s9_mutant_$n lake exe comparator ComparatorChallenges/$J.json; rc=$?; cd $P
    dec=$(grep -E 'uncaught exception|Your solution is okay' $R/logs/s9_mutant_$n.log | tail -1)
    if [ $n = control_comment ]; then exp="accept (exit 0, okay)"; [ $rc = 0 ] && [[ $dec == *okay* ]] && v=OK || v=UNEXPECTED
    else exp="reject: statement do not match"; [ $rc != 0 ] && [[ $dec == *"do not match"* ]] && v=OK || v=UNEXPECTED; fi
    check s9_mutant_$n "$exp" "exit $rc; $dec" $v
    [ $v = OK ] || alert "mutante $n resultado inesperado: rc=$rc $dec"
    rm -rf $MD
  done
fi
# ---- 10. puentes
if want 10; then
  cp $IN/bridges/ClayLiteral.lean $IN/bridges/Bridges.lean $P/
  sha256sum ClayLiteral.lean Bridges.lean > $R/receipts/bridges_inputs.sha256
  step s10_clay lake env lean -o .lake/build/lib/lean/ClayLiteral.olean ClayLiteral.lean
  step s10_bridges lake env lean -o .lake/build/lib/lean/Bridges.olean Bridges.lean
  { echo "import Bridges"; grep -oP '^theorem \K\S+' Bridges.lean | sed 's/^/#print axioms Bridges./'; echo "#print axioms ClayLiteral.altD_withoutErratum_imp_withErratum"; } > $R/work/BridgeAxioms.lean
  N=$(grep -c '#print axioms' $R/work/BridgeAxioms.lean)
  step s10_bridge_axioms lake env lean $R/work/BridgeAxioms.lean
  out=$(axiom_eval $R/logs/s10_bridge_axioms.log $N); v=${out%%|*}
  rcs=$(grep -P '^s10_' $R/receipts/steps.tsv | cut -f6 | tr '\n' ' ')
  check s10_bridges "clay, bridges, axioms exit 0; $N theorems only standard axioms" "exits $rcs; ${out#*|}" $v
fi
# ---- 7. leanchecker --fresh
if want 7; then
  for M in $MODS; do
    waitmem 14
    step s7_leanchecker_$M timeout 10h lake env leanchecker --fresh $M; rc=$?
    [ $rc = 0 ] && v=OK || v=UNEXPECTED
    check s7_leanchecker_$M "exit 0" "exit $rc; log $(stat -c %s $R/logs/s7_leanchecker_$M.log) bytes" $v
    [ $v = OK ] || { alert "LEANCHECKER NO ACEPTÓ $M (rc=$rc)"; exit 4; }
  done
fi
# ---- 8. lean4lean (R1, R2)
if want 8 && [ -n "$L4L" ]; then
  LD=<path>/l4l-$RID
  if [ ! -x $LD/.lake/build/bin/lean4lean ]; then
    rm -rf $LD; git clone -q https://github.com/digama0/lean4lean.git $LD; cd $LD; git checkout -q $L4L
    echo "lean4lean $(git rev-parse HEAD) toolchain=$(cat lean-toolchain)" > $R/receipts/lean4lean_version.txt
    grep -E '"(name|rev)"' lake-manifest.json >> $R/receipts/lean4lean_version.txt
    [ "$(cat lean-toolchain)" = "$TC" ] || alert "lean4lean $L4L toolchain $(cat lean-toolchain) != $TC"
    step s8_lean4lean_build lake build || { alert "lean4lean no compiló"; exit 5; }
  fi
  BIN=$LD/.lake/build/bin/lean4lean; sha256sum $BIN >> $R/receipts/lean4lean_version.txt
  cd $P
  for M in $MODS; do
    waitmem 14
    step s8_lean4lean_$M timeout 48h lake env $BIN --fresh $M; rc=$?
    [ $rc = 0 ] && v=OK || v=UNEXPECTED
    check s8_lean4lean_$M "exit 0" "exit $rc; $(tail -2 $R/logs/s8_lean4lean_$M.log | tr '\n' ' ')" $v
    [ $v = OK ] || { alert "LEAN4LEAN NO ACEPTÓ $M (rc=$rc)"; exit 6; }
  done
fi
log "LISTO $RID"
