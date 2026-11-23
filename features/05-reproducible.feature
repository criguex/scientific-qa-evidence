# language: es
# Evidencia: verificar.py, .github/workflows/verify.yml, evidence/reproductions/
# Explicación paso a paso: docs/METODOLOGIA.md#hu-5--otra-persona-lo-repite-sin-mí

@HU-5
Característica: Otra persona lo repite sin mí
  Como persona que quiere revisar este trabajo
  Quiero correr las comprobaciones en mi computador y obtener el mismo resultado
  Para no tener que confiar en lo que dice el autor

  @CA-5.1 @cumple
  Esquema del escenario: La misma huella en distintos sistemas
    Dado la versión de los datos "c8edd482375d"
    Cuando corro "python verificar.py" en "<sistema>" con Python "<python>"
    Entonces las seis comprobaciones dicen OK
    Y la huella es "5292-A47D-AFA5"

    Ejemplos:
      | sistema | python |
      | Ubuntu  | 3.12   |
      | macOS   | 3.9    |
      | macOS   | 3.12   |
      | Windows | 3.9    |
      | Windows | 3.12   |

  @CA-5.2 @cumple
  Esquema del escenario: Otras personas obtienen la misma huella
    Dado la versión de los datos "26791fe6546f"
    Cuando una persona corre "python verificar.py" en "<sistema>" y lo reporta en el issue "<issue>"
    Entonces su huella es "C5F0-F1A8-2F4D", igual a la referencia

    Ejemplos:
      | sistema                | issue |
      | Windows 11             | #1    |
      | macOS, Apple Silicon   | #2    |
      | macOS, Apple Silicon   | #3    |
      | macOS, Apple Silicon   | #4    |

  @CA-5.3 @pendiente
  Escenario: Una persona lo reporta desde Linux
    Cuando una persona corre "python verificar.py" en Linux y lo reporta
    Entonces su huella coincide con la referencia de su versión
    # Resultado real: todavía no hay reporte de Linux. Este criterio queda en NO.

  @CA-5.4 @pendiente
  Escenario: Alguien distinto al autor recompila las demostraciones en Lean
    Dado la guía "docs/INDEPENDENT_REPRODUCTION.md" y su plantilla de reporte
    Cuando otra persona recompila sin intervención del autor
    Entonces obtiene 609 de 609 módulos y Comparator acepta (C), (D) y Euler
    # Resultado real: nadie lo ha hecho todavía. Este criterio queda en NO.
