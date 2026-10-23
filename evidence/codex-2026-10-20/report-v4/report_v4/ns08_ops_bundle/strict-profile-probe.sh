#!/usr/bin/env bash
set -u
OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
OUT="$OPS/results/strict-profile-probe.log"
exec > >(tee "$OUT") 2>&1
echo "UTC start: $(date -u +%FT%TZ)"
systemd --version | head -n 1
systemd-analyze --version | head -n 1
echo 'Local systemd.exec excerpts:'
MANPAGER=cat man systemd.exec | col -b | grep -n -A14 -B3 -E '^ *RestrictAddressFamilies=|^ *SystemCallArchitectures=|^ *SystemCallFilter=' | head -n 110
echo 'Unit property parse + behavior probe with requested exact profile:'
PROPS=(
  --property=RestrictAddressFamilies=none
  --property=SystemCallArchitectures=native
  --property='SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register'
)
CODE='import os,socket,ctypes,errno
print("CapEff="+next(x.split()[1] for x in open("/proc/self/status") if x.startswith("CapEff:")))
fds=[]
for n in os.listdir("/proc/self/fd"):
 try:
  target=os.readlink("/proc/self/fd/"+n)
  if target.startswith("socket:"): fds.append((n,target))
 except OSError: pass
print("inherited_socket_fds="+repr(fds))
for name,fam,typ in [("tcp",socket.AF_INET,socket.SOCK_STREAM),("udp",socket.AF_INET,socket.SOCK_DGRAM),("unix",socket.AF_UNIX,socket.SOCK_STREAM)]:
 try: s=socket.socket(fam,typ); s.close(); print(name+"_socket=ALLOWED")
 except OSError as e: print(name+"_socket=DENIED errno=%d %s"%(e.errno,e.strerror))
try: a,b=socket.socketpair(); a.close(); b.close(); print("socketpair=ALLOWED")
except OSError as e: print("socketpair=DENIED errno=%d %s"%(e.errno,e.strerror))
libc=ctypes.CDLL(None,use_errno=True)
for name,num in [("io_uring_setup",425),("io_uring_enter",426),("io_uring_register",427)]:
 ctypes.set_errno(0); rc=libc.syscall(num,0,0,0,0,0,0); err=ctypes.get_errno()
 print(name+"_syscall_rc=%d errno=%d %s"%(rc,err,os.strerror(err) if err else ""))'
set +e
systemd-run --user --wait --pipe --collect --unit=ns08-strict-sockets-a5ygak "${PROPS[@]}" /usr/bin/python3 -c "$CODE"
SOCKET_RC=$?
echo "profile_probe_exit=$SOCKET_RC"
echo 'No-best-effort Landrun positive read and negative write controls under same unit profile:'
ALLOWED="$OPS/tools/landrun-control-allowed"
DENIED="$OPS/tools/landrun-control-denied"
mkdir -p "$ALLOWED" "$DENIED"
rm -f "$ALLOWED/read.txt" "$DENIED/strict-should-not-exist"
printf 'strict-profile-read-control\n' > "$ALLOWED/read.txt"
LR="$OPS/tools/landrun/landrun"
systemd-run --user --wait --pipe --collect --unit=ns08-strict-lr-read-a5ygak "${PROPS[@]}" "$LR" --ldd --add-exec --ro "$ALLOWED" /usr/bin/cat "$ALLOWED/read.txt"
READ_RC=$?
systemd-run --user --wait --pipe --collect --unit=ns08-strict-lr-write-a5ygak "${PROPS[@]}" "$LR" --ldd --add-exec --rw "$ALLOWED" /usr/bin/touch "$DENIED/strict-should-not-exist"
WRITE_RC=$?
test -e "$DENIED/strict-should-not-exist"; EXISTS=$?
echo "landrun_read_exit=$READ_RC landrun_denied_write_exit=$WRITE_RC denied_file_exists=$([ "$EXISTS" = 0 ] && echo yes || echo no)"
echo 'Available compiler versions:'
PATH="$OPS/tools/zig:$OPS/tools/go/bin:$OPS/tools/rust/bin:<WSL_HOME>/.elan/bin:$PATH"
command -v zig; zig version
command -v go; go version
command -v rustc; rustc --version
command -v lean; lean --version | head -n 1
echo 'Temporary compiler probes run only if local prerequisites exist.'
echo 'C probe:'
if command -v zig >/dev/null 2>&1; then printf 'int main(void){return 0;}\n' > "$OPS/ops/strict-probe.c"; zig cc "$OPS/ops/strict-probe.c" -o "$OPS/ops/strict-probe-c"; CBUILD_RC=$?; if [ "$CBUILD_RC" = 0 ]; then systemd-run --user --wait --pipe --collect --unit=ns08-strict-c-a5ygak "${PROPS[@]}" "$OPS/ops/strict-probe-c"; CRUN_RC=$?; else CRUN_RC=skip; fi; echo "c_build_exit=$CBUILD_RC c_run_exit=$CRUN_RC"; else echo 'C probe skipped: zig unavailable'; fi
echo 'Rust probe:'
if command -v rustc >/dev/null 2>&1; then printf 'fn main() {}\n' > "$OPS/ops/strict-probe.rs"; rustc "$OPS/ops/strict-probe.rs" -o "$OPS/ops/strict-probe-rust"; RBUILD_RC=$?; if [ "$RBUILD_RC" = 0 ]; then systemd-run --user --wait --pipe --collect --unit=ns08-strict-rust-a5ygak "${PROPS[@]}" "$OPS/ops/strict-probe-rust"; RRUN_RC=$?; else RRUN_RC=skip; fi; echo "rust_build_exit=$RBUILD_RC rust_run_exit=$RRUN_RC"; else echo 'Rust probe skipped: rustc unavailable'; fi
echo 'Lean probe:'
if command -v lean >/dev/null 2>&1; then printf 'def main : IO Unit := pure ()\n' > "$OPS/ops/StrictProbe.lean"; lean --run "$OPS/ops/StrictProbe.lean"; LBUILD_RC=$?; echo "lean_run_exit=$LBUILD_RC"; else echo 'Lean probe skipped: lean unavailable'; fi
echo 'Binary hashes:'
sha256sum "$LR" "$OPS/tools/zig/zig" "$OPS/ops/strict-probe-c" "$OPS/ops/strict-probe-rust" 2>/dev/null
echo "UTC end: $(date -u +%FT%TZ)"
exit 0
