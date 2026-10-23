set -u
date -u +%Y-%m-%dT%H:%M:%SZ
id
hostname
uname -a
cat /etc/os-release
nproc
free -h
df -h <WSL_HOME> /tmp
ps -eo pid,user,comm,pcpu,pmem,rss --sort=-rss | head -18
for tool in go rustc cargo cc gcc clang ld make time systemd-run systemctl curl git python3 elan lean lake; do
  command -v "$tool" || true
done
for tool in go rustc cargo cc gcc clang ld make; do
  if command -v "$tool" >/dev/null 2>&1; then
    if [ "$tool" = go ]; then "$tool" version; else "$tool" --version | head -2; fi
  fi
done
if [ -x /usr/bin/time ]; then /usr/bin/time --version | head -2; fi
ps -p 1 -o comm=
systemctl --user is-system-running
cat /sys/kernel/security/lsm
cat /proc/self/status | sed -n '/^Cap/p;/^NoNewPrivs/p;/^Seccomp/p'
python3 -c 'import ctypes,os,platform; assert platform.machine()=="x86_64"; libc=ctypes.CDLL(None,use_errno=True); abi=libc.syscall(444,0,0,1); print({"landlock_abi":abi,"errno":ctypes.get_errno()}); assert abi>0'
ls -la <WSL_HOME>/nse_audit_20261020
repo=<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler
cd "$repo"
git rev-parse HEAD
git status --porcelain=v1
git diff --stat
git ls-files -z | xargs -0 sha256sum
cat lean-toolchain
python3 -c 'import json; d=json.load(open("lake-manifest.json")); print(json.dumps({k:v for k,v in d.items() if k!="packages"},indent=2)); print(json.dumps([p for p in d["packages"] if p["name"] in ("Comparator","lean4export")],indent=2))'
for package in Comparator lean4export; do
  git -C ".lake/packages/$package" rev-parse HEAD
  git -C ".lake/packages/$package" status --porcelain=v1
done
sha256sum .lake/packages/Comparator/README.md
cat ComparatorChallenges/NavierStokes.json
cat ComparatorChallenges/Euler.json
ls -l .lake/packages/Comparator/.lake/build/bin/comparator .lake/packages/lean4export/.lake/build/bin/lean4export
