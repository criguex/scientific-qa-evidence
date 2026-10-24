# Reproducciones reportadas

Cada fila es una persona que corrió `python verificar.py` en su propio computador y reportó el resultado con el [formulario de reproducción](https://github.com/criguex/scientific-qa-evidence/issues/new?template=reproduccion.yml). El archivo de cada reporte es copia exacta de lo que pegó en su issue.

**Cómo se acepta un reporte**

1. La versión de los datos y la huella del reporte se comparan con la referencia de esa versión. Si no coinciden, el reporte también se publica: un resultado distinto es justo lo que buscamos encontrar.
2. Se copia `mi_resultado.txt` tal cual y se enlaza el issue original, que conserva las capturas y demás adjuntos.
3. Se indica si quien reporta conoce al autor. La reproducción de un conocido vale como corrida en otro computador, pero no es independiente en el sentido fuerte.

**Cómo subir evidencias.** Llena el formulario y arrastra tus capturas, un video corto de la terminal o tu `mi_resultado.txt` al campo de comentarios, o agrégalos después como comentario en tu propio issue. GitHub acepta imágenes, videos cortos y archivos `.txt` y `.zip`. Si además guardas una copia en tu cuenta, enlázala: es evidencia que el autor no controla.

## Referencia

Versión de los datos `26791fe6546f`, huella `C5F0-F1A8-2F4D`. La misma huella salió en el Mac del autor y en el CI de GitHub, en Ubuntu, macOS y Windows con Python 3.9 y 3.12 ([corrida 40104169962](https://github.com/criguex/scientific-qa-evidence/actions/runs/40104169962), commit f461905). Esas corridas no cuentan como reproducciones.

## Reportes

| # | Fecha (UTC) | Sistema | Python | Descarga | Huella | ¿Coincide? | Relación con el autor | Reporte |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-24 15:16 | Windows 11 (10.0.26200) | 3.9.13 | ZIP | `C5F0-F1A8-2F4D` | Sí | Conocido del autor | [issue #1](https://github.com/criguex/scientific-qa-evidence/issues/1) · [archivo](2026-10-24_gowtherw_windows.txt) |

---

**In English.** Each row is a person who ran `python verificar.py` on their own computer and reported the result with the reproduction form. Report files are verbatim copies of what they pasted. A report is published whether or not its fingerprint matches the reference, and each row states whether the reporter knows the author: a run by an acquaintance counts as a run on another computer, not as a strongly independent reproduction.
