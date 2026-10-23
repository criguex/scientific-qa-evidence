#!/usr/bin/env bash
set -euo pipefail
umask 077

OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
REPO=<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler
ROOT="$OPS/calibration_20261020T1944Z_ns08cal_6tuj6v"
COMPARATOR="$REPO/.lake/packages/Comparator/.lake/build/bin/comparator"
LEAN4EXPORT="$REPO/.lake/packages/lean4export/.lake/build/bin/lean4export"
NANODA="$OPS/tools/nanoda/target/release/nanoda_bin"
LANDRUN="$OPS/tools/landrun/landrun"
LAKE=<WSL_HOME>/.elan/bin/lake
LEAN=<WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/lean

die() { echo "INFRA_PENDING: $*" >&2; exit 90; }

# systemd-run invokes this exact file in service mode so the full argv and
# runner source remain recoverable from the script hash and command log.
if [[ "${1-}" == "--service" ]]; then
  [[ $# -eq 6 ]] || die "bad --service argument count"
  OUT=$2 ERR=$3 TIMELOG=$4 COMPARATOR_BIN=$5 CONFIG=$6
  date -u +%FT%TZ > "${OUT%.stdout.log}.start_utc.txt"
  if python3 -c 'import os,sys
p="/proc/"+sys.argv[1]+"/fd"; sockets=[]
for n in os.listdir(p):
 try:
  t=os.readlink(p+"/"+n)
  if t.startswith("socket:"): sockets.append((n,t))
 except OSError: pass
print("service_socket_fds="+repr(sockets)); raise SystemExit(bool(sockets))' "$$" > "${OUT%.stdout.log}.guard.txt" 2>&1; then GUARD_RC=0; else GUARD_RC=$?; fi
  CAP=$(awk '/^CapEff:/ {print $2}' /proc/self/status)
  NNP=$(awk '/^NoNewPrivs:/ {print $2}' /proc/self/status)
  SECCOMP=$(awk '/^Seccomp:/ {print $2}' /proc/self/status)
  printf 'socket_guard_exit=%s CapEff=%s NoNewPrivs=%s Seccomp=%s\n' "$GUARD_RC" "$CAP" "$NNP" "$SECCOMP" >> "${OUT%.stdout.log}.guard.txt"
  cat /proc/self/cgroup > "${OUT%.stdout.log}.cgroup.txt"
  if [[ "$GUARD_RC" -ne 0 || "$CAP" != 0000000000000000 || "$NNP" != 1 || "$SECCOMP" != 2 ]]; then
    printf 'infra_guard_failure=1\n' > "${OUT%.stdout.log}.process-status.txt"
    exit 91
  fi
  set +e
  /usr/bin/time -v -o "$TIMELOG" "$LAKE" env "$COMPARATOR_BIN" "$CONFIG" > "$OUT" 2> "$ERR"
  RC=$?
  set -e
  printf 'comparator_exit=%s\n' "$RC" > "${OUT%.stdout.log}.process-status.txt"
  date -u +%FT%TZ > "${OUT%.stdout.log}.end_utc.txt"
  exit "$RC"
fi

# Guarded remote launcher. Deliberately refuses to run without explicit GO at
# its caller; this local copy is not run automatically.
if [[ "${1-}" != "--execute" || $# -ne 1 ]]; then
  echo "usage: $0 --execute (or internal --service ...)" >&2
  exit 64
fi

SCRIPT_PATH=$(readlink -f "$0")
[[ "$SCRIPT_PATH" == "$ROOT/run-calibration-remote.sh" ]] || die "launcher must be staged at $ROOT/run-calibration-remote.sh"

check_hash() {
  local file=$1 expected=$2 actual
  actual=$(sha256sum "$file" | awk '{print $1}') || die "cannot hash $file"
  [[ "$actual" == "$expected" ]] || die "SHA256 mismatch: $file ($actual)"
}

[[ -d "$ROOT" ]] || die "remote fixture directory missing: $ROOT"
[[ ! -e "$ROOT/results" ]] || die "results directory already exists; refusing overwrite"
[[ "$(git -C "$REPO" rev-parse HEAD)" == f9e8bc5b38b6e212696e8a30e3e91517af887bbd ]] || die "formal checkout pin changed"
[[ -z "$(git -C "$REPO" status --porcelain=v1)" ]] || die "formal checkout dirty"
[[ "$(git -C "$REPO/.lake/packages/Comparator" rev-parse HEAD)" == 19e111e2141cf333c7daff0f64c5f24acc91dd2e ]] || die "Comparator pin changed"
[[ -z "$(git -C "$REPO/.lake/packages/Comparator" status --porcelain=v1)" ]] || die "Comparator tree dirty"
[[ "$(git -C "$REPO/.lake/packages/lean4export" rev-parse HEAD)" == cacf989bd75f608700820f6afc595f32e7a99a4d ]] || die "lean4export pin changed"
[[ -z "$(git -C "$REPO/.lake/packages/lean4export" status --porcelain=v1)" ]] || die "lean4export tree dirty"
[[ "$(git -C "$OPS/tools/nanoda" rev-parse HEAD)" == 9d6964f78d0fa4c93fd22fe956e17afe7e72a441 ]] || die "nanoda pin changed"
[[ -z "$(git -C "$OPS/tools/nanoda" status --porcelain=v1)" ]] || die "nanoda tree dirty"
[[ "$(git -C "$OPS/tools/landrun" rev-parse HEAD)" == ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a ]] || die "Landrun pin changed"
[[ -z "$(git -C "$OPS/tools/landrun" status --porcelain=v1)" ]] || die "Landrun tree dirty"

check_hash "$COMPARATOR" 514de8d2acbd6e0102575cd2c575e336b7c4a40daf3ae66abe97cef5e1e6b02a
check_hash "$LEAN4EXPORT" 4fa9e14cada304109e85da5048bcd411cf781a03539b3e50953e5c537074bd9e
check_hash "$NANODA" ccda52587ef42760dff9bc2de26edca0cb6ad207c8719cfffcd1e7daab22ccfb
check_hash "$LANDRUN" e3d26ebf2f7c786f8d34b7051ad2c655329aeadbb863404e3dd05d3a97b0518a
check_hash "$LEAN" e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550

check_hash "$ROOT/cases/positive/lean-toolchain" 8190e75a201741065fe508b28955dd64dd72d090babe5f70ce6848879d68ae88
check_hash "$ROOT/cases/positive/lakefile.toml" 5a865f30cd848c96af7ae145335d1206b440cbf2bf72f3fbf9b1f1b4056ee724
check_hash "$ROOT/cases/positive/config.json" 4fff5bf4ebcb5666c718d6a774b392fd6a43cad0c8c5e1ca6c51ea850db082bc
check_hash "$ROOT/cases/positive/Challenge.lean" 0d4a77ab995c3ebb09c58fb2a82db3eb48b5898907c65df29688694d07aba4d6
check_hash "$ROOT/cases/positive/Solution.lean" 0d4a77ab995c3ebb09c58fb2a82db3eb48b5898907c65df29688694d07aba4d6

check_hash "$ROOT/cases/mismatch/lean-toolchain" 8190e75a201741065fe508b28955dd64dd72d090babe5f70ce6848879d68ae88
check_hash "$ROOT/cases/mismatch/lakefile.toml" 485eacc8c74ecddd45d5259bedacde6883a85d5ccec556b4724ec8ad02fc0bf9
check_hash "$ROOT/cases/mismatch/config.json" 4fff5bf4ebcb5666c718d6a774b392fd6a43cad0c8c5e1ca6c51ea850db082bc
check_hash "$ROOT/cases/mismatch/Challenge.lean" 0d4a77ab995c3ebb09c58fb2a82db3eb48b5898907c65df29688694d07aba4d6
check_hash "$ROOT/cases/mismatch/Solution.lean" 4420c80f4e3248c5e03ebf62e2add2d4d94b620726bcd2bf1e108e65707b98d4

check_hash "$ROOT/cases/axiom/lean-toolchain" 8190e75a201741065fe508b28955dd64dd72d090babe5f70ce6848879d68ae88
check_hash "$ROOT/cases/axiom/lakefile.toml" 183ef39ee7b79c5e17d9fcae9cdcea724eb0c2566c81e8d3998c0ba627e96396
check_hash "$ROOT/cases/axiom/config.json" 4fff5bf4ebcb5666c718d6a774b392fd6a43cad0c8c5e1ca6c51ea850db082bc
check_hash "$ROOT/cases/axiom/Challenge.lean" ad777397fec00027e82304d9b5261e1d75154822b50b4581b5c9e6e0c64f8cf7
check_hash "$ROOT/cases/axiom/Solution.lean" d7fbcda73f36af87f525becd5bd8f814fa8ef3d0e1dfb62323f8260e7e30feec

mkdir -m 700 "$ROOT/results"
finalize_results() {
  local rc=$?
  trap - EXIT
  if [[ -d "$ROOT/results" ]]; then
    date -u +%FT%TZ > "$ROOT/results/launcher_finished_utc.txt" || true
    find "$ROOT/results" -type f ! -name all-results.sha256 -print0 | sort -z | xargs -0 sha256sum > "$ROOT/results/all-results.sha256" || true
  fi
  exit "$rc"
}
trap finalize_results EXIT
date -u +%FT%TZ > "$ROOT/results/launcher_start_utc.txt"
cp "$SCRIPT_PATH" "$ROOT/results/run-calibration-remote.sh"
sha256sum "$SCRIPT_PATH" > "$ROOT/results/launcher-source.sha256"
sha256sum "$COMPARATOR" "$LEAN4EXPORT" "$NANODA" "$LANDRUN" > "$ROOT/results/tool-binaries.sha256"
{
  printf 'formal_commit=%s\n' "$(git -C "$REPO" rev-parse HEAD)"
  printf 'comparator_commit=%s\n' "$(git -C "$REPO/.lake/packages/Comparator" rev-parse HEAD)"
  printf 'lean4export_commit=%s\n' "$(git -C "$REPO/.lake/packages/lean4export" rev-parse HEAD)"
  printf 'nanoda_commit=%s\n' "$(git -C "$OPS/tools/nanoda" rev-parse HEAD)"
  printf 'landrun_commit=%s\n' "$(git -C "$OPS/tools/landrun" rev-parse HEAD)"
  "$LAKE" --version
  printf 'lean_binary=%s\n' "$LEAN"
  "$LEAN" --version
  "$LANDRUN" --version
  grep -n -E '^(name|version)\s*=' "$OPS/tools/nanoda/Cargo.toml" | head -2
} > "$ROOT/results/pins-and-versions.txt" 2>&1

validate_build_exports() {
  local stdout=$1 stderr=$2
  python3 - "$stdout" "$stderr" <<'PY'
import pathlib, sys
text = pathlib.Path(sys.argv[1]).read_text(errors="replace") + "\n" + pathlib.Path(sys.argv[2]).read_text(errors="replace")
lines = text.splitlines()
builds = [i for i, line in enumerate(lines) if line.startswith("Build completed successfully")]
challenge = [i for i, line in enumerate(lines) if line.startswith("Exporting #[") and line.endswith(" from Challenge")]
solution = [i for i, line in enumerate(lines) if line.startswith("Exporting #[") and line.endswith(" from Solution")]
if len(builds) != 2 or len(challenge) != 1 or len(solution) != 1:
    print(f"builds={len(builds)} challenge_exports={len(challenge)} solution_exports={len(solution)}")
    raise SystemExit(1)
if not (builds[0] < challenge[0] < builds[1] < solution[0]):
    print("unexpected build/export ordering")
    raise SystemExit(1)
print("two successful builds and both exports present in Comparator output")
PY
}

validate_negative_output() {
  local stdout=$1 stderr=$2 expected_message=$3
  python3 - "$stdout" "$stderr" "$expected_message" <<'PY'
import pathlib, sys
out = pathlib.Path(sys.argv[1]).read_text(errors="replace")
err = pathlib.Path(sys.argv[2]).read_text(errors="replace")
text = out + "\n" + err
message = sys.argv[3]
if text.count(message) != 1:
    print(f"expected diagnostic count={text.count(message)}")
    raise SystemExit(1)
if any(token in text for token in (
    "Running nanoda kernel", "Running Lean default kernel",
    "nanoda kernel accepts", "Lean default kernel accepts",
    "nanoda kernel rejected", "Lean default kernel rejected")):
    print("negative unexpectedly reached or reported a kernel")
    raise SystemExit(1)
lines = out.splitlines()
builds = [i for i, line in enumerate(lines) if line.startswith("Build completed successfully")]
challenge = [i for i, line in enumerate(lines) if line.startswith("Exporting #[") and line.endswith(" from Challenge")]
solution = [i for i, line in enumerate(lines) if line.startswith("Exporting #[") and line.endswith(" from Solution")]
if len(builds) != 2 or len(challenge) != 1 or len(solution) != 1:
    print(f"builds={len(builds)} challenge_exports={len(challenge)} solution_exports={len(solution)}")
    raise SystemExit(1)
if not (builds[0] < challenge[0] < builds[1] < solution[0]):
    print("unexpected build/export order in stdout")
    raise SystemExit(1)
print("two builds and both exports recorded in stdout; one expected Comparator-stage diagnostic appears; pinned code order runs compare/check only after build/export returns; no kernel was invoked")
PY
}

run_case() {
  local case_name=$1 expected=$2 case_dir="$ROOT/cases/$1" result_dir="$ROOT/results/$1"
  local unit="ns08-cal-${case_name}-20261020t1944z-6tuj6v"
  local stdout="$result_dir/comparator.stdout.log" stderr="$result_dir/comparator.stderr.log"
  local time_log="$result_dir/time.log" unit_out="$result_dir/unit.stdout.log" unit_err="$result_dir/unit.stderr.log"
  local service_rc show_rc result exec_status comparator_exit time_exit journal_rc active_state
  mkdir -m 700 "$result_dir"
  : > "$result_dir/validation.log"
  date -u +%FT%TZ > "$result_dir/requested_start_utc.txt"
  {
    printf 'UTC=%s\ncase=%s\nunit=%s\nworking_directory=%s\n' "$(cat "$result_dir/requested_start_utc.txt")" "$case_name" "$unit" "$case_dir"
    printf 'command=%q ' "$LAKE" env "$COMPARATOR" "$case_dir/config.json"
    printf '\n'
    printf 'systemd-run --user --wait --unit=%q --working-directory=%q ' "$unit" "$case_dir"
    printf '%q ' \
      --property=RestrictAddressFamilies=~AF_UNIX \
      --property=SystemCallArchitectures=native \
      '--property=SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register' \
      --property=NoNewPrivileges=yes \
      --property=SystemCallErrorNumber=EPERM \
      --property=MemoryMax=28991029248 \
      --property=CPUQuota=800% \
      --property=RuntimeMaxSec=8h \
      --property=StandardInput=null \
      "--property=StandardOutput=append:$unit_out" \
      "--property=StandardError=append:$unit_err"
    printf '\n'
  } > "$result_dir/command.txt"

  local -a CMD=(systemd-run --user --wait --unit="$unit" --working-directory="$case_dir"
    --property=RestrictAddressFamilies=~AF_UNIX
    --property=SystemCallArchitectures=native
    '--property=SystemCallFilter=~@network-io io_uring_setup io_uring_enter io_uring_register'
    --property=NoNewPrivileges=yes
    --property=SystemCallErrorNumber=EPERM
    --property=MemoryMax=28991029248
    --property=CPUQuota=800%
    --property=RuntimeMaxSec=8h
    --property=StandardInput=null
    "--property=StandardOutput=append:$unit_out"
    "--property=StandardError=append:$unit_err"
    -E PATH=<WSL_HOME>/.elan/bin:/usr/bin:/bin
    -E "COMPARATOR_LANDRUN=$LANDRUN"
    -E "COMPARATOR_LEAN4EXPORT=$LEAN4EXPORT"
    -E "COMPARATOR_NANODA=$NANODA"
    /usr/bin/bash "$SCRIPT_PATH" --service "$stdout" "$stderr" "$time_log" "$COMPARATOR" "$case_dir/config.json")
  {
    printf 'launcher_sha256='
    sha256sum "$SCRIPT_PATH" | awk '{print $1}'
    printf 'argv='
    printf '%q ' "${CMD[@]}"
    printf '\n'
  } >> "$result_dir/command.txt"
  set +e
  "${CMD[@]}" > "$result_dir/launcher.stdout.log" 2> "$result_dir/launcher.stderr.log" &
  local launch_pid=$!
  while kill -0 "$launch_pid" 2>/dev/null; do
    systemctl --user show "$unit" \
      --property=ActiveState --property=ControlGroup --property=RestrictAddressFamilies \
      --property=RestrictAddressFamiliesAllowList --property=SystemCallArchitectures \
      --property=SystemCallFilter --property=SystemCallFilterAllowList \
      --property=NoNewPrivileges --property=SystemCallErrorNumber \
      --property=MemoryMax --property=CPUQuotaPerSecUSec --property=RuntimeMaxUSec \
      --property=StandardInput --property=StandardOutput --property=StandardError \
      > "$result_dir/unit-profile-poll.txt" 2> "$result_dir/unit-profile-poll.stderr.log"
    active_state=$(sed -n 's/^ActiveState=//p' "$result_dir/unit-profile-poll.txt" | head -1)
    if [[ "$active_state" == active ]]; then
      cp "$result_dir/unit-profile-poll.txt" "$result_dir/unit-profile-active.txt"
      break
    fi
    sleep 0.1
  done
  wait "$launch_pid"
  service_rc=$?
  set -e
  printf 'systemd_run_exit=%s\n' "$service_rc" > "$result_dir/systemd-run-status.txt"

  set +e
  systemctl --user show "$unit" \
    --property=Result --property=ExecMainCode --property=ExecMainStatus \
    --property=ActiveState --property=SubState --property=ActiveEnterTimestamp \
    --property=InactiveEnterTimestamp --property=ControlGroup --property=MemoryCurrent \
    --property=MemoryPeak --property=CPUUsageNSec \
    --property=RestrictAddressFamilies --property=RestrictAddressFamiliesAllowList \
    --property=SystemCallArchitectures --property=SystemCallFilter \
    --property=SystemCallFilterAllowList --property=NoNewPrivileges \
    --property=SystemCallErrorNumber --property=MemoryMax \
    --property=CPUQuotaPerSecUSec --property=RuntimeMaxUSec \
    --property=StandardInput --property=StandardOutput --property=StandardError \
    > "$result_dir/unit-properties.txt" 2> "$result_dir/unit-query.stderr.log"
  show_rc=$?
  set -e
  printf 'systemctl_show_exit=%s\n' "$show_rc" >> "$result_dir/unit-properties.txt"
  set +e
  journalctl --user --unit="$unit" --no-pager --output=short-iso-precise > "$result_dir/journal.log" 2> "$result_dir/journal.stderr.log"
  journal_rc=$?
  set -e
  printf 'journalctl_exit=%s\n' "$journal_rc" >> "$result_dir/journal.log"
  result=$(sed -n 's/^Result=//p' "$result_dir/unit-properties.txt" | head -1)
  exec_status=$(sed -n 's/^ExecMainStatus=//p' "$result_dir/unit-properties.txt" | head -1)
  printf 'systemd_result=%s\nexec_main_status=%s\n' "${result:-MISSING}" "${exec_status:-MISSING}" >> "$result_dir/systemd-run-status.txt"
  comparator_exit=$(sed -n 's/^comparator_exit=//p' "${stdout%.stdout.log}.process-status.txt" 2>/dev/null | head -1) || comparator_exit=
  time_exit=$(sed -n 's/^[[:space:]]*Exit status:[[:space:]]*//p' "$time_log" 2>/dev/null | head -1) || time_exit=
  printf 'comparator_exit=%s\ngnu_time_exit_status=%s\n' "${comparator_exit:-MISSING}" "${time_exit:-MISSING}" >> "$result_dir/systemd-run-status.txt"

  local case_rc=0
  if [[ ! -s "${stdout%.stdout.log}.guard.txt" || ! -s "${stdout%.stdout.log}.process-status.txt" ]]; then
    printf 'classification=INFRA_PENDING_missing_service_guard_or_status\n' > "$result_dir/classification.txt"
    case_rc=90
  elif grep -q 'infra_guard_failure=1' "${stdout%.stdout.log}.process-status.txt"; then
    printf 'classification=INFRA_PENDING_guard_failed\n' > "$result_dir/classification.txt"
    case_rc=90
  elif [[ "$show_rc" -ne 0 || "$journal_rc" -ne 0 || ! -s "$result_dir/unit-properties.txt" || ! -s "$result_dir/journal.log" ]]; then
    printf 'classification=INFRA_PENDING_manager_or_journal_record_missing\n' > "$result_dir/classification.txt"
    case_rc=90
  else
    local missing_property=
    for property in RestrictAddressFamilies RestrictAddressFamiliesAllowList SystemCallArchitectures SystemCallFilter SystemCallFilterAllowList NoNewPrivileges SystemCallErrorNumber MemoryMax CPUQuotaPerSecUSec RuntimeMaxUSec StandardInput StandardOutput StandardError; do
      if ! grep -q "^${property}=" "$result_dir/unit-properties.txt"; then
        missing_property=$property
        break
      fi
    done
    if [[ -n "$missing_property" ]]; then
      printf 'classification=INFRA_PENDING_manager_property_missing:%s\n' "$missing_property" > "$result_dir/classification.txt"
      case_rc=90
    else
      case "$expected" in
        positive)
          if [[ "$service_rc" -eq 0 && "$result" == success && "$exec_status" == 0 && \
                "$comparator_exit" == 0 && "$time_exit" == 0 && -s "$time_log" ]] && \
             validate_build_exports "$stdout" "$stderr" >> "$result_dir/validation.log" 2>&1 && \
             grep -Fq 'nanoda kernel accepts the solution' "$stdout" && \
             grep -Fq 'Lean default kernel accepts the solution' "$stdout" && \
             grep -Fq 'Your solution is okay!' "$stdout"; then
            printf 'PASS_RESPONSE_PATH_PENDING_ROOT_PROFILE_REVIEW: positive\n' > "$result_dir/classification.txt"
          else
            printf 'classification=INFRA_PENDING_or_unexpected_positive_result\n' > "$result_dir/classification.txt"
            case_rc=90
          fi
          ;;
        mismatch)
          if [[ "$result" == exit-code && "$exec_status" == 1 && "$service_rc" == 1 && \
                "$comparator_exit" == 1 && "$time_exit" == 1 && -s "$time_log" ]] && \
             validate_negative_output "$stdout" "$stderr" "Challenge and solution theorem statement do not match: 'target'" >> "$result_dir/validation.log" 2>&1; then
            printf 'PASS_RESPONSE_PATH_PENDING_ROOT_PROFILE_REVIEW: compareAt mismatch rejection; not a kernel rejection\n' > "$result_dir/classification.txt"
          else
            printf 'classification=INFRA_PENDING_or_unexpected_mismatch_result\n' > "$result_dir/classification.txt"
            case_rc=90
          fi
          ;;
        axiom)
          if [[ "$result" == exit-code && "$exec_status" == 1 && "$service_rc" == 1 && \
                "$comparator_exit" == 1 && "$time_exit" == 1 && -s "$time_log" ]] && \
             validate_negative_output "$stdout" "$stderr" "Illegal axiom detected: 'forbidden'" >> "$result_dir/validation.log" 2>&1; then
            printf 'PASS_RESPONSE_PATH_PENDING_ROOT_PROFILE_REVIEW: checkAxioms forbidden-axiom rejection; not a kernel rejection\n' > "$result_dir/classification.txt"
          else
            printf 'classification=INFRA_PENDING_or_unexpected_axiom_result\n' > "$result_dir/classification.txt"
            case_rc=90
          fi
          ;;
        *)
          printf 'classification=INFRA_PENDING_unknown_expected_case\n' > "$result_dir/classification.txt"
          case_rc=90
          ;;
      esac
    fi
  fi
  find "$result_dir" -maxdepth 1 -type f ! -name evidence.sha256 -print0 | sort -z | xargs -0 sha256sum > "$result_dir/evidence.sha256"
  date -u +%FT%TZ > "$result_dir/finished_utc.txt"
  return "$case_rc"
}

run_case positive positive
run_case mismatch mismatch
run_case axiom axiom
printf 'CALIBRATION_COMPLETE: review all three classifications and logs; not mathematical certification.\n'
