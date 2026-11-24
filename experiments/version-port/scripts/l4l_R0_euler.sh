# Paso 8 de R0, mitad perdida: lean4lean --fresh Euler.Solution con el binario de l4l.sh (~/lean/lean4lean, 0048ed7 sobre rc2), en la copia R0
R=<path>/R0; source <path>/scripts/lib.sh
BIN=~/lean/lean4lean/.lake/build/bin/lean4lean
{ echo "lean4lean $(git -C ~/lean/lean4lean rev-parse HEAD) used_toolchain=$(cat ~/lean/lean4lean/lean-toolchain)"; sha256sum $BIN; } > $R/receipts/lean4lean_version.txt
cd $R/NavierStokesAndEuler
step s8_lean4lean_Euler.Solution timeout 48h lake env $BIN --fresh Euler.Solution; rc=$?
printf 's8_lean4lean_Euler.Solution\texit 0\texit %s; %s\t%s\n' $rc "$(tail -1 $R/logs/s8_lean4lean_Euler.Solution.log)" $([ $rc = 0 ] && echo OK || echo UNEXPECTED) >> $R/receipts/checks.tsv
[ $rc = 0 ] || echo "[$(date -u +%FT%TZ)] LEAN4LEAN NO ACEPTÓ Euler.Solution rc=$rc" >> $R/ALERT
log LISTO
