> Traducción al español de [README.md](README.md). Si hay alguna diferencia, vale el original.

# Registro de una corrida nueva de Comparator

Este resumen en español y las dos transcripciones completas por desafío son registros saneados, derivados de la salida original de la terminal. Se quitan los escapes ANSI; se redactan las líneas de comando privadas, los nombres de usuario del equipo, las rutas de espacio de trabajo y herramientas, y las IP privadas. Las transcripciones originales sin procesar no se incluyen en esta distribución. Sus valores SHA-256 se conservan abajo para la procedencia. El saneador determinista es [`sanitize_comparator_logs.py`](sanitize_comparator_logs.py), con sus pruebas en [`test_sanitize_comparator_logs.py`](test_sanitize_comparator_logs.py).

| Desafío | Kernel por defecto de Lean | nanoda | Resultado de Comparator | Transcurrido | RSS máximo |
| --- | --- | --- | --- | ---: | ---: |
| Navier–Stokes | aceptado | aceptado | `Your solution is okay!`; exit 0 | 417.56 s | 8,126,256 KiB |
| Euler | aceptado | aceptado | `Your solution is okay!`; exit 0 | 654.43 s | 7,921,768 KiB |

Esto es una recomprobación independiente registrada de los desafíos configurados después de la compilación clean03 desde fuente nueva, no una afirmación de descubrimiento de teoremas ni una verificación universal. Los logs muestran marcadores `sorry` del lado del desafío durante la repetición; son declaraciones del desafío y no un hallazgo de que la solución de Comparator entregada esté incompleta. La salida de Euler lista aparte los axiomas estándar para dos declaraciones. Cualquier auditoría de axiomas anterior es aparte; estos logs no se presentan como una auditoría nueva ni como una revisión humana de los teoremas.

- [Transcripción completa saneada de Navier–Stokes](NavierStokes.full.sanitized.log)
- [Transcripción completa saneada de Euler](Euler.full.sanitized.log)

## Hashes de las transcripciones originales

| Archivo original | SHA-256 |
| --- | --- |
| NavierStokes.typescript | `bb1c50fcbc18aba9d429e14cfb1c5a49be2a43aaf440e509aab525225f81c1c5` |
| Euler.typescript | `b808f7015c47df453fe4e8eee7753acab9015eedeb092a7b009b395acc64b500` |
| NavierStokes.time.txt | `2f4ccac6d49941754ef5dde87d48b02700d9fffacb791106bca5ab3f4411504e` |
| Euler.time.txt | `b0b36c7c62ca0ef152bee2dce7feb23ff747c7c828b53e4ce1c1a2769b8dfec1` |

Los valores de tiempo transcurrido y RSS vienen de los archivos de tiempos originales. Las decisiones del desafío y el estado final vienen de las transcripciones de la terminal. El SHA-256 del archivo comprimido es `abd1537aeca731f169a4c288a1937919fa1f6024aad7c6c8c1fd969071304421`; el archivo comprimido en sí no se distribuye.
