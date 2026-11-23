# language: es
# Evidencia: evidence/SHA256SUMS.txt, evidence/test_consistency.py, experiments/receipt-check/, evidence/numerical/
# Explicación paso a paso: docs/METODOLOGIA.md#hu-6--la-evidencia-es-trazable-y-la-herramienta-se-revisa-a-sí-misma

@HU-6
Característica: La evidencia es trazable y la herramienta se revisa a sí misma
  Como auditor
  Quiero que cada resultado apunte a un archivo intacto y que las herramientas reporten sus propios fallos
  Para confiar en la evidencia y no solo en el informe

  @CA-6.1 @cumple
  Escenario: Cada archivo de evidencia está intacto
    Dado los hashes registrados en "evidence/SHA256SUMS.txt"
    Cuando recalculo el SHA-256 de cada archivo
    Entonces todos coinciden con su hash registrado

  @CA-6.2 @cumple
  Escenario: Los documentos dicen los mismos números que los registros
    Dado el README, CLAIMS.md y los registros legibles por máquina
    Cuando corro "evidence/test_consistency.py"
    Entonces cada número publicado coincide con su registro

  @CA-6.3 @cumple
  Escenario: Se detecta un recibo que nombra un log que falta
    Dado los archivos auténticos de una corrida
    Y un recibo que nombra un log que no existe
    Cuando corro el procedimiento publicado y la revisión de recibos P6
    Entonces el procedimiento publicado termina con código 0 y no lo nota
    Pero P6 termina con código 1 y reporta "P6:receipt-log-missing-comparator-run.log"

  @CA-6.4 @cumple
  Escenario: Las pruebas numéricas atrapan los errores sembrados
    Dado nueve modelos sintéticos con 84 variantes por equipo
    Cuando corro la campaña en macOS y en Linux
    Entonces cada equipo da 27 PASS, 54 KILLED y 3 SURVIVED
    Y los dos equipos clasifican igual cada variante
    Y los 3 sobrevivientes quedan visibles a propósito

  @CA-6.5 @cumple
  Escenario: La herramienta no da un éxito falso cuando falla el oráculo
    Dado un oráculo que lanza una excepción o devuelve NaN
    Cuando el ejecutor numérico procesa el caso
    Entonces marca el caso como "INCONCLUSIVE" con "oracle_valid: false"
    Y si falla al exportar, marca la corrida como incompleta y sale con código 2
