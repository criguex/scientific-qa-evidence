---
name: escenarios-verificables
description: Diseñar y ejecutar escenarios reproducibles con contratos, oráculos, refinamiento y mutantes para contrastar modelos computables, sin confundir simulación con demostración.
---

# Escenarios verificables

Convierte una afirmación computable en un experimento cuyo alcance, condiciones de aceptación y fallos sean inspeccionables. La agnosticidad está en el protocolo: **cada fenómeno necesita su propio modelo, contrato, oráculo y adaptador**. No prometas simular cualquier teoría.

## Delimitar antes de ejecutar

Identifica qué afirmación se contrasta, dominio y unidades, condiciones iniciales y de borde, parámetros, horizonte, observables y riesgos. Distingue el sistema real, el modelo matemático, su discretización y la representación visual.

Elige un oráculo independiente de la implementación evaluada: solución analítica, datos experimentales trazables, implementación independiente o propiedad necesaria. Si solo hay invariantes, decláralo: conservar energía no garantiza precisión. Fija tolerancias y refinamientos antes de observar los mutantes; justifica sus escalas y registra cambios posteriores.

Si falta un contrato verificable, entrega una propuesta y enumera qué información falta. No inventes un oráculo ni conviertas una animación convincente en evidencia de verdad.

## Ejecutar con evidencia

- Usa una referencia sin mutaciones que cumpla el contrato. Una referencia fallida impide atribuir crédito de detección.
- Cambia operadores, ecuaciones o condiciones concretas para cada mutante. Conserva el nombre, la modificación exacta y la causa observada del rechazo.
- Separa pruebas analíticas, refinamiento temporal, sensibilidad espacial, invariantes, controles de infraestructura y revisión visual.
- Registra fuentes, versiones, máquina, parámetros, semillas, UTC, duración monotónica, comando, stdout/stderr, returncode y hashes de artefactos. Nunca registres secretos ni variables de entorno indiscriminadamente.
- Trabaja en carpetas nuevas; no sobrescribas la evidencia previa. Usa los recursos autorizados y límites explícitos de tiempo/hilos. Paraleliza solo trabajos independientes y evita competir con producción.

## Clasificar sin inflar resultados

| Estado | Condición |
|---|---|
| `KILLED` | referencia válida; mutante ejecutado; violación reproducible del contrato atribuible al cambio |
| `SURVIVED` | mutante ejecutado y aceptado por el contrato elegido; no implica corrección |
| `EQUIVALENT` | equivalencia justificada para el modelo/dominio, no meramente una prueba que pasó |
| `INFRA_FAIL` | fallo de instalación, importación, transporte, archivos, runner o entorno; sin crédito de detección |
| `INCONCLUSIVE` | referencia inválida/ausente, timeout sin diagnóstico causal o evidencia insuficiente |

Un `NaN` causado por una modificación documentada puede infringir el contrato de finitud; un crash sin explicación no cuenta como `KILLED`. No fuerces una tasa del 100 %. Excluye equivalentes e infraestructura de cualquier tasa de detección y muestra siempre los denominadores.

## Recursos incluidos

Para una calibración pequeña de ecuaciones periódicas 1D, lee [contratos-1d.md](references/contratos-1d.md). El helper [`run_scenario.py`](scripts/run_scenario.py) cubre **solo** calor, advección y onda con los contratos explícitos de esa referencia. No lo presentes como un motor universal.

```sh
python scripts/run_scenario.py --case heat --mutant baseline --output resultados/calor_base
python scripts/run_scenario.py --case heat --mutant sign --baseline resultados/calor_base/run.json --output resultados/calor_signo
```

La referencia se ejecuta antes del mutante en cada entorno que se quiera contrastar. Conserva resultados de ambos hosts para comparar reproducibilidad, sin afirmar que dos máquinas sustituyen una revisión matemática independiente.

Para osciladores lineales amortiguados o reacciones reversibles genéricas de primer orden, lee [contratos-ode-v3.md](references/contratos-ode-v3.md) y usa [`run_ode_scenario.py`](scripts/run_ode_scenario.py). Cubre 18 configuraciones adimensionales fijadas; no sustancias reales ni toda la física o química. Cada mutante necesita la referencia de su propia configuración. Los casos de equilibrio que no excitan un error no acreditan equivalencia del operador.

## Entrega

Expón primero la afirmación realmente respaldada y la limitación más importante. Incluye tabla de contratos, resultados y causas de clasificación; enlaces a datos/logs; instrucciones reproducibles; y qué evidencia adicional podría cambiar la conclusión. Mantén separadas prueba formal, aproximación numérica, datos observados e interpretación editorial.
