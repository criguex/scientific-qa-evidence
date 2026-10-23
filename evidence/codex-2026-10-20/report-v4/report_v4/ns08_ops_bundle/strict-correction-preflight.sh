OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
echo "UTC $(date -u +%FT%TZ)"
echo 'Current shell sockets:'
python3 -c 'import os; p="/proc/"+str(os.getppid())+"/fd"; out=[]
for n in os.listdir(p):
 try:
  t=os.readlink(p+"/"+n)
  if t.startswith("socket:"): out.append((n,t))
 except OSError: pass
print(repr(out))'
echo 'Exact tool paths:'
for f in \
 "$OPS/tools/landrun/landrun" \
 "$OPS/tools/zig-0.17.0/zig-x86_64-linux-0.17.0/zig" \
 "$OPS/tools/go-1.27.3/go/bin/go" \
 "$OPS/tools/rust-1.98.1/bin/rustc" \
 <WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/lean; do
  test -x "$f" && ls -l "$f" || echo "MISSING $f"
done
echo 'Versions:'
"$OPS/tools/landrun/landrun" --version
"$OPS/tools/zig-0.17.0/zig-x86_64-linux-0.17.0/zig" version
"$OPS/tools/go-1.27.3/go/bin/go" version
"$OPS/tools/rust-1.98.1/bin/rustc" --version
<WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/lean --version
echo 'systemd properties in local man:'
MANPAGER=cat man systemd.exec | col -b | grep -n -A5 -B2 -E '^ *NoNewPrivileges=|^ *SystemCallErrorNumber=' | head -50
