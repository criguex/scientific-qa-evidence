> Traducción al español de [clay-lean-risk.md](clay-lean-risk.md). Si hay alguna diferencia, vale el original.

# Clay ↔ Lean: ¿podrían (C) y (D) formales ser más fáciles que las de Clay?

Una revisión de riesgo, basada en lectura, del enunciado formal que demostró OpenAI, cuyas 18 declaraciones coinciden con el enunciado público de Google DeepMind tras la normalización textual, sin que se haya verificado la resolución de nombres ([procedencia](statement-provenance/README.md)). Compara cada cláusula del texto oficial de Clay (Fefferman, [PDF](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf), SHA-256 `c1b5f27b…a06d0c`) con las declaraciones en Lean en el commit `f9e8bc5` de OpenAI.

> **Estado:** escrito por un ingeniero de QA con asistencia de IA el 2026-10-21. **No** ha sido revisado por un matemático. Las filas de "hecho estándar" se formalizaron después como lemas puente en Lean ([tabla de puentes](clay-lean-bridges.md), [`bridges/`](../../bridges/README.md)), en relación con una transcripción literal del texto de Clay que todavía no ha sido revisada de forma independiente. Afina la [tabla de fidelidad](clay-lean-fidelity.md); no sustituye una revisión experta.

## Por qué importa la dirección

(C) y (D) tienen la forma **"existen datos tales que no existe solución"**. Una formalización puede volver esto más fácil de demostrar que la versión de Clay exactamente de dos maneras:

| Riesgo | Qué saldría mal | Es seguro cuando |
| --- | --- | --- |
| **Resquicio en los datos** | El enunciado formal le permite a quien demuestra elegir una velocidad inicial o una fuerza que Clay no permite. | Toda condición formal sobre los datos implica la condición de Clay. |
| **Resquicio en la solución** | La clase formal de soluciones es más estricta que la de Clay, así que "no existe solución" excluye menos candidatos. | Toda solución de Clay es también una solución formal. |

Una cláusula más estricta que la de Clay del lado de los datos, o más laxa del lado de la solución, solo hace más difícil demostrar el teorema formal, así que es inofensiva para (C) y (D).

## Cláusula por cláusula

Estado: **directo** significa la misma condición leída literalmente. **Hecho estándar** significa igual por un resultado de libro de texto; cuando se escribió esta revisión estaba nombrado pero no formalizado, y ahora está demostrado en Lean en [`bridges/`](../../bridges/README.md). **Atención** significa que depende de la interpretación.

| Cláusula de Clay | Lado | Lean | Lectura | Estado |
| --- | --- | --- | --- | --- |
| ν > 0, n = 3 | parámetro | `(nu : ℝ) (hnu : nu > 0)`, `ℝ³ = EuclideanSpace ℝ (Fin 3)` | Lean lo demuestra para todo ν > 0, lo que cubre el ν dado de Clay. | directo |
| u° suave | datos | `ContDiff ℝ ∞ u₀` | `∞` es C^∞ (`(⊤ : ℕ∞)`), no analítica `ω`. | directo |
| div u° = 0 | datos | `∀ x, ∇⬝ u₀ x = 0`, divergencia = traza de `fderiv` | Para un campo diferenciable, la traza del jacobiano es Σ ∂uᵢ/∂xᵢ. | hecho estándar (e) |
| (4) decaimiento de u° | datos, (C) | `∀ m K, ∃ C, ∀ x, ‖iteratedFDeriv ℝ m u₀ x‖ ≤ C / (1 + ‖x‖) ^ K` | La norma de operador de la derivada m-ésima y la mayor parcial ∂^α con abs(α) = m se acotan mutuamente salvo constantes que dependen de m y n. `K : ℝ` recorre todos los exponentes que usa Clay. | hecho estándar (a), (b) |
| f suave en ℝ³ × [0, ∞) | datos | `ContDiffOn ℝ ∞ (↿f) (univ ×ˢ Ici 0)` | Suavidad dentro de un semiespacio cerrado es igual a suavidad hasta la frontera. | hecho estándar (c) |
| (5) decaimiento de f | datos, (C) | `iteratedFDerivWithin ℝ m (↿f) (univ ×ˢ Ici 0) (x, t)` acotada por `C / (1 + ‖x‖ + t) ^ K` para t ≥ 0 | La derivada conjunta de orden m en (x, t) controla y es controlada por las parciales mixtas ∂x^α ∂t^k con abs(α) + k = m. | hecho estándar (a), (c) |
| (8) u°, f periódicas | datos, (D) | `IsOnePeriodic u₀`; `∀ t ≥ 0, IsOnePeriodic (f · t)` | `f (x + eᵢ) = f x` para cada vector unitario. | directo |
| (9) decaimiento de f periódica | datos, (D) | misma cota de derivada con `C / (1 + t) ^ K` | Como en (5). | hecho estándar (a), (c) |
| (1) la ecuación | solución | `derivWithin (v x ·) (Ici 0) t + fderiv ℝ (v · t) x (v x t) = nu • Δ (v · t) x - gradient (p · t) x + f x t` para t ≥ 0 | (u·∇)u es la derivada espacial aplicada a u. `Δ` y `gradient` son las versiones de Mathlib, sin coordenadas, de las sumas de Clay. La derivada temporal unilateral en t = 0 coincide con "t ≥ 0". Las soluciones son suaves, así que no aparecen valores espurios. | hecho estándar (c), (e) |
| (2) div u = 0 | solución | `∀ x, ∀ t ≥ 0, ∇⬝ (v · t) x = 0` | Como para div u°. | hecho estándar (e) |
| (3) condición inicial | solución | `∀ x, v x 0 = u₀ x` | Lo mismo. | directo |
| (6), (11) p, u ∈ C^∞(ℝ³ × [0, ∞)) | solución | `ContDiffOn ℝ ∞ (↿v) …`, `ContDiffOn ℝ ∞ (↿p) …` en `univ ×ˢ Ici 0` | En un semiespacio cerrado, suave-dentro-del-conjunto coincide con C^∞ hasta la frontera, que por el teorema de extensión de Seeley (Proc. AMS 15, 1964) es la restricción de una función C^∞. Ninguna de las dos clases es más estricta. | hecho estándar (c) |
| (7) energía acotada | solución, (C) | `∀ t ≥ 0, MemLp (‖v · t‖) 2` y `∃ E, ∀ t ≥ 0, ∫ x, ‖v x t‖ ^ 2 < E` | La cláusula `MemLp` evita que la integral de Bochner de Lean, que vale 0 para funciones no integrables, vuelva vacía la cota. Toda solución de Clay la satisface, porque una integral de Lebesgue finita de la función continua ‖u‖² significa u(·, t) ∈ L². La constante viene antes de "para todo t", como en Clay. | hecho estándar (d) |
| (10) u periódica | solución, (D) | `∀ t ≥ 0, IsOnePeriodic (v · t)` | Lo mismo. | directo |
| Fe de erratas: p periódica | solución, (D) | `∀ t ≥ 0, IsOnePeriodic (p · t)` | Ver abajo. | **atención** |
| Forma lógica de (C), (D) | — | `∃ u₀ f, data ∧ ¬ ∃ v p, solution` | "there exist u°, f … for which there exist no solutions (p, u)". | directo |

**Recuento:** 16 filas. 6 directas, 9 iguales por un hecho estándar, 1 que necesita atención, ninguna que abra un resquicio.

## El único punto que necesita atención: presión periódica en (D)

La fe de erratas de Clay dice: *"The further condition p(x + e_j, t) = p(x, t) should be made explicit in Eqn (8)."* La ecuación (8) es la lista de condiciones sobre los datos u° y f, pero p es parte de la solución. La formalización lee la fe de erratas como una condición sobre las soluciones, la única lectura en la que restringe algo, y agrega `isOnePeriodic_pressure` a la clase de soluciones periódicas.

Esto es una restricción del lado de la solución, así que importa para (D):

- Con u y f periódicas, la ecuación (1) obliga a que ∇p sea periódico, pero p misma puede entonces llevar una parte lineal espacial, p = q + c(t)·x, con q periódico. Esa parte es un gradiente de presión uniforme: integrar (1) sobre el toro da d/dt ∫u dx = ∫f dx − c(t), así que cambia la velocidad media.
- Sin la fe de erratas, esas presiones están permitidas, la clase de soluciones es más grande, y "no existe solución" sería una afirmación **más fuerte** que la (D) formal.
- Con la fe de erratas leída como un requisito sobre las soluciones, las clases coinciden.

Así que la (D) formal demuestra el problema enmendado por la fe de erratas. (C) está en ℝ³ y no se ve afectada. Si el enunciado enmendado es el problema del premio que se pretendía no es algo que esta revisión pueda resolver; es una pregunta para Clay y para revisores expertos.

## Puentes (ahora formalizados)

El plan de trabajo para estos puentes, como una tabla afirmación → lema → prueba → revisión → pendiente, está en [clay-lean-bridges.md](clay-lean-bridges.md).


Los hechos estándar (a)–(e) son los [puentes abiertos](clay-lean-fidelity.md#open-bridges-to-equivalence) de la tabla de fidelidad, ahora ubicados cláusula por cláusula. Son análisis de libro de texto, todos se pueden enunciar en Mathlib, y desde entonces se han demostrado como lemas en Lean en vez de solo citarse (ver la [tabla de puentes](clay-lean-bridges.md)). El punto de la fe de erratas necesita una decisión humana, no una demostración.
