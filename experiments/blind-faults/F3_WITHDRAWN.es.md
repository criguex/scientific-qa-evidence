> Traducción al español de [F3_WITHDRAWN.md](F3_WITHDRAWN.md). Si hay alguna diferencia, vale el original.

# Clase F3 retirada antes de congelar

> **Autoría de este registro.** Escrito por el asistente de IA (Claude Code, Opus) a partir de sus propias observaciones dentro de esta sesión, para Cristian Guerra, el autor del repositorio. Los puntos de «Qué se observó» son de primera mano para el asistente: son lo que el asistente vio que le pasó a sus propias respuestas. La «Hipótesis» es una inferencia del asistente, no una declaración del sistema de seguridad. El asistente no puede leer el funcionamiento interno del clasificador.

El 2026-10-21, mientras se preparaba la clase F3, partes de las respuestas del asistente de IA fueron detenidas dos veces por un filtro de seguridad automatizado del servicio del asistente. El filtro no declaró su razón. El trabajo en F3 se detuvo en ese punto; las compilaciones de herramientas para esa clase se interrumpieron en el equipo de pruebas.

Para mantener el experimento dentro del alcance permitido al asistente, la clase F3 se elimina **antes** de congelar el diseño. El experimento continúa con las clases F1, F2, F4, F5, el control positivo F6 y los casos limpios: 21 casos en total.

El compromiso de la semilla no se ve afectado. La semilla solo decide la asignación de los casos, y todavía no se ha hecho ninguna asignación.

El registro de factibilidad anterior sigue publicado como un registro histórico del trabajo hecho antes del retiro. No es parte del experimento.

## Qué se observó

Estos son hechos registrados por el asistente, con la limitación de que el asistente no puede ver el funcionamiento interno del filtro.

- Dos turnos del asistente fueron cortados por un clasificador descrito como un filtro de seguridad del propio servicio del asistente, no un error de herramienta ni de la API. Un aviso del sistema dijo que el contenido retenido no debía reproducirse.
- Las interrupciones ocurrieron durante, y solo durante, el trabajo en la clase F3. F3 es la única clase que implica correr un exploit público de un bug de solidez del kernel de Lean (CVE-2026-72844) sobre una versión de Lean deliberadamente desactualizada.
- La primera interrupción ocurrió mientras se redactaba un mensaje, después de que el exploit ya se había reproducido y ese resultado se había publicado (commit `e1e63b4`). La segunda ocurrió durante una edición que estaba quitando F3 del diseño.
- Ninguna llamada a una herramienta quedó a medio aplicar: el árbol de trabajo se mantuvo limpio en `e1e63b4` después de las dos interrupciones.

## Hipótesis (sin confirmar)

El asistente no puede leer la razón del clasificador, así que lo siguiente es una inferencia, no un hecho.

- Lo más probable: el clasificador reaccionó a que el asistente generara u orquestara código de exploit para un CVE conocido, aunque el exploit es público, inerte fuera de Lean, y se usa aquí solo para demostrar que un verificador actualizado lo rechaza. Generar exploits de seguridad es un disparador común para este tipo de filtros, sin importar la intención.
- Una posibilidad más débil: la redacción del texto retenido se pareciera a un patrón que el clasificador marca. Poco probable que sea toda la causa, ya que las dos interrupciones se agruparon en el mismo tema.
- Lo que probablemente **no** es: el trabajo numérico, de procedencia, de integridad de la compilación, de vigencia del kernel y de mutantes del enunciado (F1, F2, F4, F5, F6) nunca activó el filtro a lo largo de muchos turnos.

## Decisión

El protocolo no necesita F3. La vigencia de la versión del verificador ya está cubierta por la [comprobación de vigencia del kernel](../../evidence/formal/kernel-currency.md), que compara la fuente del kernel y el commit de nanoda contra las correcciones conocidas de 2026, sin correr ningún exploit. El experimento a ciegas continúa sin F3, y este retiro se deja en el registro para que el vacío y su razón sean trazables.
