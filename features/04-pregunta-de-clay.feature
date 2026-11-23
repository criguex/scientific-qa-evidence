# language: es
# Evidencia: evidence/formal/clay-lean-risk.md, bridges/, evidence/formal/clay-correspondence.md
# Explicación paso a paso: docs/METODOLOGIA.md#hu-4--es-la-pregunta-de-clay

@HU-4
Característica: Es la pregunta del Instituto Clay
  Como comunidad matemática
  Quiero que el enunciado en Lean diga lo mismo que el texto oficial del Instituto Clay
  Para saber si lo demostrado responde las alternativas (C) y (D) del problema

  Antecedentes:
    Dado el texto oficial de Clay escrito por C. L. Fefferman, con su fe de erratas
    Y los enunciados formales de (C) y (D)

  @CA-4.1 @cumple
  Escenario: Cada cláusula de Clay se revisa frente al enunciado formal
    Cuando comparo las 16 cláusulas una por una, ordenadas por riesgo
    Entonces 6 coinciden directamente
    Y 9 coinciden mediante hechos estándar con nombre
    Y 1 necesita una decisión humana: la presión periódica en (D)

  @CA-4.2 @cumple
  Escenario: Los teoremas de OpenAI implican el texto literal de Clay en Lean
    Dado mi transcripción literal de Clay en "bridges/ClayLiteral.lean"
    Cuando demuestro en Lean "k1_C" y "k1_D" a partir de los teoremas de OpenAI
    Entonces los dos quedan demostrados para toda viscosidad mayor que 0
    Y valen con las dos lecturas de "suave" en el tiempo cero
    Y la solución cero cumple todas las condiciones de Clay, así que el resultado no es vacío

  @CA-4.3 @pendiente
  Escenario: Un experto independiente revisa la transcripción de Clay
    Dado la hoja de revisión "bridges/K0_REVIEW.md" con 14 puntos
    Cuando una persona que conoce Lean o el problema la compara con el PDF de Clay
    Entonces confirma que la transcripción es fiel
    # Resultado real: nadie la ha revisado todavía. Este criterio queda en NO.

  @CA-4.4 @pendiente
  Escenario: Se decide la lectura de la presión periódica en (D)
    Dado la fe de erratas de Clay sobre la presión periódica
    Cuando un matemático decide si es una condición de la solución
    Entonces la cláusula 16 queda resuelta
    # Resultado real: el Instituto Clay no la interpretó. Este criterio queda en NO.
