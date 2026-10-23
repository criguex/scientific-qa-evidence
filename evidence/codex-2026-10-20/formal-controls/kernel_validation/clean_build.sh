#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

PIN=f9e8bc5b38b6e212696e8a30e3e91517af887bbd
REPO=
PRIVATE_ROOT=
EVIDENCE_DIR=
TOOLCHAIN_BIN=
SCRIPT=$(readlink -f "$0")

die() { printf 'INFRA_PENDING: %s\n' "$*" >&2; exit 90; }

if [[ "${1-}" == "--service" ]]; then
  [[ $# -eq 4 ]] || die "argumentos internos inválidos"
  WORK=$2 RAW=$3 TOOLCHAIN_BIN=$4
  trap 'exit 143' TERM
  trap 'exit 130' INT
  trap 'exit 129' HUP
  cd "$WORK"
  python3 - "$RAW/preflight.network.txt" <<'PY'
import errno, os, pathlib, socket, sys
status = dict(line.split(":", 1) for line in pathlib.Path("/proc/self/status").read_text().splitlines() if ":" in line)
if int(status.get("CapEff", "1"), 16) != 0 or status.get("NoNewPrivs", "").strip() != "1" or status.get("Seccomp", "").strip() != "2":
    raise SystemExit("service capability/seccomp guard failed")
for pid in (os.getpid(), os.getppid()):
    for fd in pathlib.Path(f"/proc/{pid}/fd").iterdir():
        try:
            if os.readlink(fd).startswith("socket:"):
                raise SystemExit("inherited socket fd found")
        except FileNotFoundError:
            pass
for family in (socket.AF_INET, socket.AF_UNIX):
    try:
        socket.socket(family, socket.SOCK_STREAM)
    except PermissionError as error:
        if error.errno != errno.EPERM:
            raise SystemExit(f"socket denial errno mismatch: {error.errno}")
    else:
        raise SystemExit(f"socket family unexpectedly available: {family}")
pathlib.Path(sys.argv[1]).write_text("CapEff=0\nNoNewPrivs=1\nSeccomp=2\nAF_INET=EPERM\nAF_UNIX=EPERM\ninherited_socket_fds=0\n")
PY
  date -u +%Y-%m-%dT%H:%M:%SZ > "$RAW/build.started_utc.txt"
  touch "$RAW/preflight.ready"
  for ((i=0; i<600; i++)); do
    [[ -e "$RAW/preflight.release" ]] && break
    [[ -e "$RAW/preflight.abort" ]] && exit 91
    sleep 0.2
  done
  [[ -e "$RAW/preflight.release" ]] || exit 92
  set +e
  /usr/bin/time -f 'elapsed_seconds=%e\nuser_seconds=%U\nsystem_seconds=%S\nmax_rss_kib=%M' -o "$RAW/build.time.txt" "$TOOLCHAIN_BIN/lake" --no-cache build > "$RAW/build.stdout.log" 2> "$RAW/build.stderr.log"
  RC=$?
  set -e
  printf '%s\n' "$RC" > "$RAW/build.exit_code.txt"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$RAW/build.finished_utc.txt"
  exit "$RC"
fi

while (($#)); do
  case "$1" in
    --repo) REPO=${2:?}; shift 2 ;;
    --private-root) PRIVATE_ROOT=${2:?}; shift 2 ;;
    --evidence-dir) EVIDENCE_DIR=${2:?}; shift 2 ;;
    --toolchain-bin) TOOLCHAIN_BIN=${2:?}; shift 2 ;;
    *) die "argumento desconocido: $1" ;;
  esac
done
[[ -n "$REPO" && -n "$PRIVATE_ROOT" && -n "$EVIDENCE_DIR" && -n "$TOOLCHAIN_BIN" ]] || die "uso: $SCRIPT --repo RUTA --private-root RUTA_NUEVA --evidence-dir RUTA_NUEVA --toolchain-bin RUTA"
REPO=$(realpath -e "$REPO")
PRIVATE_ROOT=$(realpath -m "$PRIVATE_ROOT")
EVIDENCE_DIR=$(realpath -m "$EVIDENCE_DIR")
TOOLCHAIN_BIN=$(realpath -e "$TOOLCHAIN_BIN")
[[ ! -e "$PRIVATE_ROOT" ]] || die "private-root ya existe"
[[ ! -e "$EVIDENCE_DIR" ]] || die "evidence-dir ya existe"
[[ "$EVIDENCE_DIR" != "$REPO" && "$EVIDENCE_DIR" != "$REPO"/* ]] || die "evidence-dir no puede estar dentro del checkout"
[[ "$PRIVATE_ROOT" != "$REPO" && "$PRIVATE_ROOT" != "$REPO"/* ]] || die "private-root no puede estar dentro del checkout"
[[ "$EVIDENCE_DIR" != "$PRIVATE_ROOT" && "$EVIDENCE_DIR" == "$PRIVATE_ROOT"/* ]] || die "evidence-dir debe ser una subcarpeta nueva de private-root"

mkdir -m 700 -p "$PRIVATE_ROOT"
mkdir -m 755 -p "$EVIDENCE_DIR"
RAW="$PRIVATE_ROOT/raw"
WORK="$PRIVATE_ROOT/workspace"
mkdir -m 700 "$RAW"
START_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)
START_EPOCH=$(date +%s)
RC=90
PHASE=preflight
COMMIT=
ARCHIVE_SHA=
INVENTORY_SHA=
MANIFEST_SHA=
TOOLCHAIN_SHA=
UNIT=

finish() {
  local exit_rc=$?
  trap - EXIT
  if ((exit_rc != 0)) && [[ -n "$UNIT" ]]; then
    touch "$RAW/preflight.abort" 2>/dev/null || true
    systemctl --user stop "$UNIT" >/dev/null 2>&1 || true
    journalctl --user -u "$UNIT" --no-pager > "$RAW/systemd.journal.log" 2>&1 || true
  fi
  local ended duration
  ended=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  duration=$(( $(date +%s) - START_EPOCH ))
  printf '%s\n' "$exit_rc" > "$RAW/exit_code.txt"
  printf '%s\n' "$ended" > "$RAW/finished_utc.txt"
  python3 - "$RAW" "$EVIDENCE_DIR" "$SCRIPT" "$REPO" "$PRIVATE_ROOT" "$WORK" "$TOOLCHAIN_BIN" "$START_UTC" "$ended" "$duration" "$PHASE" "$COMMIT" "$ARCHIVE_SHA" "$INVENTORY_SHA" "$MANIFEST_SHA" "$TOOLCHAIN_SHA" "$UNIT" "$exit_rc" <<'PY'
import hashlib, json, os, pathlib, re, sys
raw, public, script, repo, private, work, toolchain, started, ended, seconds, phase, commit, archive, inventory, manifest, toolhash, unit, rc = sys.argv[1:]
raw, public = pathlib.Path(raw), pathlib.Path(public)
def digest(path):
    try:
        return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
    except OSError:
        return None
replacements = [(x, token) for x, token in ((repo, "<SOURCE_CHECKOUT>"), (private, "<PRIVATE_ROOT>"), (work, "<CLEAN_WORKSPACE>"), (toolchain, "<LEAN_TOOLCHAIN_BIN>")) if x]
def scrub(text):
    text = text.replace(os.uname().nodename, "<HOST>")
    for value, token in sorted(replacements, key=lambda pair: len(pair[0]), reverse=True):
        text = text.replace(value, token)
    text = re.sub(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])", "<IP>", text)
    text = re.sub(r"/(?:home|Users)/[^/\s]+", "/<USER>", text)
    text = re.sub(r"user-\d+\.slice|user@\d+\.service", "<USER_SLICE>", text)
    return text
for name in ("build.stdout.log", "build.stderr.log", "service.stdout.log", "service.stderr.log", "systemd.stdout.log", "systemd.stderr.log", "systemd.journal.log", "systemd.properties.txt", "command.txt", "preflight.txt", "preflight.network.txt", "tool_versions.txt", "toolchain.sha256", "build.time.txt", "build.started_utc.txt", "build.finished_utc.txt", "build.exit_code.txt"):
    source = raw / name
    if source.is_file():
        (public / name).write_text(scrub(source.read_text(errors="replace")), encoding="utf-8")
build_exit_path = raw / "build.exit_code.txt"
build_exit = int(build_exit_path.read_text().strip()) if build_exit_path.is_file() else None
build_complete = all((raw / name).is_file() for name in ("build.stdout.log", "build.finished_utc.txt", "build.time.txt"))
def classify(run_phase, run_exit, kernel_exit, evidence_complete):
    return run_phase == "complete" and int(run_exit) == 0 and kernel_exit == 0 and evidence_complete
assert classify("preflight", 0, None, False) is False
assert classify("service_start", 0, 0, False) is False
passed = classify(phase, rc, build_exit, build_complete)
status = "PASS" if passed else ("BUILD_FAILED" if build_complete and build_exit not in (None, 0) else "INFRA_INCONCLUSIVE")
network_status = "preflight probó sockets AF_INET y AF_UNIX bajo el perfil; no acredita sandbox hermética" if (raw / "preflight.network.txt").is_file() else "preflight de sockets no completado"
summary = {
    "scope": "build completo de fuentes en checkout limpio; dependencias reutilizadas; no valida teoremas ni kernels",
    "started_utc": started, "finished_utc": ended, "duration_seconds": int(seconds),
    "phase": phase, "exit_code": int(rc), "build_exit_code": build_exit,
    "build_complete_evidence_present": build_complete, "status": status, "passed": passed,
    "commit": commit or None, "archive_sha256": archive or None,
    "source_inventory_sha256": inventory or None, "lake_manifest_sha256": manifest or None,
    "toolchain_binaries_sha256": toolhash or None, "launcher_sha256": digest(script),
    "systemd_unit": unit or None,
    "limits": {"cpu_quota": "600%", "memory_max_bytes": 25769803776, "runtime_max_seconds": 7200, "lean_num_threads": 6},
    "network_scope": network_status,
}
(public / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
  exit "$exit_rc"
}
trap 'exit 143' TERM
trap 'exit 130' INT
trap 'exit 129' HUP
trap finish EXIT

[[ -x "$TOOLCHAIN_BIN/lake" && -x "$TOOLCHAIN_BIN/lean" ]] || die "faltan lake/lean en toolchain"
[[ "$(git -C "$REPO" rev-parse HEAD)" == "$PIN" ]] || die "checkout no coincide con el commit fijado"
[[ -z "$(git -C "$REPO" status --porcelain=v1)" ]] || die "checkout formal no está limpio"
COMMIT=$PIN
[[ -d "$REPO/.lake/packages" ]] || die "cache .lake/packages ausente; no se descargarán dependencias"
[[ -f "$REPO/lake-manifest.json" && -f "$REPO/lean-toolchain" ]] || die "manifest o toolchain ausente"
[[ "$(<"$REPO/lean-toolchain")" == "leanprover/lean4:v4.34.0-rc2" ]] || die "lean-toolchain no coincide con el pin"

git -C "$REPO" archive --format=tar "$PIN" > "$PRIVATE_ROOT/source.tar"
ARCHIVE_SHA=$(sha256sum "$PRIVATE_ROOT/source.tar" | awk '{print $1}')
mkdir -m 700 "$WORK"
tar -xf "$PRIVATE_ROOT/source.tar" -C "$WORK"
[[ -z "$(find "$WORK" -type f -name '*.olean' -print -quit)" ]] || die "el archivo fuente limpio contiene .olean"
[[ ! -e "$WORK/.lake/build" ]] || die "el archivo fuente contiene build del proyecto"

(cd "$WORK" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$RAW/source_inventory.sha256"
INVENTORY_SHA=$(sha256sum "$RAW/source_inventory.sha256" | awk '{print $1}')
MANIFEST_SHA=$(sha256sum "$WORK/lake-manifest.json" | awk '{print $1}')

python3 - "$REPO/.lake/packages" "$REPO/lake-manifest.json" "$RAW/dependency_pins.txt" <<'PY'
import json, pathlib, subprocess, sys
root, manifest, output = pathlib.Path(sys.argv[1]), json.loads(pathlib.Path(sys.argv[2]).read_text()), pathlib.Path(sys.argv[3])
lines = []
for package in manifest.get("packages", []):
    name, revision = package["name"], package["rev"]
    path = root / name
    if not path.is_dir():
        raise SystemExit(f"missing cached dependency: {name}")
    head = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], text=True, capture_output=True)
    dirty = subprocess.run(["git", "-C", str(path), "status", "--porcelain=v1"], text=True, capture_output=True)
    if head.returncode or dirty.returncode or head.stdout.strip() != revision or dirty.stdout:
        raise SystemExit(f"dependency pin/status mismatch: {name}")
    lines.append(f"{name} {revision}")
output.write_text("\n".join(lines) + "\n")
PY

mkdir -p "$WORK/.lake"
cp -a "$REPO/.lake/packages" "$WORK/.lake/"
(
  cd "$TOOLCHAIN_BIN"
  sha256sum lake lean
) > "$RAW/toolchain.sha256"
TOOLCHAIN_SHA=$(sha256sum "$RAW/toolchain.sha256" | awk '{print $1}')
"$TOOLCHAIN_BIN/lake" --version > "$RAW/tool_versions.txt" 2>&1
"$TOOLCHAIN_BIN/lean" --version >> "$RAW/tool_versions.txt" 2>&1
cp "$RAW/source_inventory.sha256" "$EVIDENCE_DIR/"
cp "$RAW/dependency_pins.txt" "$EVIDENCE_DIR/"
printf 'source_archive_sha256=%s\nsource_inventory_sha256=%s\nlake_manifest_sha256=%s\nlean_toolchain=%s\n' "$ARCHIVE_SHA" "$INVENTORY_SHA" "$MANIFEST_SHA" "leanprover/lean4:v4.34.0-rc2" > "$RAW/preflight.txt"
PHASE=service_start
UNIT="adv050-clean-build-$(date -u +%Y%m%dT%H%M%SZ)-$$"
printf 'invocation=' > "$RAW/command.txt"
printf '%q ' "$SCRIPT" --repo "$REPO" --private-root "$PRIVATE_ROOT" --evidence-dir "$EVIDENCE_DIR" --toolchain-bin "$TOOLCHAIN_BIN" >> "$RAW/command.txt"
printf '\n' >> "$RAW/command.txt"
printf 'systemd_run=systemd-run --user --wait --unit=%q --property=RestrictAddressFamilies=~AF_UNIX --property=SystemCallArchitectures=native --property=SystemCallFilter=~@network-io,io_uring_setup,io_uring_enter,io_uring_register --property=SystemCallErrorNumber=EPERM --property=NoNewPrivileges=yes --property=MemoryMax=25769803776 --property=CPUQuota=600%% --property=RuntimeMaxSec=2h --property=StandardInput=null --property=StandardOutput=append:<PRIVATE_ROOT>/raw/service.stdout.log --property=StandardError=append:<PRIVATE_ROOT>/raw/service.stderr.log\n' "$UNIT" >> "$RAW/command.txt"
printf 'service_command=/usr/bin/bash %q --service %q %q %q\ninner_command=%q --no-cache build\nLEAN_NUM_THREADS=6\n' "$SCRIPT" "$WORK" "$RAW" "$TOOLCHAIN_BIN" "$TOOLCHAIN_BIN/lake" >> "$RAW/command.txt"

set +e
systemd-run --user --wait --unit="$UNIT" --property=RestrictAddressFamilies=~AF_UNIX \
  --property=SystemCallArchitectures=native \
  '--property=SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register' \
  --property=SystemCallErrorNumber=EPERM --property=NoNewPrivileges=yes \
  --property=MemoryMax=25769803776 --property=CPUQuota=600% --property=RuntimeMaxSec=2h \
  --property=StandardInput=null --property="StandardOutput=append:$RAW/service.stdout.log" \
  --property="StandardError=append:$RAW/service.stderr.log" \
  -E "PATH=$TOOLCHAIN_BIN:/usr/bin:/bin" -E LEAN_NUM_THREADS=6 \
  /usr/bin/bash "$SCRIPT" --service "$WORK" "$RAW" "$TOOLCHAIN_BIN" \
  > "$RAW/systemd.stdout.log" 2> "$RAW/systemd.stderr.log" &
SYSTEMD_PID=$!
set -e

for ((i=0; i<600; i++)); do
  if [[ -f "$RAW/preflight.ready" ]]; then break; fi
  if ! kill -0 "$SYSTEMD_PID" 2>/dev/null; then die "systemd-run terminó antes del preflight"; fi
  sleep 0.2
done
[[ -f "$RAW/preflight.ready" ]] || { systemctl --user stop "$UNIT" >/dev/null 2>&1 || true; die "timeout esperando preflight de la unidad"; }
systemctl --user show "$UNIT" --property=ActiveState --property=RestrictAddressFamilies --property=SystemCallArchitectures --property=SystemCallFilter --property=SystemCallErrorNumber --property=NoNewPrivileges --property=MemoryMax --property=CPUQuotaPerSecUSec --property=RuntimeMaxUSec --property=StandardInput --property=StandardOutput --property=StandardError --property=ControlGroup > "$RAW/systemd.properties.txt"
python3 - "$RAW/systemd.properties.txt" <<'PY'
import pathlib, sys
p = dict(line.split("=", 1) for line in pathlib.Path(sys.argv[1]).read_text().splitlines() if "=" in line)
expected = {"ActiveState": "active", "RestrictAddressFamilies": "~AF_UNIX", "SystemCallArchitectures": "native", "SystemCallErrorNumber": "1", "NoNewPrivileges": "yes", "MemoryMax": "25769803776", "CPUQuotaPerSecUSec": "6s", "RuntimeMaxUSec": "2h", "StandardInput": "null", "StandardOutput": "append", "StandardError": "append"}
bad = [f"{key}: expected {value}, got {p.get(key)}" for key, value in expected.items() if p.get(key) != value]
filter_value = p.get("SystemCallFilter", "")
rules = filter_value.lstrip("~").split()
network_denied = "@network-io" in rules or all(name in rules for name in ("socket", "socketpair", "connect"))
if not filter_value.startswith("~") or not network_denied or any(name not in rules for name in ("io_uring_setup", "io_uring_enter", "io_uring_register")):
    bad.append("SystemCallFilter does not match deny profile")
if not p.get("ControlGroup", "").startswith("/"):
    bad.append("ControlGroup missing")
if bad:
    raise SystemExit("\n".join(bad))
PY
touch "$RAW/preflight.release"
PHASE=lake_build
set +e
wait "$SYSTEMD_PID"
RC=$?
set -e
SYSTEMD_RC=$RC
if [[ -f "$RAW/build.exit_code.txt" && -f "$RAW/build.finished_utc.txt" && -f "$RAW/build.stdout.log" && -f "$RAW/build.time.txt" ]]; then
  BUILD_RC=$(<"$RAW/build.exit_code.txt")
  if [[ "$BUILD_RC" == 0 && "$SYSTEMD_RC" == 0 ]]; then
    RC=0
    PHASE=complete
  else
    RC=${BUILD_RC:-$SYSTEMD_RC}
    ((RC != 0)) || RC=94
    PHASE=build_failed
  fi
else
  ((SYSTEMD_RC != 0)) || SYSTEMD_RC=95
  RC=$SYSTEMD_RC
  PHASE=infra_inconclusive
fi
exit "$RC"
