# Seed commitment for the blind-fault experiment

The author generated a secret random seed on his own machine, outside the AI assistant's session:

```sh
openssl rand -hex 16 > ~/semilla-experimento.txt
```

Only its SHA-256 hash was shared and is published here, before the experiment design is frozen and before any fault is assigned:

```text
6ab9f825a6e0102f06589795a3f3afb81b954ec054362e7e0352018547614d5e  semilla-experimento.txt
```

The hash covers the file exactly as generated: 32 hexadecimal characters followed by a newline.

## Rules

1. The seed decides which copies receive which faults. It is used only by the assignment script, run by the author.
2. The person running the checks does not read the seed file or the assignment key until every check has been recorded. The assistant has filesystem access to the author's machine, so this rule rests on that commitment; the published hash makes any later change of seed detectable.
3. After all results are recorded, the author reveals the seed file. Anyone can then check `shasum -a 256` against the hash above and rerun the assignment script to reproduce the exact fault allocation.
4. If the seed file is lost or edited, the experiment is void and must be restarted with a new commitment.
