set -u
opsroot=<WSL_HOME>/ns08_validation_20261020_a5YGak
if [ -e "$opsroot" ]; then
  printf 'Target already exists: %s\n' "$opsroot"
  exit 3
fi
mkdir -p "$opsroot/tools" "$opsroot/results" "$opsroot/ops" "$opsroot/downloads"
exec > >(tee "$opsroot/results/preflight-tools-and-afunix.log") 2>&1
date -u +%Y-%m-%dT%H:%M:%SZ
ls -la <WSL_HOME>/.elan/bin <WSL_HOME>/.elan/toolchains
cd <WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler
<WSL_HOME>/.elan/bin/elan which lean
<WSL_HOME>/.elan/bin/lake --version
ls -la <WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin
ls -la <WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/lib
dpkg-query -W -f='${binary:Package} ${Version} ${Status}\n' gcc g++ clang libc6-dev linux-libc-dev build-essential make 2>&1
python3 -c 'import socket; s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); s.close(); print("BASELINE_AF_UNIX_ALLOWED")'
baseline_code=$?
systemd-run --user --wait --pipe --collect --unit=ns08-afunix-probe-a5ygak --property=RestrictAddressFamilies=~AF_UNIX /usr/bin/python3 -c '
import errno, socket
try:
    unix_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
except OSError as error:
    print("AF_UNIX_DENIED", error.errno, str(error))
    assert error.errno in (errno.EAFNOSUPPORT, errno.EPERM, errno.EACCES)
else:
    unix_socket.close()
    raise SystemExit("AF_UNIX_UNEXPECTEDLY_ALLOWED")
inet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
inet_socket.close()
print("AF_INET_SOCKET_CREATION_ALLOWED")
'
restricted_code=$?
printf 'BASELINE_EXIT=%s RESTRICTED_EXIT=%s\n' "$baseline_code" "$restricted_code"
date -u +%Y-%m-%dT%H:%M:%SZ
if [ "$baseline_code" -ne 0 ] || [ "$restricted_code" -ne 0 ]; then exit 1; fi
