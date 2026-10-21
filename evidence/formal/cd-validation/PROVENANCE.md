# Provenance of the 2026-10-21 revalidation files

Each public file in this folder, the original record it comes from on the test host, and that original's SHA-256. `<RUN>` stands for the private run directory. Originals are not distributed. "Sanitized" means [`../comparator/sanitize_comparator_logs.py`](../comparator/sanitize_comparator_logs.py) was applied: ANSI codes removed, private paths and private IPs redacted.

| Public file | Original | Original SHA-256 | Transformation |
| --- | --- | --- | --- |
| `logs/comparator2_NavierStokes.sanitized.log` | `<RUN>/comparator2_NavierStokes/stdout.log` | `86f19cfa0e008549d11147e7fe3ceefc5bfd317ffa4b0824eeb6e3327ec973bf` | stdout and stderr combined, sanitized |
| `logs/comparator2_NavierStokes.sanitized.log` | `<RUN>/comparator2_NavierStokes/stderr.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | stdout and stderr combined, sanitized |
| `logs/comparator2_Euler.sanitized.log` | `<RUN>/comparator2_Euler/stdout.log` | `5f410965535ca08ed4cfca05bd9fb259ece2ef95858319a83134f92bc83b96ba` | stdout and stderr combined, sanitized |
| `logs/comparator2_Euler.sanitized.log` | `<RUN>/comparator2_Euler/stderr.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | stdout and stderr combined, sanitized |
| `logs/comparator3_clean_NavierStokes.sanitized.log` | `<RUN>/comparator3_clean_NavierStokes/stdout.log` | `86f19cfa0e008549d11147e7fe3ceefc5bfd317ffa4b0824eeb6e3327ec973bf` | stdout and stderr combined, sanitized |
| `logs/comparator3_clean_NavierStokes.sanitized.log` | `<RUN>/comparator3_clean_NavierStokes/stderr.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | stdout and stderr combined, sanitized |
| `logs/comparator3_clean_Euler.sanitized.log` | `<RUN>/comparator3_clean_Euler/stdout.log` | `5f410965535ca08ed4cfca05bd9fb259ece2ef95858319a83134f92bc83b96ba` | stdout and stderr combined, sanitized |
| `logs/comparator3_clean_Euler.sanitized.log` | `<RUN>/comparator3_clean_Euler/stderr.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | stdout and stderr combined, sanitized |
| `logs/mutant_control_comment.sanitized.log` | `<RUN>/mutants/control_comment/stdout.log` | `d3a2b1fce86b2b51df16fd962dc065feb5f3ad098afd725aa0a19b1a68034285` | stdout and stderr combined, sanitized |
| `logs/mutant_control_comment.sanitized.log` | `<RUN>/mutants/control_comment/stderr.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | stdout and stderr combined, sanitized |
| `mutants/control_comment.diff` | `<RUN>/mutants/control_comment.diff` | `20923ef340fe7cac200a3f8292dc81e9d066b96929eca7ab7e4bf58f3dc716aa` | sanitized |
| `logs/mutant_force_zero_R3.sanitized.log` | `<RUN>/mutants/force_zero_R3/stdout.log` | `9eb4ded8d681232cdd5c2bf82c6949476cb74e0fbca90e5f5e4b5ae599c84d07` | stdout and stderr combined, sanitized |
| `logs/mutant_force_zero_R3.sanitized.log` | `<RUN>/mutants/force_zero_R3/stderr.log` | `ff03063c9fbc40fae471bd8c695852d2c1fa37e4c20797dfd882dcdf7c5b2a3f` | stdout and stderr combined, sanitized |
| `mutants/force_zero_R3.diff` | `<RUN>/mutants/force_zero_R3.diff` | `2125f51c41c03dbf4d6d5dbc5aea80a9343e59eb1cc80895855d467a4e714709` | sanitized |
| `logs/mutant_force_zero_periodic.sanitized.log` | `<RUN>/mutants/force_zero_periodic/stdout.log` | `227c974b3d65d28955366bf5a6a6f99af769f3e89cc7aa7b80636745e95fd64d` | stdout and stderr combined, sanitized |
| `logs/mutant_force_zero_periodic.sanitized.log` | `<RUN>/mutants/force_zero_periodic/stderr.log` | `63446e597a26220ae20335753b86ccef121bb1255eeec95a024c197f85ccf07f` | stdout and stderr combined, sanitized |
| `mutants/force_zero_periodic.diff` | `<RUN>/mutants/force_zero_periodic.diff` | `43db52345f01c64c7b134888f109e83f3dc0ba0d374a42ae75c3a7135f96b343` | sanitized |
| `logs/mutant_domain_R3_to_periodic_data.sanitized.log` | `<RUN>/mutants/domain_R3_to_periodic_data/stdout.log` | `0747d144f28b1e9a94ce60d3121744babb741b6bccad3e6f1938932380f0c103` | stdout and stderr combined, sanitized |
| `logs/mutant_domain_R3_to_periodic_data.sanitized.log` | `<RUN>/mutants/domain_R3_to_periodic_data/stderr.log` | `ff03063c9fbc40fae471bd8c695852d2c1fa37e4c20797dfd882dcdf7c5b2a3f` | stdout and stderr combined, sanitized |
| `mutants/domain_R3_to_periodic_data.diff` | `<RUN>/mutants/domain_R3_to_periodic_data.diff` | `63beb94d90c79fd543a1c645f4f7bd839e46247e69a1bb523ac93ef7339823f5` | sanitized |
| `logs/mutant_viscosity_nonneg_R3.sanitized.log` | `<RUN>/mutants/viscosity_nonneg_R3/stdout.log` | `0747d144f28b1e9a94ce60d3121744babb741b6bccad3e6f1938932380f0c103` | stdout and stderr combined, sanitized |
| `logs/mutant_viscosity_nonneg_R3.sanitized.log` | `<RUN>/mutants/viscosity_nonneg_R3/stderr.log` | `ff03063c9fbc40fae471bd8c695852d2c1fa37e4c20797dfd882dcdf7c5b2a3f` | stdout and stderr combined, sanitized |
| `mutants/viscosity_nonneg_R3.diff` | `<RUN>/mutants/viscosity_nonneg_R3.diff` | `07a3e4143cb08b249cc009fd97617a86bb6ef29e7a4aef80f82fb9f82e3420bd` | sanitized |
| `logs/mutant_existence_not_breakdown_periodic.sanitized.log` | `<RUN>/mutants/existence_not_breakdown_periodic/stdout.log` | `71c327714600d61a1088312aeda5d3408ee4cf7cdd50b0ca80b408e15338a97b` | stdout and stderr combined, sanitized |
| `logs/mutant_existence_not_breakdown_periodic.sanitized.log` | `<RUN>/mutants/existence_not_breakdown_periodic/stderr.log` | `63446e597a26220ae20335753b86ccef121bb1255eeec95a024c197f85ccf07f` | stdout and stderr combined, sanitized |
| `mutants/existence_not_breakdown_periodic.diff` | `<RUN>/mutants/existence_not_breakdown_periodic.diff` | `4f91bc386f4eab1578ed649a796bb0f2217bfb4e02d9b2f1bc49a1ce99692766` | sanitized |
| `logs/mutant_euler_tstar_half.sanitized.log` | `<RUN>/mutants/euler_tstar_half/stdout.log` | `01e507146ec980dcf353ec2b0eb6a7746ffa33ac991c2f1456978c7a0f9bb305` | stdout and stderr combined, sanitized |
| `logs/mutant_euler_tstar_half.sanitized.log` | `<RUN>/mutants/euler_tstar_half/stderr.log` | `ee160da5cdd168f08be12a06cf679e42bf33db58d503bf3be8a3c868f00d6690` | stdout and stderr combined, sanitized |
| `mutants/euler_tstar_half.diff` | `<RUN>/mutants/euler_tstar_half.diff` | `e48ebbcb1f68014ca841e65bb0c609624398a522828629eca379101ac5793f21` | sanitized |
| `logs/clean_build.excerpt.log` | `<RUN>/clean/build.log` | `627f1474a9cf3ac698693aa295445574343239364b563a89975e4efbe8522011` | first 40 and last 15 lines, sanitized |
| `logs/leanchecker_fresh_NavierStokes.ComparatorSolution.log` | `<RUN>/leanchecker/NavierStokes.ComparatorSolution.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | copied byte for byte (empty: leanchecker prints nothing on success) |
| `receipts/leanchecker_fresh_NavierStokes.ComparatorSolution.txt` | `<RUN>/leanchecker/NavierStokes.ComparatorSolution.time.log` | `df04cc36337ac6e8476d679bd69b599887a04abed2f76d0345da936a71c57fe2` | GNU time lines kept: command, elapsed, max RSS, exit status |
| `logs/leanchecker_fresh_Euler.Solution.log` | `<RUN>/leanchecker/Euler.Solution.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | copied byte for byte (empty: leanchecker prints nothing on success) |
| `receipts/leanchecker_fresh_Euler.Solution.txt` | `<RUN>/leanchecker/Euler.Solution.time.log` | `dc7cd14c52602438a37a9063a3c604a6b22c154a9cf11c63666e3143ac237841` | GNU time lines kept: command, elapsed, max RSS, exit status |
| `logs/lean4lean_build.error-excerpt.log` | `<RUN>/lean4lean_build.log` | `4c9eaa87f9dce57cc65b55777b5da1be820e190f4f6d9a65fb3d9c19eda5ef72` | lines 70–105 (the failing job and summary), sanitized |
