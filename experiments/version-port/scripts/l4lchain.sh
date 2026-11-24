# Paso 8 (lean4lean) de R1 y luego R2, cada uno cuando su paso 7 haya terminado bien
source <path>/scripts/lib.sh
for RID in R1 R2; do
  until grep -qP "^$RID\t" <path>/run/chain.tsv 2>/dev/null; do sleep 120; done
  rc=$(grep -P "^$RID\t" <path>/run/chain.tsv | cut -f2)
  [ "$rc" = 0 ] || { log "$RID terminó rc=$rc; no corro lean4lean"; continue; }
  STEPS="8" bash <path>/scripts/target.sh $RID > <path>/run/l4l-$RID.log 2>&1; rc=$?
  log "lean4lean $RID rc=$rc"; echo -e "$RID\t$rc" >> <path>/run/l4lchain.tsv
done
