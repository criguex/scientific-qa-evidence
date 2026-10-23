set -eu
cd <WSL_HOME>/ns08_validation_20261020_a5YGak
tar -czf - \
  results/abi-resource-limits-preflight.log \
  results/install-portable-toolchains.log \
  results/zig-toolchain.log \
  results/ns08-linker-archive-prebuild.log \
  results/nanoda-build.log \
  results/landrun-build.log \
  results/lake-build.log \
  results/landrun-controls.log \
  results/landrun-no-best-effort.log \
  results/preflight-tools-and-afunix.log \
  results/strict-profile-probe.log \
  results/strict-property-isolation.log \
  results/strict-correction-controls.log \
  results/formal-repo-archive-listing.txt \
  results/comparator-ns-20261020-1901 \
  results/comparator-ns-attempt2-20261020-1905 \
  results/comparator-euler-20261020-1914 \
  | base64 -w0
