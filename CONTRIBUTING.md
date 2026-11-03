# Contributing

Rules for anyone, human or agent, who changes this repository.

- **Keep the English and Spanish documents in step.** [README.md](README.md) and [README.es.md](README.es.md), and [docs/DETAILS.md](docs/DETAILS.md) and [docs/DETAILS.es.md](docs/DETAILS.es.md), say the same thing; change each pair together. The README stays short; details go to `docs/DETAILS*.md`, terms to [docs/GLOSSARY.md](docs/GLOSSARY.md), and every new document gets a line in the [documentation map](docs/README.md). Detailed records (CLAIMS, evidence guides, the numerical contract) stay in English.
- **Never rewrite an original evidence file.** The numerical and formal evidence are curated allowlists, and the English summaries are derived translations of the originals.
- **Update the checksums.** After editing any file listed in `evidence/SHA256SUMS.txt`, update its entry and confirm the whole list still verifies. Editing a listed file under `evidence/`, `experiments/` or `bridges/` changes the data version and the fingerprint printed by `verificar.py`; if that happens, add the new pair to `REFS` in `site/index.html` (CI fails otherwise) and to the table in `evidence/reproductions/README.md`.
- **Keep counts honest.** The 54 KILLED cases are 51 distinct behaviors, and the 84 variants per host are paired runs, not 168 distinct cases. Every public claim needs a row in [CLAIMS.md](CLAIMS.md) that points to its evidence.
- **No private data.** Before any commit, check that no private IPs, host usernames, private paths, credentials or employer names have entered the diff.

Run these from the repository root before pushing:

```sh
shasum -a 256 -c evidence/SHA256SUMS.txt     # on Linux: sha256sum -c
python3 evidence/verify_numerical.py
python3 -m unittest discover -s animations -p 'test_*.py'
python3 -m unittest discover -s evidence/formal/comparator -p 'test_*.py'
```
