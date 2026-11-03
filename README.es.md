# Scientific QA Evidence

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23925749.svg)](https://doi.org/10.5281/zenodo.23925749) [![verify](https://github.com/criguex/scientific-qa-evidence/actions/workflows/verify.yml/badge.svg)](https://github.com/criguex/scientific-qa-evidence/actions/workflows/verify.yml)

**Una auditoría independiente, con métodos de QA de software, de las demostraciones en Lean que OpenAI publicó sobre las ecuaciones de Navier–Stokes y de Euler.** La matemática es de OpenAI. Este repositorio la comprueba y deja esa comprobación lista para que cualquiera la repita.

[Página pública](https://criguex.github.io/scientific-qa-evidence/) · [Read in English](README.md) · [Glosario](docs/GLOSSARY.md) · [Cada afirmación con su evidencia](CLAIMS.md) · [Informe detallado](docs/DETAILS.es.md)

Por **Cristian Guerra Gómez**, ingeniero de QA de software, Medellín, Colombia · [ORCID 0009-0001-7189-5214](https://orcid.org/0009-0001-7189-5214) · [@criguex](https://github.com/criguex)

## En un minuto

En 2026 OpenAI publicó demostraciones, verificadas con el asistente de pruebas Lean, de que las ecuaciones de Navier–Stokes **con fuerza externa** pueden romperse: hay datos iniciales y fuerzas suaves para los que no existe una solución suave para todo tiempo. En el problema oficial del Instituto Clay de Matemáticas son las alternativas (C) y (D). OpenAI también demostró una singularidad en tiempo finito para las ecuaciones de Euler.

Soy probador de software, no matemático. Revisé esas demostraciones como revisaría una versión importante de un software:

- las recompilé desde una versión fija y las volví a verificar con herramientas independientes;
- cambié el enunciado a propósito, para confirmar que las comprobaciones lo notan;
- escribí en Lean el texto del propio Instituto Clay y demostré que los teoremas de OpenAI lo implican;
- registré cada comando, versión, hash y código de salida, incluidos mis propios errores.

**Resultado: no encontré ningún defecto dentro de este alcance.** Eso no es una certificación. Faltan dos cosas: que un experto revise mi transcripción a Lean del texto de Clay, y que alguien distinto a mí recompile las demostraciones en Lean.

**Qué no es.** No es matemática nueva ni una solución del problema del milenio: el problema sin fuerza externa, las alternativas (A) y (B) de Clay, sigue abierto. Todavía no lo ha revisado nadie con formación matemática.

## Compruébalo tú en cinco minutos

1. Instala [Python](https://www.python.org/downloads/) 3.9 o más reciente.
2. [Descarga este repositorio en ZIP](https://github.com/criguex/scientific-qa-evidence/archive/refs/heads/main.zip) y descomprímelo.
3. Abre una terminal en esa carpeta y ejecuta:

   ```sh
   python verificar.py
   ```

   En Mac o Linux puede ser `python3 verificar.py`. En menos de un minuto corre seis comprobaciones, muestra OK o FALLA en cada una y entrega una **huella** corta. Si tu huella coincide con la de otra persona para la misma versión de los datos, a los dos les dio exactamente lo mismo.

   Referencia de la versión actual de los datos (`c8edd482375d`): huella **`5292-A47D-AFA5`**, la misma en mi Mac y en los equipos de GitHub con Ubuntu, macOS y Windows.

4. Cuéntame qué te dio, igual o distinto, con el [formulario de reproducción](https://github.com/criguex/scientific-qa-evidence/issues/new?template=reproduccion.yml). Hasta ahora hay 4 reportes de 3 personas, y las tres me conocen ([reportes](evidence/reproductions/README.md)). Un resultado distinto es igual de útil.

Las mismas comprobaciones corren en cada push en [GitHub Actions](.github/workflows/verify.yml). Los comandos uno por uno, las versiones y qué resultados se recalculan o solo se verifican por hash están en [docs/REPRODUCE.md](docs/REPRODUCE.md) (en inglés).

## Qué se comprobó

| Pregunta | Respuesta | Registro |
| --- | --- | --- |
| ¿Compilan las demostraciones de OpenAI? | Sí. Cinco compilaciones desde el commit fijado de OpenAI `f9e8bc5`; las dos últimas (`lake --no-cache build`) compilaron localmente todas las dependencias de Lean, aunque se reutilizaron el toolchain de Lean y los binarios de los verificadores. Una recompilación posterior en la nube, el 2026-10-23 (609 de 609 módulos, salida 0), usó la caché de Mathlib. | [compilaciones](evidence/formal/cd-validation/README.md), [recompilación en la nube](evidence/lean-cloud-2026-10-23/README.md) |
| ¿Las aceptan verificadores independientes? | Sí. Comparator, con el kernel de Lean y el verificador separado nanoda, aceptó Navier–Stokes (C), (D) y Euler en las cinco compilaciones. Terminaron las 18 pruebas. | [revalidación](evidence/formal/cd-validation/README.md) |
| ¿El enunciado verificado es el publicado? | Sí. Seis cambios de un símbolo en el enunciado fueron rechazados, y un cambio solo en un comentario fue aceptado. Las 18 declaraciones coinciden tras normalización textual; la resolución de nombres no se verificó. | [mutantes](evidence/formal/cd-validation/mutants/), [procedencia](evidence/formal/statement-provenance/README.md) |
| ¿Coincide con el texto del Instituto Clay? | De 16 cláusulas, 6 coinciden directamente, 9 coinciden mediante hechos estándar y 1 necesita una decisión humana. En Lean, los teoremas de OpenAI implican mi transcripción literal de (C) y (D) de Clay; nadie independiente ha revisado esa transcripción. | [revisión de riesgos](evidence/formal/clay-lean-risk.md), [puentes](bridges/README.md) |
| ¿Qué significa que el verificador rechace algo? | Solo que «el enunciado cambió», no que «el teorema es falso». Se mostró con tres teoremas que Mathlib ya demuestra. | [controles con Mathlib](experiments/mathlib-controls/RESULTS.md) |
| ¿El procedimiento publicado revisa sus propios logs? | No. Un log cambiado dejó su resultado igual, y una comprobación contra hashes registrados al momento de correr lo detectó. Es práctica estándar en seguridad de la cadena de suministro (in-toto, SLSA); aquí se muestra como estudio de caso. | [revisión de recibos](experiments/receipt-check/RESULTS.md) |
| ¿Las pruebas numéricas detectan errores? | En nueve modelos sintéticos: 27 PASS · 54 KILLED · 3 SURVIVED por equipo, idénticos en macOS y Linux. Las 54 variantes eliminadas son 51 comportamientos eliminados distintos, y las 3 que sobreviven son cambios mínimos que se dejaron visibles a propósito. Todos los modelos son sintéticos; nada de esto es una medición empírica. | [evidencia numérica](evidence/README.md) |

Mis propios errores, encontrados y corregidos en público, están en el [informe detallado](docs/DETAILS.es.md#lo-que-encontramos) y en [FINDINGS.md](FINDINGS.md). [CLAIMS.md](CLAIMS.md) presenta cada afirmación con su evidencia y su limitación.

## Qué pido

1. **Una revisión de mi transcripción del texto de Clay.** Si sabes Lean o conoces el problema de Navier–Stokes: ¿es [`bridges/ClayLiteral.lean`](bridges/ClayLiteral.lean) fiel al enunciado oficial de Clay? La [hoja de revisión](bridges/K0_REVIEW.md) tiene 14 puntos para comparar con el PDF, cada uno con su página, ecuación y línea de Lean. Hay dos dudas principales: qué significa «suave» en el tiempo cero, y si la fe de erratas sobre la presión periódica aplica a las soluciones en (D).
2. **Una recompilación independiente de las demostraciones en Lean.** Todas las corridas en Lean hasta ahora las hice yo o herramientas bajo mi dirección. La [guía de reproducción](docs/INDEPENDENT_REPRODUCTION.md) tiene los pasos exactos y una plantilla de reporte.
3. **Que corras `verificar.py` en tu computador** y lo reportes con el formulario de arriba. Todavía falta un reporte desde Linux hecho por una persona.

## Limitaciones principales

- **Sin revisión de un matemático.** La conexión con el texto de Clay depende de una transcripción que nadie independiente ha revisado.
- **No es independiente.** Todas las compilaciones de Lean corrieron en infraestructura que yo escogí (un equipo Linux y un contenedor en la nube operado por un agente de IA), y los reportes de reproducción hasta ahora vienen de personas que conozco.
- **Solo dos implementaciones de kernel.** El kernel de Lean y nanoda revisaron las demostraciones; que dos verificadores coincidan no dice nada sobre errores que nadie conoce todavía.
- **Fuera de alcance:** si la demostración en Lean sigue el artículo escrito de OpenAI, algo que [arXiv:2610.08144](https://arxiv.org/abs/2610.08144) discute.
- **Pruebas numéricas pequeñas y sintéticas**, con mutantes gruesos, así que no hay una tasa de detección en el mundo real.

La lista completa está en el [informe detallado](docs/DETAILS.es.md#limitaciones-conocidas).

## Para saber más

| Si quieres… | Lee |
| --- | --- |
| Entender un término (Comparator, nanoda, mutante, huella…) | [Glosario](docs/GLOSSARY.md) |
| Ver el estudio completo: método, partes A–D, animaciones, todas las limitaciones | [Informe detallado](docs/DETAILS.es.md) |
| Revisar una afirmación contra su evidencia | [CLAIMS.md](CLAIMS.md) (en inglés) |
| Revisar la transcripción a Lean del texto de Clay | [bridges/K0_REVIEW.md](bridges/K0_REVIEW.md) (en inglés) |
| Recompilar tú las demostraciones en Lean | [docs/INDEPENDENT_REPRODUCTION.md](docs/INDEPENDENT_REPRODUCTION.md) (en inglés) |
| Ver las escenas de evidencia | [animaciones](animations/index.html) |
| Saber cómo se usó la IA | [docs/AUTHORSHIP.md](docs/AUTHORSHIP.md) (en inglés) |
| Encontrar cualquier archivo | [Mapa de la documentación](docs/README.md) |

## Citar, licencia y créditos

- **Cómo citar:** Guerra Gómez, C. *Scientific QA Evidence*. Zenodo. [doi:10.5281/zenodo.23925749](https://doi.org/10.5281/zenodo.23925749) (todas las versiones; ver [CITATION.cff](CITATION.cff)).
- **Licencia:** el código bajo [Apache-2.0](LICENSE); los textos, datos y medios bajo [CC BY 4.0](LICENSE-CC-BY-4.0.txt). Puedes reutilizarlo dando crédito ([detalles](LICENSE_STATUS.md)).
- **Demostraciones originales:** OpenAI, [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler) en `f9e8bc5` (Apache-2.0). **Enunciado del problema:** C. L. Fefferman, [Existence and smoothness of the Navier–Stokes equation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf), Instituto Clay de Matemáticas. **Enunciado del desafío:** Google DeepMind, [Formal Conjectures](https://github.com/google-deepmind/formal-conjectures). Las herramientas y sus versiones están en el [informe detallado](docs/DETAILS.es.md#créditos-derechos-y-estado).
- **Uso de IA:** hice este trabajo con asistentes de IA (OpenAI Codex y Anthropic Claude Code) bajo mi dirección. Yo escogí las preguntas, decidí qué cuenta como evidencia y respondo por cada afirmación ([detalles](docs/AUTHORSHIP.md)).
- **Versiones:** [todas las versiones](https://github.com/criguex/scientific-qa-evidence/releases), cada una archivada en Zenodo.
