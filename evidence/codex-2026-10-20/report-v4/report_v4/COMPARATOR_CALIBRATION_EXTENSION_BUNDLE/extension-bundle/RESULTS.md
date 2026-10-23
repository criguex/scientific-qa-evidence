# NS-08 calibration extension — execution record

Run date: 2026-10-20 UTC. This is a bounded three-case Comparator calibration,
not a universal false-positive study, mathematical certification, clean-root
reproduction, or independent human review. No formal checkout files were
modified and no installations were made.

Remote ROOT:
<WSL_HOME>/ns08_validation_20261020_a5YGak/calibration_20261020T2002Z_ns08extra_5r9k2m/

Launcher SHA-256:
dad31e650b6aed7b80ce6844a399652ce07e86198a111990df8902d72f83ca39

The three cases ran sequentially with the accepted systemd outer profile and
the same pinned Comparator/Lean/Lake/lean4export/nanoda/Landrun executables.
All three active-profile captures passed value validation. Each service guard
reported service_socket_fds=[], CapEff=0000000000000000, NoNewPrivs=1, and
Seccomp=2. The active systemd profile recorded:

- RestrictAddressFamilies=~AF_UNIX
- SystemCallArchitectures=native
- SystemCallFilter deny entries for network I/O/socketpair and
  io_uring_setup/io_uring_enter/io_uring_register
- NoNewPrivileges=yes and SystemCallErrorNumber=1 (EPERM)
- MemoryMax=28991029248; CPUQuotaPerSecUSec=8s; RuntimeMaxUSec=8h
- StandardInput=null; StandardOutput=append; StandardError=append

## Results

| Case | systemd-run / Comparator / GNU time exits | Comparator result | Elapsed / max RSS |
|---|---:|---|---:|
| alpha | 0 / 0 / 0 | Two builds and exports completed; nanoda and Lean kernels accepted; “Your solution is okay!” | 3.16 s / 742252 KiB |
| hidden_axiom | 1 / 1 / 1 | After two builds and exports, “Illegal axiom detected: 'forbidden'”; no kernel invocation | 1.52 s / 742632 KiB |
| weakened_condition | 1 / 1 / 1 | After two builds and exports, “Challenge and solution theorem statement do not match: 'target'”; no kernel invocation | 1.45 s / 742140 KiB |

For negative cases, these are Comparator-stage checkAxioms and statement
comparison rejections, respectively—not kernel rejections. Any such result is
specific to these fixtures and pinned build/profile.

## Preserved evidence

- results/ has separate raw stdout/stderr, GNU time, process and systemd-run
  status, journal, active properties, guard, cgroup, command, classification,
  timestamps, and SHA manifests for each case.
- raw-results-copy.tar.gz is the byte-for-byte exported result archive from
  WSL; SHA-256:
  7367f7dbbeef93287b21e4e7db0efb02fd3b202b302c8e444440f97cbb1dff89
- stage-input.tar.gz is the exact staged input; SHA-256:
  537d2803c5fcb58fbe983656f6955b651d4920d5787b3d4ba2b2dbca415265bd
- PRE_RUN_SHA256SUMS preserves the reviewed source manifest before execution.

No fourth case or extra dependency was added. This does not establish that
Comparator has zero false positives beyond these controls or that prior formal
runs reproduce from a clean adversarial root.
