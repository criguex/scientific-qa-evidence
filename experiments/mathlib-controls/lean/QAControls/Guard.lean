import Lean

open Lean Elab Command

namespace QAControls

def transitiveConsts (env : Environment) (root : Name) : NameSet := Id.run do
  let mut seen : NameSet := {}
  let mut todo : Array Name := #[root]
  while !todo.isEmpty do
    let n := todo.back!
    todo := todo.pop
    if seen.contains n then continue
    seen := seen.insert n
    if let some ci := env.find? n then
      for c in ci.getUsedConstantsAsSet do
        if !seen.contains c then todo := todo.push c
  return seen

syntax (name := guardIndependent) "#guard_independent " ident " of " ident+ : command

@[command_elab guardIndependent] def elabGuardIndependent : CommandElab := fun stx => do
  let n ← liftCoreM <| realizeGlobalConstNoOverloadWithInfo stx[1]
  let deps := transitiveConsts (← getEnv) n
  for f in stx[3].getArgs do
    let fn ← liftCoreM <| realizeGlobalConstNoOverloadWithInfo f
    if deps.contains fn then
      throwError "guard: {n} depends on {fn}"
  logInfo m!"guard: {n} uses none of the theorems under test ({deps.size} constants checked)"

end QAControls
