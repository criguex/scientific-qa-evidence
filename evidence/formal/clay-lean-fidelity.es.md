> Traducción al español de [clay-lean-fidelity.md](clay-lean-fidelity.md). Si hay alguna diferencia, vale el original.

# Correspondencia documental Clay–Lean: Navier–Stokes

**Estado:** solo una comparación documental de las cláusulas del enunciado. Esto no es una prueba de que los enunciados en Lean sean equivalentes a la formulación de Clay, no es una opinión matemática especializada, y no ha recibido revisión experta independiente. Lee los enunciados citados; nombres parecidos por sí solos no establecen correspondencia.

| Texto de Clay (PDF oficial, páginas 1–2 y 6) | Declaración o cláusula visible en Lean en la instantánea fijada de OpenAI | Nota de alcance |
| --- | --- | --- |
| (1) Ecuación de Navier–Stokes | `NavierStokesExistenceAndSmoothness.navier_stokes` | Propósito y forma parecidos; los detalles de operadores y convenciones todavía necesitan comparación. |
| (2) Incompresibilidad | `div_free` | La definición y las convenciones de coordenadas todavía necesitan comparación. |
| (3) Datos iniciales | `initial_condition` | El nombre por sí solo no establece la igualdad de las clases de datos admisibles. |
| (4) Decaimiento de la velocidad inicial | `InitialVelocityConditionDecay.decay` | Comparar el cuantificador exacto y la forma del decaimiento. |
| (5) Decaimiento de la fuerza | `ForceConditionDecay.decay` | Comparar las condiciones completas. |
| (6), (11) Suavidad de la velocidad y la presión | `velocity_smooth`, `pressure_smooth` | La regularidad espacial y temporal y el dominio requieren comparación. |
| (7) Energía | `MemLp` y `globally_bounded_energy` | La norma, el exponente, la medida y los cuantificadores requieren verificación. |
| (8) Periodicidad de los datos iniciales y la fuerza | `IsOnePeriodic u₀`, `IsOnePeriodic f` | Verificar la convención de período y el dominio. |
| (9) Decaimiento temporal de la fuerza periódica | `ForceConditionPeriodic.decay` | La instancia concreta de fuerza cero satisface esta condición. |
| (10) Periodicidad de la velocidad | `isOnePeriodic_velocity` | Verificar el período, el dominio y la representación. |
| Fe de erratas de la página 6 a (8): periodicidad de la presión | `isOnePeriodic_pressure` | Corrección editorial asociada a (8), no una condición (10) numerada aparte. |
| (C), (D) Ruptura con viscosidad positiva | `ν > 0`, `n = 3`, existencia de `u₀, f`, y no existencia de `v, p` en el teorema de ruptura | Comparar todas las hipótesis, la conclusión y la estructura lógica. Euler es aparte y no forma parte de esta comparación A–D de Clay. |

## Fuentes fijadas

- [Clay Mathematics Institute, descripción oficial de Navier–Stokes (PDF)](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf), páginas 1–2 y 6. SHA-256: `c1b5f27b1a64705cfaf1afceea513db5deedca8a18ca56ab32e7f86445a06d0c`.
- [Google DeepMind FormalConjectures, fuente de Navier–Stokes fijada](https://github.com/google-deepmind/formal-conjectures/blob/8bf45ed70d48b2b2a501de9c00b26bfa38c573ee/FormalConjectures/Millenium/NavierStokes.lean), commit `8bf45ed70d48b2b2a501de9c00b26bfa38c573ee`.
- Repositorio de fuente formal de OpenAI, commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`. Las pruebas formales pertenecen a sus autores originales; este paquete de QA no reclama autoría de esas pruebas.

## Puentes abiertos hacia la equivalencia

Un argumento de equivalencia todavía necesitaría justificar al menos: (a) derivadas por multiíndice frente a normas de derivadas de Fréchet; (b) el exponente real `K` y su convención de decaimiento frente a las definiciones formales; (c) la regularidad en `t = 0` y el uso de `derivWithin`; (d) las formulaciones de integrabilidad y medida, incluido evitar integrales vacías; y (e) la equivalencia de coordenadas y operadores. Una transferencia de la no existencia también necesita las dos direcciones: los datos formales admisibles deben implicar datos admisibles de Clay, y toda solución de Clay debe inducir una solución en la formalización.

Una [revisión de riesgo](clay-lean-risk.md) cláusula por cláusula ya ubica cada uno de estos puentes y señala el único punto interpretativo, la presión periódica en (D).

El control positivo periódico no nulo es una instancia concreta en el toro y reporta los axiomas estándar. No establece estos puentes, no cubre toda hipótesis de Clay, ni demuestra la conclusión global.
