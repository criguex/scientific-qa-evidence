> Traducción al español de [SEED_COMMITMENT.md](SEED_COMMITMENT.md). Si hay alguna diferencia, vale el original.

# Compromiso de semilla para el experimento de fallos a ciegas

El autor generó una semilla aleatoria secreta en su propia máquina, fuera de la sesión del asistente de IA:

```sh
openssl rand -hex 16 > ~/semilla-experimento.txt
```

Solo se compartió su hash SHA-256, y se publica aquí, antes de congelar el diseño del experimento y antes de asignar cualquier fallo:

```text
6ab9f825a6e0102f06589795a3f3afb81b954ec054362e7e0352018547614d5e  semilla-experimento.txt
```

El hash cubre el archivo exactamente como se generó: 32 caracteres hexadecimales seguidos de un salto de línea.

## Reglas

1. La semilla decide qué copias reciben qué fallos. Solo la usa el script de asignación, corrido por el autor.
2. Quien corre las comprobaciones no lee el archivo de la semilla ni la clave de asignación hasta que se haya registrado cada comprobación. El asistente tiene acceso de sistema de archivos a la máquina del autor, así que esta regla descansa en ese compromiso; el hash publicado hace detectable cualquier cambio posterior de la semilla.
3. Después de registrar todos los resultados, el autor revela el archivo de la semilla. Cualquiera puede entonces comprobar `shasum -a 256` contra el hash de arriba y volver a correr el script de asignación para reproducir exactamente la misma asignación de fallos.
4. Si el archivo de la semilla se pierde o se edita, el experimento queda anulado y debe reiniciarse con un compromiso nuevo.
