> Traducción al español de [Glossary · Glosario](GLOSSARY.md). Si hay alguna diferencia, vale el original. Nota: el original es un documento bilingüe que repite cada término en inglés y en español; esta traducción conserva solo la sección en español, sin duplicar las entradas.

# Glosario

Las palabras usadas en este repositorio, en lenguaje sencillo.

**Lean.** Un asistente de pruebas: un programa que revisa cada paso de una demostración matemática escrita en su lenguaje. Si Lean acepta una demostración, cada paso se sigue de los anteriores y de los axiomas permitidos.

**Mathlib.** La gran biblioteca compartida de matemáticas escrita en Lean. Las demostraciones de OpenAI dependen de ella.

**Kernel.** El núcleo pequeño de Lean que da el sí o el no final sobre una demostración. El resto de Lean puede tener errores sin afectar ese veredicto, siempre que el kernel esté bien.

**nanoda.** Un segundo kernel para Lean, escrito por separado y en otro lenguaje. Correr los dos sobre la misma demostración reduce el riesgo de que un error en uno de ellos deje pasar una demostración equivocada.

**Comparator.** Una herramienta de los desarrolladores de Lean que toma un enunciado fijo (el *desafío*) y una demostración (la *solución*) y comprueba que la demostración prueba exactamente ese enunciado, usando solo los axiomas permitidos.

**Axiomas.** Los supuestos básicos que una demostración puede usar. Aquí solo se permiten los tres estándar de Lean: `propext`, `Classical.choice` y `Quot.sound`. `sorry` es lo que Lean usa para marcar una demostración que falta; una demostración que lo contiene está incompleta.

**Alternativas (A)–(D) de Clay.** El problema del milenio del Instituto Clay sobre Navier–Stokes se puede resolver de cuatro maneras. (A) y (B) piden soluciones suaves que existan para siempre, sin fuerza externa; siguen abiertas. (C) y (D) piden un ejemplo, con fuerza externa, en el que no exista una solución suave para todo tiempo. Las demostraciones de OpenAI son sobre (C) y (D).

**Transcripción, `ClayLiteral`.** Lo que escribí en Lean a partir del texto oficial de Clay, cláusula por cláusula ([`bridges/ClayLiteral.lean`](../bridges/ClayLiteral.lean)). Lean puede revisar demostraciones sobre ella, pero no si dice lo mismo que el PDF de Clay; eso lo tiene que revisar una persona.

**Puentes, K0, K1.** Los *puentes* son las demostraciones en Lean que conectan el enunciado formal de OpenAI con mi transcripción del texto de Clay. **K1** es el nombre de los cuatro teoremas puente (`k1_C`, `k1_D` y sus variantes unilaterales). **K0** es la revisión humana de la transcripción misma, con su [hoja de revisión](../bridges/K0_REVIEW.md).

**Fe de erratas.** Una corrección que Clay publicó a su enunciado, sobre la presión periódica. Si aplica a las soluciones en (D) es una de las dos preguntas abiertas de la revisión.

**Compilación, B1–B5.** Una compilación completa de las demostraciones de OpenAI. B1 a B5 son las cinco registradas aquí; B4 y B5 usaron `lake --no-cache build`, que compila todas las dependencias de Lean en vez de descargar archivos ya compilados.

**Caché de Mathlib.** Archivos de Mathlib ya compilados que Lean puede descargar en vez de compilarlos. Usarla es normal y ahorra horas, pero una compilación que la usa no es una compilación desde cero.

**Revisión desde cero (fresh replay).** `leanchecker --fresh` vuelve a revisar cada paso de una demostración terminada desde un estado vacío. Usa otra vez el kernel de Lean, así que no es un tercer kernel independiente.

**Pruebas de mutación, mutante.** Una forma de probar las pruebas: se daña el código (o el enunciado) a propósito y se comprueba que las pruebas lo notan. Cada copia dañada es un *mutante*. Un *mutante del enunciado* es un enunciado con un símbolo cambiado.

**PASS, KILLED, SURVIVED.** Los tres resultados posibles en la campaña numérica. PASS: una versión correcta pasó, como debía. KILLED: una versión dañada fue detectada, como debía. SURVIVED: una versión dañada no fue detectada. Aquí las 3 que sobreviven son cambios mínimos a propósito, que se dejaron visibles.

**Oráculo.** Una forma independiente de calcular la respuesta esperada, escrita aparte del código que se prueba, para que sea poco probable que un error esté en los dos.

**Recibo, hash, P6.** Un *recibo* registra lo que corrió un paso: su comando, sus entradas, sus salidas y su código de salida. Un *hash* (SHA-256) es la huella de un archivo: cualquier cambio en el archivo lo cambia. **P6** es una comprobación de este estudio: marca un recibo que nombra un log que no existe.

**Fallos sembrados, clases de fallo.** En el [benchmark de fallos a ciegas](../experiments/blind-faults/) se insertan fallos a propósito en evidencia registrada para ver qué comprobaciones los detectan. Cada tipo de fallo tiene un código (F1 a F6; F3 se retiró) y los casos van numerados de `case-01` a `case-21`; el [diseño](../experiments/blind-faults/DESIGN.md) los define.

**Versión de los datos, huella.** `verificar.py` imprime las dos. La *versión de los datos* es un código corto calculado a partir de los hashes de los archivos de evidencia. La *huella* la combina con el resultado de las seis comprobaciones. Dos personas con la misma versión y la misma huella obtuvieron exactamente el mismo resultado.

**Reproducción independiente.** Una repetición hecha por alguien que no es el autor y que no depende de su configuración. La corrida de alguien que conoce al autor también ayuda, pero no es una reproducción independiente en sentido estricto.

**DOI, Zenodo, ORCID.** Un *DOI* es un identificador permanente para citar un trabajo. *Zenodo*, del CERN, archiva cada versión de este repositorio y le asigna un DOI. *ORCID* es un identificador permanente de un investigador.
