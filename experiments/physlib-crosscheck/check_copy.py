import hashlib
import pathlib
import sys

here = pathlib.Path(__file__).resolve().parent
src = here.parents[1] / "bridges" / "ClayLiteral.lean"
cpy = here / "PhyslibCrosscheck" / "ClayLiteralCopy.lean"
ranges = [((22, 23), (12, 13)), ((25, 26), (15, 16)), ((62, 64), (18, 20)), ((66, 76), (22, 32))]

s = src.read_text().splitlines()
c = cpy.read_text().splitlines()
print("source:", src.relative_to(here.parents[1]), hashlib.sha256(src.read_bytes()).hexdigest())
ok = True
for (a, b), (x, y) in ranges:
    same = s[a - 1:b] == c[x - 1:y]
    ok &= same
    print(f"source lines {a}-{b} vs copy lines {x}-{y}: {'identical' if same else 'DIFFERENT'}")
sys.exit(0 if ok else 1)
