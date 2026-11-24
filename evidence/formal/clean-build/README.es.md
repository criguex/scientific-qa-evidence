> Traducción al español de [README.md](README.md). Si hay alguna diferencia, vale el original.

# Fidelidad de la compilación desde una fuente limpia

La compilación registrada usó el checkout de fuente limpia autorizado en el commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`. Corrió `lake --no-cache build`, salió con 0, y completó 11,424 tareas. Esto reutilizó las cachés de dependencias y de toolchain; no fue un arranque completo desde cero y no validó teoremas ni kernels.

| Componente | Versión o commit registrado |
| --- | --- |
| Lean | `leanprover/lean4:v4.34.0-rc2` · commit `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| Lake | `5.0.0-src+6a10ac8` |
| Comparator | `19e111e2141cf333c7daff0f64c5f24acc91dd2e` |
| mathlib | `85e3a25e006c35636f0e53b0e9296caca2685bc0` |
| lean4export | `cacf989bd75f608700820f6afc595f32e7a99a4d` |
| plausible | `d9598f07b1bc701f1e3aae163d2681c1fd978793` |
| LeanSearchClient | `ba67e212be1197b84c1f1f6299488a10a3002713` |
| importGraph | `d8823026ac7ef130c253089d95685f9877b95323` |
| proofwidgets | `a8acbfd87375ff4abe14ce09db5b7664d383bc7f` |
| aesop | `18889deb9e83ea7420ef51c160d6f88552e744e3` |
| Qq | `507746ab8f4b643ccdacb2ec4cdb5853fa9f8ab3` |
| batteries | `d54dddc581e08be364c278052863524bff7a99a9` |
| Cli | `ab3a82db9fea14cf0fd7f5a2de650f4b534640af` |

Los pines exactos se conservan en `dependency-pins.txt`; las versiones de las herramientas y los hashes de los ejecutables están en `tool-versions.txt` y `toolchain.sha256`. El siguiente extracto de stdout está saneado a partir del `build.stdout.log` original (SHA-256 `dcbc3208f09dcb9f22a0c359931a713660727c447f6a28c9b2c028942ce25c72`): [build-output-excerpt.txt](build-output-excerpt.txt).

Este registro documenta la fidelidad al checkout y los pines listados; no es una auditoría independiente de la fuente anterior ni de la corrección matemática.
