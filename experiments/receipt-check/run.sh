#!/bin/bash
set -u
B4=/home/nse/validacion_cd_20261021/nocache
PS=/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe
host_free_gb() { $PS -NoProfile -Command '[math]::Floor((Get-PSDrive C).Free/1GB)' | tr -d '\r'; }
guard() { local f=$(host_free_gb); if [ "$f" -lt "$1" ]; then echo "ABORT: host drive has ${f} GB free, need $1" >&2; exit 3; fi; }
W=/home/nse/receipt_check_20261022
OPS=/home/nse/ns08_validation_20261020_a5YGak
OLD=/home/nse/nse_audit_20261020/NavierStokesAndEuler
CLONE=$W/qa
rm -rf $W; mkdir -p $W/bin $W/out
git clone -q https://github.com/criguex/scientific-qa-evidence.git $CLONE
ln -s $OPS/tools/landrun/landrun $W/bin/landrun
ln -s $OLD/.lake/packages/lean4export/.lake/build/bin/lean4export $W/bin/lean4export
ln -s $OPS/tools/nanoda/target/release/nanoda_bin $W/bin/nanoda_bin
export PATH=$W/bin:/home/nse/.elan/bin:/usr/bin:/bin
guard 40
cp -a $B4/NavierStokesAndEuler-* $W/tree
guard 15
T=$W/tree
now() { date -u +%FT%TZ; }
sha() { sha256sum "$1" | cut -c1-64; }
J=$W/out/receipts.jsonl
step() {
  local variant=$1 name=$2 log=$3; shift 3
  local t0=$(now)
  (cd $T && "$@" > $log 2>&1); local rc=$?
  sed -i -e 's|/home/nse/[A-Za-z0-9_./-]*|<path>|g' $log
  printf '{"variant": "%s", "step": "%s", "command": "%s", "log_sha256": "%s", "exit_code": %s, "started": "%s", "finished": "%s"}\n' "$variant" "$name" "$*" "$(sha $log)" "$rc" "$t0" "$(now)" >> $J
  return $rc
}
{ lake --version; lean --version; git -C $CLONE log -1 --format='qa clone %H'; sha256sum $W/bin/* $(readlink -f $W/bin/*) 2>/dev/null | sed 's|/home/nse/[^ ]*/||'; } > $W/out/versions.txt
E=$W/evidence; mkdir -p $E
printf 'step\tcommand\tlog\texit\n' > $E/receipt.tsv
step bundle cache_get $E/cache_get.log lake exe cache get; printf 'cache_get\tlake exe cache get\tcache_get.log\t%s\n' $? >> $E/receipt.tsv
step bundle build $E/build.log lake build; printf 'build\tlake build\tbuild.log\t%s\n' $? >> $E/receipt.tsv
step bundle comparator $E/comparator.log lake exe comparator ComparatorChallenges/NavierStokes.json; printf 'comparator\tlake exe comparator ComparatorChallenges/NavierStokes.json\tcomparator.log\t%s\n' $? >> $E/receipt.tsv
for v in C F5; do
  rm -rf $W/out/$v; cp -r $E $W/out/$v
  if [ $v = F5 ]; then sed -i 's|\tcomparator.log\t|\tcomparator-run.log\t|' $W/out/$v/receipt.tsv; fi
  diff $E/receipt.tsv $W/out/$v/receipt.tsv > $W/out/$v.receipt.diff
  rm -rf $T/qa-evidence; cp -r $W/out/$v $T/qa-evidence
  step $v Z_comparator $W/out/$v.Z.log lake exe comparator ComparatorChallenges/NavierStokes.json
  t0=$(now); python3 $CLONE/experiments/receipt-check/check_p6.py $W/out/$v > $W/out/$v.X.json 2>&1; rc=$?
  printf '{"variant": "%s", "step": "X_p6", "command": "python3 experiments/receipt-check/check_p6.py <bundle>", "log_sha256": "%s", "exit_code": %s, "started": "%s", "finished": "%s"}\n' $v "$(sha $W/out/$v.X.json)" $rc "$t0" "$(now)" >> $J
done
rm -rf $T/qa-evidence
echo DONE
