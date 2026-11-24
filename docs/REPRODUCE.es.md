> Traducción al español de [Reproducing this release](REPRODUCE.md). Si hay alguna diferencia, vale el original.

# Cómo reproducir esta versión

Cómo repetir cada resultado de este paquete desde un checkout limpio, y qué resultados se recalculan frente a cuáles solo se verifican por hash.

## 1. Qué prueba cada paso

| Resultado | Cómo lo compruebas | ¿Recalculado o verificado? |
| --- | --- | --- |
| Cada archivo curado es el que se publicó | `shasum -a 256 -c evidence/SHA256SUMS.txt` | Verificado por hash |
| Las corridas guardadas de 84 casos están intactas y coinciden entre máquinas | `python3 evidence/verify_numerical.py` | Verificado: hashes registrados y comparación entre máquinas de los valores guardados |
| La campaña numérica da los mismos resultados | `test_runner.py` (abajo) | **Recalculado:** las 84 variantes se corren de nuevo y se comparan con los registros guardados |
| El runner maneja fallos del oráculo y del simulador | `test_runner.py` | **Recalculado:** excepciones forzadas, oráculos NaN, fallo de exportación |
| El README, CLAIMS y los registros coinciden | `python3 evidence/test_consistency.py` | Comprobado contra los registros legibles por máquina |
| Las páginas de animación y el manifiesto vienen de la evidencia | `animations/test_build.py` | **Recalculado:** páginas y manifiesto regenerados, hashes de las entradas comprobados |
| El texto del desafío de OpenAI coincide con el enunciado de DeepMind | `compare_statements.py` (abajo) | **Recalculado** a partir de los dos archivos fijados que descargas |
| Compilaciones en Lean, corridas de Comparator, mutantes del enunciado, leanchecker | Sección 4 | No se puede reproducir solo desde este repositorio; los logs y recibos guardados se verifican por hash |

## 2. Comprobación rápida (solo Python, cerca de un minuto)

Necesita git y Python 3.9 o más reciente. Sin paquetes de terceros.

```sh
git clone https://github.com/criguex/scientific-qa-evidence.git
cd scientific-qa-evidence
git checkout v1.3.3                                 # the tag of this release; later releases are listed on GitHub
shasum -a 256 -c evidence/SHA256SUMS.txt          # on Linux, sha256sum -c also works
python3 evidence/verify_numerical.py
(cd evidence/numerical/source && python3 -m unittest -v test_runner)
python3 evidence/test_consistency.py -v
python3 -m unittest discover -s animations -p 'test_*.py'
(cd evidence/formal/comparator && python3 -m unittest test_sanitize_comparator_logs)
(cd evidence/formal/statement-provenance && python3 -m unittest test_compare_statements)
(cd experiments/blind-faults && python3 -m unittest test_protocol)          # benchmark v1, frozen
(cd experiments/blind-faults/v2 && python3 -m unittest test_protocol_v2 fuzz_v2)  # corrected evaluator + fuzzer
(cd experiments/mathlib-controls && python3 verify.py && python3 -m unittest test_verify)  # receipts of the Mathlib controls
(cd experiments/receipt-check && python3 -m unittest test_results)  # receipt checks on authentic bundles
```

Los mismos comandos corren en [GitHub Actions](../.github/workflows/verify.yml) en Ubuntu y macOS con Python 3.9 y 3.12. Las notas de la versión de cada tag (aquí `v1.3.3`) enlazan la corrida de CI exitosa para ese commit exacto, con sus logs.

Para volver a correr la suite numérica en una carpeta nueva e inspeccionar la salida bruta:

```sh
cd evidence/numerical/source
python3 runner.py --out /tmp/sqe-rerun     # must not exist yet
```

Resultado esperado: 84 variantes, `KILLED: 54, PASS: 27, SURVIVED: 3`, `collection_complete: true`, sin `export_errors`.

## 3. Comparación del enunciado

```sh
cd evidence/formal/statement-provenance
curl -fL -o deepmind.lean https://raw.githubusercontent.com/google-deepmind/formal-conjectures/8bf45ed70d48b2b2a501de9c00b26bfa38c573ee/FormalConjectures/Millenium/NavierStokes.lean
curl -fL -o openai.lean https://raw.githubusercontent.com/openai/NavierStokesAndEuler/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/ComparatorChallenges/NavierStokes.lean
python3 compare_statements.py deepmind.lean openai.lean > /tmp/result.json
diff <(python3 -m json.tool --sort-keys result.json) <(python3 -m json.tool --sort-keys /tmp/result.json)
```

Que `diff` no dé salida significa el mismo resultado: 18 declaraciones nombradas que coinciden tras la normalización textual.

## 4. Las corridas formales (Lean, Comparator, kernels)

Estas necesitan el repositorio de OpenAI y una máquina Linux; no se pueden volver a correr desde este paquete. Lo que se usó:

| Elemento | Versión o hash |
| --- | --- |
| Fuente | `openai/NavierStokesAndEuler` en `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, SHA-256 del archivo `afd4d2263a4cabefd1317e890b49bc04f8538402c322db4317a08161e834b4b5` |
| Lean y Lake | `leanprover/lean4:v4.34.0-rc2`, commit `6a10ac8`; hashes de los binarios en [`receipts/tools.tsv`](../evidence/formal/cd-validation/receipts/tools.tsv) |
| Mathlib y dependencias | Fijadas en el `lake-manifest.json` de la fuente; las revisiones resueltas están en [`receipts/fresh_build_versions.txt`](../evidence/formal/cd-validation/receipts/fresh_build_versions.txt) |
| Comparator, lean4export, nanoda, landrun | Revisiones y hashes de los binarios en [`receipts/`](../evidence/formal/cd-validation/receipts/) |
| Máquina | Linux x86_64 (WSL2), 12 vCPU, 30 GiB de RAM; unos 28 GB de disco por compilación. `landrun` necesita Linux Landlock. |

Comandos, corridos desde la fuente extraída:

```sh
# Full build with no downloaded build caches (B4)
XDG_CACHE_HOME="$(mktemp -d)" MATHLIB_NO_CACHE_ON_UPDATE=1 lake --no-cache build

# Comparator (with COMPARATOR_LANDRUN, COMPARATOR_LEAN4EXPORT and COMPARATOR_NANODA pointing to the tools)
lake env <path-to>/comparator ComparatorChallenges/NavierStokes.json
lake env <path-to>/comparator ComparatorChallenges/Euler.json

# Fresh kernel replay
lake env leanchecker --fresh NavierStokes.ComparatorSolution
lake env leanchecker --fresh Euler.Solution
```

Un mutante del enunciado es una edición de una línea en `ComparatorChallenges/NavierStokes.lean` o `Euler.lean`, seguida del comando de Comparator. Las ediciones exactas son los diffs en [`evidence/formal/cd-validation/mutants/`](../evidence/formal/cd-validation/mutants/). Cada corrida registrada, su compilación, sus tiempos, su código de salida y el SHA-256 de su log original están en [`evidence/formal/cd-validation/README.md`](../evidence/formal/cd-validation/README.md) y en [`PROVENANCE.md`](../evidence/formal/cd-validation/PROVENANCE.md).

Una corrida desde un clon nuevo de las comprobaciones en Python, los puentes en Lean y los pasos de los controles con Mathlib, con sus resultados, está en [`evidence/FROM_ZERO.md`](../evidence/FROM_ZERO.md); no repitió la compilación de OpenAI, que se repitió aparte como la compilación B5 ([registro](../evidence/formal/b5/README.md)).

## 5. Los lemas puente (Lean)

`bridges/ClayLiteral.lean` y `bridges/Bridges.lean` se comprueban contra el mismo Lean 4.34.0-rc2 y Mathlib que las corridas formales, desde un árbol compilado de `openai/NavierStokesAndEuler`; los comandos exactos y el recibo de `#print axioms` están en [`bridges/README.md`](../bridges/README.md).

## 6. Benchmark de fallos a ciegas

La asignación es reproducible a partir de la semilla revelada; los comandos están en [`experiments/blind-faults/RESULTS.md`](../experiments/blind-faults/RESULTS.md#reproduce-the-assignment).

## 7. Opcional: vistas previas en GIF

`python3 animations/export_gifs.py` necesita Python Playwright con Chromium y FFmpeg. Los GIF no son parte de la evidencia; son vistas previas de las escenas HTML.
