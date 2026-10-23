OPS=<WSL_HOME>/ns08_validation_20261020_a5YGak
printf 'TOOLS\n'
find "$OPS/tools" -maxdepth 3 -type f -printf '%p\n' | head -50
printf 'SYSCALL HEADER\n'
grep -h 'io_uring_' /usr/include/x86_64-linux-gnu/asm/unistd_64.h /usr/include/asm-generic/unistd.h 2>/dev/null
printf 'SYSTEMD FILTER GROUP\n'
systemd-analyze syscall-filter @network-io
printf 'SYSTEMD GROUP NAME CHECK\n'
systemd-analyze syscall-filter io_uring
printf 'SYSTEMD MAN PACKAGE\n'
dpkg-query -W -f='${Version}\n' systemd
