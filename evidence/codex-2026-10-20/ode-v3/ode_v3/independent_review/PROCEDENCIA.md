# Revisión local adicional: procedencia y reproducción

Esta revisión se ejecutó por un agente revisor distinto del escritor del adaptador, en el mismo equipo del usuario. **No es una auditoría de una entidad externa, certificación acreditada ni campaña remota WAR/GUERRA.** Empleó un oráculo de exponencial matricial 2×2 mediante serie, escalado y cuadrados, distinto de las fórmulas por regímenes del adaptador.

Se preserva `raw/` con **30 ejecuciones CLI**: 18 referencias y 12 controles de clasificación. `raw/osc05_altered_parameters/` es una **copia deliberadamente mal formada**, no una ejecución número 31. Solo se cambió `parameters.omega` de `0.8` a `0.81` en su `run.json`. Sus seis artefactos numéricos copiados permanecen idénticos al original.

El revisor verificó 180 hashes de artefactos de las 30 ejecuciones, más seis de la copia. El agregador V3 vuelve a verificarlos y registra los hashes de los 31 `run.json`. Resultados: 18 `BASELINE_PASS`, cuatro `EQUIVALENT`, tres `KILLED`, dos `SURVIVED` y tres `INCONCLUSIVE`. Los tres inconcluyentes son el resultado correcto de suministrar una referencia de otro escenario, otra familia o parámetros alterados; no reciben crédito como mutantes detectados.

## Entorno y fuentes

- Python 3.12.13, NumPy 2.5.4, macOS arm64, `float64`, little-endian.
- Ejecutable resuelto: `/opt/homebrew/Cellar/python@3.12/3.12.13_2/Frameworks/Python.framework/Versions/3.12/bin/python3.12`.
- NumPy de caché ya existente: `<HOME>/.cache/uv/archive-v0/tXyTf_NLV2jB6U41`. No se instaló una nueva dependencia para esta revisión.
- Adaptador: `f118929e692f90ff86cc9bda0f1e3a5288abd0191dceaae432eafaf0c00db9a8`.
- Helper: `cc9259992eee682d9ebb7c368e0cb91454b3f777d4b41ae3a87baf72e19094b9`.
- Contrato: `cee74957ddab6f5fa196d06840cfa642f5c08c15eb7b70540eb7e56c9bf5ed06`.

## Transcripción de los comandos ejecutados

Los siguientes cuerpos fueron ejecutados por entrada estándar, **no desde archivos de script que existieran entonces**. Se documentan después de la ejecución a partir de la transcripción del revisor. Las salidas resumidas se comunicaron en su handoff; los `run.json` sí son artefactos crudos persistidos. No se fabrica un archivo histórico de stdout.

Prefijo de ambos comandos:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<HOME>/.cache/uv/archive-v0/tXyTf_NLV2jB6U41 /opt/homebrew/opt/python@3.12/bin/python3.12 - <<'PY'
```

Primer cuerpo, seguido de `PY`:

```python
import importlib.util, math, pathlib, subprocess, sys, json, numpy as np
source=pathlib.Path('<TMP>/skills/escenarios-verificables/scripts/run_ode_scenario.py')
out=pathlib.Path('<TMP>')
spec=importlib.util.spec_from_file_location('review_ode',source);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def multiply(a,b):
 return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def independent(case,p,t):
 if case=='oscillator': M=[[0.,1.],[-p['omega']**2,-2*p['zeta']*p['omega']]]; y=[p['x0'],p['v0']]
 else: M=[[-p['kf'],p['kr']],[p['kf'],-p['kr']]];y=[p['A0'],p['B0']]
 norm=max(sum(abs(v*t) for v in row) for row in M); scale=max(0,math.ceil(math.log2(norm/.25))) if norm else 0
 a=[[v*t/(2**scale) for v in row] for row in M]; result=[[1.,0.],[0.,1.]]; term=[[1.,0.],[0.,1.]]
 for n in range(1,80):
  term=multiply(term,a);term=[[v/n for v in row] for row in term];result=[[result[i][j]+term[i][j] for j in range(2)] for i in range(2)]
  if max(abs(v) for row in term for v in row)<1e-18:break
 for _ in range(scale):result=multiply(result,result)
 return [sum(result[i][j]*y[j] for j in range(2)) for i in range(2)]
max_oracle=0.;max_fine=0.;count=0
for case,scenarios in mod.SCENARIOS.items():
 for scenario,p in scenarios.items():
  for t in [0.,.137,.7,1.3,4.]:
   max_oracle=max(max_oracle,max(abs(a-b) for a,b in zip(mod.oracle(case,p,t),independent(case,p,t))))
  folder=out/f'{scenario}_baseline'
  command=[sys.executable,str(source),'--case',case,'--scenario',scenario,'--mutant','baseline','--output',str(folder),'--no-plot']
  result=subprocess.run(command,capture_output=True,text=True,check=False)
  assert result.returncode==0,(scenario,result.stderr)
  report=json.loads((folder/'run.json').read_text())
  assert report['status']=='BASELINE_PASS',(scenario,report['result'])
  with np.load(folder/'fields.npz') as fields:
   ts=fields['times_2'];ys=fields['states_2']
   error=max(math.sqrt(sum((a-b)**2 for a,b in zip(y,independent(case,p,float(t))))/2) for t,y in zip(ts[::4],ys[::4]))
   max_fine=max(max_fine,error)
   assert error<1e-6,(scenario,error)
  count+=1
assert max_oracle<1e-12,max_oracle
print(json.dumps({'baselines_passed':count,'oracle_vs_independent_matrix_exponential_linf_max':max_oracle,'raw_fine_vs_independent_matrix_exponential_rms_max':max_fine,'python':sys.version.split()[0],'numpy':np.__version__,'output':str(out)}))
```

Salida comunicada, exit code 0:

```json
{"baselines_passed":18,"oracle_vs_independent_matrix_exponential_linf_max":9.103828801926284e-15,"raw_fine_vs_independent_matrix_exponential_rms_max":4.2667693015526346e-08,"python":"3.12.13","numpy":"2.5.4","output":"<TMP>"}
```

El primer máximo contrasta dos oráculos en 90 puntos: cinco tiempos por configuración. El segundo contrasta los estados finos guardados en los 81 tiempos comunes. No es el máximo sobre los 321 tiempos finos.

Antes del segundo cuerpo se ejecutó:

```sh
cp -R <TMP>/osc05_baseline <TMP>/osc05_altered_parameters
```

Luego `apply_patch` cambió únicamente `"omega": 0.8,` por `"omega": 0.81,` en el `run.json` de la copia.

Segundo cuerpo, con el mismo prefijo y cierre `PY`:

```python
import pathlib,subprocess,sys,json
source='<TMP>/skills/escenarios-verificables/scripts/run_ode_scenario.py'
out=pathlib.Path('<TMP>')
cases=[('oscillator','osc01','damping_sign','osc01_baseline','EQUIVALENT'),('oscillator','osc09','spring_sign','osc09_baseline','EQUIVALENT'),('oscillator','osc09','frozen','osc09_baseline','KILLED'),('reaction','rxn01','frozen','rxn01_baseline','EQUIVALENT'),('reaction','rxn08','frozen','rxn08_baseline','SURVIVED'),('reaction','rxn09','reverse_sign','rxn09_baseline','SURVIVED'),('reaction','rxn03','reverse_sign','rxn03_baseline','EQUIVALENT'),('oscillator','osc05','spring_sign','osc05_baseline','KILLED'),('reaction','rxn07','mass_leak','rxn07_baseline','KILLED'),('oscillator','osc05','damping_sign','osc01_baseline','INCONCLUSIVE'),('reaction','rxn05','forward_coefficient','osc01_baseline','INCONCLUSIVE'),('oscillator','osc05','damping_sign','osc05_altered_parameters','INCONCLUSIVE')]
for i,(case,scenario,mutant,base,expected) in enumerate(cases):
 folder=out/f'check_{i:02}_{scenario}_{mutant}'
 run=subprocess.run([sys.executable,source,'--case',case,'--scenario',scenario,'--mutant',mutant,'--baseline',str(out/base/'run.json'),'--output',str(folder),'--no-plot'],capture_output=True,text=True,check=False)
 assert run.returncode==0,(i,run.stderr)
 report=json.loads((folder/'run.json').read_text())
 assert report['status']==expected,(i,report['status'],expected)
 print(json.dumps({'check':i,'case':scenario,'mutant':mutant,'baseline':base,'status':report['status'],'baseline_valid':report['baseline_valid'],'validation_reason':report['baseline_validation_reason']}))
print('ALL_12_END_TO_END_CHECKS_PASSED')
```

Salida comunicada: doce líneas con los estados esperados y cierre `ALL_12_END_TO_END_CHECKS_PASSED`, exit code 0. Para reproducir, sustituir las rutas históricas por una carpeta de fuentes fijadas y **una carpeta nueva de resultados**; no sobrescribir la evidencia conservada.
