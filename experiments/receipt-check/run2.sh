#!/bin/bash
set -u
QA_COMMIT=${QA_COMMIT:?set QA_COMMIT to the commit of scientific-qa-evidence to run}
W=/home/nse/receipt_check_case2
rm -rf $W; mkdir -p $W/out2 || { echo "ABORT: cannot create $W" >&2; exit 3; }
git clone -q https://github.com/criguex/scientific-qa-evidence.git $W/qa2 </dev/null && git -C $W/qa2 checkout -q $QA_COMMIT || { echo "ABORT: cannot check out $QA_COMMIT" >&2; exit 3; }
. $W/qa2/experiments/receipt-check/preflight.sh
R=$W/qa2/experiments/receipt-check
link_tools $W/bin
export PATH=$W/bin:/home/nse/.elan/bin:/usr/bin:/bin
copy_tree $W/tree
T=$W/tree
J=$W/out2/receipts.jsonl
rec() { printf '{"variant": "%s", "step": "%s", "command": "%s", "log_sha256": "%s", "exit_code": %s, "started": "%s", "finished": "%s"}\n' "$1" "$2" "$3" "$(sha $4)" "$5" "$6" "$(now)" >> $J; }
record_toolchain $T $W/out2/toolchain.txt
for v in C F5 F7; do
  rm -rf $W/out2/$v; cp -r $R/results/C $W/out2/$v || die "copy of the bundle failed ($v)"
  if [ $v = F5 ]; then sed -i 's|\tcomparator.log\t|\tcomparator-run.log\t|' $W/out2/$v/receipt.tsv || die "receipt edit failed"; fi
  if [ $v = F7 ]; then cp $W/qa2/evidence/formal/b5/comparator5_NavierStokes.stdout.log $W/out2/$v/comparator.log || die "log substitution failed"; fi
  (cd $W/out2 && diff -r C $v > $v.diff); expect $? "bundle diff ($v)" 0 1
  rm -rf $T/qa-evidence; cp -r $W/out2/$v $T/qa-evidence || die "placing the bundle failed ($v)"
  t0=$(now); (cd $T && lake exe comparator ComparatorChallenges/NavierStokes.json > $W/out2/$v.Z.log 2>&1 </dev/null); rc=$?
  sed -i -e 's|/home/nse/[A-Za-z0-9_./-]*|<path>|g' $W/out2/$v.Z.log
  rec $v Z_comparator "lake exe comparator ComparatorChallenges/NavierStokes.json" $W/out2/$v.Z.log $rc $t0
  expect $rc "Z_comparator ($v)" 0
  t0=$(now); python3 $R/check_p6.py $W/out2/$v > $W/out2/$v.X1.json 2>&1 </dev/null; rc=$?
  rec $v X1_p6 "python3 experiments/receipt-check/check_p6.py <bundle>" $W/out2/$v.X1.json $rc $t0
  expect $rc "check_p6 ($v)" 0 1
  t0=$(now); python3 $R/check_hash.py $W/out2/$v > $W/out2/$v.X2.json 2>&1 </dev/null; rc=$?
  rec $v X2_hash "python3 experiments/receipt-check/check_hash.py <bundle>" $W/out2/$v.X2.json $rc $t0
  expect $rc "check_hash ($v)" 0 1
done
check_comparator_exe $T
rm -rf $T/qa-evidence $T
git -C $W/qa2 log -1 --format='qa clone %H' >> $W/out2/toolchain.txt
echo DONE
