# R0 -> R1 -> R2 (pasos 1-7, 9, 10); el paso 8 de R1/R2 corre aparte (l4lchain.sh)
source <path>/scripts/lib.sh
for RID in R0 R1 R2; do
  STEPS="1 2 3 4 5 6 9 10 7" bash <path>/scripts/target.sh $RID > <path>/run/target-$RID.log 2>&1; rc=$?
  log "$RID terminó rc=$rc"; echo -e "$RID\t$rc" >> <path>/run/chain.tsv
  case $rc in 3|4|6) log "RECHAZO DE UN VERIFICADOR en $RID: detengo la cadena"; exit $rc;; esac
done
log LISTO
