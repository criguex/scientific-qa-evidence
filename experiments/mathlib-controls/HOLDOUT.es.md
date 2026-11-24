> Traducción al español de [HOLDOUT.md](HOLDOUT.md). Si hay alguna diferencia, vale el original.

# Casos reservados (held-out): cómo contribuir

Los casos en [`DESIGN.md`](DESIGN.md) los escogió todos el autor. Para probar el protocolo sin ajustarse a esas decisiones, alguien que no haya trabajado en esto debería preparar casos adicionales.

1. Escoge un teorema que ya esté en Mathlib (commit fijado `85e3a25`).
2. Escribe hasta tres enunciados en Lean: el original, y los cambios que quieras (equivalentes, más débiles, falsos, o de los que no estés seguro).
3. Para cada uno, escribe la etiqueta que esperas: SAME, CHANGED_EQUIVALENT, CHANGED_WEAKER, CHANGED_FALSE o CHANGED_UNKNOWN.
4. Pon las etiquetas en un archivo, publica solo su SHA-256 (por ejemplo en un issue o un correo), y envía los enunciados sin las etiquetas.

Los casos se corren a ciegas, los resultados se publican, y solo después se pide el archivo de etiquetas y se compara con su hash. Los casos recibidos y sus resultados se listarán aquí, con el nombre de quien contribuyó si así lo desea.

**Recibidos hasta ahora:** ninguno.
