> Traducción al español de [Independent reproduction guide](INDEPENDENT_REPRODUCTION.md). Si hay alguna diferencia, vale el original.

# Guía de reproducción independiente

Cada corrida registrada en este repositorio la hizo su autor, con un asistente de IA, en las mismas dos máquinas. Esas corridas cuentan, pero no son independientes. Esta guía es para otra persona que quiera recompilar las demostraciones de OpenAI desde una versión fija, comprobarlas y publicar lo que obtuvo. Una corrida que no coincide con la nuestra es tan útil como una que sí coincide.

## Qué está fijo

| Entrada | Versión fijada | Cómo comprobarlo |
| --- | --- | --- |
| Fuente de OpenAI | [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler), commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` | Manifiesto de contenido más abajo. Los bytes del archivo no son estables: el archivo que fijamos en octubre de 2026 tiene SHA-256 `afd4d226…834b4b5`, una descarga nueva de GitHub tiene uno distinto, y las dos extraen los mismos 2.669 archivos |
| Manifiesto de contenido | `95bb21c93e834581e1400e31e33a9fb7943db2f64f11425b034f97b9b52e95fc` | Comando en el paso 1; el mismo valor en macOS y en Linux |
| Toolchain de Lean | `leanprover/lean4:v4.34.0-rc2` (commit `6a10ac8`), tomado del `lean-toolchain` del proyecto | `lean --version` dentro del proyecto |
| Comparator y sus verificadores | [leanprover/comparator](https://github.com/leanprover/comparator) `19e111e2141cf333c7daff0f64c5f24acc91dd2e`; lean4export `cacf989bd75f608700820f6afc595f32e7a99a4d`; nanoda_lib `9d6964f78d0fa4c93fd22fe956e17afe7e72a441`; landrun `ec104f6edc1e14d7fec6d31146f1ec6f9c192c5a` | Compílalos siguiendo el README de Comparator en esas revisiones y registra el SHA-256 de cada binario que uses. Los nuestros están en [el registro de B4](../evidence/formal/cd-validation/README.md#reused-tools) |
| Puentes de Clay | [`bridges/ClayLiteral.lean`](../bridges/ClayLiteral.lean) y [`bridges/Bridges.lean`](../bridges/Bridges.lean) de este repositorio | SHA-256 listados en [`bridges/README.md`](../bridges/README.md) |

## Pasos

Basta con Linux x86_64, unos 30 GB de disco libre y 16 GB de memoria; nuestra compilación tardó 1 h 15 min en 12 núcleos. Corre cada paso en Bash, desde el directorio del proyecto, después de definir este ayudante. Envía la salida de cada comando a un log y registra el código de salida del propio comando (no el de `tee`) junto con su hora de inicio y fin en `../exit_codes.tsv`:

```
set -o pipefail
step() {
  local name=$1 start rc; shift
  start=$(date -u +%FT%TZ)
  "$@" 2>&1 | tee "../$name.log"; rc=${PIPESTATUS[0]}
  printf '%s\t%s\t%s\t%s\n' "$name" "$start" "$(date -u +%FT%TZ)" "$rc" >> ../exit_codes.tsv
  return "$rc"
}
```

1. **Obtén la fuente y compruébala.**
   ```
   git clone https://github.com/openai/NavierStokesAndEuler.git && cd NavierStokesAndEuler
   git checkout f9e8bc5b38b6e212696e8a30e3e91517af887bbd
   (LC_ALL=C find . -path ./.git -prune -o -type f -print | LC_ALL=C sort | while IFS= read -r f; do sha256sum "$f"; done) | sha256sum
   ```
   Resultado esperado: `95bb21c9…52e95fc`. (En macOS usa `shasum -a 256` en vez de `sha256sum`, en los dos casos.)
2. **Compila desde la fuente, sin archivos precompilados.**
   ```
   mkdir -p ../xdg
   step build env XDG_CACHE_HOME=$PWD/../xdg MATHLIB_NO_CACHE_ON_UPDATE=1 lake --no-cache build
   ```
   Resultado esperado: exit 0. La nuestra: 11.424 jobs.
3. **Corre Comparator sobre los dos desafíos.**
   ```
   step comparator_NavierStokes lake env <path-to-comparator> ComparatorChallenges/NavierStokes.json
   step comparator_Euler lake env <path-to-comparator> ComparatorChallenges/Euler.json
   ```
   Resultado esperado: exit 0 y `Your solution is okay!` en cada uno.
4. **Compila los puentes de Clay contra tu compilación e imprime sus axiomas.** Copia `ClayLiteral.lean` y `Bridges.lean` de este repositorio a la raíz del proyecto, comprueba su SHA-256 y crea ahí `Axioms.lean`:
   ```
   import Bridges
   #print axioms Bridges.k1_C
   #print axioms Bridges.k1_D
   #print axioms Bridges.k1_C_oneSided
   #print axioms Bridges.k1_D_oneSided
   #print axioms Bridges.zero_solution_C
   #print axioms Bridges.zero_solution_D
   ```
   Luego:
   ```
   step clay lake env lean -o .lake/build/lib/lean/ClayLiteral.olean ClayLiteral.lean
   step bridges lake env lean -o .lake/build/lib/lean/Bridges.olean Bridges.lean
   step axioms lake env lean Axioms.lean
   ```
   Resultado esperado: exit 0 en los tres, y `depends on axioms: [propext, Classical.choice, Quot.sound]` para cada uno de los seis teoremas. Los tres comandos `lake env lean` se probaron el 2026-10-22 contra la compilación B4.
5. **Registra las versiones,** dentro del directorio del proyecto: `lean --version`, `lake --version`, `uname -a`, y el SHA-256 de `lean`, `lake` y cada binario verificador.

## Qué publicar

Una página pública (un gist, un repositorio, un issue en [este repositorio](https://github.com/criguex/scientific-qa-evidence/issues)) con lo siguiente, ya completado:

```
Reproducer:            name or handle, and whether you used AI tools
Date (UTC):
Machine:               OS, CPU, cores, memory
Source commit:         f9e8bc5b38b6e212696e8a30e3e91517af887bbd
Content manifest:      <value from step 1>
lean --version:
lake --version:
Checker binaries:      <name, revision, SHA-256 for comparator, lean4export, nanoda, landrun>
| Step | Command | Start | End | Exit code | Result |
| build | ... | | | | <jobs; any downloaded caches?> |
| comparator NavierStokes | ... | | | | <last line> |
| comparator Euler | ... | | | | <last line> |
| bridges | ... | | | | <axioms printed> |
exit_codes.tsv:         <contents>
Full logs or their SHA-256:
Differences from the expected results, if any:
Deviations from this guide, if any:
```

También vale la pena publicar resultados que difieran de los nuestros, pasos que fallaron o pasos que no pudiste correr. Si abres un issue aquí, quedará enlazado desde esta página tal como se recibió, sin editar lo que escribiste.

## Reproducciones recibidas

Todavía no hay una recompilación independiente de las demostraciones en Lean: todas las corridas en Lean hasta ahora las hizo el autor o herramientas bajo su dirección, la más reciente el 2026-10-23 ([registro](../evidence/lean-cloud-2026-10-23/README.md)). Los reportes de la comprobación más liviana de un solo comando, `verificar.py`, que no recompila Lean, están en [evidence/reproductions/](../evidence/reproductions/README.md).
