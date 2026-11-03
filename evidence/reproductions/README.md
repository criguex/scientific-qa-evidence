# Reproducciones reportadas

Cada fila corresponde a una persona que ejecutó `python verificar.py` en su propio computador y me reportó el resultado con el [formulario de reproducción](https://github.com/criguex/scientific-qa-evidence/issues/new?template=reproduccion.yml). Guardo cada reporte como copia exacta de lo que esa persona pegó en su issue. Gracias a quienes se tomaron el tiempo de probarlo y compartir el resultado.

**Cómo se acepta un reporte**

1. La versión de los datos y la huella del reporte se comparan con la referencia de esa versión. Si no coinciden, el reporte también se publica: un resultado distinto es justo lo que buscamos encontrar.
2. Se copia `mi_resultado.txt` tal cual y se enlaza el issue original, que conserva las capturas y demás adjuntos.
3. Indico si quien reporta me conoce. La reproducción de alguien conocido cuenta como una corrida en otro computador, pero no como una reproducción independiente en el sentido estricto.

**Cómo subir evidencias.** Llena el formulario y arrastra tus capturas, un video corto de la terminal o tu `mi_resultado.txt` al campo de comentarios, o agrégalos después como comentario en tu propio issue. GitHub acepta imágenes, videos cortos y archivos `.txt` y `.zip`. Si además guardas una copia en tu cuenta, puedes enlazarla. Así también queda evidencia fuera de mi control.

## Referencias

Cada versión de los datos tiene su propia huella. Comparo cada reporte con la referencia de la versión que dice haber usado. Las corridas en mi Mac y en el CI de GitHub no cuentan como reproducciones.

| Versión de los datos | Huella | Vigente | Notas |
|---|---|---|---|
| `c8edd482375d` | `5292-A47D-AFA5` | desde el 3 de noviembre de 2026 | La versión depende solo de la evidencia. Incluye la evidencia Lean del 23 de octubre en el manifiesto. Ver la [bitácora del 3 de noviembre](../bitacora/2026-11-03.md) |
| `727c5b5f98ef` | `1A86-6B19-21C7` | 27 de octubre al 3 de noviembre | Cambió solo porque un arreglo del CI tocó un archivo del manifiesto. No recibí reportes de esta versión |
| `26791fe6546f` | `C5F0-F1A8-2F4D` | 24 al 27 de octubre | La que compartí en Instagram. Misma huella en mi Mac y en el CI de GitHub, en Ubuntu, macOS y Windows con Python 3.9 y 3.12 ([corrida 40104169962](https://github.com/criguex/scientific-qa-evidence/actions/runs/40104169962), commit f461905) |

## Reportes

| # | Fecha (UTC) | Sistema | Python | Descarga | Versión y huella | ¿Coincide con su versión? | Relación conmigo | Reporte |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-24 15:16 | Windows 11 (10.0.26200) | 3.9.13 | ZIP | `26791fe6546f` · `C5F0-F1A8-2F4D` | Sí | Me conoce | [issue #1](https://github.com/criguex/scientific-qa-evidence/issues/1) · [archivo](2026-10-24_gowtherw_windows.txt) |
| 2 | 2026-10-24 16:16 | macOS 27.0.1, Apple Silicon | 3.14.7 | git clone | `26791fe6546f` · `C5F0-F1A8-2F4D` | Sí | Me conoce o es familiar, según el propio reporte | [issue #2](https://github.com/criguex/scientific-qa-evidence/issues/2) · [archivo](2026-10-24_6uerra_macos.txt) |
| 3 | 2026-10-24 16:51 | macOS 26.5.2, Apple Silicon | 3.9.6 | git clone | `26791fe6546f` · `C5F0-F1A8-2F4D` | Sí | No declarada | [issue #3](https://github.com/criguex/scientific-qa-evidence/issues/3) · [archivo](2026-10-24_akegiraldo_macos_py39.txt) |
| 4 | 2026-10-24 17:04 | macOS 26.7.1, Apple Silicon | 3.14.4 | git clone | `26791fe6546f` · `C5F0-F1A8-2F4D` | Sí | No declarada (misma persona que el 3) | [issue #4](https://github.com/criguex/scientific-qa-evidence/issues/4) · [archivo](2026-10-24_akegiraldo_macos_py314.txt) |

Hasta ahora he recibido 4 reportes de 3 personas, todos iguales a la referencia de su versión. Todavía no hay reportes de Linux ni huellas distintas. Gracias a quienes ya lo probaron.

---

**In English.** Each row is someone who ran `python verificar.py` on their own computer and sent me the result through the reproduction form. I keep each report as a verbatim copy of what they pasted. I publish a report whether or not its fingerprint matches the reference for its data version. I also say whether the person knows me: a run by someone I know counts as a run on another computer, but not as a strongly independent reproduction. Thank you to everyone who has tried it.
