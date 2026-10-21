# Contributing

Rules for anyone, human or agent, who changes this repository.

- **Keep both READMEs in step.** [README.md](README.md) (English) and [README.es.md](README.es.md) (Spanish) say the same thing; change them together. Detailed records (CLAIMS, evidence guides, the numerical contract) stay in English.
- **Never rewrite an original evidence file.** The numerical and formal evidence are curated allowlists, and the English summaries are derived translations of the originals.
- **Update the checksums.** After editing any file listed in `evidence/SHA256SUMS.txt`, update its entry and confirm the whole list still verifies.
- **Keep counts honest.** The 54 KILLED cases are 51 distinct behaviors, and the 84 variants per host are paired runs, not 168 distinct cases. Every public claim needs a row in [CLAIMS.md](CLAIMS.md) that points to its evidence.
- **No private data.** Before any commit, check that no private IPs, host usernames, private paths, credentials or employer names have entered the diff.

Run these from the repository root before pushing:

```sh
shasum -a 256 -c evidence/SHA256SUMS.txt     # on Linux: sha256sum -c
python3 evidence/verify_numerical.py
python3 -m unittest discover -s animations -p 'test_*.py'
python3 -m unittest discover -s evidence/formal/comparator -p 'test_*.py'
```
