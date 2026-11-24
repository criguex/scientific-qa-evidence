R=<path>/tools; source <path>/scripts/lib.sh
mkdir -p $R/bin $R/receipts; cd $R
# Rust
if [ ! -x ~/.cargo/bin/cargo ]; then step rustup bash -c 'curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain stable'; fi
export PATH=$HOME/.cargo/bin:$PATH
# Go
if [ ! -x /usr/local/go/bin/go ]; then
  GOV=$(curl -sSf 'https://go.dev/VERSION?m=text' | head -1); log "go $GOV"
  step go_install bash -c "curl -sSfL https://go.dev/dl/$GOV.linux-amd64.tar.gz -o /tmp/go.tgz && sha256sum /tmp/go.tgz && tar -C /usr/local -xzf /tmp/go.tgz"
fi
export PATH=/usr/local/go/bin:$PATH
# landrun ec104f6 (misma revisión que la auditoría)
[ -d landrun ] || git clone -q https://github.com/Zouuup/landrun.git
(cd landrun && git checkout -q ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a && step landrun_build go build -o $R/bin/landrun ./cmd/landrun)
# nanoda 0da9f98
[ -d nanoda_lib ] || git clone -q https://github.com/ammkrn/nanoda_lib.git
(cd nanoda_lib && git checkout -q 0da9f98 && step nanoda_build cargo build --release && cp target/release/nanoda_bin $R/bin/nanoda_bin)
# comparator + lean4export por etiqueta
for T in v4.34.0-rc2 v4.34.0 v4.35.0; do
  D=$R/cmp-$T
  [ -d $D ] || git clone -q https://github.com/leanprover/comparator.git $D
  (cd $D && git checkout -q $T && step "cmp_build_$T" lake build lean4export comparator)
  mkdir -p $R/bin-$T && cp $D/.lake/packages/lean4export/.lake/build/bin/lean4export $R/bin-$T/lean4export
done
# versiones y hashes
{
  printf 'tool\trevision\tsha256\tpath\n'
  printf 'landrun\t%s\t%s\t%s\n' "$(git -C landrun rev-parse HEAD)" "$(sha256sum bin/landrun|cut -d' ' -f1)" "tools/bin/landrun"
  printf 'nanoda_bin\t%s\t%s\t%s\n' "$(git -C nanoda_lib rev-parse HEAD)" "$(sha256sum bin/nanoda_bin|cut -d' ' -f1)" "tools/bin/nanoda_bin"
  for T in v4.34.0-rc2 v4.34.0 v4.35.0; do D=cmp-$T
    printf 'comparator(%s)\t%s\t%s\t%s\n' $T "$(git -C $D rev-parse HEAD)" "$(sha256sum $D/.lake/build/bin/comparator|cut -d' ' -f1)" "tools/$D/.lake/build/bin/comparator"
    printf 'lean4export(%s)\t%s\t%s\t%s\n' $T "$(git -C $D/.lake/packages/lean4export rev-parse HEAD)" "$(sha256sum bin-$T/lean4export|cut -d' ' -f1)" "tools/bin-$T/lean4export"
  done
} > $R/receipts/tools.tsv
{ rustc --version; cargo --version; go version; } > $R/receipts/compilers.txt 2>&1
cat $R/receipts/tools.tsv $R/receipts/compilers.txt
log LISTO
