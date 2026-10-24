# Recompilación de las demostraciones de OpenAI en un contenedor en la nube (23-oct-2026)

Con ayuda de un asistente de IA y bajo mi dirección, recompilé las demostraciones en Lean de OpenAI en un contenedor Linux en la nube, separado de mi computador. En esta carpeta guardo la evidencia completa de esa corrida, la misma que envié a soporte de OpenAI (caso 17914950).

## Resultado

| Paso | Resultado |
|---|---|
| `lake build +NavierStokes.ComparatorSolution:olean` | código 0 a las 21:53:04 UTC; 609 de 609 módulos `NavierStokes` de la cadena de imports ([final del log](build-tail.log)) |
| Axiomas de `navier_stokes_breakdown_R3` y `navier_stokes_breakdown_periodic` | `propext`, `Classical.choice`, `Quot.sound`; sin `sorryAx` |
| `ClayLiteral`, `Bridges` y `Audit` en tres versiones fijas de este repositorio (c5f4f55, 059a53c, ac195f7) | 9 de 9 pasos con código 0, el último a las 21:58:36 UTC ([resumen](final-verification-summary.json)) |

Versiones: Lean v4.34.0-rc2, un solo proceso (`LEAN_NUM_THREADS=1`), OpenAI `NavierStokesAndEuler` en f9e8bc5b38b6e212696e8a30e3e91517af887bbd.

## Límites

- **No es una compilación desde cero:** se usó la caché oficial de dependencias de Mathlib. Las compilaciones completas sin caché son B4 y B5, en [evidence/formal](../formal/).
- **No es independiente:** la operé con ayuda de un asistente de IA y bajo mi dirección. Sigue pendiente que otra persona la recompile ([guía](../../docs/INDEPENDENT_REPRODUCTION.md)).
- **La auditoría imprime declaraciones y axiomas;** no es una comprobación con un segundo kernel.
- **La versión c5f4f55 conserva hipótesis explícitas de puente.** 059a53c y ac195f7 no las tienen y requieren viscosidad positiva. La rama D concluye `AltD_withErratum`.
- **Hubo una interrupción:** la corrida que empezó a las 20:55 UTC perdió el seguimiento después de 281 módulos. Se registró como interrumpida, con salida desconocida, y se reanudó a las 21:19:24 UTC sin sobrescribir logs. El detalle está en `LEEME_RESULTADO.txt`.

## Cómo comprobar el paquete

```sh
shasum -a 256 evidencia_Lean_completa_20261023.zip
# 639cdab5f067d3e421132c9495962755408d30baf78d1455f4deeb41be27b080
```

El zip contiene 242 archivos: comandos, fuentes fijadas, logs, recibos con hashes de entrada y salida, y las cadenas de eventos de cada corrida. Empieza por [`LEEME_RESULTADO.txt`](LEEME_RESULTADO.txt). Un hash coincidente prueba que el archivo es el mismo que se envió, no quién lo hizo.

---

**In English.** With help from an AI assistant and under my direction, I rebuilt OpenAI's Lean proofs in a cloud Linux container on 2026-10-23. `ComparatorSolution` built with exit code 0 (609/609 modules). The two headline theorems use only `propext`, `Classical.choice` and `Quot.sound`. The Clay transcription, bridges and axiom audit passed in three pinned versions of this repository (9/9). I used the official Mathlib cache, so this is not an independent reproduction.
