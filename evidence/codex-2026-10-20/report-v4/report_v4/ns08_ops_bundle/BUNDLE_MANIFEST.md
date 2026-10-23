# Bundle operativo NS-08 (sanitizado)

Generado el 2026-10-20. El bundle incluye scripts de operación, handoff,
manifiestos/pins, comprobaciones previas, controles de sandbox, ambos terminales
NS/Euler, intento NS interrumpido y registros de instalación/build portables.
`remote-results-sanitized.tar.gz` conserva las copias íntegras de WAR para
contrastar los logs locales.

Resultados: Comparator aceptó NS y Euler mediante nanoda y el kernel Lean; ambos
registraron `Your solution is okay!`, exit 0. NS warnings `sorry` en los
placeholders del desafío `NavierStokes.lean:273,280`; Euler en
`Euler.lean:85,170`. Las soluciones listaron solo los tres axiomas permitidos:
`propext`, `Quot.sound`, `Classical.choice`. No confundir las advertencias de
los placeholders del desafío con los axiomas declarados por la solución.

Limitaciones importantes: ejecución sobre checkout ya compilado, por lo que no
acredita clean/adversarial start ni independencia de revisión humana. El kernel
WSL tiene Landlock ABI 7; upstream Landrun usa `--best-effort`, así que esto no
equivale a ABI 10 ni a una garantía completa del sandbox. El perfil externo
systemd/seccomp fue conservado y observado; no se relajó entre los dos runs.
Memoria máxima fue 13.6 GiB NS / 13.1 GiB Euler, bajo MemoryMax 27 GiB; swap 0.

El bundle **no** contiene: source archive formal (`NavierStokesAndEuler-*.tar.gz`,
preservado aparte con SHA en el handoff), ejecutables/SDK, descargas, `.lake`,
`target/`, `.git`, cachés, credenciales, tokens, llaves ni archivos `.ssh`.
El listado de la snapshot formal sí se incluye; el repositorio se obtuvo de
`https://github.com/openai/NavierStokesAndEuler.git`, commit exacto
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd`; versión del archivo incluye
`LICENSE`, `README.md` y `ComparatorChallenges/README.md`.

El snapshot formal se conserva aparte en
`NavierStokesAndEuler-f9e8bc5b38b6e212696e8a30e3e91517af887bbd.tar.gz`:
6,550,235 bytes, SHA256
`afd4d2263a4cabefd1317e890b49bc04f8538402c322db4317a08161e834b4b5`.
El paquete de resultados operativos remoto incluido en este bundle es
`remote-results-sanitized.tar.gz`, 34,414 bytes, SHA256
`9e2e54a0919235e28a9fab253f7689566d60c992185c39582095697d62253f32`.

Integridad de terminales locales:

- NS stdout `86f19cfa0e008549d11147e7fe3ceefc5bfd317ffa4b0824eeb6e3327ec973bf`
- NS stderr (0 bytes) `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- NS status `bde294368bfed77c2cddf8cec271d398aee9cdbab3b26e1059281bd33adb0120`
- NS GNU time `66129a4f5ca1c4d8914eee2c09488f0d767faf407c7ed9f834ae1d80c116264d`
- Euler stdout `5f410965535ca08ed4cfca05bd9fb259ece2ef95858319a83134f92bc83b96ba`
- Euler stderr (0 bytes) `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Euler status `bde294368bfed77c2cddf8cec271d398aee9cdbab3b26e1059281bd33adb0120`
- Euler GNU time `85c9deb6655199fd1b0055ee5eee03fb513ffce5de5f19a82d81b538d169b7e9`

La primera invocación NS está registrada como `INTERRUPTED_USER_MANAGER_LIFECYCLE`,
sin status ni EOF; no cuenta como aceptación ni rechazo matemático. El segundo
NS se mantuvo con sesión SSH y `systemd-run --wait`, y terminó antes de Euler.
