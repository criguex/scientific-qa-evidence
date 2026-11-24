> Traducción al español de [Authorship and AI disclosure](AUTHORSHIP.md). Si hay alguna diferencia, vale el original.

# Autoría y divulgación de IA

Cristian Guerra (criguex) es el autor humano de este estudio de QA y de la reproducción independiente. Es colombiano, de Medellín, y se describe con más de ocho años de experiencia en QA Automation. En términos concisos de CRediT, sus roles son Conceptualización, Metodología, Software, Validación, Curaduría de datos, y Redacción — borrador original y revisión y edición. Aquí «validación» significa correr y revisar la evidencia de QA dentro de su alcance, no una verificación matemática independiente.

A OpenAI se le da crédito por las demostraciones originales y por el repositorio original. Este paquete no reclama autoría de esas demostraciones, descubrimiento de un teorema, ni validación de un problema matemático abierto.

Las herramientas de IA ayudaron con el análisis, la traducción, la edición y la preparación de código. Se declaran como asistencia, no como coautores académicos ni codescubridores. Un trailer de Git `Co-Authored-By: Codex`, requerido donde se usó, registra la contribución de código asistida por herramientas bajo la convención de atribución del repositorio; no es una afirmación de autoría académica. El autor humano sigue siendo responsable de las afirmaciones, las limitaciones, la selección de evidencia y la decisión de publicar. La autorización de publicación se dio el 2026-10-20.

Los ejemplos numéricos sintéticos son cálculos bajo contratos de software explícitos. El material formal consiste en comprobaciones acotadas de fixtures, compilaciones desde la fuente y corridas de Comparator registradas, mutantes del enunciado, lemas puente en Lean relativos a una transcripción literal del texto de Clay, y controles registrados antes de correrlos sobre teoremas de Mathlib y sobre recibos. Ninguno de los dos se presenta como validación experimental ni como una certificación matemática general.

## Trabajo de Codex, sesión por sesión

Lo que hizo el agente Codex el 2026-10-20 (19 sesiones, con roles, horarios, acciones y hashes de los archivos de sesión) está en [`docs/CODEX_WORK_LOG.md`](CODEX_WORK_LOG.md), y la evidencia que produjo y que se había quedado privada se publica en [`evidence/codex-2026-10-20/`](../evidence/codex-2026-10-20/), con un manifiesto que empareja cada archivo con el hash de su original.

## Identidad del asistente de IA a lo largo de esta sesión (trazabilidad)

Para una trazabilidad completa de quién produjo cada commit, la identidad del asistente de IA declarada por el entorno cambió a mitad del trabajo del 2026-10-21, y los trailers de los commits lo registran:

- Los commits hasta `e1e63b4` inclusive llevan `Co-Authored-By: Claude Opus 5.5`. En ese momento el entorno de la sesión reportaba el modelo como `claude-opus-5-5`, con fecha de corte de conocimiento de junio de 2026.
- Desde el commit `aa47c98` en adelante el trailer es `Co-Authored-By: Claude Opus 4.8`, después de que un aviso del sistema cambiara el modelo reportado a `claude-opus-4-8`, con fecha de corte de conocimiento de enero de 2026.

Esto se registra como un hecho observable. El asistente corre bajo la identidad que declara su entorno y no puede verificar desde adentro cuál etiqueta es exacta, así que aquí no se afirma intención ni engaño. Los trailers `Co-Authored-By` de cada commit en `git log` son el registro autoritativo de qué etiqueta estaba activa para cada cambio. La autoría humana, la responsabilidad y la decisión de publicar siguen siendo de Cristian Guerra sin importar la etiqueta del asistente.

Más tarde ese mismo día el autor corrió el comando `/model` de Claude Code, que fijó el modelo en Opus 5.5, y los trailers de los commits desde `ae55a24` en adelante dicen otra vez `Claude Opus 5.5`. Esto muestra que el modelo se puede elegir en el cliente, que es la explicación más probable del cambio anterior: un cambio de modelo en la sesión, no un engaño.
