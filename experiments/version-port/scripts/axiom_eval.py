import re, sys
log, n = sys.argv[1], int(sys.argv[2])
txt = open(log).read()
ok3 = {"propext", "Classical.choice", "Quot.sound"}
dep = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", txt)
none = re.findall(r"'([^']+)' does not depend on any axioms", txt)
bad = [(t, a) for t, a in dep if not set(x.strip() for x in a.split(",")) <= ok3]
full = sum(1 for t, a in dep if set(x.strip() for x in a.split(",")) == ok3)
errs = len(re.findall(r"error", txt))
v = "OK" if (len(dep) + len(none) == n and not bad and errs == 0) else "UNEXPECTED"
print(f"{v}|{len(dep)+len(none)}/{n} reported; {full} with exactly [propext, Classical.choice, Quot.sound]; {len(none)} with no axioms; non-standard: {bad or 'none'}; error lines: {errs}")
