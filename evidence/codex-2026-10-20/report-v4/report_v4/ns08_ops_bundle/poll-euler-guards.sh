set -eu
UNIT=ns08-comparator-euler-20261020-1914
date -u +%FT%TZ
CG=$(systemctl --user show "$UNIT.service" -p ControlGroup --value)
echo "ControlGroup=$CG"
python3 - "$CG" <<'PY'
import pathlib,sys
cg=pathlib.Path('/sys/fs/cgroup')/sys.argv[1].lstrip('/')
pids=sorted(int(x) for x in (cg/'cgroup.procs').read_text().split())
print('cgroup_pids='+repr(pids))
bad=[]
for pid in pids:
 p=pathlib.Path('/proc')/str(pid)
 try:
  caps=next(x.split()[1] for x in (p/'status').read_text().splitlines() if x.startswith('CapEff:'))
  sockets=[]
  for fd in (p/'fd').iterdir():
   try:
    t=str(fd.readlink())
    if t.startswith('socket:'): sockets.append((fd.name,t))
   except (FileNotFoundError,PermissionError,OSError): pass
  print(f'pid={pid} CapEff={caps} socketfds={sockets}')
  if caps!='0000000000000000' or sockets: bad.append(pid)
 except (FileNotFoundError,ProcessLookupError): print(f'pid={pid} exited_during_scan')
if bad: raise SystemExit('guard_violation='+repr(bad))
PY
systemctl --user show "$UNIT.service" -p ActiveState -p SubState -p Result -p MemoryPeak -p CPUUsageNSec -p InvocationID
