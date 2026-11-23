# language: es
# Evidencia: evidence/formal/cd-validation/, evidence/formal/b5/, evidence/lean-cloud-2026-10-23/
# Explicación paso a paso: docs/METODOLOGIA.md#hu-1--las-demostraciones-compilan

@HU-1
Característica: Las demostraciones de OpenAI compilan
  Como revisor de la demostración
  Quiero que el código que publicó OpenAI compile desde una versión fija
  Para saber que Lean revisó cada paso y que no hay pasos sin demostrar

  Antecedentes:
    Dado el repositorio openai/NavierStokesAndEuler en el commit "f9e8bc5"
    Y la versión de Lean "v4.34.0-rc2"

  @CA-1.1 @cumple
  Esquema del escenario: El código compila desde el commit fijado
    Cuando lo compilo en la compilación "<compilación>"
    Entonces la compilación termina con código de salida 0
    Y el registro queda en "<evidencia>"

    Ejemplos:
      | compilación                 | evidencia                                         |
      | B1 · 20-oct                 | evidence/formal/cd-validation/README.md           |
      | B2 · 20-oct · caché oficial | evidence/formal/cd-validation/README.md           |
      | nube · 23-oct · 609 de 609  | evidence/lean-cloud-2026-10-23/README.md          |

  @CA-1.2 @cumple
  Esquema del escenario: Compila sin piezas compiladas por otros
    Dado una carpeta de caché vacía
    Cuando compilo con "lake --no-cache build" en la compilación "<compilación>"
    Entonces la compilación termina con código de salida 0
    Y cada archivo ".olean" es más nuevo que el inicio de la compilación
    Y no se descargó ningún paquete ya compilado

    Ejemplos:
      | compilación              |
      | B4 · 21-oct · 1 h 29 min |
      | B5 · 21/22-oct · 1 h 15 min |

  @CA-1.3 @cumple
  Escenario: Las conclusiones usan solo los axiomas estándar
    Dado la compilación B5
    Cuando le pido a Lean los axiomas de "k1_C" y "k1_D"
    Entonces la lista es exactamente "propext", "Classical.choice" y "Quot.sound"
    Pero no aparece "sorryAx" ni ningún axioma adicional
