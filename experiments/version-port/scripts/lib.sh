# Biblioteca común del experimento version-port. Uso: R=<path>/R1; source <path>/scripts/lib.sh
set -u
export PATH=$HOME/.elan/bin:$HOME/lean/port/tools/bin:$PATH
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
# step NAME CMD... : corre CMD en el cwd actual, log en $R/logs/NAME.log, recibo en $R/receipts/steps.tsv
step(){
  local name=$1; shift
  mkdir -p "$R/logs" "$R/receipts"
  [ -s "$R/receipts/steps.tsv" ] || printf 'step\tcommand\tcwd\tstart_utc\tend_utc\texit\tlog_sha256\tlog_bytes\n' > "$R/receipts/steps.tsv"
  local start end rc sha bytes
  start=$(date -u +%FT%TZ); log "INICIO $name: $* (cwd $PWD)"
  /usr/bin/time -v -o "$R/receipts/$name.time.txt" "$@" > "$R/logs/$name.log" 2>&1; rc=$?
  end=$(date -u +%FT%TZ)
  sha=$(sha256sum "$R/logs/$name.log" | cut -d' ' -f1); bytes=$(stat -c %s "$R/logs/$name.log")
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$*" "$PWD" "$start" "$end" "$rc" "$sha" "$bytes" >> "$R/receipts/steps.tsv"
  log "FIN $name rc=$rc"
  return $rc
}
