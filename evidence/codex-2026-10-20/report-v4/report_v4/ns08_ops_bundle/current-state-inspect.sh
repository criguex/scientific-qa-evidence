OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
echo 'Tool binaries:'
find "$OPS/tools" -maxdepth 3 -type f \( -name zig -o -name go -o -name rustc -o -name cargo -o -name nanoda_bin -o -name landrun \) -printf '%p\n' 2>/dev/null | sort
find "$OPS/tools" -maxdepth 6 -type f \( -name go -o -name nanoda_bin \) -printf '%p\n' 2>/dev/null | sort
echo 'Result logs:'
find "$OPS/results" -maxdepth 1 -type f -printf '%f %s bytes\n' | sort
echo 'Version outputs:'
find "$OPS/tools" -maxdepth 6 -type f -name zig -exec {} version \; 2>/dev/null
find "$OPS/tools" -maxdepth 6 -type f -name go -exec {} version \; 2>/dev/null
"$OPS/tools/rust-1.98.1/bin/rustc" --version 2>&1 || true
"$OPS/tools/landrun/landrun" --version 2>&1 || true
find "$OPS/tools" -maxdepth 7 -type f -name nanoda_bin -exec {} --version \; 2>&1 | head -10
