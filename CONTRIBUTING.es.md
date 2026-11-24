> Traducción al español de [Contributing](CONTRIBUTING.md). Si hay alguna diferencia, vale el original.

# Cómo contribuir

Reglas para cualquiera, persona o agente, que cambie este repositorio.

- **Mantén al día los documentos en inglés y en español.** [README.md](README.md) y [README.es.md](README.es.md), y [docs/DETAILS.md](docs/DETAILS.md) y [docs/DETAILS.es.md](docs/DETAILS.es.md), dicen lo mismo; cambia cada par junto. El README se mantiene corto; los detalles van a `docs/DETAILS*.md`, los términos al [glosario](docs/GLOSSARY.md), y cada documento nuevo recibe una línea en el [mapa de la documentación](docs/README.md). Los registros detallados (CLAIMS, las guías de evidencia, el contrato numérico) se quedan en inglés.
- **Nunca reescribas un archivo de evidencia original.** La evidencia numérica y formal son listas curadas, y los resúmenes en inglés son traducciones derivadas de los originales.
- **Actualiza los checksums.** Después de editar cualquier archivo listado en `evidence/SHA256SUMS.txt`, actualiza su entrada y confirma que toda la lista sigue verificando. Editar un archivo listado bajo `evidence/`, `experiments/` o `bridges/` cambia la versión de los datos y la huella que imprime `verificar.py`; si eso pasa, agrega el par nuevo a `REFS` en `site/index.html` (si no, falla el CI) y a la tabla en `evidence/reproductions/README.md`.
- **Mantén los conteos honestos.** Los 54 casos KILLED son 51 comportamientos distintos, y las 84 variantes por máquina son corridas pareadas, no 168 casos distintos. Cada afirmación pública necesita una fila en [CLAIMS.md](CLAIMS.md) que apunte a su evidencia.
- **Sin datos privados.** Antes de cualquier commit, comprueba que no hayan entrado al diff IPs privadas, nombres de usuario de la máquina, rutas privadas, credenciales ni nombres de empleadores.

Corre esto desde la raíz del repositorio antes de hacer push:

```sh
shasum -a 256 -c evidence/SHA256SUMS.txt     # on Linux: sha256sum -c
python3 evidence/verify_numerical.py
python3 -m unittest discover -s animations -p 'test_*.py'
python3 -m unittest discover -s evidence/formal/comparator -p 'test_*.py'
```
