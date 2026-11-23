# language: es
# Evidencia: evidence/formal/cd-validation/mutants/, evidence/formal/statement-provenance/, experiments/mathlib-controls/
# Explicación paso a paso: docs/METODOLOGIA.md#hu-3--el-enunciado-no-deja-pasar-trampas

@HU-3
Característica: El enunciado no deja pasar trampas
  Como revisor
  Quiero saber que el verificador compara el enunciado exacto
  Para estar seguro de que lo demostrado es lo que se publicó y no una versión más fácil

  Antecedentes:
    Dado la compilación B2
    Y una copia del enunciado del desafío

  @CA-3.1 @cumple
  Esquema del escenario: Cada trampa de un símbolo es rechazada
    Dado que cambio un solo símbolo del enunciado: "<trampa>"
    Cuando corro Comparator con el enunciado cambiado
    Entonces Comparator lo rechaza con "statements do not match"
    Y el código de salida no es 0

    Ejemplos:
      | trampa                                              |
      | (C) sin fuerza externa: f = 0                       |
      | (D) sin fuerza externa: f = 0                       |
      | (C) datos periódicos en vez de datos en ℝ³          |
      | (C) viscosidad ≥ 0 en vez de > 0                    |
      | (D) sin la negación: existencia en vez de ruptura   |
      | Euler: tiempo T* ≤ 1/2 en vez de T* ≤ 1             |

  @CA-3.2 @cumple
  Escenario: Un cambio sin significado es aceptado (control)
    Dado que solo cambio un comentario del enunciado
    Cuando corro Comparator
    Entonces Comparator responde "Your solution is okay!"
    # Sin este control no se distingue una prueba exacta de una que rechaza todo.

  @CA-3.3 @cumple
  Escenario: El enunciado es el que publicó Google DeepMind
    Dado las 18 declaraciones del desafío de OpenAI
    Y el enunciado público de Formal Conjectures de Google DeepMind
    Cuando los comparo después de normalizar el texto
    Entonces las 18 declaraciones coinciden
    Pero la resolución de nombres no se verificó

  @CA-3.4 @cumple
  Escenario: Un rechazo significa "el enunciado cambió", no "el teorema es falso"
    Dado tres teoremas que Mathlib ya demuestra
    Y 11 casos registrados antes de correrlos
    Cuando le paso a Comparator 8 cambios al enunciado, 4 de ellos equivalentes
    Entonces Comparator rechaza los 8
    Y una segunda ruta clasifica cada cambio como equivalente, más débil o falso
