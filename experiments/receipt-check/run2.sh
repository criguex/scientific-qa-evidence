#!/bin/bash
set -u
B4=/home/nse/validacion_cd_20261021/nocache
W=/home/nse/receipt_check_20261022
OPS=/home/nse/ns08_validation_20261020_a5YGak
PS=/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe
host_free_gb() { $PS -NoProfile -Command '[math]::Floor((Get-PSDrive C).Free/1GB)' | tr -d '\r'; }
guard() { local f=$(host_free_gb); if [ "$f" -lt "$1" ]; then echo "ABORT: host drive has ${f} GB free, need $1" >&2; exit 3; fi; }
export PATH=$W/bin:/home/nse/.elan/bin:/usr/bin:/bin
rm -rf $W/qa2 $W/out2 && mkdir -p $W/out2
git clone -q https://github.com/criguex/scientific-qa-evidence.git $W/qa2 </dev/null
R=$W/qa2/experiments/receipt-check
guard 40
rm -rf $W/tree && cp -a $B4/NavierStokesAndEuler-* $W/tree </dev/null
guard 15
T=$W/tree
now() { date -u +%FT%TZ; }
sha() { sha256sum "$1" | cut -c1-64; }
J=$W/out2/receipts.jsonl
rec() { printf '{"variant": "%s", "step": "%s", "command": "%s", "log_sha256": "%s", "exit_code": %s, "started": "%s", "finished": "%s"}\n' "$1" "$2" "$3" "$(sha $4)" "$5" "$6" "$(now)" >> $J; }
(cd $T && { lake --version; lean --version; cat lean-toolchain; }) > $W/out2/toolchain.txt 2>&1 </dev/null
for v in C F5 F7; do
  rm -rf $W/out2/$v; cp -r $R/results/C $W/out2/$v
  if [ $v = F5 ]; then sed -i 's|\tcomparator.log\t|\tcomparator-run.log\t|' $W/out2/$v/receipt.tsv; fi
  if [ $v = F7 ]; then cp $W/qa2/evidence/formal/b5/comparator5_NavierStokes.stdout.log $W/out2/$v/comparator.log; fi
  (cd $W/out2 && diff -r C $v > $v.diff)
  rm -rf $T/qa-evidence; cp -r $W/out2/$v $T/qa-evidence
  t0=$(now); (cd $T && lake exe comparator ComparatorChallenges/NavierStokes.json > $W/out2/$v.Z.log 2>&1 </dev/null); rc=$?
  sed -i -e 's|/home/nse/[A-Za-z0-9_./-]*|<path>|g' $W/out2/$v.Z.log
  rec $v Z_comparator "lake exe comparator ComparatorChallenges/NavierStokes.json" $W/out2/$v.Z.log $rc $t0
  t0=$(now); python3 $R/check_p6.py $W/out2/$v > $W/out2/$v.X1.json 2>&1 </dev/null; rc=$?
  rec $v X1_p6 "python3 experiments/receipt-check/check_p6.py <bundle>" $W/out2/$v.X1.json $rc $t0
  t0=$(now); python3 $R/check_hash.py $W/out2/$v > $W/out2/$v.X2.json 2>&1 </dev/null; rc=$?
  rec $v X2_hash "python3 experiments/receipt-check/check_hash.py <bundle>" $W/out2/$v.X2.json $rc $t0
done
rm -rf $T/qa-evidence $T
git -C $W/qa2 log -1 --format='qa clone %H' >> $W/out2/toolchain.txt
echo DONE
