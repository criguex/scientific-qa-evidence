#!/bin/bash
set -u
QA_COMMIT=${QA_COMMIT:?set QA_COMMIT to the commit of scientific-qa-evidence to run}
W=/home/nse/receipt_check_case1
CLONE=$W/qa
rm -rf $W; mkdir -p $W/out || { echo "ABORT: cannot create $W" >&2; exit 3; }
git clone -q https://github.com/criguex/scientific-qa-evidence.git $CLONE </dev/null && git -C $CLONE checkout -q $QA_COMMIT || { echo "ABORT: cannot check out $QA_COMMIT" >&2; exit 3; }
. $CLONE/experiments/receipt-check/preflight.sh
link_tools $W/bin
export PATH=$W/bin:/home/nse/.elan/bin:/usr/bin:/bin
copy_tree $W/tree
T=$W/tree
J=$W/out/receipts.jsonl
step() {
  local variant=$1 name=$2 log=$3; shift 3
  local t0=$(now)
  (cd $T && "$@" > $log 2>&1); local rc=$?
  sed -i -e 's|/home/nse/[A-Za-z0-9_./-]*|<path>|g' $log
  printf '{"variant": "%s", "step": "%s", "command": "%s", "log_sha256": "%s", "exit_code": %s, "started": "%s", "finished": "%s"}\n' "$variant" "$name" "$*" "$(sha $log)" "$rc" "$t0" "$(now)" >> $J
  return $rc
}
record_toolchain $T $W/out/toolchain.txt
{ git -C $CLONE log -1 --format='qa clone %H'; sha256sum $(readlink -f $W/bin/*) | sed 's|/home/nse/[^ ]*/||'; } > $W/out/versions.txt
E=$W/evidence; mkdir -p $E
printf 'step\tcommand\tlog\texit\n' > $E/receipt.tsv
step bundle cache_get $E/cache_get.log lake exe cache get; rc=$?; printf 'cache_get\tlake exe cache get\tcache_get.log\t%s\n' $rc >> $E/receipt.tsv; expect $rc "bundle step cache_get" 0
step bundle build $E/build.log lake build; rc=$?; printf 'build\tlake build\tbuild.log\t%s\n' $rc >> $E/receipt.tsv; expect $rc "bundle step build" 0
step bundle comparator $E/comparator.log lake exe comparator ComparatorChallenges/NavierStokes.json; rc=$?; printf 'comparator\tlake exe comparator ComparatorChallenges/NavierStokes.json\tcomparator.log\t%s\n' $rc >> $E/receipt.tsv; expect $rc "bundle step comparator" 0
check_comparator_exe $T
for v in C F5; do
  rm -rf $W/out/$v; cp -r $E $W/out/$v || die "copy of the bundle failed ($v)"
  if [ $v = F5 ]; then sed -i 's|\tcomparator.log\t|\tcomparator-run.log\t|' $W/out/$v/receipt.tsv || die "receipt edit failed"; fi
  diff $E/receipt.tsv $W/out/$v/receipt.tsv > $W/out/$v.receipt.diff; expect $? "receipt diff ($v)" 0 1
  rm -rf $T/qa-evidence; cp -r $W/out/$v $T/qa-evidence || die "placing the bundle failed ($v)"
  step $v Z_comparator $W/out/$v.Z.log lake exe comparator ComparatorChallenges/NavierStokes.json; expect $? "Z_comparator ($v)" 0
  t0=$(now); python3 $CLONE/experiments/receipt-check/check_p6.py $W/out/$v > $W/out/$v.X.json 2>&1; rc=$?
  printf '{"variant": "%s", "step": "X_p6", "command": "python3 experiments/receipt-check/check_p6.py <bundle>", "log_sha256": "%s", "exit_code": %s, "started": "%s", "finished": "%s"}\n' $v "$(sha $W/out/$v.X.json)" $rc "$t0" "$(now)" >> $J
  expect $rc "check_p6 ($v)" 0 1
done
rm -rf $T/qa-evidence
echo DONE
