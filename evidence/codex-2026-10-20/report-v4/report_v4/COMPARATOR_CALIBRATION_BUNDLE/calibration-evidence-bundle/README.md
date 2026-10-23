# NS-08 Comparator calibration evidence bundle

UTC date: 2026-10-20. This bundle is operational evidence for three small
Comparator response-path controls, not proof that NS/Euler are correct and not
independent human mathematical review.

## Remote runs preserved

- attempt1-preflight/results/: no Comparator case ran. pins-and-versions.txt
  records the elan "no default toolchain configured" failure before any case.
- attempt2-positive-only/results/: the positive Comparator path returned 0 and
  both kernels accepted. The launcher then stopped before negatives because its
  parser required the nonexistent RestrictAddressFamiliesAllowList property.
  This is preserved as an observed positive, not a completed calibration.
- attempt3-three-cases/results/: final reviewed launcher executed all three
  cases serially in a new root. Each result directory contains stdout/stderr,
  GNU time, status, guard, active systemd profile capture, journal, exact
  command, classification, and per-case SHA manifest.

Attempt 3 remote root:
<WSL_HOME>/ns08_validation_20261020_a5YGak/calibration_20261020T1957Z_ns08cal_3p8kza/

The active unit profile was checked by values: RestrictAddressFamilies=~AF_UNIX,
native syscall architecture, NoNewPrivileges=yes, seccomp deny filter covering
network I/O and socketpair plus the three io_uring syscalls, EPERM numeric 1,
27 GiB MemoryMax, 800% CPU, 8 h runtime, null stdin, append stdout/stderr.
Each service guard recorded no inherited socket FDs, CapEff=0,
NoNewPrivs=1, and Seccomp=2.

## Attempt 3 result summary

- Positive: process, time, and systemd-run --wait exits 0. Two module builds
  and Challenge/Solution exports completed; nanoda and Lean default kernels
  accepted; Comparator emitted Your solution is okay!. GNU time reports 2.82 s
  elapsed and 742144 KiB maximum RSS.
- Statement mismatch: all three exits 1 after both builds and exports;
  Comparator emitted Challenge and solution theorem statement do not match:
  'target'. This is compareAt-stage rejection, not a kernel rejection. GNU time
  reports 1.44 s elapsed and 742024 KiB maximum RSS.
- Unpermitted axiom: all three exits 1 after both builds and exports;
  Comparator emitted Illegal axiom detected: 'forbidden'. This is the
  axiom-check stage, not a kernel rejection. GNU time reports 1.49 s elapsed
  and 742108 KiB maximum RSS.

The three positive/negative fixtures and the exact attempt 3 launcher are under
sources/ and launchers/attempt3.sh. No toolchain binaries, .lake caches,
or repository .git directories are included. Attempt 3 used the existing
prebuilt formal checkout and pinned tool binaries; it does not establish a
clean adversarial start or ABI 10 sandbox guarantees.

## Provenance hashes

Launcher v1 (attempt 1): bf9256699ca32b1ea5be44edce91cde969d06ac741ec14b7306148c6f1ddd285
Launcher v2 (attempt 2): 11382df9c8ae43c8430617dd0ac00b051269580276b03e3f2e2168e3f078f2a6
Launcher v3 (attempt 3): f17f7a69cc7843a59bffc3434f21bab1b723942d2307099a2318d1f29c9f5cf1

Result exports copied from WSL and their SHA-256 values:

- Attempt 1 preflight: 4da45b3deabce24e87a3fbdcfcaf8b0417e7be0a64b375d66326692dc34053a3
- Attempt 2 positive-only: 4a5baeb25fe0ffc2ce14b708f97fe36f7bcd059d672f4eec3da91f98de826f15
- Attempt 3 three cases: b973ebee4152fff9a7442223834ba20d6e896b6c9b2a208a2e94942924a5f8e0

Stage archives: v1 cd94042b9d0f93f857702dce27255c2774071ca74f1e2124ae8f9214120ed2ff,
v2 6108b9ee0095e425d7bdc7e9c7056fcd466ceb1f859647ab409ea1cc8c9c5d64, v3
9a2cb5ab160cfba4a9882fd87752f3dadb61f9db50c9f38e8a2ff0782ab5a606.

## Source and tool pins

Formal checkout: f9e8bc5b38b6e212696e8a30e3e91517af887bbd

Comparator: 19e111e2141cf333c7daff0f64c5f24acc91dd2e
Lean4export: cacf989bd75f608700820f6afc595f32e7a99a4d
Nanoda: 9d6964f78d0fa4c93fd22fe956e17afe7e72a441
Landrun: ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a

Tool binary hashes and exact versions are retained in each attempt's
results/tool-binaries.sha256 and results/pins-and-versions.txt.
