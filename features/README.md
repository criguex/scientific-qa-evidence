# Escenarios en Gherkin

Cada archivo `.feature` es una historia de usuario de la auditoría, escrita en Gherkin en español (`# language: es`): **Dado** el contexto, **Cuando** la acción y **Entonces** el resultado que se puede medir.

| Archivo | Historia | Criterios que cumplen |
| --- | --- | --- |
| [01-compilacion.feature](01-compilacion.feature) | HU-1 · Las demostraciones compilan | 3 de 3 |
| [02-verificadores.feature](02-verificadores.feature) | HU-2 · Otros verificadores dicen lo mismo | 3 de 4 |
| [03-trampas-al-enunciado.feature](03-trampas-al-enunciado.feature) | HU-3 · El enunciado no deja pasar trampas | 4 de 4 |
| [04-pregunta-de-clay.feature](04-pregunta-de-clay.feature) | HU-4 · Es la pregunta de Clay | 2 de 4 |
| [05-reproducible.feature](05-reproducible.feature) | HU-5 · Otra persona lo repite sin mí | 2 de 4 |
| [06-trazabilidad.feature](06-trazabilidad.feature) | HU-6 · La evidencia es trazable | 5 de 5 |

**Cómo leer las etiquetas.** `@HU-n` es la historia, `@CA-n.m` el criterio de aceptación, `@cumple` un criterio que la evidencia respalda y `@pendiente` uno que todavía no. Los escenarios pendientes terminan con un comentario que dice por qué.

**Qué son y qué no son.** Estos escenarios describen las comprobaciones que ya se ejecutaron y apuntan a su evidencia. No son pruebas automatizadas: las compilaciones de Lean toman más de una hora y corren aparte. Lo que sí se ejecuta en cada push está en [`verificar.py`](../verificar.py) y en el [CI](../.github/workflows/verify.yml).

La explicación completa, con casos de prueba, ejecuciones, defectos y la matriz de trazabilidad, está en [docs/METODOLOGIA.md](../docs/METODOLOGIA.md) ([English](../docs/METHODOLOGY.md)). La versión interactiva, con los escenarios también traducidos al inglés, está en [criguex.github.io/scientific-qa-evidence/metodologia](https://criguex.github.io/scientific-qa-evidence/metodologia/).
