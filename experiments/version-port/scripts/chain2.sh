# Reanudación tras el apagado de WSL (2026-11-24T01:27:56Z): R0 pasos 9,10,7; luego R1 y R2 completos (sin paso 8)
source <path>/scripts/lib.sh
echo -e "R0_interrupted\twsl_shutdown_2026-11-24T01:27:56Z" >> <path>/run/chain.tsv
run(){ RID=$1; STEPS="$2" bash <path>/scripts/target.sh $RID > <path>/run/target-$RID.$3.log 2>&1; rc=$?
  log "$RID terminó rc=$rc"; echo -e "$RID\t$rc" >> <path>/run/chain.tsv
  case $rc in 3|4|6) log "RECHAZO DE UN VERIFICADOR en $RID: detengo la cadena"; exit $rc;; esac; }
run R0 "9 10 7" resume
run R1 "1 2 3 4 5 6 9 10 7" run
run R2 "1 2 3 4 5 6 9 10 7" run
log LISTO
