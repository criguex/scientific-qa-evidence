> Traducción al español de [README.md](README.md). Si hay alguna diferencia, vale el original.

# ¿Es el desafío de OpenAI el enunciado público de DeepMind?

**Hallazgo (2026-10-21):** las 18 declaraciones coinciden tras la normalización textual; la resolución de nombres no se verificó. Tras quitar comentarios, atributos y espacios en blanco, toda declaración nombrada en el desafío de Comparator de OpenAI, incluidos los teoremas de ruptura (C) y (D), es textualmente igual a la del archivo público Formal Conjectures de Google DeepMind. Las diferencias restantes son de imports, espacio de nombres y notación.

**Alcance.** Esto es una comparación textual. No muestra identidad semántica. Eso requeriría comparar las declaraciones elaboradas y sus constantes y dependencias en Lean, para probar que los distintos imports, espacio de nombres y notación no cambian el significado. Esa comparación no se hizo.

| | Referencia | Candidato |
| --- | --- | --- |
| Archivo | [`FormalConjectures/Millenium/NavierStokes.lean`](https://github.com/google-deepmind/formal-conjectures/blob/8bf45ed70d48b2b2a501de9c00b26bfa38c573ee/FormalConjectures/Millenium/NavierStokes.lean) | [`ComparatorChallenges/NavierStokes.lean`](https://github.com/openai/NavierStokesAndEuler/blob/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/ComparatorChallenges/NavierStokes.lean) |
| Repositorio y commit | google-deepmind/formal-conjectures `8bf45ed` | openai/NavierStokesAndEuler `f9e8bc5` |
| SHA-256 | `f446284f2aa54375f558c263a580b34e2e7bc9f44a28829637199cc72257d25d` | `0cd193b8d5cbd0266e6e2f72e68dd5abcdcf2430ebd435dd9289737e9aa7da61` |

## Resultado

**20 bloques son idénticos** tras quitar comentarios, atributos y espacios en blanco: `open scoped Laplacian`, `variable {n : ℕ}` y 18 declaraciones nombradas. Son `divergence` y sus cinco lemas auxiliares, `IsOnePeriodic`, las seis condiciones de velocidad inicial y de fuerza, las tres clases de solución, y los dos teoremas de ruptura `navier_stokes_breakdown_R3` (C) y `navier_stokes_breakdown_periodic` (D).

Las únicas diferencias:

| Diferencia | Por qué no cambia la matemática |
| --- | --- |
| `import FormalConjecturesUtil` → `import Mathlib` | El desafío debe compilar sin la biblioteca auxiliar de DeepMind. |
| Espacio de nombres `NavierStokes` → `NavierStokes.Comparator` | Solo un prefijo de nombre. |
| `EuclideanGeometry` se quita de la línea `open` | En la fuente original aporta la notación con alcance `ℝ^n` y `ℝ³`, que ahora se define localmente. El archivo de OpenAI compila sin el `open`; la nota "No verificado" de abajo cubre la resolución de nombres. |
| La notación `ℝ^n` y `ℝ³` se copia al archivo como `local notation` | La fuente original las define como `EuclideanSpace ℝ (Fin n)` y `EuclideanSpace ℝ (Fin 3)` en `FormalConjecturesForMathlib/Geometry/Euclidean.lean` y `Geometry/3d.lean` en el mismo commit. Las copias son las mismas definiciones. |
| La notación `∇⬝` se vuelve `local` | Solo alcance. |
| Se quitan los teoremas de existencia (A) y (B) | El envío de OpenAI aborda (C) y (D), así que solo esos se desafían. |

También se verificó leyendo el Mathlib fijado: `∞` en `ContDiff ℝ ∞` es `((⊤ : ℕ∞) : WithTop ℕ∞)`, es decir, suavidad C^∞, no analiticidad (`ω`). `Δ` es `Laplacian.laplacian` de Mathlib, y `gradient` es el `gradient` de Mathlib.

**No verificado:** si algún nombre se resuelve de forma distinta en los dos archivos, por ejemplo porque la biblioteca auxiliar de DeepMind o el espacio de nombres `EuclideanGeometry` tape un nombre de Mathlib como `gradient`. En el archivo de OpenAI esos nombres se resuelven a Mathlib.

## Qué muestra esto y qué no

Dentro de ese alcance, muestra que el texto del desafío de OpenAI no se adaptó a partir del enunciado público. La pregunta "¿el enunciado formal dice lo que dice Clay?" ahora concierne al enunciado público de DeepMind, no a un archivo escrito por quien demuestra. No responde esa pregunta; ver [`../clay-lean-risk.md`](../clay-lean-risk.md).

## Reproducir

```sh
curl -fLO https://raw.githubusercontent.com/google-deepmind/formal-conjectures/8bf45ed70d48b2b2a501de9c00b26bfa38c573ee/FormalConjectures/Millenium/NavierStokes.lean
mv NavierStokes.lean deepmind.lean
curl -fLO https://raw.githubusercontent.com/openai/NavierStokesAndEuler/f9e8bc5b38b6e212696e8a30e3e91517af887bbd/ComparatorChallenges/NavierStokes.lean
mv NavierStokes.lean openai.lean
python3 compare_statements.py deepmind.lean openai.lean
```

La salida debe coincidir con [`result.json`](result.json). El comparador usa solo la biblioteca estándar de Python y tiene sus propias pruebas en [`test_compare_statements.py`](test_compare_statements.py).
