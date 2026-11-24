> Traducción al español de [RESULTS.md](RESULTS.md). Si hay alguna diferencia, vale el original.

# Controles con Mathlib: resultados

Corrido el 2026-10-21 en el mismo equipo Linux y con los mismos binarios de verificadores que la auditoría principal (Comparator `19e111e` con nanoda y el kernel de Lean, Lean 4.34.0-rc2, Mathlib `85e3a25`; hashes en [`results/tools.sha256`](results/tools.sha256), idénticos a [`tools.tsv`](../../evidence/formal/cd-validation/receipts/tools.tsv)). Cada paso tiene un recibo en [`results/receipts.jsonl`](results/receipts.jsonl): el comando, el SHA-256 de cada archivo de entrada (idéntico a los archivos en [`lean/`](lean/), incluidos los enunciados registrados), el SHA-256 de su stdout y stderr saneados, y su código de salida. Diseño y expectativas: [`DESIGN.md`](DESIGN.md), registrado en el commit `046a128` y enmendado una vez antes de correr nada (`c1c6a0b`).

**Los 11 casos y los dos controles salieron según lo registrado.** `python3 experiments/mathlib-controls/verify.py` revisa cada log y entrada contra su recibo, exige código de salida 0 para cada segunda vía, y recalcula las clases; el CI lo corre junto con sus pruebas en cada push. **Comprueba los registros publicados; no es una repetición independiente de los teoremas.**

**Historial de registros.** La primera corrida (commit `ac195f7`) no guardó códigos de salida para las segundas vías, y su verificador no detectó el aviso real de `sorry` de Lean, que usa comillas invertidas. Las dos cosas las encontró un revisor externo. Los pasos se volvieron a correr con recibos el mismo día, con los mismos veredictos; los logs de la primera corrida se conservan en el historial de git. `test_verify.py` ahora cubre el aviso con comillas invertidas, un log vacío con y sin código de salida 0, un recibo faltante, y logs y entradas alterados.

| Caso | Comparator | Segunda vía | Clase | Según lo registrado |
| --- | --- | --- | --- | --- |
| primes/orig | aceptado, los dos kernels | — | ACCEPTED_BY_CHECKER | sí |
| primes/defeq | rechazado: `statement do not match` | equivalencia, `Iff.rfl` (definicional) | CHANGED_EQUIVALENT | sí |
| primes/reform | rechazado | equivalencia como esquema sobre todo `P`, pasó la guarda | CHANGED_EQUIVALENT | sí |
| primes/bounded | rechazado | original ⇒ cambiado, y un predicado donde el cambiado vale pero el original falla | CHANGED_WEAKER | sí |
| primes/swap | rechazado | refutación: `¬ ∃ p, ∀ n, n < p ∧ …` | CHANGED_FALSE | sí |
| cs/orig | aceptado, los dos kernels | — | ACCEPTED_BY_CHECKER | sí |
| cs/reform | rechazado | equivalencia mediante `abs a ≤ bc ↔ a² ≤ b²c²` para b, c ≥ 0, pasó la guarda | CHANGED_EQUIVALENT | sí |
| cs/strict | rechazado | refutación con x = y = 1 en ℝ | CHANGED_FALSE | sí |
| dct/orig | aceptado, los dos kernels | — | ACCEPTED_BY_CHECKER | sí |
| dct/reform | rechazado | equivalencia usando que la dominación hace la cota no negativa en casi todo punto, pasó la guarda | CHANGED_EQUIVALENT | sí |
| dct/nodom | rechazado | refutación: `(n+1)·1_(0, 1/(n+1))` tiende a 0 puntualmente, cada integral vale 1 | CHANGED_FALSE | sí |

| Control | Resultado |
| --- | --- |
| Equivalencia tramposa para primes/reform que usa `Nat.exists_infinite_primes` | **rechazada por la guarda**: `depends on Nat.exists_infinite_primes` |
| `g = -1` en ℝ: medible, `∫⁻ ofReal g = 0 < ∞`, no integrable | la refutación compila, así que la reformulación de DCT solo es equivalente bajo dominación |

## Qué muestra esto

1. **El rechazo de Comparator significa «el enunciado cambió», nada más.** Rechazó los ocho cambios, incluidas cuatro equivalentes (una de ellas igual por definición) y una más débil pero verdadera. Distinguirlas exigió una prueba aparte en Lean cada vez.
2. **Comparator compara los enunciados de forma estructural.** Rechazó `n + 1 ≤ p`, que Lean reduce a `n < p` por definición (`Iff.rfl`). Así que una aceptación es igualdad tal como la comprueba Comparator, y una equivalencia matemática hay que probarla aparte.
3. **La guarda importa.** Sin ella, dos enunciados verdaderos cualesquiera son «equivalentes». Atrapó la prueba deliberadamente tramposa.
4. **Una versión limitada a ejemplos no es el teorema.** `∀ n ≤ 100` se cumple, el enunciado completo la implica, y ella no lo implica como esquema.

## Límites

El autor escogió cada caso y escribió las pruebas de la segunda vía después del registro, junto con el asistente. La corrida es pequeña (tres teoremas, once casos) y no da una tasa de detección. Todavía faltan casos reservados de otra persona ([`HOLDOUT.md`](HOLDOUT.md)). Los logs se sanean solo para reemplazar las rutas del equipo con `<path>`, y los hashes de los recibos son de los archivos saneados; cada corrida de Comparator tomó entre 17 y 45 s.
