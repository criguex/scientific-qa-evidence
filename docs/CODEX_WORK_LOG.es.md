> Traducción al español de [Work done with OpenAI Codex, step by step](CODEX_WORK_LOG.md). Si hay alguna diferencia, vale el original.

# Trabajo hecho con OpenAI Codex, paso a paso

Este registro documenta lo que hizo el agente de código Codex para este estudio, para que un revisor pueda separar lo que se ejecutó de lo que solo se discutió o se ilustró. Lo compiló Claude Code el 2026-10-22 a partir de los archivos de sesión de Codex guardados en el Mac mini del autor, después de los hechos. Las horas están en UTC.

## Cómo se construyó este registro

1. Se leyeron los 213 archivos de sesión locales de Codex y el historial de prompts de Codex (470 entradas).
2. Se conservaron las sesiones que pertenecen a este estudio. Diecinueve califican, todas del 2026-10-20: una sesión principal y dieciocho subagentes que esta inició. Cada archivo de sesión de subagente nombra a su padre y su rol (por ejemplo `/root/localizar_5070`), así que el árbol de abajo se lee de los archivos, no se infiere.
3. Para cada una, se extrajeron las llamadas a herramientas (comandos de shell, parches de archivos, `git commit`, `git push`, `ssh` a las dos máquinas Windows), y se contaron.
4. Las transcripciones completas **no** se publican. Contienen datos personales del autor y comandos que manejan credenciales. En su lugar, el SHA-256 de cada archivo de sesión se lista más abajo, calculado el 2026-10-22, para que los archivos de los que se construyó este registro puedan identificarse más adelante.

## Paso a paso

Los roles son los nombres que la sesión principal les dio a sus subagentes. «Sin parches de archivos» significa que la sesión solo corrió comandos o leyó archivos.

| # | Sesión (UTC) | Rol | Llamadas a herramientas | Qué hizo | Dónde vive el resultado |
| --- | --- | --- | --- | --- | --- |
| 1 | `…112a8e2f` 16:09 → 00:08 del día siguiente | main | 2.067 | Tomó el pedido del autor de compilar y comprobar las pruebas de OpenAI en la máquina RTX 5070 (WAR) y de ampliar los escenarios de mutantes más allá del agua. Instaló Ubuntu 24.04 bajo WSL en WAR, clonó el repositorio de OpenAI en el commit fijado, corrió la comprobación previa de hashes, la compilación y los primeros controles, inició los subagentes y fusionó su trabajo. 11 llamadas a `git push`, entre ellas el primer push de este repositorio | Este repositorio (primeros 16 commits, abajo) y los repositorios privados `adv-050-*` del autor |
| 2 | `…84df4b88` 16:09 → 18:35 | `localizar_5070` | 188 | Localizó y preparó la máquina 5070; escenarios ODE (versión 3), comprobaciones de paso de tiempo en GUERRA, operaciones NS08 en WAR, una vista previa de voz | `adv-050-auditoria` privado |
| 3 | `…2659af2c` 16:18 → 18:29 | `material_evidencia` | 354 | Ensambló el paquete de evidencia (154 parches de archivo). Su simulación de fluidos registra el tiempo de ejecución con `time.perf_counter`, que mide cuánto corre el programa, no ninguna reparación | `adv-050-auditoria` privado |
| 4 | `…f7e53ba8` 17:33 → 18:21 | `validacion_matematica` | 108 | Comprobación independiente de los resultados de ODE | `adv-050-auditoria` privado |
| 5 | `…b5d648` 18:26 | `gwar_video_v4` | 2 | Sin parches de archivo | ninguno |
| 6 | `…329d11` 18:26 → 18:29 | `inventario_video_v4` | 17 | Inventario del video versión 4; sin parches de archivo | ninguno |
| 7 | `…bd05cc04` 18:34 → 20:35 | `entrega_v4_luna` | 762 | Versión 4 de la auditoría: video, controles, informe y borrador de artículo | `adv-050-auditoria-v4` privado |
| 8 | `…b7fa5a99` 18:35 → 20:21 | `ns08_luna` | 546 | Calibración NS08 y corridas adicionales en WAR (138 llamadas a `ssh`) | `adv-050-auditoria` privado |
| 9 | `…c4694b6a` 18:36 → 20:32 | `voz4060_luna` | 508 | Voz versión 4 en GUERRA, y los tres experimentos ejecutables del laboratorio de mutantes | [criguex/war-paradigm](https://github.com/criguex/war-paradigm) (antes `mutant-lab`) |
| 10 | `…0276f8` 20:05 → 20:06 | `gwar_mutant_scope` | 1 | Sin parches de archivo | ninguno |
| 11 | `…ab43b8` 20:24 → 22:54 | `gwar_elevenlabs_voice` | 34 | Comprobación del proveedor de voz (según el nombre de su rol); sin parches de archivo | ninguno |
| 12 | `…dd2b45` 20:35 → 21:45 | `validar_correcciones_adv050` | 201 | Comprobó las correcciones (según el nombre de su rol); sin parches de archivo | ninguno |
| 13 | `…88bc5b87` 20:44 → 21:48 | `validation_writer_luna` | 567 | Escribió la suite numérica de nueve modelos (`CONTRACT.md`, `oracles.py`, `runner.py`, `suite.py`, `sut.py`), incluida la refracción de Snell con la mutación `index_swap` y un oráculo que invierte `asin` por bisección; controles y documentación de validación | `adv-050-auditoria-validacion` privado; la suite y sus corridas pareadas están en este repositorio bajo [`evidence/numerical/`](../evidence/numerical/) |
| 14 | `…3eda86` 21:46 → 22:03 | `jd_tts_a` | 8 | Primer juez ciego de la revisión de seguridad de texto a voz (según el nombre de su rol) | ninguno |
| 15 | `…93486e` 21:46 → 22:03 | `jd_tts_b` | 6 | Segundo juez ciego de la misma revisión (según el nombre de su rol) | ninguno |
| 16 | `…00f08820` 21:48 → 21:50 | `tts_safety_fix` | 20 | Aplicó las notas de seguridad de texto a voz de los jueces | `adv-050-auditoria-tts-safety` privado |
| 17 | `…f920ff` 21:58 → 23:11 | `english_delivery_inventory` | 82 | Inventario de la entrega en inglés; sin parches de archivo | ninguno |
| 18 | `…d756876c` 22:00 → 23:35 | `english_release_writer` | 656 | Paquete de entrega en inglés y los explicativos animados, con la escena de Snell incluida | Medios renderizados, reconstruidos después en [`animations/`](../animations/) de este repositorio |
| 19 | `…b5febf` 22:59 → 23:40 | `animation_export_batch` | 138 | Renderizó los archivos MP4 de las animaciones; sin parches de archivo | Medios reconstruidos después en este repositorio |

La campaña numérica pareada corrió en el Mac mini (macOS arm64) y en WAR (Linux x86_64); las dos máquinas clasificaron las 84 variantes de forma idéntica ([`CLAIMS.md`](../CLAIMS.md)).

## Evidencia publicada de estas sesiones

El código, los contratos, los resultados brutos y los logs que estas sesiones produjeron en el repositorio privado están ahora en [`evidence/codex-2026-10-20/`](../evidence/codex-2026-10-20/), una carpeta por experimento, con las rutas locales reemplazadas por marcadores de posición y un manifiesto que empareja cada archivo con el hash de su original. El audio, la voz y el video siguen siendo privados.

## Commits de este repositorio con asistencia de Codex

Todos del 2026-10-20 (UTC−5), cada uno con un trailer `Co-Authored-By: Codex`:

`20d67e5` prepare English QA evidence and video review package · `3281ad5` clarify AI attribution and English publication identity · `b39e7d6` record rendered English delivery and review checks · `a2e063f` add animated evidence review package · `f97e8b9` improve explainer canvas attribution · `554a678` add narration-synced V2 video compositions · `0264eb8` add visual evidence landing page · `43520e2` clarify available animation preview · `df64ec1` explain each evidence animation · `4ec9814` prepare Spanish narration pipeline · `46ba636` add animated previews to evidence guides · `098f4ca` correct V2 visual claims and layout · `275e6b0` add Spanish V2 narration compositions · `a8aa21d` record X animation preview receipts · `6ac3c07` update Spanish delivery readiness · `f49fcd5` preserve proportional visual scales.

El trabajo posterior (desde el 2026-10-21) se hizo con Claude Code; sus commits llevan trailers `Co-Authored-By: Claude …` ([`AUTHORSHIP.md`](AUTHORSHIP.md)).

## Lo que no se ejecutó: los escenarios de «auto-fix»

Un conjunto de ilustraciones tituladas «WarParadigm, escenarios 2-5» muestra un rayo de luz en un cubo, una curvatura extra de 1°, un índice de −1, renderizado por nivel de detalle, y una gráfica donde un «auto-fix» corrige la luz en 5 ms frente a una anomalía de 195 ms. **Nada de eso se corrió jamás.**

- Ninguna sesión, ni en Codex ni en Claude Code, contiene código para una simulación autocorrectora, un monitor o regenerador, una deflexión de 1°, un índice de −1, lógica de nivel de detalle, ni una medición de tiempo de detección o reparación en milisegundos. La búsqueda cubrió las 213 sesiones de Codex, el historial de prompts de Codex, el historial de shell y las carpetas de proyecto del autor, y el repositorio `war-paradigm`.
- Las ilustraciones son imágenes conceptuales generadas con herramientas de IA. Los valores de 5 ms y +195 ms en la gráfica son parte del dibujo, no mediciones.
- Los «escenarios» numerados que Codex leyó el 2026-10-20 venían de una conversación con Gemini que el autor compartió, y eran temas distintos (zona de Brillouin, factor de corte, refinamiento de malla, perturbaciones de acoplamiento).
- Lo que sí se ejecutó con luz es el modelo de Snell de arriba: tres configuraciones fijas y dos fallos sembrados (índices intercambiados, grados leídos como radianes), detectados frente a un oráculo independiente. El código, el contrato y los resultados brutos están en [`evidence/numerical/`](../evidence/numerical/).

Para un revisor externo, todo lo relacionado con un experimento de auto-fix está por tanto **sin registrar**, porque nunca se llevó a cabo. Si se construye más adelante, será un experimento nuevo, registrado antes de correrlo: qué se espera, qué contaría en su contra, y cómo se miden por separado el tiempo de detección, el tiempo de reparación y el tiempo simulado.

## Archivos de sesión (SHA-256 calculado el 2026-10-22, después de los hechos)

```text
947073b778aadcb612eebcb33f94e45c1e6eb36a92fc228d7e20dc64a36b0f70  rollout-2026-10-20T11-08-20-01a15a12-2369-7193-a4e0-112a8e2f2ed3.jsonl
2955525c3a340d26bc71d07848f8b0cb348be5332c0746f9cc0312b4226dc57e  rollout-2026-10-20T11-09-36-01a15a13-4dba-76c1-8fe0-84df4b88d138.jsonl
c234e1e13a53b89f428d740561cfa3bb7f7a48c0d74d14b7281d8ea9cf7ad289  rollout-2026-10-20T11-18-44-01a15a1b-a98c-7b31-bab8-2659af2cdb22.jsonl
0c7c7c5022dcb246009e2164bf46c73e7f3e2cbc6adca622211a2a2daa169e73  rollout-2026-10-20T12-33-52-01a15a60-7111-7011-90f7-f7e53ba87994.jsonl
e123c26adfb4f80034e734b97305db670e3102c98544418f4c029a79d50f48ab  rollout-2026-10-20T13-26-11-01a15a90-58ac-74b2-80de-9ddb76b5d648.jsonl
9f70822f227a537273ffdc836f4d85e6d9c317158aa49924ee19f39a71b6aee2  rollout-2026-10-20T13-26-20-01a15a90-7abc-7a43-945f-850f31329d11.jsonl
05cd206fc2e287840320bfc7585db1c7d5ef367bb7f5ad582fb1e4184ffee45c  rollout-2026-10-20T13-34-46-01a15a98-318c-73a2-8e91-bd05cc04a5a8.jsonl
035b44a27a6963f4ea022b621a760f0f77816c69424a9525cff8f13bf85d69f4  rollout-2026-10-20T13-35-57-01a15a99-48a8-7fb1-b1bc-b7fa5a99ae05.jsonl
ac777c2d7f502d7fe3f2090f43fa70d3fcf10c318aae04c373fee36d40a052b9  rollout-2026-10-20T13-36-28-01a15a99-c0af-7b52-aca2-c4694b6a7785.jsonl
4769bb0b8f0382159fc9f24549f27ccf901bfee1b8d38a32c7a338f6ab620d8b  rollout-2026-10-20T15-05-58-01a15aeb-b204-7ab3-ac90-2ddb9a0276f8.jsonl
b153e81be9a8246316f99ae8f086196fa06bf7cc0d3cbe4feff8625b496bdff5  rollout-2026-10-20T15-24-51-01a15afc-fd19-79a0-955f-e7cbdeab43b8.jsonl
52e15aba0299744195729c246d163941a29263e6a7ddc7f97f50fac6e5799239  rollout-2026-10-20T15-35-52-01a15b07-112c-7940-b3c4-3c299ddd2b45.jsonl
bb294cb1d92973d978165571fdc3002ce701d6c1865ba6c2e197d37774e4d6d9  rollout-2026-10-20T15-44-42-01a15b0f-27b4-7fb0-857d-88bc5b87f848.jsonl
f3323ff5a2ab219c7a774a38875c7bcf69c39ee1363da789b365e45661475c3e  rollout-2026-10-20T16-46-22-01a15b47-9e89-7062-8cc8-a8fd933eda86.jsonl
dd2ed72cc7d471ecea4731d7aeb28862166da7cdde841587e55c4ddc2c9366db  rollout-2026-10-20T16-46-28-01a15b47-b4d3-73e0-9cfc-d560df93486e.jsonl
67e7125a6794d86b6060e8678b79ebf3cb4b581e6e30c4536fafbc55c39b6288  rollout-2026-10-20T16-48-42-01a15b49-c147-7df0-914d-00f08820c196.jsonl
4e93d8ec0c2b0a79688ddf334db2c6eac902934783c92153be9e17b48299f124  rollout-2026-10-20T16-58-41-01a15b52-e310-79c1-9e09-f2cd7ef920ff.jsonl
726ea0a998fdfcd8c79d35b78e7382f83ddf0b35bd29f603fe0ecbf19828e908  rollout-2026-10-20T17-00-52-01a15b54-e33c-78b1-8b1d-d756876cc4cb.jsonl
4ff9d3bc77a9b245033e67d272418a407436391f254faa3de8dffe911f0d685f  rollout-2026-10-20T17-59-02-01a15b8a-268d-7271-a56a-d79619b5febf.jsonl
```

Los nombres de archivo llevan la hora local (UTC−5) en la que empezó cada sesión.

## Límites

- Construido después de los hechos por otra herramienta de IA, a partir de archivos de sesión que solo tiene el autor. Un revisor puede comprobar los commits y la evidencia de este repositorio, pero no las transcripciones mismas.
- Los conteos de llamadas a herramientas miden actividad, no calidad ni corrección.
- Los repositorios privados no se publican; este registro solo dice qué contienen.
