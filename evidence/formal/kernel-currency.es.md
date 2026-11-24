> Traducción al español de [kernel-currency.md](kernel-currency.md). Si hay alguna diferencia, vale el original.

# ¿Estaban los verificadores al día con las correcciones de solidez del kernel de 2026?

En 2026 se encontraron y corrigieron varios errores de solidez del kernel de Lean 4, y en un caso el verificador independiente nanoda tenía un error aparte que dejaba pasar el mismo exploit ([de Moura, postmortem del #14576](https://leodemoura.github.io/blog/2026-8-1-postmortem-for-kernel-soundness-bug-14576/); [postmortem de la búsqueda del error](https://leodemoura.github.io/blog/2026-8-24-postmortem-for-the-kernel-soundness-bug-hunt/); [notas de la versión de Lean 4.34.0](https://lean-lang.org/doc/reference/latest/releases/v4.34.0/)). Una corrida en verde de Comparator vale solo lo que valgan los kernels detrás de ella, así que esto verifica las versiones usadas aquí contra esas correcciones. Verificado el 2026-10-21.

## Kernel de Lean

El toolchain en cada corrida reporta `Lean (version 4.34.0-rc2, … commit 6a10ac8c22beadecabdbb0919c2b50214762f91d)`. El árbol de Git de `src/kernel` en cada etiqueta de versión de `leanprover/lean4`:

| Etiqueta | Commit | Árbol de `src/kernel` | Relación con las correcciones |
| --- | --- | --- | --- |
| v4.33.0 | `d8b1897` | `2de8c537…` | Antes del parche de solidez de v4.33.1 |
| v4.33.1 | `819816b` | `636837af…` | Parche de solidez (#14806, #14807, #14808) |
| v4.34.0-rc1 | `3447a66` | `2066bfde…` | Kernel distinto; listado como afectado por los avisos |
| **v4.34.0-rc2 (usado aquí)** | **`6a10ac8`** | **`636837af…`** | **Misma fuente de kernel que v4.33.1, v4.34.0 y v4.34.1** |
| v4.34.0 | `293d5d0` | `636837af…` | Versión que anuncia tres problemas de solidez corregidos |
| v4.34.1 | `5045d00` | `636837af…` | Solo correcciones en tiempo de ejecución; el kernel no cambia |

**Resultado.** La fuente del kernel usada en cada corrida es idéntica byte a byte, como árbol de Git, a la del kernel de v4.34.0 y v4.34.1, así que contiene toda corrección de solidez del kernel publicada hasta v4.34.1. La corrección del #14576 es anterior a ambas (v4.32.2).

**No cubierto.** v4.34.1 también corrige problemas de tiempo de ejecución fuera de `src/kernel`; el toolchain usado aquí no los tiene. Esta verificación compara árboles de fuente; no recompila los binarios desde la fuente.

Reproducir:

```sh
for t in v4.33.1 v4.34.0-rc1 v4.34.0-rc2 v4.34.0 v4.34.1; do
  gh api "repos/leanprover/lean4/contents/src?ref=$t" -q '.[] | select(.name=="kernel") | "'$t' " + .sha'
done
```

## nanoda

El nanoda que usa Comparator es `ammkrn/nanoda_lib` en `9d6964f78d0fa4c93fd22fe956e17afe7e72a441` (2026-10-19, "Merge pull request #58 from ammkrn/nat_fvar"). Según el postmortem del #14576, el error de verificación de proyecciones de nanoda se corrigió cerca de una semana antes de que se reportara ese error de Lean a finales de julio de 2026, así que este commit es posterior a la corrección.

**No cubierto.** La corrección se ubicó a partir de la fecha del postmortem, no identificando el commit que la corrige en el historial de nanoda.

## Control positivo

El exploit público del #14576 ([`endrazine/lean-cve-poc`](https://github.com/endrazine/lean-cve-poc) en `db52dfd`) demuestra `0 = 1` sin axiomas en Lean v4.31.0, y es rechazado por el kernel del toolchain v4.34.0-rc2 usado aquí (exit 1, la declaración forjada no se admite). Detalles: [reproducción F3](../../experiments/blind-faults/feasibility/f3-exploit-reproduction.md).

## Qué no cambia esto

Que dos kernels coincidan descarta que un error de solo uno de ellos deje pasar una prueba falsa. No descarta un error compartido, ni dos errores coincidentes, que es lo que pasó en julio de 2026. Estar al día con las correcciones conocidas no dice nada sobre las desconocidas.
