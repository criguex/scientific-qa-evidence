# Auditoría reproducible de verificaciones formales y contratos numéricos en modelos de fluidos, osciladores y reacciones

**Informe técnico de síntesis · versión interna · 20 de octubre de 2026**
**Estado editorial:** autores, afiliación, ORCID, consentimiento y revisión matemática humana pendientes. No es una postulación ni una solución propia al problema del Milenio.

## Resumen

Este informe reúne varias líneas de evidencia que responden preguntas distintas: una comparación de dos mallas para un flujo Taylor–Green; campañas numéricas acotadas de calor, transporte, onda, osciladores amortiguados y reacciones reversibles; y verificaciones formales reproducibles de cuatro teoremas configurados en desafíos de Navier–Stokes y Euler. En V3 se registraron 150 ejecuciones reales (90 principales, 30 réplicas entre equipos y 30 controles de revisión local; un fixture copiado se excluye del conteo). El mayor error RMS frente a referencias analíticas fue 4,2667693 × 10⁻⁸, calculado para las 18 integraciones de referencia (nueve osciladores y nueve reacciones) en 81 tiempos comunes; no resume las 150 ejecuciones ni las trayectorias mutantes. El umbral era 10⁻⁶. Se detectaron 51 de 56 pares de configuración y mutante evaluados, después de excluir 16 combinaciones etiquetadas `EQUIVALENT`; cinco pares sobrevivieron. Esta proporción describe los pares evaluados, no una probabilidad de verdad ni una equivalencia global de operadores.

En la verificación formal posterior al corte, Comparator informó aceptación de los cuatro teoremas configurados para Navier–Stokes y Euler por nanoda y por el kernel predeterminado de Lean, bajo los tres axiomas autorizados. Seis controles pequeños de respuesta Comparator —dos positivos y cuatro negativos— dieron las respuestas previstas; los rechazos ocurrieron antes de invocar los kernels. Estos resultados son computacionales y acotados. No son certificación externa, revisión matemática humana ni una afirmación de que el equipo haya resuelto el problema del Milenio.

## Pregunta y alcance

La pregunta práctica es qué permiten concluir contratos numéricos explícitos, mutantes intencionales, comparaciones de referencia y comprobaciones formales cuando sus entradas, versiones y límites quedan registrados. El trabajo se organiza como una auditoría de artefactos y herramientas concretos, no como una teoría universal de verificación numérica ni como una re-demostración independiente de los teoremas fuente.

Los desafíos formales y sus soluciones pertenecen a sus autores originales. El checkout usado fue fijado al commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`. Navier–Stokes incluye fuerza externa; los autores adaptaron el enunciado de Euler. La aceptación de una prueba en esos enunciados configurados no responde automáticamente a otros enunciados de regularidad o existencia.

## Métodos y evidencia

### Modelos numéricos

V1 compara simulaciones de Taylor–Green en mallas 32³ y 64³. La velocidad final de Euler difiere 16,7223 % entre esas mallas; Navier–Stokes difiere 0,0535176 %. Son dos niveles de resolución, insuficientes para establecer convergencia. La evidencia espacial no debe confundirse con una prueba formal.

V2 registra 42 ejecuciones en dos equipos para modelos analíticos unidimensionales de calor, transporte y onda. Por equipo hubo tres referencias, trece mutantes detectados, dos sobrevivientes y tres equivalentes. Los clips muestran intervalos mayores que el horizonte de validación numérica del solver; representan fórmulas analíticas y no fluidos tridimensionales ni validación experimental.

V3 evalúa nueve osciladores amortiguados y nueve reacciones reversibles lineales. Los pasos fueron 0,05, 0,025 y 0,0125 hasta T=4. El máximo RMS de 4,2667693 × 10⁻⁸ corresponde solo a las 18 integraciones base comparadas con referencias analíticas en 81 tiempos comunes; no es el máximo de las 150 ejecuciones ni incluye las trayectorias mutantes. Los invariantes se comprobaron en los pasos del contrato. Un cálculo matricial 2×2 contrastó los oráculos en 90 puntos. El diseño incluye 90 corridas principales, 30 réplicas entre hosts y 30 controles de revisión local. Las salidas, contratos, métricas y resúmenes están vinculados abajo.

### Verificación formal y calibración de respuesta

El build Lean documentado terminó OK a las 12:02:18 de Bogotá. Se inspeccionaron cuatro teoremas, sus axiomas estándar y ausencia de `sorryAx`. En la ejecución posterior con Comparator, nanoda y el kernel predeterminado de Lean aceptaron los cuatro teoremas configurados de los desafíos NS/Euler; el proceso terminó con código 0 y listó `propext`, `Classical.choice` y `Quot.sound`. Las advertencias `sorry` existentes corresponden a placeholders del desafío y no se interpretan como axiomas de la solución.

La primera tanda de tres fixtures produjo un positivo válido (ambos kernels aceptaron; 2,82 s) y dos rechazos esperados: mismatch entre enunciados (1,44 s) y axioma no permitido (1,49 s). Una extensión de otros tres fixtures aceptó un renombrado alfa válido (ambos kernels; 3,16 s), rechazó un axioma oculto (1,52 s) y rechazó una condición existencial debilitada con testigo cero (1,45 s). Los cuatro negativos fueron detenidos por Comparator antes de los kernels. La calibración muestra estas seis respuestas concretas; no establece tasa de falsos positivos, no verifica rechazo de prueba inválida por los kernels y no reemplaza una corrida adversarial desde cero.

El checkout formal ya estaba compilado; no se hizo un arranque limpio. La versión fijada de Landrun exige ABI 10 por defecto, mientras que el host ofrecía Landlock ABI 7. La ejecución usó `--best-effort` upstream y controles externos systemd/seccomp observados en los logs. Esto no equivale a probar ABI 10 ni acredita una sandbox completa.

## Resultados principales

| Línea | Resultado reproducible | Qué no demuestra |
| --- | --- | --- |
| V1, fluido | Diferencia de velocidad final 16,7223 % para Euler y 0,0535176 % para Navier–Stokes entre 32³/64³ | Convergencia espacial o precisión suficiente |
| V2, PDE analíticas 1D | 42 ejecuciones entre dos hosts; conteos separados de referencias, detecciones, sobrevivientes y equivalentes | Flujo 3D, validez hasta todo el tiempo visualizado o comportamiento de sustancias reales |
| V3, ODE | 150 ejecuciones en total; error RMS máximo 4,2667693 × 10⁻⁸ en 18 integraciones de referencia × 81 tiempos comunes, frente al umbral 10⁻⁶; 51/56 pares evaluados detectados | El RMS no resume las 150 ejecuciones ni mutantes; no implica probabilidad de verdad, detección universal o equivalencia global de sobrevivientes |
| Formal, NS/Euler | Cuatro teoremas configurados aceptados por Comparator/nanoda y kernel Lean en el checkout fijado | Certificación externa, auditoría desde cero o equivalencia con cualquier otro enunciado |
| Calibración Comparator | Seis controles: dos positivos aceptados por ambos kernels y cuatro negativos rechazados por Comparator antes de invocar los kernels | Ausencia general de falsos positivos ni rechazo demostrado de prueba inválida por los kernels |

En V3, las 16 combinaciones etiquetadas `EQUIVALENT` se excluyeron del denominador de 56 pares evaluados. Los cinco sobrevivientes pueden coincidir en la trayectoria del caso probado por equilibrio o valor cero; eso no demuestra que los operadores sean equivalentes fuera de esa trayectoria. En `rxn05`, un mutante de fuga aumentó A+B un 40,3126 %, mientras que un mutante congelado conservó A+B pese a un error de trayectoria 0,345866. Un invariante aislado no garantiza que la solución sea correcta.

## Amenazas a la validez y asuntos abiertos

Las ecuaciones V2/V3 son modelos analíticos y adimensionales, no ensayos de laboratorio. No se probaron sustancias reales, incertidumbre instrumental, ruido, química no lineal, transporte espacial de especies ni familias arbitrarias de ecuaciones. Las réplicas V3 comparten código y no constituyen independencia algorítmica completa. La comparación de dos mallas no prueba convergencia.

En lo formal permanecen pendientes el control positivo global no nulo de Euler, la revisión matemática humana y una ejecución clean/adversarial start. NS-09 se limita a incompatibilidad de un helper/testigo observado; no demuestra imposibilidad matemática ni que toda demostración requiera fuerza. Los desafíos se inspeccionaron en el alcance exacto del checkout y de sus autores. Ningún resultado aquí constituye una demostración propia de explosión ni resuelve el problema del Milenio.

La calibración documentada cubre seis respuestas de Comparator distribuidas en dos tandas con bundles separados. No establece garantías universales ni reemplaza pruebas adversariales desde una instalación limpia.

## Trazabilidad, herramientas de IA y responsabilidad humana

El usuario declara más de ocho años de experiencia en QA automation e infraestructura propia. Se registra como autodeclaración, no como currículum verificado de forma independiente. Los nombres, afiliación institucional, ORCID, contribuciones formales y consentimiento de cada autor siguen pendientes; por tanto este documento no identifica autores ni está listo para envío.

| Herramienta | Estado documentado en esta versión | Límite de atribución |
| --- | --- | --- |
| OpenAI Codex | Apoyo en implementación, composición de video, pruebas, organización de evidencia y redacción técnica del repositorio | El registro de sesión/modelo exacto y la asignación detallada de contribuciones deben archivarse antes de cualquier envío; no es revisor independiente ni autor responsable |
| Google Gemini | Tres enlaces revisados en UI con alcances distintos: A solo metadatos y cuerpo vacío; B opiniones/propuestas sin artefactos de ejecución; C intercambio exploratorio registrado manualmente | No se atribuyen resultados científicos o código ejecutado. Las respuestas y valores citados por el modelo no son evidencia de este proyecto |
| Anthropic Claude | Reconstrucción documental actual, Claude Code CLI 2.1.143, Sonnet 4.6 (uso auxiliar reportado de Haiku 4.5); no es sesión histórica | No se recuperó conversación histórica pertinente. La reconstrucción se basó en el repositorio actual y no es corroboración independiente |
| Revisión humana | Pendiente para revisión matemática y validación final de narración | ASR, compiladores y asistentes de IA no sustituyen la responsabilidad humana de revisar y defender cada afirmación |

La [nota de procedencia y aportes](../provenance/PROCEDENCIA_IA_Y_APORTES.md) contiene el registro observado de Claude/Gemini, transcripciones manuales acotadas y vacíos de atribución. La declaración de uso de herramientas no implica aprobación, autoría académica automática ni verificación por los proveedores. Antes de publicación se debe completar un registro reproducible de modelos/versiones, tareas, prompts o referencias, cambios aceptados/rechazados y revisión humana. Las personas autoras deben confirmar que leyeron las fuentes citadas y pueden defender el contenido.

## Trabajo relacionado y posición de la contribución

Li et al. describen en su preprint [*A semantic mutation metric for metamorphic relation adequacy in scientific computing programs*, arXiv:2605.17437v2](https://arxiv.org/abs/2605.17437v2) el problema del oráculo en cómputo científico, operadores de mutación semántica y una clasificación por capas para separar fallos de tolerancia, distribución u artefactos. Esa literatura es contexto relevante, no evidencia de novedad de este repositorio. Este informe no afirma haber inventado pruebas metamórficas, mutación semántica, verificación formal ni un método universal. Su contribución acotada es organizar y volver inspeccionables contratos, fixtures, resultados, hashes y límites de estas campañas concretas.

## Reproducibilidad y artefactos

- [Informe técnico V3](../ode-v3/INFORME_FISICA_QUIMICA_V3.md), [resumen de campaña](../ode-v3/ode_v3/campaign_summary.json), [mediciones cuantitativas](../ode-v3/ode_v3/quantitative_measurements.json) y [contratos congelados](../scenario-runners/escenarios-verificables/references/contratos-ode-v3.md).
- [Acta formal poscorte](../report-v4/report_v4/ACTA_VERIFICACION_FORMAL_POSCORTE.md), [logs terminales seleccionados](../report-v4/report_v4/ns08_terminales/) y [bundle operativo NS08](../report-v4/report_v4/ns08_ops_bundle/).
- [Acta de calibración Comparator](../report-v4/report_v4/ACTA_CALIBRACION_COMPARATOR.md), [bundle inicial](../report-v4/report_v4/COMPARATOR_CALIBRATION_BUNDLE/) y [extensión](../report-v4/report_v4/COMPARATOR_CALIBRATION_EXTENSION_BUNDLE/); verificar los SHA consignados en el acta.
- [Resumen derivado V1](../report-v4/report_v4/qa/formal_derived.json) y [resumen derivado V3](../report-v4/report_v4/qa/ode_derived.json) son comprobaciones de artefactos preservados, no ejecuciones científicas nuevas.
- [Guion base V4](video/guion_v4_escenas.json) y [anexo 12](video/guion_v4_anexo12_poscorte.json) mantienen su corte y SHA congelados. El montaje técnico final `INFORME_VISUAL_ADV050_V4.mp4` y su sidecar VTT están disponibles en el paquete privado de entrega; el QA de decodificación/metadatos y dos fotogramas codificados no equivale a revisión humana completa de movimiento o voz.

Desde la raíz del repositorio, las comprobaciones de paquete disponibles son:

```sh
python3 controls/test_informe_v4.py
python3 controls/test_para_ninos.py
shasum -a 256 evidence/report_v4/COMPARATOR_CALIBRATION_BUNDLE.tar.gz
tar -tzf evidence/report_v4/COMPARATOR_CALIBRATION_BUNDLE.tar.gz
```

Los dos primeros comandos verifican contratos, sincronía y trazabilidad del paquete; no vuelven a ejecutar las campañas V1–V3 ni las pruebas Lean. La reproducción de esos resultados requiere las fuentes, toolchains, datos y comandos fijados en los informes y bundles correspondientes.

La versión de entrega debe preservar manifiestos históricos sin reescribirlos. Los hashes comprueban identidad de bytes frente al manifiesto, no autoría, fecha cierta ni verdad matemática.
