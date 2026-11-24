> Traducción al español de [README.md](README.md). Si hay alguna diferencia, vale el original.

# Compilación B5: una segunda compilación desde la fuente, para la versión v1.3.0

El 2026-10-21/22 se volvió a compilar el repositorio de OpenAI desde el tarball fijado, sin nada precompilado, para verificar que el resultado no depende de ninguna compilación anterior. Mismo equipo, toolchain y binarios de verificadores que B4 ([registro de B4](../cd-validation/README.md#builds-used-by-each-run), [hashes de las herramientas](../cd-validation/receipts/tools.tsv)).

| Paso | Comando | Inicio (UTC) | Fin (UTC) | Exit | Resultado |
| --- | --- | --- | --- | --- | --- |
| Tarball | `sha256sum -c` contra `afd4d226…` | | | 0 | OK ([`tarball_sha.txt`](tarball_sha.txt)) |
| Compilación | `XDG_CACHE_HOME=<dir vacío> MATHLIB_NO_CACHE_ON_UPDATE=1 lake --no-cache build` | 2026-10-21T23:56:44Z | 2026-10-22T01:12:24Z | 0 | 11,424 tareas, 1 h 15 min 39 s |
| Comparator · Navier–Stokes (C, D) | `lake env <comparator> ComparatorChallenges/NavierStokes.json` | 01:12:24Z | 01:19:02Z | 0 | **ACEPTADO** por nanoda y el kernel de Lean, 6 min 38 s |
| Comparator · Euler | `lake env <comparator> ComparatorChallenges/Euler.json` | 01:19:02Z | 01:30:08Z | 0 | **ACEPTADO** por nanoda y el kernel de Lean, 11 min 6 s |
| Puentes de Clay | `lean --root=. ClayLiteral.lean`, luego `Bridges.lean`, contra B5 | 01:30:09Z | 01:30:17Z | 0 | `k1_C`, `k1_D`, `k1_C_oneSided`, `k1_D_oneSided` y ambos controles de no vacuidad: `[propext, Classical.choice, Quot.sound]` |

**No se precompiló nada** ([`build_facts.txt`](build_facts.txt)): 0 barriles de Reservoir, 0 archivos en el directorio de caché de compilación, y cada uno de los 11,406 archivos `.olean` (Mathlib 8,371, proyecto 2,659, dependencias 376) es más reciente que el inicio de la compilación. Las entradas de los puentes tienen el mismo SHA-256 que en [`bridges/README.md`](../../../bridges/README.md) ([`inputs.sha256`](inputs.sha256)).

Registros: [`receipts.tsv`](receipts.tsv), [`versions.txt`](versions.txt) (**vacío**: el wrapper corrió los comandos de versión fuera del proyecto, donde no hay ningún toolchain configurado; las versiones, registradas después desde los mismos binarios, cuyos hashes coinciden con el registro de B4, están en [`versions-recorded-after.txt`](versions-recorded-after.txt)), [`build.time.txt`](build.time.txt), el SHA-256 del log completo de la compilación ([`build.log.sha256`](build.log.sha256); el log en sí no se publica), stdout, stderr y los tiempos de Comparator por desafío, y los logs de compilación y de axiomas de Lean. Las rutas del equipo se reemplazan por `<path>`.

**Límites.** Mismo único equipo Linux y mismos toolchain de Lean y binarios de verificadores reutilizados que B1–B4; una recompilación externa sigue siendo la comprobación más fuerte.
