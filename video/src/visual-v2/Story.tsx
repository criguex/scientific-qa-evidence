import { Audio, Video } from "@remotion/media";
import type React from "react";
import { AbsoluteFill, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CanvasScene } from "../animations/CanvasScene";
import generatedMedia from "../generatedMedia.json";
import generatedSpanishMedia from "../generatedSpanishMedia.json";
import narration from "../../../production/narration.json";
import campaignSummary from "../../../evidence/numerical/multidomain_derived.json";
import rcBaseline from "../../../evidence/numerical/fixtures/rc-baseline.json";
import rcMutation from "../../../evidence/numerical/fixtures/rc-tau-double.json";

type SceneId = "rc" | "chemistry" | "campaign" | "formal" | "cooling" | "snell";
type Chapter = { id: string; title: string; audio: string; duration_in_frames: number; clip_end_frame: number; from_frame: number; captions: { text: string; startMs: number; endMs: number }[] };
type MediaManifest = { status: string; fps: number; width: number; height: number; long_duration_in_frames: number; chapters: Chapter[] };
type Beat = { at: number; scene: SceneId | "flow"; kind: string; title: string; body: string; values?: string[]; video?: boolean; videoStart?: number };
type Language = "en" | "es";
type SpanishBeat = Omit<Beat, "at"> & { anchor: string };

const media = generatedMedia as MediaManifest;
const chapters = narration.chapters;
const counts = campaignSummary.per_host.classification_counts;
const modelNames = ["RC circuit", "Newton cooling", "2nd-order consumption", "Beer–Lambert", "Snell refraction", "Thin lens", "Acoustic interface", "Fechner scale*", "Logistic response"];
const colors = { navy: "#071b2b", deep: "#0d2638", panel: "#123448", mint: "#55dfbd", white: "#f4f7f5", muted: "#abc0c8", coral: "#fb8176", gold: "#ffc56e", blue: "#70b9ff" };

const spanishMedia = generatedSpanishMedia as MediaManifest;
const spanishBeats: SpanishBeat[][] = [
  [
    { anchor: "Una suite de pruebas en verde", scene: "rc", kind: "flow", title: "¿Qué puede demostrar una prueba?", body: "Una suite en verde no basta. Este clip es contexto ilustrativo, no evidencia de colapso ni de la campaña.", video: true, videoStart: 0 },
    { anchor: "Antes de probar", scene: "rc", kind: "contract", title: "Fijar el contrato primero", body: "Definimos dominio, unidades, tolerancia e invariantes antes de conocer los resultados.", values: ["Dominio", "Unidades", "Tolerancia", "Invariantes"] },
    { anchor: "Luego ejecutamos", scene: "rc", kind: "mutation", title: "Ejecutar cambios deliberados", body: "Comparamos una línea base con mutaciones controladas, como invertir un signo o duplicar un coeficiente.", values: ["Línea base", "Signo invertido", "Coeficiente ×2"] },
    { anchor: "La pregunta es si", scene: "rc", kind: "detect", title: "Medir sensibilidad de prueba", body: "La pregunta es si un oráculo independiente detecta el cambio conocido; no si se descubrió un teorema.", values: ["Cambio conocido", "Oráculo independiente", "Clasificación"] },
    { anchor: "Si el programa y el oráculo", scene: "chemistry", kind: "independent", title: "Evitar errores compartidos", body: "Si el programa y el oráculo comparten fórmula e integrador, también pueden compartir el mismo error.", values: ["Sistema bajo prueba", "Formulación distinta", "Varias observaciones"] },
    { anchor: "El contrato define", scene: "formal", kind: "contract", title: "Mantener fijo el criterio", body: "Una línea base que falla bloquea la interpretación. Una mutación pequeña puede sobrevivir bajo la tolerancia.", values: ["La línea base debe pasar", "Mutación evaluada", "Tolerancia fija"] },
    { anchor: "Una línea base que falla", scene: "rc", kind: "survivor", title: "Un superviviente también informa", body: "Las variaciones pequeñas pueden permanecer dentro del contrato. Se reportan, no se declaran equivalentes.", values: ["SOBREVIVE", "Dentro de tolerancia", "Sin equivalencia"] },
    { anchor: "El umbral no se cambia", scene: "campaign", kind: "tolerance", title: "El umbral no cambia después", body: "El criterio queda fijado antes de revisar los resultados.", values: ["Tolerancia fija", "Sin ajuste posterior", "Clasificación trazable"] },
    { anchor: "Separamos cálculos sintéticos", scene: "campaign", kind: "scope", title: "Categorías de evidencia separadas", body: "Cálculos sintéticos, controles de kernel y campañas anteriores no se mezclan.", values: ["Modelos sintéticos", "Controles formales", "Contexto histórico"] },
    { anchor: "Soy Cristian Guerra", scene: "rc", kind: "author", title: "Autor del estudio de QA", body: "Cristian Guerra · criguex · profesional colombiano de QA Automation de Medellín · más de ocho años (autodeclarado).", values: ["Estudio de QA", "Reproducción independiente", "Revisión humana"] },
    { anchor: "Soy autor de este estudio", scene: "rc", kind: "author", title: "Autoría y contribuciones humanas", body: "Cristian Guerra realizó la estrategia de pruebas, las mutaciones, la reproducción y la validación.", values: ["Estrategia", "Mutaciones", "Validación"] },
    { anchor: "Declaro el uso", scene: "formal", kind: "ai", title: "Asistencia de IA declarada", body: "Las herramientas de IA apoyaron el análisis y la preparación de código; no son coautoras ni descubridoras.", values: ["Estudio escrito por una persona", "Preparación asistida por IA", "Transparencia"] },
    { anchor: "OpenAI recibe crédito", scene: "formal", kind: "openai", title: "Crédito por las pruebas originales", body: "Las pruebas originales se acreditan a OpenAI. Este estudio no reclama autoría ni descubrimiento de teoremas.", values: ["Pruebas originales · OpenAI", "Nueva evidencia de QA", "Sin reclamo de descubrimiento"] },
    { anchor: "La contribución consiste", scene: "campaign", kind: "scope", title: "Un aporte de QA trazable", body: "Hacemos auditables los cambios deliberados, los fallos detectados y los límites del método.", values: ["Estrategia de pruebas", "Mutaciones", "Validación"] },
  ],
  [
    { anchor: "La suite contiene nueve", scene: "rc", kind: "models", title: "Nueve modelos sintéticos", body: "La lista evalúa el instrumento de QA; no representa nueve regímenes físicos independientes.", values: ["Circuito RC", "Enfriamiento de Newton", "Consumo de segundo orden", "Beer–Lambert", "Refracción de Snell", "Lente delgada", "Interfaz acústica", "Escala de Fechner*", "Respuesta logística"] },
    { anchor: "circuito RC, enfriamiento", scene: "campaign", kind: "models", title: "Modelos en varias áreas", body: "La lista combina ejemplos de circuitos, cinética, óptica y respuestas sintéticas.", values: ["Circuito", "Química", "Óptica", "Acústica"] },
    { anchor: "respuesta logística sintética", scene: "chemistry", kind: "logistic", title: "Respuesta logística sintética", body: "Los ejemplos son cálculos reproducibles, no mediciones de laboratorio.", values: ["Entrada normalizada", "Salida acotada", "Sin experimento"] },
    { anchor: "Un ejemplo concreto", scene: "rc", kind: "circuit", title: "Caso concreto: circuito RC", body: "Una resistencia de un kiloohmio y un capacitor de un milifaradio dan τ = 1 segundo.", values: ["R = 1.000 Ω", "C = 0,001 F", "τ = 1 s"] },
    { anchor: "Cambiar deliberadamente", scene: "rc", kind: "circuit", title: "Una mutación cambia el voltaje", body: "A los tres segundos, los valores registrados difieren al duplicar τ.", values: [`Línea base ${rcBaseline.values["256"][3].toFixed(3)} V`, `τ duplicada ${rcMutation.values["256"][3].toFixed(3)} V`] },
    { anchor: "Son cálculos reproducibles", scene: "rc", kind: "notlab", title: "Calculado, no medido", body: "Son cálculos sintéticos reproducibles, no mediciones de instrumentos de laboratorio.", values: ["Observaciones JSON", "Unidades fijadas", "Sin experimento"] },
    { anchor: "El caso RC se ejecuta", scene: "rc", kind: "resolution", title: "Refinar la integración RC", body: "El registro cubre tres segundos con tres resoluciones de integración.", values: ["64 pasos", "128 pasos", "256 pasos"] },
    { anchor: "A los tres segundos", scene: "rc", kind: "circuit", title: "A 3 segundos: 4,751 vs 3,884 V", body: "Son los valores registrados a 256 pasos para línea base y mutación.", values: [`Línea base ${rcBaseline.values["256"][3].toFixed(3)} V`, `Mutación ${rcMutation.values["256"][3].toFixed(3)} V`] },
    { anchor: "Son valores JSON redondeados", scene: "rc", kind: "notlab", title: "Valores JSON, no lecturas físicas", body: "Los números se redondean solo para mostrarlos en pantalla.", values: ["Datos registrados", "Unidades", "Sin instrumento físico"] },
    { anchor: "La constante de tiempo nominal", scene: "rc", kind: "equation", title: "Por qué cambia la curva", body: "La constante de tiempo del circuito es resistencia por capacitancia.", values: ["τ = R × C", "Mutación: τ × 2", "Horizonte: 3 s"] },
    { anchor: "Los demás oráculos", scene: "snell", kind: "oracles", title: "Modelos distintos, oráculos distintos", body: "La suite no usa una única estrategia de oráculo para todos los modelos.", values: ["EDO · solución cerrada", "Snell · bisección", "Lente · trazado de rayos", "Acústica · sistema de frontera", "Fechner · integral numérica"] },
    { anchor: "para Fechner", scene: "chemistry", kind: "fechner", title: "Fechner con integral numérica", body: "El oráculo trapezoidal es un cálculo finito, no datos de participantes humanos.", values: ["Integral trapezoidal", "Cálculo finito", "Sin datos humanos"] },
    { anchor: "El modelo logístico", scene: "chemistry", kind: "logistic", title: "Modelos ilustrativos, bien rotulados", body: "La respuesta logística es sintética; Fechner es ilustrativo, no una ley universal.", values: ["Estímulo normalizado", "Respuesta entre 0 y 1", "Sin validación humana"] },
    { anchor: "Algunas configuraciones", scene: "campaign", kind: "rescaling", title: "Nueve nombres no son nueve regímenes", body: "Algunas configuraciones comparten estructura matemática después del reescalamiento.", values: ["Nueve modelos sintéticos", "Configuraciones fijas", "Sin independencia asumida"] },
    { anchor: "No se usaron mediciones", scene: "rc", kind: "scope", title: "Sin mediciones experimentales", body: "Los gráficos muestran cálculos de modelos y puntos numéricos registrados.", values: ["Sintético", "Calculado", "Reproducible"] },
    { anchor: "no certifica el desempeño", scene: "rc", kind: "scope", title: "Sin certificación del mundo real", body: "La suite evalúa la detección de cambios conocidos en ejemplos controlados.", values: ["Sensibilidad a mutaciones", "Sin rendimiento de campo", "Sin certificación"] },
  ],
  [
    { anchor: "El control de kernel", scene: "formal", kind: "baseline-proof", title: "Un fixture mínimo de kernel", body: "La declaración objetivo afirma 0 = 0 y el valor de prueba exportado es rfl.", values: ["objetivo : 0 = 0", "valor := rfl"] },
    { anchor: "La mutación conserva", scene: "formal", kind: "mutated-proof", title: "Cambiar solo el valor de prueba", body: "La mutación conserva el tipo declarado, pero sustituye la prueba por una de True.", values: ["Esperado: 0 = 0", "Entregado: True.intro", "Solo cambia el valor exportado"] },
    { anchor: "Lean y nanoda", scene: "formal", kind: "proof-result", title: "Línea base aceptada · mutación rechazada", body: "Lean registra una incompatibilidad de tipos. nanoda llega a una aserción de igualdad definicional; su clasificación se deriva de la fuente fijada.", values: ["Lean · línea base aceptada", "Lean · incompatibilidad", "nanoda · rechazo derivado de fuente"] },
    { anchor: "Por separado, Lean acepta", scene: "formal", kind: "torus", title: "Control periódico independiente", body: "Lean acepta un campo de velocidad constante no nulo en un toro periódico, con presión y fuerza cero y viscosidad unitaria.", values: ["Dominio periódico", "Velocidad constante", "ν = 1"] },
    { anchor: "Lean informa que True", scene: "formal", kind: "proof-diagnostic", title: "La incompatibilidad es local", body: "Lean informa que True no coincide con el tipo de igualdad esperado.", values: ["Esperado: Eq Nat 0 0", "Encontrado: True", "Una declaración"] },
    { anchor: "El ejemplo periódico está", scene: "formal", kind: "axioms", title: "Tres axiomas reportados", body: "El reporte de axiomas del fixture periódico enumera estos nombres.", values: ["propext", "Classical.choice", "Quot.sound"] },
    { anchor: "Una velocidad constante", scene: "formal", kind: "scope", title: "No extrapolar a ℝ³", body: "Un campo de velocidad constante tiene energía infinita en todo el espacio euclidiano.", values: ["Toro: periódico", "ℝ³: energía infinita", "Alcance distinto"] },
    { anchor: "Después de la compilación", scene: "formal", kind: "comparator", title: "Comparator tras compilar desde fuente", body: "Después de compilar desde fuente limpia, ambos kernels aceptaron los dos desafíos configurados.", values: ["Navier–Stokes · nanoda + Lean", "Euler · nanoda + Lean", "Rechequeo registrado"] },
    { anchor: "La calibración incluyó", scene: "formal", kind: "calibration", title: "Calibración del harness separada", body: "Antes de invocar el kernel, dos fixtures positivos fueron aceptados y cuatro negativos rechazados.", values: ["2 positivos aceptados", "4 negativos rechazados", "Antes de invocar kernel"] },
    { anchor: "Estos resultados registrados", scene: "formal", kind: "scope", title: "Control acotado, no auditoría universal", body: "Estos resultados registrados no equivalen a una verificación universal.", values: ["Control positivo", "Fixture finito", "Sin reclamo amplio"] },
    { anchor: "Los nombres exactos aparecen", scene: "formal", kind: "trace", title: "Inspeccionar registros conservados", body: "Fixture, declaraciones y salidas siguen vinculados para revisión.", values: ["Fuente", "Harness", "Registros sanitizados"] },
  ],
  [
    { anchor: "La suite se ejecutó", scene: "campaign", kind: "hosts", title: "Dos entornos, una suite", body: "La misma campaña corrió en macOS arm64 y Linux x86_64.", values: ["macOS arm64", "Linux x86_64"] },
    { anchor: "Cada entorno evaluó", scene: "campaign", kind: "campaign", title: "84 variantes por host", body: "Cada host evalúa las mismas 84 variantes pareadas.", values: ["27 PASS", "54 KILLED", "3 SURVIVED"] },
    { anchor: "Las clasificaciones y", scene: "campaign", kind: "pairing", title: "Registros pareados, no 168 casos", body: "Las clasificaciones y parámetros coinciden entre las dos ejecuciones de host.", values: ["84 macOS", "84 Linux", "84 coincidencias pareadas"] },
    { anchor: "Los supervivientes", scene: "campaign", kind: "survivor", title: "Los supervivientes siguen visibles", body: "Pequeñas mutaciones de calibración sobrevivieron bajo el umbral fijo; no se forzó su rechazo.", values: ["3 SOBREVIVEN", "Reportadas", "Sin equivalencia por prueba"] },
    { anchor: "La comparación incluyó", scene: "campaign", kind: "finite", title: "738 valores finitos + 18 nulos", body: "Los nulos corresponden a resultados no finitos del mutante químico de inversión de signo.", values: ["738 finitos", "18 no finitos", "18 registrados como null"] },
    { anchor: "La mayor diferencia escalada", scene: "campaign", kind: "delta", title: "Diferencia máxima: 1,11 × 10⁻¹⁶", body: "Es la mayor diferencia escalada en los valores finitos pareados entre hosts.", values: ["738 pares finitos", "Diferencia escalada máx.", "1,11 × 10⁻¹⁶"] },
    { anchor: "Cada línea base usa", scene: "campaign", kind: "tolerance", title: "Umbral explícito de error 10⁻⁶", body: "Cada línea base se compara con un oráculo independiente y una tolerancia normalizada fija.", values: ["Oráculo", "Error normalizado", "Tolerancia 10⁻⁶"] },
    { anchor: "Las ecuaciones diferenciales usan", scene: "rc", kind: "resolution", title: "Refinar solo cuando aplica", body: "Las ecuaciones diferenciales usan resoluciones aplicables; los modelos algebraicos no reciben pasos inventados.", values: ["EDO · refinamientos aplicables", "Álgebra · sin pasos ficticios"] },
    { anchor: "En quince líneas base", scene: "campaign", kind: "convergence", title: "El orden observado es diagnóstico", body: "En 15 líneas base de EDO, los órdenes observados se acercaron a cuatro; no es una cota general.", values: ["15 EDO", "Orden observado ≈ 4", "Solo diagnóstico"] },
    { anchor: "El mayor error fino", scene: "campaign", kind: "fine-errors", title: "Errores finos bajo la tolerancia", body: "El mayor error fino fue logístico; Fechner usó un oráculo trapezoidal.", values: ["Logística · 1,12 × 10⁻⁹", "Fechner · 7,63 × 10⁻⁸", "Tolerancia · 10⁻⁶"] },
    { anchor: "Fechner llegó", scene: "chemistry", kind: "fechner", title: "Fechner usa una integral trapezoidal", body: "Es una comparación numérica finita, no una validación de percepción humana.", values: ["Oráculo trapezoidal", "Cálculo finito", "No valida percepción"] },
    { anchor: "Las mutaciones RC pequeñas", scene: "rc", kind: "survivor", title: "Una mutación pequeña sobrevivió", body: "Sobrevivir bajo este contrato no demuestra equivalencia matemática.", values: ["Dentro del umbral", "SOBREVIVE", "Sin inferencia de equivalencia"] },
    { anchor: "Se conservaron JSON", scene: "campaign", kind: "trace", title: "JSON siguió siendo la fuente", body: "JSON y clasificaciones se conservaron al corregir la exportación CSV.", values: ["JSON original", "CSV derivado", "Clasificación preservada"] },
  ],
  [
    { anchor: "El repositorio público", scene: "campaign", kind: "trace", title: "Una ruta de evidencia revisable", body: "El repositorio público enlaza código, registros y verificaciones reproducibles para revisión independiente.", values: ["Código", "Evidencia", "Reproducción"] },
    { anchor: "Reproducir archivos", scene: "campaign", kind: "reproduce", title: "Reproducir archivos no es repetir experimentos", body: "Verificar registros guardados y volver a ejecutar la suite sintética son acciones distintas.", values: ["Verificar registros", "Reejecutar suite", "No es experimento"] },
    { anchor: "El valor está en seguir", scene: "campaign", kind: "trace", title: "Seguir el contrato hasta los datos", body: "La trazabilidad permite auditar decisiones, detectar errores de exportación y conservar criterios previos.", values: ["Contrato", "Datos", "Criterios previos"] },
    { anchor: "Las campañas anteriores", scene: "campaign", kind: "historical", title: "Campañas anteriores, por separado", body: "Los contextos previos conservan parámetros y resultados para su revisión independiente.", values: ["Parámetros", "Resultados", "Contexto separado"] },
    { anchor: "La verificación local confirmó", scene: "campaign", kind: "chain", title: "Integridad, filas y pares", body: "Las verificaciones locales confirmaron integridad de artefactos, filas CSV y correspondencia entre hosts.", values: ["SHA-256", "Filas CSV", "Registros pareados"] },
    { anchor: "Clean03 completó", scene: "campaign", kind: "build", title: "Compilación limpia: 11.424 trabajos", body: "Clean03 terminó con código cero y reutilizó cachés de dependencias y toolchain; no fue un bootstrap completo.", values: ["PASS · código 0", "11.424 trabajos", "Caché reutilizada"] },
    { anchor: "Después, Comparator", scene: "formal", kind: "comparator", title: "Comparator rechecó ambos desafíos", body: "Tras la compilación desde fuente limpia, nanoda y Lean aceptaron cada solución configurada.", values: ["Navier–Stokes · aceptado", "Euler · aceptado", "Sin reclamo de descubrimiento"] },
    { anchor: "El contexto anterior", scene: "rc", kind: "historical", title: "Ejecuciones EDO anteriores", body: "Son 150 ejecuciones en grupos de 90, 30 y 30; no 150 casos independientes.", values: ["90 + 30 + 30", "Campaña anterior", "Evidencia separada"] },
    { anchor: "Los errores máximos", scene: "rc", kind: "ode-errors", title: "El error histórico baja con h", body: "Estos tres valores corresponden a un contexto EDO anterior y separado.", values: ["h = 0,05 · 1,3023 × 10⁻⁵", "h = 0,025 · 7,24 × 10⁻⁷", "h = 0,0125 · 4,27 × 10⁻⁸"] },
    { anchor: "siete coma veinticuatro", scene: "rc", kind: "ode-errors", title: "Paso intermedio: h = 0,025", body: "El error máximo registrado fue 7,24 × 10⁻⁷ para este paso histórico.", values: ["h = 0,025", "Error = 7,24 × 10⁻⁷", "Contexto anterior"] },
    { anchor: "y cuatro coma veintisiete", scene: "rc", kind: "ode-errors", title: "Paso fino: h = 0,0125", body: "El error máximo registrado fue 4,27 × 10⁻⁸ para este paso histórico.", values: ["h = 0,0125", "Error = 4,27 × 10⁻⁸", "Contexto anterior"] },
    { anchor: "frente a una tolerancia fina", scene: "campaign", kind: "tolerance", title: "Comparar con tolerancia fina", body: "La referencia de esta campaña anterior fue una tolerancia de 10⁻⁶.", values: ["Error máximo", "Tolerancia 10⁻⁶", "Registro histórico"] },
    { anchor: "Taylor–Green V1", scene: "flow", kind: "flow", title: "Taylor–Green es contexto visual", body: "El clip real ilustra flujo; no es una construcción formal ni evidencia de blow-up.", video: true, videoStart: 0 },
    { anchor: "La contribución es definir", scene: "campaign", kind: "contribution", title: "Aporte de este trabajo de QA", body: "Contratos, mutaciones conocidas, entornos pareados y evidencia rastreable hacen auditable el proceso.", values: ["Criterios fijos", "Fallos conocidos", "Trazabilidad"] },
    { anchor: "Cristian Guerra, criguex", scene: "formal", kind: "author", title: "Autoría y declaración de IA", body: "Cristian Guerra recibe crédito por el estudio de QA y la reproducción independiente. La IA se declara como asistencia.", values: ["Cristian Guerra · criguex", "QA Automation", "Medellín, Colombia"] },
    { anchor: "OpenAI recibe crédito", scene: "formal", kind: "openai", title: "Pruebas originales acreditadas a OpenAI", body: "No se reclama un teorema nuevo, una certificación ni la validación de un problema abierto.", values: ["OpenAI · pruebas originales", "Sin reclamo de descubrimiento", "Sin certificación"] },
    { anchor: "Invitamos a revisar", scene: "campaign", kind: "scope", title: "Revisar alcance y límites", body: "Invitamos a revisar evidencia, supuestos y limitaciones antes de reutilizar el material.", values: ["Inspeccionar", "Reproducir", "Cuestionar el alcance"] },
  ],
];

const getSpanishBeats = (chapterIndex: number): Beat[] => spanishBeats[chapterIndex].map(({ anchor, ...beat }) => {
  const cue = spanishMedia.chapters[chapterIndex].captions.find((caption) => caption.text.includes(anchor));
  if (!cue) throw new Error(`Spanish visual anchor missing: ${anchor}`);
  return { ...beat, at: cue.startMs / 1000 };
});

const beats: Beat[][] = [
  [
    { at: 0, scene: "rc", kind: "flow", title: "What can a test actually show?", body: "A green suite is not enough. This footage is illustrative context—not evidence of blow-up or of the campaign.", video: true, videoStart: 0 },
    { at: 5, scene: "rc", kind: "contract", title: "Freeze the contract first", body: "Specify the domain, units, tolerance and invariants before results are known.", values: ["Domain", "Units", "Tolerance", "Invariants"] },
    { at: 12, scene: "rc", kind: "mutation", title: "Run deliberate changes", body: "A baseline is compared with controlled mutations such as a sign reversal or doubled coefficient.", values: ["Baseline", "Sign reversal", "Coefficient ×2"] },
    { at: 18, scene: "rc", kind: "detect", title: "Measure test sensitivity", body: "The test asks whether an independent oracle detects the known change—not whether a theorem was discovered.", values: ["Known change", "Independent oracle", "Classification"] },
    { at: 26, scene: "chemistry", kind: "independent", title: "Avoid shared implementation errors", body: "A program and oracle that share a formula and integrator can share a mistake.", values: ["SUT", "Different formulation", "Multiple observations"] },
    { at: 36, scene: "formal", kind: "contract", title: "Keep success criteria fixed", body: "A failing baseline blocks interpretation of its mutants. A tiny change can survive if it stays below the fixed threshold.", values: ["Baseline must pass", "Mutant evaluated", "Tolerance unchanged"] },
    { at: 45, scene: "rc", kind: "survivor", title: "A survivor is still a result", body: "Small variations can remain inside the contract. They are reported, not silently promoted to equivalence.", values: ["SURVIVED", "Within tolerance", "No equivalence claim"] },
    { at: 55, scene: "campaign", kind: "trace", title: "Preserve the evidence chain", body: "Parameters, source, hashes and outputs stay linked so a reviewer can trace each classification.", values: ["Contract", "Source + parameters", "Outputs + hashes"] },
    { at: 56, scene: "rc", kind: "author", title: "Who made this QA study?", body: "Cristian Guerra · criguex · Colombian QA Automation professional from Medellín · 8+ years of experience (self-reported).", values: ["QA study", "Independent reproduction", "Human review"] },
    { at: 64, scene: "campaign", kind: "contribution", title: "A traceable testing contribution", body: "The contribution is making known failures, test sensitivity and limitations auditable.", values: ["Test strategy", "Mutations", "Validation"] },
    { at: 72, scene: "formal", kind: "ai", title: "AI assistance is disclosed", body: "AI tools assisted analysis and code preparation; they are not coauthors or co-discoverers.", values: ["Human-authored QA study", "AI-assisted preparation", "Disclosure included"] },
    { at: 78, scene: "formal", kind: "openai", title: "Credit for the original proofs", body: "The original proofs are credited to OpenAI. This study claims neither their authorship nor theorem discovery.", values: ["Original proofs · OpenAI", "New QA evidence", "No discovery claim"] },
    { at: 84, scene: "formal", kind: "scope", title: "Scope stays narrow", body: "Synthetic calculations, bounded kernel controls and historical campaigns are distinct evidence categories.", values: ["Synthetic models", "Formal controls", "Historical context"] },
  ],
  [
    { at: 0, scene: "rc", kind: "models", title: "Nine synthetic models", body: "Nine model names; some configurations share mathematical structure after rescaling.", values: modelNames },
    { at: 8, scene: "chemistry", kind: "notlab", title: "Synthetic examples—not experiments", body: "This model list evaluates the QA instrument; it does not represent nine independent physical regimes.", values: ["Synthetic calculations", "No laboratory measurements", "QA sensitivity"] },
    { at: 15, scene: "rc", kind: "circuit", title: "One concrete case: an RC circuit", body: "A one-kiloohm resistor and one-millifarad capacitor give τ = R × C = 1 second.", values: ["R = 1,000 Ω", "C = 0.001 F", "τ = 1 s"] },
    { at: 18, scene: "rc", kind: "circuit", title: "The observed quantity is voltage", body: "At three seconds, the fine-resolution recorded values differ after doubling τ.", values: [`Baseline ${rcBaseline.values["256"][3].toFixed(3)} V`, `Doubled τ ${rcMutation.values["256"][3].toFixed(3)} V`] },
    { at: 23, scene: "rc", kind: "notlab", title: "Calculated—not measured", body: "These values come from reproducible synthetic calculations, not laboratory instruments.", values: ["JSON observations", "Fixed units", "No experiment"] },
    { at: 30, scene: "chemistry", kind: "configurations", title: "Three configurations per model", body: "The fixed contract defines units and observation points; model counts do not imply independent regimes.", values: ["Configuration 1", "Configuration 2", "Configuration 3"] },
    { at: 36, scene: "rc", kind: "resolution", title: "Refine the RC integration", body: "The RC record uses 64, 128 and 256 integration steps over a three-second horizon.", values: ["64 steps", "128 steps", "256 steps"] },
    { at: 44, scene: "rc", kind: "circuit", title: "At 3 seconds: 4.751 vs 3.884 V", body: "The baseline and doubled-time-constant output are the recorded 256-step values.", values: [`Baseline ${rcBaseline.values["256"][3].toFixed(3)} V`, `Mutant ${rcMutation.values["256"][3].toFixed(3)} V`] },
    { at: 52, scene: "rc", kind: "equation", title: "Why the curve changes", body: "The circuit time constant is resistance multiplied by capacitance.", values: ["τ = R × C", "Mutation: τ × 2", "Horizon: 3 s"] },
    { at: 61, scene: "snell", kind: "oracles", title: "Different models, different oracles", body: "The suite avoids one shared oracle strategy for every model.", values: ["ODEs · closed form", "Snell · bisection", "Lens · ray tracing", "Acoustics · boundary system", "Fechner · numerical integral"] },
    { at: 73, scene: "chemistry", kind: "logistic", title: "Illustrative models stay labeled", body: "Logistic response is synthetic; Fechner is illustrative, not a universal law.", values: ["Normalized stimulus", "Response in [0, 1]", "Not human validation"] },
    { at: 81, scene: "campaign", kind: "rescaling", title: "Nine names are not nine regimes", body: "Some configurations share mathematical structure after rescaling.", values: ["Nine synthetic models", "Fixed configurations", "No independence claim"] },
    { at: 89, scene: "rc", kind: "notlab", title: "No experimental measurements", body: "The plots show model calculations and recorded numerical points only.", values: ["Synthetic", "Calculated", "Reproducible"] },
    { at: 94, scene: "rc", kind: "scope", title: "No real-world certification", body: "The suite evaluates detection of known changes in controlled examples.", values: ["Mutation sensitivity", "Not field performance", "Not certification"] },
  ],
  [
    { at: 0, scene: "formal", kind: "baseline-proof", title: "A minimal kernel fixture", body: "The target declaration states 0 = 0 and the exported proof value is rfl.", values: ["target : 0 = 0", "value := rfl"] },
    { at: 5, scene: "formal", kind: "mutated-proof", title: "Change only the proof value", body: "The mutation preserves the declared type but substitutes a proof of True.", values: ["Expected: 0 = 0", "Supplied: True.intro", "Only exported proof value changed"] },
    { at: 10, scene: "formal", kind: "proof-result", title: "Baseline accepted · mutation rejected", body: "Lean records a type mismatch. nanoda reaches a definitional-equality assertion; its classification is derived from pinned source.", values: ["Lean · baseline accepted", "Lean · type mismatch", "nanoda · source-derived rejection"] },
    { at: 18, scene: "formal", kind: "torus", title: "A separate periodic control", body: "Lean accepts a nonzero constant-velocity field on a periodic torus, with zero pressure and force and unit viscosity.", values: ["Periodic domain", "Constant velocity", "ν = 1"] },
    { at: 25, scene: "formal", kind: "scope", title: "Do not transfer the result to ℝ³", body: "A constant velocity field has infinite energy over all of Euclidean space.", values: ["Torus: periodic", "ℝ³: infinite energy", "Different scope"] },
    { at: 27, scene: "formal", kind: "proof-diagnostic", title: "The mismatch is local", body: "Lean reports that True does not match the expected equality type.", values: ["Expected Eq Nat 0 0", "Found True", "One declaration"] },
    { at: 34, scene: "formal", kind: "axioms", title: "Three reported axioms", body: "The periodic fixture's axiom report lists these names.", values: ["propext", "Classical.choice", "Quot.sound"] },
    { at: 41, scene: "formal", kind: "scope", title: "A bounded control, not a theorem audit", body: "The periodic example is intentionally separate from the minimal proof-value mutation.", values: ["Positive control", "Finite fixture", "No broad verification claim"] },
    { at: 47, scene: "formal", kind: "comparator", title: "Fresh Comparator recheck", body: "After the clean-source build, both configured challenges were accepted by both kernels.", values: ["Navier–Stokes · nanoda + Lean", "Euler · nanoda + Lean", "Recorded independent recheck"] },
    { at: 53, scene: "formal", kind: "comparator-runtime", title: "Long, recorded runs", body: "The saved logs show the configured comparison and successful command exits.", values: ["NS · 417.56 s", "Euler · 654.43 s", "Exit code 0"] },
    { at: 59, scene: "formal", kind: "calibration", title: "Harness calibration is separate", body: "Calibration used two positive fixtures accepted and four negative fixtures rejected before kernel calls.", values: ["2 positive accepted", "4 negative rejected", "Before kernel calls"] },
    { at: 62, scene: "formal", kind: "trace", title: "Inspect the preserved records", body: "The fixture, declarations and outputs remain linked for review.", values: ["Source", "Harness", "Sanitized logs"] },
  ],
  [
    { at: 0, scene: "campaign", kind: "hosts", title: "Two environments, one suite", body: "The same campaign ran on macOS arm64 and Linux x86_64.", values: ["macOS arm64", "Linux x86_64"] },
    { at: 4, scene: "campaign", kind: "campaign", title: "84 variants per host", body: "Counts below are per host; the variants are paired across hosts.", values: ["27 PASS", "54 KILLED", "3 SURVIVED"] },
    { at: 12, scene: "campaign", kind: "pairing", title: "84 paired records—not 168 cases", body: "Classifications and parameters match across the two host runs.", values: ["84 macOS", "84 Linux", "84 paired matches"] },
    { at: 19, scene: "campaign", kind: "survivor", title: "Survivors remain visible", body: "Tiny calibration mutations survived under the fixed threshold; they were not forced into rejection.", values: ["3 SURVIVED", "Reported", "Not equivalent by proof"] },
    { at: 22, scene: "campaign", kind: "paired-total", title: "The denominator matters", body: "The suite records counts per host and does not add a second platform as new variants.", values: ["84 / host", "2 paired hosts", "No 168-case claim"] },
    { at: 32, scene: "campaign", kind: "finite", title: "738 finite comparisons + 18 nulls", body: "The nulls come from the known chemical sign-reversal mutant's non-finite outputs.", values: ["738 finite", "18 non-finite", "18 represented as null"] },
    { at: 40, scene: "campaign", kind: "delta", title: "Cross-host difference: 1.11 × 10⁻¹⁶", body: "This is the largest scaled delta across finite paired values.", values: ["738 finite pairs", "Max scaled delta", "1.11 × 10⁻¹⁶"] },
    { at: 46, scene: "campaign", kind: "tolerance", title: "An explicit 10⁻⁶ error threshold", body: "Baselines are compared to an independent oracle using the fixed normalized tolerance.", values: ["Oracle", "Normalized error", "Tolerance 10⁻⁶"] },
    { at: 52, scene: "rc", kind: "resolution", title: "ODEs use applicable refinements", body: "Algebraic models receive no invented refinement levels.", values: ["ODE: refine where applicable", "Algebraic: no fabricated steps"] },
    { at: 57, scene: "campaign", kind: "convergence", title: "Observed order is diagnostic", body: "Across 15 ODE baselines, observed orders were near four; this is not a general error bound.", values: ["15 ODE baselines", "Observed order ≈ 4", "Diagnostic only"] },
    { at: 64, scene: "campaign", kind: "fine-errors", title: "Largest fine errors stayed below tolerance", body: "The largest fine ODE error was logistic; the Fechner result used a trapezoidal oracle.", values: ["Logistic · 1.12 × 10⁻⁹", "Fechner · 7.63 × 10⁻⁸", "Tolerance · 10⁻⁶"] },
    { at: 70, scene: "chemistry", kind: "fechner", title: "Fechner remains illustrative", body: "The logarithmic formula is compared with a trapezoidal numerical integral; this does not validate perception.", values: ["Trapezoidal oracle", "Finite computation", "Not human-subject data"] },
    { at: 76, scene: "rc", kind: "survivor", title: "A tiny RC mutation survived", body: "Survival under this contract does not establish mathematical equivalence.", values: ["Inside threshold", "SURVIVED", "No equivalence inference"] },
    { at: 80, scene: "campaign", kind: "scope", title: "Known changes, controlled examples", body: "The campaign tests detection and paired cross-platform consistency.", values: ["Synthetic QA", "Paired reruns", "No empirical validation"] },
    { at: 85, scene: "campaign", kind: "trace", title: "JSON stayed authoritative", body: "JSON and classifications were preserved when the CSV export was corrected.", values: ["Raw JSON", "Derived CSV", "Classification preserved"] },
  ],
  [
    { at: 0, scene: "campaign", kind: "trace", title: "A reviewable evidence path", body: "The public repository links source, records and reproducible checks for independent review.", values: ["Source", "Evidence", "Reproduction"] },
    { at: 8, scene: "formal", kind: "chain", title: "Integrity, rows, paired correspondence", body: "Local checks confirmed artifact integrity, CSV row counts and cross-host correspondence.", values: ["SHA-256", "CSV rows", "Paired host records"] },
    { at: 17, scene: "campaign", kind: "reproduce", title: "Reproducing files is not repeating experiments", body: "A saved-evidence check verifies artifacts; the synthetic suite rerun is a distinct action.", values: ["Verify saved records", "Rerun synthetic suite", "Different from experiment"] },
    { at: 22, scene: "campaign", kind: "build", title: "Clean source build: 11,424 jobs", body: "Clean03 exited successfully and reused dependency and toolchain caches; it was not a full bootstrap.", values: ["PASS · exit 0", "11,424 jobs", "Cache reused"] },
    { at: 27, scene: "campaign", kind: "build", title: "A cached source build—not a bootstrap", body: "The successful source build reused cached dependencies and toolchain artifacts.", values: ["11,424 jobs", "Cache reused", "Bootstrap not claimed"] },
    { at: 36, scene: "formal", kind: "comparator", title: "Comparator rechecked both challenges", body: "The recorded recheck followed the clean-source build; both nanoda and Lean accepted each configured solution.", values: ["Navier–Stokes · accepted", "Euler · accepted", "Not theorem discovery"] },
    { at: 41, scene: "rc", kind: "historical", title: "Earlier ODE runs are separate context", body: "150 recorded runs in groups of 90, 30 and 30—not 150 independent cases.", values: ["90 + 30 + 30", "Earlier campaign", "Separate evidence"] },
    { at: 50, scene: "rc", kind: "ode-errors", title: "Historical maximum error falls with h", body: "The three step-size values come from a separate earlier ODE context.", values: ["h = 0.05 · 1.3023 × 10⁻⁵", "h = 0.025 · 7.24 × 10⁻⁷", "h = 0.0125 · 4.27 × 10⁻⁸"] },
    { at: 59, scene: "rc", kind: "convergence", title: "The finest historical step met the stated tolerance", body: "These historical ODE errors are context, separate from the current 84-variant campaign.", values: ["h = 0.0125", "Max error 4.27 × 10⁻⁸", "Fine tolerance 10⁻⁶"] },
    { at: 65, scene: "flow", kind: "flow", title: "Taylor–Green is visual context", body: "This actual cropped clip illustrates flow only. It is not a formal construction or evidence of blow-up.", video: true, videoStart: 0 },
    { at: 69, scene: "campaign", kind: "contribution", title: "What this QA work contributes", body: "Contracts, known mutations, paired environments and traceable evidence make the testing process auditable.", values: ["Fixed criteria", "Known failures", "Traceability"] },
    { at: 75, scene: "formal", kind: "author", title: "Authorship and AI disclosure", body: "Cristian Guerra receives credit for the QA study and independent reproduction. AI is disclosed as assistance.", values: ["Cristian Guerra · criguex", "QA Automation", "Medellín, Colombia"] },
    { at: 84, scene: "formal", kind: "openai", title: "Original proofs credited to OpenAI", body: "No new theorem, certification or validation of an open mathematical problem is claimed.", values: ["OpenAI · original proofs", "No discovery claim", "No certification claim"] },
    { at: 90, scene: "campaign", kind: "scope", title: "Review scope and limits", body: "We invite review of the evidence, assumptions and limitations before reuse.", values: ["Inspect", "Reproduce", "Challenge the scope"] },
  ],
];

const chapterScene: SceneId[] = ["rc", "rc", "formal", "campaign", "formal"];

const Shell: React.FC<{ vertical: boolean; children: React.ReactNode }> = ({ vertical, children }) => (
  <AbsoluteFill style={{ background: "radial-gradient(ellipse at 75% 10%, #173b4c 0%, #071b2b 58%)", color: colors.white, fontFamily: "Inter, Avenir Next, Arial, sans-serif", overflow: "hidden" }}>
    <div style={{ position: "absolute", inset: 0, opacity: 0.14, backgroundImage: "linear-gradient(#557080 1px, transparent 1px), linear-gradient(90deg, #557080 1px, transparent 1px)", backgroundSize: vertical ? "90px 90px" : "120px 120px", maskImage: "linear-gradient(to bottom, black, transparent 90%)" }} />
    {children}
  </AbsoluteFill>
);

const ModelGrid: React.FC<{ progress: number; vertical: boolean; language: Language }> = ({ progress, vertical, language }) => {
  const displayedModels = language === "es" ? ["Circuito RC", "Enfriamiento de Newton", "Consumo de 2.º orden", "Beer–Lambert", "Refracción de Snell", "Lente delgada", "Interfaz acústica", "Escala de Fechner*", "Respuesta logística"] : modelNames;
  return (
  <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: vertical ? 9 : 12, marginTop: 22 }}>
    {displayedModels.map((name, index) => {
      const opacity = interpolate(progress * modelNames.length - index, [0, 0.8], [0.18, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      return <div key={name} style={{ opacity, minHeight: vertical ? 74 : 84, padding: vertical ? 12 : 16, borderRadius: 14, background: index === 7 ? "#342f28" : "#102f43", border: `1px solid ${index === 7 ? colors.gold : "#315264"}`, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center", fontSize: vertical ? 19 : 22, fontWeight: 700 }}>{name}</div>;
    })}
  </div>
  );
};

const Matrix: React.FC<{ vertical: boolean; progress: number }> = ({ vertical, progress }) => {
  const cells = Array.from({ length: 84 }, (_, index) => index < counts.PASS ? colors.mint : index < counts.PASS + counts.KILLED ? colors.coral : colors.gold);
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: vertical ? 16 : 24, marginTop: 28 }}>
      {["macOS arm64", "Linux x86_64"].map((host) => <div key={host} style={{ background: "#0b2434", border: "1px solid #315264", borderRadius: 20, padding: vertical ? 16 : 22 }}><div style={{ fontSize: vertical ? 20 : 26, color: colors.mint, fontWeight: 800 }}>{host} · 84</div><div style={{ display: "grid", gridTemplateColumns: "repeat(14,1fr)", gap: 4, marginTop: 14 }}>{cells.map((color, index) => <div key={index} style={{ opacity: interpolate(progress * 84 - index, [0, 1], [0.08, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }), height: vertical ? 13 : 17, borderRadius: 5, background: color }} />)}</div><div style={{ marginTop: 10, fontSize: vertical ? 17 : 21, lineHeight: 1.5 }}>27 PASS · 54 KILLED · 3 SURVIVED</div></div>)}
    </div>
  );
};

const TorusDiagram: React.FC<{ frame: number; vertical: boolean; language: Language }> = ({ frame, vertical, language }) => {
  const particleX = 52 + ((frame * 2.4) % 316);
  const labels = language === "es" ? ["Velocidad constante", "Presión y fuerza cero", "Viscosidad unitaria"] : ["Constant velocity", "Zero pressure and force", "Unit viscosity"];
  return (
    <div style={{ display: "grid", gridTemplateColumns: vertical ? "1fr" : "1fr 1fr", alignItems: "center", gap: 24, marginTop: 20 }}>
      <svg viewBox="0 0 420 270" style={{ width: "100%", height: vertical ? 220 : 280 }} aria-label="Periodic box schematic with parallel equal-length constant-velocity arrows">
        <rect x="42" y="48" width="336" height="150" rx="16" fill="#0b2434" stroke={colors.mint} strokeWidth="4" />
        {[82, 128, 174].map((y, index) => <g key={y}><line x1="90" y1={y} x2="170" y2={y} stroke={index === 1 ? colors.gold : colors.mint} strokeWidth="5" /><path d={`M170 ${y}l-16 -9v18z`} fill={index === 1 ? colors.gold : colors.mint} /></g>)}
        <circle cx={particleX} cy="128" r="8" fill={colors.white} />
        <path d="M45 214h330" stroke="#315264" strokeWidth="2" strokeDasharray="7 7" />
        <text x="210" y="242" fill={colors.muted} fontSize="18" textAnchor="middle">{language === "es" ? "Dominio periódico · esquema" : "Periodic wrap · schematic"}</text>
      </svg>
      <div style={{ display: "grid", gap: 12 }}>{labels.map((value, i) => <div key={value} style={{ padding: 16, background: "#102f43", borderLeft: `5px solid ${i === 1 ? colors.gold : colors.mint}`, borderRadius: 12, fontSize: vertical ? 22 : 28, fontWeight: 750 }}>{value}</div>)}</div>
    </div>
  );
};

const ODEBars: React.FC<{ vertical: boolean; language: Language }> = ({ vertical, language }) => {
  const values = [{ h: "0.05", value: 1.3023e-5, label: "1.3023 × 10⁻⁵" }, { h: "0.025", value: 7.24e-7, label: "7.24 × 10⁻⁷" }, { h: "0.0125", value: 4.27e-8, label: "4.27 × 10⁻⁸" }];
  return <div style={{ display: "grid", gap: vertical ? 12 : 18, marginTop: 24 }}><div style={{ fontSize: vertical ? 17 : 20, color: colors.muted }}>{language === "es" ? "Longitud proporcional al error absoluto" : "Bar length proportional to absolute error"}</div>{values.map((item, index) => <div key={item.h} style={{ display: "grid", gridTemplateColumns: vertical ? "150px 1fr" : "210px 1fr", alignItems: "center", gap: 16 }}><div style={{ fontSize: vertical ? 21 : 27, fontWeight: 700 }}>h = {item.h}</div><div><div style={{ height: vertical ? 32 : 42, width: `${item.value / values[0].value * 100}%`, minWidth: 2, background: index === 0 ? colors.coral : index === 1 ? colors.gold : colors.mint, borderRadius: 9 }} /><div style={{ marginTop: 4, fontSize: vertical ? 20 : 25, fontWeight: 800 }}>{item.label}</div></div></div>)}</div>;
};

const PhaseGraphic: React.FC<{ beat: Beat; progress: number; frame: number; vertical: boolean; language: Language }> = ({ beat, progress, frame, vertical, language }) => {
  if (beat.kind === "models") return <ModelGrid progress={progress} vertical={vertical} language={language} />;
  if (beat.kind === "campaign") return <Matrix vertical={vertical} progress={progress} />;
  if (beat.kind === "torus") return <TorusDiagram frame={frame} vertical={vertical} language={language} />;
  if (beat.kind === "ode-errors") return <ODEBars vertical={vertical} language={language} />;
  if (beat.kind === "comparator" || beat.kind === "comparator-runtime") {
    const values = beat.values ?? [];
    return <div style={{ display: "grid", gap: 12, marginTop: 24 }}>{values.map((value, index) => <div key={value} style={{ display: "grid", gridTemplateColumns: vertical ? "1fr" : "1fr auto", alignItems: "center", gap: 14, padding: 17, borderRadius: 14, background: "#102f43", border: "1px solid #315264", fontSize: vertical ? 22 : 27, fontWeight: 750 }}><span>{value}</span><span style={{ color: index < 2 ? colors.mint : colors.gold }}>{index < 2 ? (language === "es" ? "ACEPTADO" : "ACCEPTED") : (language === "es" ? "REGISTRADO" : "RECORDED")}</span></div>)}</div>;
  }
  if (beat.kind === "convergence") return <div style={{ display: "grid", gap: 14, marginTop: 26 }}>{(beat.values ?? []).map((value, index) => <div key={value} style={{ padding: 18, borderRadius: 15, background: "#102f43", borderLeft: `5px solid ${[colors.mint, colors.gold, colors.coral][index % 3]}`, fontSize: vertical ? 22 : 30, fontWeight: 800 }}>{value}</div>)}</div>;
  if (beat.kind === "resolution") {
    const items = beat.values ?? [];
    const stepCounts = items.map((item) => Number(item.match(/\d+/)?.[0] ?? 0));
    const maxSteps = Math.max(...stepCounts, 1);
    return <div style={{ display: "grid", gridTemplateColumns: `repeat(${items.length},1fr)`, gap: 12, marginTop: 28, alignItems: "end", minHeight: vertical ? 180 : 230 }}>{items.map((item, index) => <div key={item} style={{ height: `${stepCounts[index] / maxSteps * 100}%`, minHeight: 36, borderRadius: "14px 14px 4px 4px", background: [colors.blue, colors.gold, colors.mint][index % 3], display: "flex", alignItems: "flex-end", justifyContent: "center", padding: 12, color: colors.navy, fontSize: vertical ? 17 : 21, fontWeight: 800, opacity: interpolate(progress * 3 - index, [0, 1], [0.25, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>{item}</div>)}</div>;
  }
  if (beat.kind === "axioms") return <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: 14, marginTop: 26 }}>{(beat.values ?? []).map((value, index) => <div key={value} style={{ padding: 20, borderRadius: 16, background: "#102f43", border: `1px solid ${[colors.mint, colors.gold, colors.coral][index]}`, fontFamily: "ui-monospace,Menlo,monospace", fontSize: vertical ? 24 : 34, fontWeight: 800, textAlign: "center" }}>{value}</div>)}</div>;
  if (beat.kind === "flow") return <div style={{ color: colors.gold, fontSize: vertical ? 19 : 24, fontWeight: 850, paddingTop: 22 }}>{language === "es" ? "FLUJO ILUSTRATIVO · NO ES EVIDENCIA DE CAMPAÑA" : "ILLUSTRATIVE FLOW · NOT CAMPAIGN EVIDENCE"}</div>;
  if (beat.kind === "baseline-proof" || beat.kind === "mutated-proof" || beat.kind === "proof-result" || beat.kind === "proof-diagnostic") {
    return <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, marginTop: 25 }}><div style={{ border: "1px solid #315264", background: "#0b2434", borderRadius: 18, padding: 22 }}><div style={{ color: colors.mint, fontSize: vertical ? 21 : 26, fontWeight: 800 }}>{language === "es" ? "LÍNEA BASE" : "BASELINE"}</div><div style={{ marginTop: 16, fontFamily: "ui-monospace,Menlo,monospace", fontSize: vertical ? 27 : 38, fontWeight: 800 }}>0 = 0</div><div style={{ marginTop: 8, fontFamily: "ui-monospace,Menlo,monospace", fontSize: vertical ? 22 : 29 }}>rfl</div><div style={{ color: colors.mint, marginTop: 14, fontSize: vertical ? 19 : 23, fontWeight: 700 }}>{language === "es" ? "aceptada" : "accepted"}</div></div><div style={{ border: "1px solid #315264", background: "#0b2434", borderRadius: 18, padding: 22 }}><div style={{ color: colors.coral, fontSize: vertical ? 21 : 26, fontWeight: 800 }}>{language === "es" ? "VALOR MUTADO" : "MUTATED VALUE"}</div><div style={{ marginTop: 16, fontFamily: "ui-monospace,Menlo,monospace", fontSize: vertical ? 25 : 34, fontWeight: 800 }}>True.intro</div><div style={{ color: colors.gold, marginTop: 14, fontSize: vertical ? 19 : 23, fontWeight: 700 }}>{language === "es" ? "Tipo incompatible" : "Type mismatch"}</div></div></div>;
  }
  if (beat.kind === "hosts") return <Matrix vertical={vertical} progress={progress} />;
  const values = beat.values ?? [];
  const metricSize = values.length < 3 ? (vertical ? 36 : 48) : (vertical ? 25 : 32);
  return (
    <div style={{ display: "grid", gridTemplateColumns: `repeat(${values.length >= 3 ? 2 : values.length || 1},minmax(0,1fr))`, gap: 16, marginTop: 24 }}>
      {values.map((value, index) => <div key={value} style={{ minHeight: vertical ? 88 : 110, padding: vertical ? 16 : 22, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center", borderRadius: 18, border: "1px solid #315264", borderTop: `5px solid ${[colors.mint, colors.gold, colors.coral][index % 3]}`, background: "linear-gradient(140deg,#123448,#0b2434)", fontSize: metricSize, fontWeight: 800, lineHeight: 1.12, opacity: interpolate(progress * 100 - index * 12, [0, 24], [0.35, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>{value}</div>)}
    </div>
  );
};

const StageArt: React.FC<{ beat: Beat; scene: SceneId; sceneTime: number; vertical: boolean; startFrame: number; duration: number; fps: number; language: Language }> = ({ beat, scene, sceneTime, vertical, startFrame, duration, fps, language }) => (
  <div style={{ width: vertical ? 792 : 700, height: vertical ? 792 : 700, overflow: "hidden", border: "1px solid #315264", borderRadius: 22, background: colors.navy, position: "relative" }}>
    {beat.video ? (
      <Sequence from={startFrame} durationInFrames={duration} trimBefore={Math.round((beat.videoStart ?? 0) * fps)} premountFor={fps} style={{ position: "absolute", inset: 0 }}>
        <Video src={staticFile("english/media/flow-illustration.mp4")} muted premountFor={fps} objectFit="contain" style={{ position: "absolute", left: 0, right: 0, top: vertical ? 184 : 196, width: "100%", height: vertical ? 211 : 187, opacity: 0.95 }} />
      </Sequence>
    ) : (
      <div style={{ width: 1080, height: 1080, transform: vertical ? "scale(.7333)" : "scale(.6481)", transformOrigin: "top left" }}><CanvasScene sceneId={scene} timeOverrideSeconds={sceneTime} /></div>
    )}
    {beat.video && <><div style={{ position: "absolute", top: vertical ? 128 : 138, left: 20, right: 20, textAlign: "center", color: colors.white, fontSize: vertical ? 19 : 22, fontWeight: 800 }}>{language === "es" ? "CLIP DE DOS PANELES · ENCUADRE COMPLETO" : "TWO-PANEL FLOW CLIP · FULL FRAME"}</div><div style={{ position: "absolute", left: 18, right: 18, bottom: 16, textAlign: "center", borderRadius: 12, padding: 10, background: "#071b2bd9", color: colors.gold, fontSize: vertical ? 16 : 20, fontWeight: 850 }}>{language === "es" ? "FLUJO ILUSTRATIVO · NO ES EVIDENCIA NI PRUEBA" : "ILLUSTRATIVE FLOW · NOT CAMPAIGN EVIDENCE OR PROOF"}</div></>}
  </div>
);

const StoryVisual: React.FC<{ chapterIndex: number; vertical: boolean; language: Language }> = ({ chapterIndex, vertical, language }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const second = frame / fps;
  const list = language === "es" ? getSpanishBeats(chapterIndex) : beats[chapterIndex];
  let beatIndex = 0;
  for (let index = 1; index < list.length; index += 1) if (second >= list[index].at) beatIndex = index;
  const beat = list[beatIndex];
  const elapsed = second - beat.at;
  const nextBeat = list[beatIndex + 1];
  const activeMedia = language === "es" ? spanishMedia : media;
  const beatDuration = nextBeat ? nextBeat.at - beat.at : activeMedia.chapters[chapterIndex].duration_in_frames / fps - beat.at;
  const progress = interpolate(elapsed / Math.max(0.01, beatDuration), [0, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const sceneTime = Math.min(20, Math.max(0, elapsed));
  const canvasScene = beat.scene === "flow" ? chapterScene[chapterIndex] : beat.scene;
  const startFrame = Math.round(beat.at * fps);
  const duration = Math.max(1, Math.round(beatDuration * fps));
  const title = language === "es" ? spanishMedia.chapters[chapterIndex].title : chapters[chapterIndex].en.title;

  return (
    <Shell vertical={vertical}>
      {vertical ? (
        <>
          <div style={{ position: "absolute", top: 42, left: 54, right: 54, display: "grid", gap: 10, color: colors.mint, textTransform: "uppercase", fontWeight: 800 }}>
            <div style={{ fontSize: 20, letterSpacing: 2 }}>ADV-050 · {language === "es" ? "QA Y EVIDENCIA" : "QA EVIDENCE"} · {String(chapterIndex + 1).padStart(2, "0")} / 05</div>
            <div style={{ fontSize: 17, letterSpacing: 0.5 }}>Cristian Guerra · QA Automation · Medellín, Colombia · @criguex</div>
          </div>
          <div style={{ position: "absolute", top: 145, left: 54, right: 54, fontSize: 48, fontWeight: 850, lineHeight: 1.05, minWidth: 0, overflowWrap: "anywhere" }}>{title}</div>
          <div style={{ position: "absolute", top: 280, left: 144 }}><StageArt beat={beat} scene={beat.scene === "flow" ? chapterScene[chapterIndex] : canvasScene} sceneTime={sceneTime} vertical startFrame={startFrame} duration={duration} fps={fps} language={language} /></div>
          <div style={{ position: "absolute", top: 1105, left: 54, right: 54, border: "1px solid #315264", borderRadius: 22, background: "linear-gradient(145deg,#15374a,#0d2638)", padding: 24 }}>
            <div style={{ color: colors.gold, fontSize: 18, fontWeight: 800, letterSpacing: 1.6 }}>{language === "es" ? "EVIDENCIA Y CONTEXTO" : beat.kind.toUpperCase().replace(/-/g, " ")}</div>
            <div style={{ marginTop: 10, fontSize: 34, fontWeight: 850, lineHeight: 1.08 }}>{beat.title}</div>
            <div style={{ marginTop: 12, color: colors.muted, fontSize: 22, lineHeight: 1.28, minWidth: 0, maxWidth: "100%", overflowWrap: "anywhere" }}>{beat.body}</div>
            <PhaseGraphic beat={beat} progress={progress} frame={frame} vertical language={language} />
          </div>
          <div style={{ position: "absolute", left: 54, right: 54, bottom: 280, height: 8, background: "#25485a", borderRadius: 6 }}><div style={{ width: `${progress * 100}%`, height: "100%", borderRadius: 6, background: colors.mint }} /></div>
        </>
      ) : (
        <>
          <div style={{ position: "absolute", top: 48, left: 90, right: 90, display: "flex", justifyContent: "space-between", alignItems: "center", color: colors.mint, fontSize: 22, letterSpacing: 2, fontWeight: 800, textTransform: "uppercase" }}><span>ADV-050 · {language === "es" ? "QA Y EVIDENCIA" : "QA EVIDENCE"} · {String(chapterIndex + 1).padStart(2, "0")} / 05</span><span style={{ fontSize: 17, letterSpacing: 0.5 }}>Cristian Guerra · QA Automation · Medellín, Colombia · @criguex</span></div>
          <div style={{ position: "absolute", top: 120, left: 90, right: 90, display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 32, minWidth: 0 }}><div style={{ fontSize: 32, fontWeight: 800, minWidth: 0, overflowWrap: "anywhere" }}>{title}</div><div style={{ color: colors.muted, fontSize: 21, whiteSpace: "nowrap" }}>{language === "es" ? "Tiempo" : "Chapter time"} {second.toFixed(1)} s</div></div>
          <div style={{ position: "absolute", top: 210, left: 90 }}><StageArt beat={beat} scene={beat.scene === "flow" ? chapterScene[chapterIndex] : canvasScene} sceneTime={sceneTime} vertical={false} startFrame={startFrame} duration={duration} fps={fps} language={language} /></div>
          <div style={{ position: "absolute", top: 210, left: 830, right: 90, height: 700, border: "1px solid #315264", borderRadius: 22, background: "linear-gradient(145deg,#15374a,#0d2638)", padding: 36, overflow: "hidden" }}>
            <div style={{ color: colors.gold, fontSize: 20, fontWeight: 800, letterSpacing: 2 }}>{language === "es" ? "EVIDENCIA Y CONTEXTO" : beat.kind.toUpperCase().replace(/-/g, " ")}</div>
            <div style={{ marginTop: 18, fontSize: 47, fontWeight: 850, lineHeight: 1.04 }}>{beat.title}</div>
            <div style={{ marginTop: 18, color: colors.muted, fontSize: 26, lineHeight: 1.3, minWidth: 0, maxWidth: "100%", overflowWrap: "anywhere" }}>{beat.body}</div>
            <PhaseGraphic beat={beat} progress={progress} frame={frame} vertical={false} language={language} />
          </div>
          <div style={{ position: "absolute", left: 90, right: 90, bottom: 94, height: 8, background: "#25485a", borderRadius: 6 }}><div style={{ width: `${progress * 100}%`, height: "100%", borderRadius: 6, background: colors.mint }} /></div>
          <div style={{ position: "absolute", right: 90, bottom: 52, color: colors.muted, fontSize: 17 }}>{language === "es" ? "Evidencia sintética / acotada · alcance de revisión" : "Synthetic / bounded evidence · review scope only"}</div>
        </>
      )}
    </Shell>
  );
};

const CaptionOverlay: React.FC<{ chapterIndex: number; vertical: boolean; language: Language }> = ({ chapterIndex, vertical, language }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentMs = frame * 1000 / fps;
  const activeMedia = language === "es" ? spanishMedia : media;
  const caption = activeMedia.chapters[chapterIndex].captions.find((item) => currentMs >= item.startMs && currentMs < item.endMs);
  if (!caption) return null;
  return <div style={{ position: "absolute", zIndex: 20, left: vertical ? 66 : 120, right: vertical ? 66 : 120, bottom: vertical ? 164 : 38, display: "flex", justifyContent: "center", fontFamily: "Inter, Avenir Next, Arial, sans-serif" }}><div style={{ maxWidth: vertical ? 930 : 1650, textAlign: "center", border: "1px solid #55dfbd", borderRadius: 18, padding: vertical ? "20px 28px" : "16px 30px", background: "#061723ed", color: colors.white, fontSize: vertical ? 40 : 32, fontWeight: 700, lineHeight: 1.18, fontFamily: "inherit" }}>{caption.text}</div></div>;
};

const ChapterSegment: React.FC<{ chapterIndex: number; vertical: boolean; language: Language }> = ({ chapterIndex, vertical, language }) => {
  const activeMedia = language === "es" ? spanishMedia : media;
  const chapter = activeMedia.chapters[chapterIndex];
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      <Audio src={staticFile(chapter.audio)} premountFor={fps} />
      <StoryVisual chapterIndex={chapterIndex} vertical={vertical} language={language} />
      <CaptionOverlay chapterIndex={chapterIndex} vertical={vertical} language={language} />
    </AbsoluteFill>
  );
};

export const LongVisualV2: React.FC<{ language?: Language }> = ({ language = "en" }) => {
  const { fps } = useVideoConfig();
  const activeMedia = language === "es" ? spanishMedia : media;
  return (
    <AbsoluteFill>
      {activeMedia.chapters.map((chapter, index) => <Sequence key={chapter.id} from={chapter.from_frame} durationInFrames={chapter.duration_in_frames} premountFor={fps}><ChapterSegment chapterIndex={index} vertical={false} language={language} /></Sequence>)}
    </AbsoluteFill>
  );
};

export const ShortVisualV2: React.FC<{ chapterIndex: number; language?: Language }> = ({ chapterIndex, language = "en" }) => <ChapterSegment chapterIndex={chapterIndex} vertical language={language} />;
