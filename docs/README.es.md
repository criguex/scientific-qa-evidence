> Traducción al español de [Documentation map · Mapa de la documentación](README.md). Si hay alguna diferencia, vale el original.

# Mapa de la documentación

Empieza por el [README](../README.es.md) ([in English](../README.md)). Esta página ordena cada documento según lo que quieras hacer. Los términos se explican en el [glosario](GLOSSARY.md). Salvo donde se indica, los documentos detallados están en inglés.

## Soy nuevo

| Documento | Qué es |
| --- | --- |
| [README](../README.md) · [README en español](../README.es.md) | Qué es esto y qué no, en un minuto, y cómo correr la comprobación |
| [Public page · Página pública](https://criguex.github.io/scientific-qa-evidence/) | Dos videos cortos, los cuatro pasos y los reportes recibidos, en español |
| [GLOSSARY.md](GLOSSARY.md) | Cada término en palabras simples, en inglés y en español |
| [Animations · Animaciones](../animations/index.html) | Trece escenas de evidencia y una escena ilustrativa ([guía](../animations/README.md)) |

## Quiero revisar las afirmaciones

| Documento | Qué es |
| --- | --- |
| [CLAIMS.md](../CLAIMS.md) | Cada afirmación, el archivo que la respalda, el resultado y la limitación |
| [DETAILS.md](DETAILS.md) · [DETAILS.es.md](DETAILS.es.md) | El informe completo: método, partes A-D, todas las limitaciones, créditos |
| [FINDINGS.md](../FINDINGS.md) | Qué encontró este protocolo que el procedimiento documentado de OpenAI no muestra |
| [RELATED_WORK.md](RELATED_WORK.md) | Trabajo previo y por qué no se afirma novedad |
| [evidence/README.md](../evidence/README.md) | Cómo está organizada y verificada la evidencia |
| [report/](report/README.md) | Resumen en PDF de siete páginas, una foto de la v1.3.1 |

## Quiero repetirlo

| Documento | Qué es |
| --- | --- |
| [`verificar.py`](../verificar.py) | Un comando, seis comprobaciones, una huella ([cómo](../README.md#check-it-yourself-in-five-minutes)) |
| [REPRODUCE.md](REPRODUCE.md) | Versiones, pasos desde un checkout limpio, qué se recalcula frente a qué solo se verifica por hash |
| [INDEPENDENT_REPRODUCTION.md](INDEPENDENT_REPRODUCTION.md) | Cómo recompilar las pruebas de OpenAI en Lean de forma independiente, con una plantilla de reporte |
| [evidence/reproductions/](../evidence/reproductions/README.md) | Reportes recibidos hasta ahora, en español |
| [evidence/FROM_ZERO.md](../evidence/FROM_ZERO.md) | Las comprobaciones corridas de nuevo desde un clon nuevo |

## Sé Lean

| Documento | Qué es |
| --- | --- |
| [bridges/K0_REVIEW.md](../bridges/K0_REVIEW.md) | La hoja de revisión de 14 puntos para la transcripción en Lean del texto de Clay |
| [bridges/ClayLiteral.lean](../bridges/ClayLiteral.lean) · [bridges/Bridges.lean](../bridges/Bridges.lean) | La transcripción y la prueba de que los teoremas de OpenAI la implican |
| [bridges/README.md](../bridges/README.md) | Recibo de compilación de los puentes |
| [evidence/formal/](../evidence/formal/) | Compilaciones, corridas de Comparator, mutantes del enunciado, revisiones desde cero, procedencia, vigencia del kernel, revisión de riesgos de Clay |
| [evidence/lean-cloud-2026-10-23/](../evidence/lean-cloud-2026-10-23/README.md) | La recompilación en la nube del 23 de octubre de 2026 (609/609, caché de Mathlib), en español y en inglés |

## Experimentos

| Documento | Qué es |
| --- | --- |
| [experiments/blind-faults/](../experiments/blind-faults/) | Benchmark de fallos sembrados: diseño, v1 congelada con fe de erratas, v2 corregida |
| [experiments/mathlib-controls/](../experiments/mathlib-controls/) | «El enunciado cambió» no es «el teorema es falso», sobre tres teoremas de Mathlib |
| [experiments/receipt-check/](../experiments/receipt-check/README.md) | Recibos frente a logs sobre registros auténticos, dos casos ([solicitud de revisión](REVIEW_REQUEST.md)) |
| [experiments/version-port/](../experiments/version-port/RESULTS.es.md) | Las comprobaciones repetidas en tres versiones de Lean: lean4lean como tercer kernel sobre la versión auditada; las pruebas no compilan sin cambios en v4.34.0 ni en v4.35.0 |
| [evidence/numerical/source/CONTRACT.md](../evidence/numerical/source/CONTRACT.md) | El contrato congelado de los nueve modelos numéricos |

## Sobre el proyecto

| Documento | Qué es |
| --- | --- |
| [AUTHORSHIP.md](AUTHORSHIP.md) | Quién hizo qué, y cómo se usaron los asistentes de IA |
| [CODEX_WORK_LOG.md](CODEX_WORK_LOG.md) | Qué hizo Codex el 2026-10-20, sesión por sesión |
| [evidence/bitacora/](../evidence/bitacora/) | Registro fechado de mi trabajo, en español |
| [LICENSE_STATUS.md](../LICENSE_STATUS.md) | Apache-2.0 para el código, CC BY 4.0 para el texto, los datos y los medios |
| [CITATION.cff](../CITATION.cff) | Cómo citar: DOI de Zenodo y ORCID |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Reglas para cambiar este repositorio |
