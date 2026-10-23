set -eu
REPO=<WSL_HOME>/nse_audit_20261020/NavierStokesAndEuler
git -C "$REPO" remote -v
git -C "$REPO" show --format=fuller --no-patch HEAD
git -C "$REPO" ls-tree --name-only HEAD | rg -i '^(readme|licen[cs]e|copying)'
find "$REPO" -maxdepth 1 -type f -iname 'readme*' -o -iname 'licen[cs]e*' -o -iname 'copying*' -printf '%f\n' | sort
