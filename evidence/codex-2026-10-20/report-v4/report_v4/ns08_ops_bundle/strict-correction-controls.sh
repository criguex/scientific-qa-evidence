OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
OUT="$OPS/results/strict-correction-controls.log"
exec > >(tee "$OUT") 2>&1
set -u
echo "UTC start: $(date -u +%FT%TZ)"
echo "landrun version: $($OPS/tools/landrun/landrun --version)"
echo "lean version: $(<WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/lean --version)"
echo 'outer process socket descriptors:'
python3 -c 'import os; p="/proc/"+str(os.getppid())+"/fd"; a=[]
for n in os.listdir(p):
 try:
  t=os.readlink(p+"/"+n)
  if t.startswith("socket:"): a.append((n,t))
 except OSError: pass
print(repr(a)); raise SystemExit(bool(a))'
PRE_RC=$?
echo "outer_socket_inspection_exit=$PRE_RC"
test "$PRE_RC" = 0 || exit 20
TESTROOT="$OPS/ops/strict-correction-$(date -u +%H%M%S)"
if test -e "$TESTROOT"; then echo "refusing existing test path $TESTROOT"; exit 21; fi
ALLOW="$TESTROOT/allow"
DENY="$TESTROOT/deny"
mkdir -p "$ALLOW" "$DENY" || exit 22
printf 'landrun-read-control-a5ygak\n' > "$ALLOW/input.txt" || exit 23
printf 'def main : IO Unit := pure ()\n' > "$TESTROOT/LeanProbe.lean" || exit 24
PY_CODE='import ctypes,errno,os,socket
cap=next(line.split()[1] for line in open("/proc/self/status") if line.startswith("CapEff:"))
print("CapEff="+cap)
if int(cap,16)!=0: raise SystemExit("FAIL: CapEff nonzero")
fds=[]
for n in os.listdir("/proc/self/fd"):
 try:
  t=os.readlink("/proc/self/fd/"+n)
  if t.startswith("socket:"): fds.append((n,t))
 except OSError: pass
print("inherited_socket_fds="+repr(fds))
if fds: raise SystemExit("FAIL: inherited socket descriptors")
def denied(label,fn):
 try:
  obj=fn()
  if isinstance(obj,tuple):
   for x in obj: x.close()
  else: obj.close()
  print(label+"=ALLOWED (FAIL)")
  raise SystemExit(31)
 except OSError as e:
  print(label+"=DENIED errno=%d %s"%(e.errno,e.strerror))
  if e.errno!=errno.EPERM: raise SystemExit(32)
denied("tcp_socket",lambda:socket.socket(socket.AF_INET,socket.SOCK_STREAM))
denied("udp_socket",lambda:socket.socket(socket.AF_INET,socket.SOCK_DGRAM))
denied("unix_socket",lambda:socket.socket(socket.AF_UNIX,socket.SOCK_STREAM))
denied("socketpair",lambda:socket.socketpair())
libc=ctypes.CDLL(None,use_errno=True)
for label,n in [("io_uring_setup",425),("io_uring_enter",426),("io_uring_register",427)]:
 ctypes.set_errno(0); rc=libc.syscall(n,0,0,0,0,0,0); e=ctypes.get_errno()
 print(label+"_rc=%d errno=%d"%(rc,e))
 if rc!=-1 or e!=errno.EPERM: raise SystemExit(33)'
set +e
python3 -c "$PY_CODE"
SOCKET_RC=$?
set -e
echo "socket_syscall_controls_exit=$SOCKET_RC"
test "$SOCKET_RC" = 0 || exit 30
LR="$OPS/tools/landrun/landrun"
echo 'Landrun best-effort allowed read:'
READ_OUT=$("$LR" --best-effort --ldd --add-exec --ro "$ALLOW" /usr/bin/cat "$ALLOW/input.txt" 2>&1)
READ_RC=$?
printf '%s\n' "$READ_OUT"
echo "landrun_allowed_read_exit=$READ_RC"
test "$READ_RC" = 0 && test "$READ_OUT" = 'landrun-read-control-a5ygak' || exit 40
echo 'Landrun best-effort allowed write:'
"$LR" --best-effort --ldd --add-exec --rw "$ALLOW" /usr/bin/touch "$ALLOW/inside.txt"
WRITE_ALLOW_RC=$?
echo "landrun_allowed_write_exit=$WRITE_ALLOW_RC"
test "$WRITE_ALLOW_RC" = 0 && test -f "$ALLOW/inside.txt" || exit 41
echo 'Landrun best-effort denied outside write:'
set +e
"$LR" --best-effort --ldd --add-exec --rw "$ALLOW" /usr/bin/touch "$DENY/outside.txt"
WRITE_DENY_RC=$?
set -e
echo "landrun_outside_write_exit=$WRITE_DENY_RC"
if test "$WRITE_DENY_RC" = 0 || test -e "$DENY/outside.txt"; then echo 'FAIL: outside write was not denied'; exit 42; fi
echo 'Lean trivial run under the same unit:'
<WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/lean --run "$TESTROOT/LeanProbe.lean"
LEAN_RC=$?
echo "lean_probe_exit=$LEAN_RC"
test "$LEAN_RC" = 0 || exit 43
echo 'CapEff recheck:'
python3 -c 'cap=next(x.split()[1] for x in open("/proc/self/status") if x.startswith("CapEff:")); print("CapEff="+cap); raise SystemExit(int(cap,16)!=0)'
CAP_RC=$?
echo "capeff_exit=$CAP_RC"
test "$CAP_RC" = 0 || exit 44
echo 'Binary hashes:'
sha256sum "$LR" <WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/lean
echo 'CONTROL_SUMMARY=PASS'
echo "UTC end: $(date -u +%FT%TZ)"
exit 0
