> Traducción al español de [Related work and novelty assessment](RELATED_WORK.md). Si hay alguna diferencia, vale el original.

# Trabajo relacionado y evaluación de novedad

¿Es nuevo el método de este paquete? Esto es una **búsqueda dirigida**, no una revisión sistemática. Se hizo el 2026-10-21 con búsquedas web sobre cuatro temas: mutación de especificaciones, mutación de proyectos de verificación formal, pruebas de verificadores de pruebas, y QA de software científico. La columna de verificación dice hasta dónde se comprobó cada fuente; «abstract» o «registro de búsqueda» significa que no se leyó el texto completo.

## Qué ya existe

| Área | Trabajo previo | Qué hace | Relación con este estudio | Verificado |
| --- | --- | --- | --- | --- |
| Pruebas de mutación | DeMillo, Lipton y Sayward (1978) | Sembrar fallos conocidos y comprobar que las pruebas los notan | La base de las dos líneas | Referencia estándar |
| Mutación de especificaciones | Budd y Gopal, «Program testing by specification mutation», *Computer Languages* 10(1):63-73 (1985); Black, Okun y Yesha, «Mutation operators for specifications», ASE 2000 | Mutar la especificación, no solo el código | Los mutantes del enunciado son mutantes de especificación | Registro de búsqueda |
| Mutación de proyectos de asistentes de pruebas | Celik, Palmskog, Parovic, Gallego Arias y Gligoric, «Mutation Analysis for Coq», ASE 2019; Jain et al., demo de la herramienta mCoq, ICSE 2020 | Mutar definiciones de Coq y volver a revisar las pruebas; un mutante cuyas pruebas siguen pasando apunta a una especificación incompleta | El antecedente más cercano para la mutación formal. mCoq muta definiciones y espera que las pruebas se rompan; este estudio muta el enunciado del desafío y espera que el verificador del enunciado lo rechace. | [Diapositivas](https://users.ece.utexas.edu/~gligoric/slides/CelikETAL19mCoq.pdf), [página de ASE](https://2019.ase-conferences.org/details/ase-2019-papers/90/Mutation-Analysis-for-Coq) |
| Mutación en proyectos de Lean | Práctica de la comunidad, por ejemplo [una puerta de mutación en Lean](https://github.com/MorphIQ-Labs/tollgate/pull/23) que muta los cuerpos de las definiciones y exige que los mutantes sobrevivientes se justifiquen | La misma idea que mCoq, en Lean 4 | Muestra que la práctica existe en Lean | Solo el texto del pull request |
| Mutación de verificadores y oráculos | Du, Luu, Huang y Ng, «Measuring the Checker: Mutation Analysis for GPU-Kernel Benchmark Oracles», [arXiv:2609.22220](https://arxiv.org/abs/2609.22220) (2026) | Análisis de mutación dirigido al verificador de un benchmark en vez de al código bajo prueba | El mismo objetivo que los mutantes del enunciado, en otro dominio | Solo el título |
| Mutación con conciencia de tolerancia para código numérico | Hook y Kelly: pruebas de sensibilidad a la mutación (tesis de Hook, Queen's University, 2009; MATmute) | Barrer el tamaño de una mutación para medir qué tan pequeño es un error que una prueba todavía detecta, bajo una tolerancia numérica | Llena un vacío que este estudio declara abiertamente: el umbral de detección no se midió | Registro de tesis |
| Pruebas de software científico | Kanewala y Bieman, «Testing scientific software: a systematic literature review», *Information and Software Technology* (2014), [arXiv:1804.01954](https://arxiv.org/abs/1804.01954) | Revisa el problema del oráculo y sus remedios | Contexto para los oráculos independientes y las tolerancias congeladas | Abstract |
| Verificadores de pruebas independientes | criterio de de Bruijn; [Lean4Lean](https://arxiv.org/abs/2403.14064) (Carneiro); [nanoda](https://github.com/ammkrn/nanoda_lib) (Bailey); [Comparator](https://github.com/leanprover/comparator) y la [guía de validación de pruebas](https://lean-lang.org/doc/reference/4.35.0/ValidatingProofs/) de Lean | Volver a revisar pruebas con kernels pequeños y separados, y comprobar el enunciado contra un desafío confiable | Este estudio usa estas herramientas; no las extiende | Páginas primarias |
| Límites de los kernels independientes | Bugs de solidez del kernel de Lean en 2026: [post mortem de #14576](https://leodemoura.github.io/blog/2026-8-1-postmortem-for-kernel-soundness-bug-14576/), [post mortem de la caza de bugs](https://leodemoura.github.io/blog/2026-8-24-postmortem-for-the-kernel-soundness-bug-hunt/), [notas de Lean 4.34.0](https://lean-lang.org/doc/reference/latest/releases/v4.34.0/) | Un bug del kernel y un bug separado de nanoda dejaron pasar la misma prueba falsa | Que dos kernels coincidan no es una garantía; ver [vigencia del kernel](../evidence/formal/kernel-currency.md) | Páginas primarias |
| Enunciados mal formalizados | Ospanov, Farnia y Yousefzadeh, «miniF2F-Lean Revisited» ([arXiv:2511.03108](https://arxiv.org/abs/2511.03108)); Poiroux, Weiss, Kunčak y Bosselut, «Reliable Evaluation and Benchmarks for Statement Autoformalization», que presenta ProofNet# ([arXiv:2406.07222](https://arxiv.org/abs/2406.07222)); Ammanamanchi, Bhat y Biderman, «Faults in Our Formal Benchmarking» ([arXiv:2606.29493](https://arxiv.org/abs/2606.29493)) | Los enunciados formales en los benchmarks a menudo difieren de los informales que se pretendían | Por qué importan la procedencia del enunciado y la revisión de Clay | Abstracts |
| Procedencia de la cadena de suministro y atestación de pasos | [in-toto](https://in-toto.io/) (`in-toto-run` registra el comando de cada paso, los hashes de los archivos de entrada y salida, el valor de retorno y stdout/stderr, firmados, y los verifica contra un layout); [procedencia SLSA](https://slsa.dev/provenance/v1) (constructor, definición de la compilación y dependencias resueltas con hash) | Atar cada paso de una compilación o pipeline a los artefactos exactos que usó y produjo | La comprobación de recibos (P6 y la comprobación por hash) es un subconjunto pequeño de lo que registra in-toto; detectar un log cambiado por SHA-256 es práctica establecida | Documentación; añadido el 2026-10-22 tras una revisión externa |
| **Esta prueba exacta** | Bastounis, Circelli y Hansen, «Navier-Stokes lost in translation: Why Lean verification of AI autoformalisation does not guarantee correct natural language proofs», [arXiv:2610.08144](https://arxiv.org/abs/2610.08144) (6 oct. 2026) | Sostiene que la prueba formalizada en Lean de OpenAI no corresponde a la prueba en lenguaje natural del artículo de OpenAI | Una capa distinta de este estudio; ver abajo | Abstract |

## Dónde se ubica este estudio

Que una comprobación en Lean pase involucra preguntas separadas:

| Capa | Pregunta | Este estudio |
| --- | --- | --- |
| Aceptación del kernel | ¿La prueba en Lean deriva el enunciado formal? | Probado: cinco compilaciones, dos kernels en Comparator, una revisión desde cero, lean4lean como tercer kernel sobre la versión auditada, vigencia del kernel |
| Fidelidad del enunciado | ¿El enunciado formal es el problema que se pretendía? | Parcialmente: procedencia textual frente al enunciado de DeepMind y una revisión basada en lectura frente al texto de Clay |
| Correspondencia de la prueba | ¿La prueba en Lean sigue el argumento del artículo? | **No probado.** arXiv:2610.08144 sostiene que no. Su abstract no afirma que algún teorema de Lean sea falso ni que el enunciado final difiera del de Clay. |

Así que los resultados aquí dicen que los teoremas formales se aceptan, repetidamente y desde cero. No dicen nada sobre si el artículo en lenguaje natural de OpenAI es correcto.

## Evaluación de novedad

**No es nuevo:** atar los pasos de un pipeline a entradas, salidas y logs con hash (in-toto, SLSA), mutar especificaciones (1985, 2000), mutar proyectos de verificación formal (mCoq, 2019), mutar el verificador de un benchmark (2026), kernels independientes y comprobación de enunciados (Comparator, nanoda, Lean4Lean), mutación con conciencia de tolerancia de código numérico (Hook y Kelly), y oráculos independientes para software científico.

**No encontrado en las fuentes consultadas:** usar mutantes de un solo símbolo de un enunciado de desafío, con un control de solo comentario, como control negativo sobre un verificador de igualdad de enunciados como Comparator; y correr eso junto con una campaña de mutación numérica bajo un solo protocolo reproducible y atado por hash, sobre una formalización pública de un problema del milenio.

**Conclusión.** El método es una combinación y aplicación de técnicas establecidas. Una afirmación de novedad metodológica **no está respaldada**. La afirmación más estrecha de que el control de mutante del enunciado no se encontró en las fuentes consultadas vale solo para esta búsqueda dirigida y podría revertirse con una revisión sistemática.

## Qué cambia esto en el paquete

- La pregunta abierta sobre «novedad» en [CLAIMS.md](../CLAIMS.md) queda respondida: no se afirma, y se nombra el trabajo previo.
- La correspondencia de la prueba con el artículo de OpenAI se marca como fuera de alcance, citando arXiv:2610.08144.
- Se añadió una [comprobación de vigencia del kernel](../evidence/formal/kernel-currency.md) después de que la búsqueda sacara a la luz los bugs de solidez de 2026.
- Las pruebas de sensibilidad a la mutación de Hook y Kelly son el siguiente paso natural para la línea numérica: miden el umbral de detección que este estudio dejó sin medir.
