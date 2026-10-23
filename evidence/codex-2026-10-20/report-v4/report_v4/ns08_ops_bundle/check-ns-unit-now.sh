set -e
UNIT=ns08-comparator-ns-20261020-1901.service
OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
RUNDIR="$OPS/results/comparator-ns-20261020-1901"
echo "UTC inspection: $(date -u +%FT%TZ)"
systemctl --user show "$UNIT" -p ActiveState -p SubState -p Result -p MainPID -p ControlGroup -p MemoryPeak -p CPUUsageNSec -p RuntimeMaxUSec
python3 - "$UNIT" <<'PY'
import os,pathlib,subprocess,sys
unit=sys.argv[1]
cg=subprocess.check_output(['systemctl','--user','show',unit,'-p','ControlGroup','--value'],text=True).strip()
print('ControlGroup='+cg)
procs=pathlib.Path('/sys/fs/cgroup'+cg+'/cgroup.procs')
if not procs.exists():
 print('cgroup_procs=none')
 raise SystemExit(0)
for pid in procs.read_text().split():
 p=pathlib.Path('/proc')/pid
 try:
  cmd=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
  cap=next(x.split()[1] for x in (p/'status').read_text().splitlines() if x.startswith('CapEff:'))
  fds=[]
  for f in (p/'fd').iterdir():
   try:
    t=os.readlink(f)
    if t.startswith('socket:'): fds.append((f.name,t))
   except OSError: pass
  print(f'pid={pid} cmd={cmd} CapEff={cap} socket_fds={fds}')
 except OSError as e: print(f'pid={pid} inspection_error={e}')
PY
echo 'Run files:'
find "$RUNDIR" -maxdepth 1 -type f -printf '%f %s bytes\n' | sort
if test -f "$RUNDIR/status.txt"; then cat "$RUNDIR/status.txt"; fi
