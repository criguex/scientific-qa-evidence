import Lean
import Export.Parse

def streamFromString (value : String) : BaseIO IO.FS.Stream := do
  let buffer ← IO.mkRef { data := value.toUTF8 }
  return IO.FS.Stream.ofBuffer buffer

def main (args : List String) : IO UInt32 := do
  if args.length != 1 then
    IO.eprintln "usage: ReplayExport <export.ndjson>"
    return 64
  let contents ← IO.FS.readFile args.head!
  let stream ← streamFromString contents
  let exported ← try
    Export.parseStream stream
  catch error =>
    IO.eprintln s!"EXPORT_PARSE_REJECT: {error}"
    return 3
  let environment ← Lean.mkEmptyEnvironment
  try
    let _ ← environment.toKernelEnv.replay exported.constMap
    IO.println "LEAN_KERNEL_ACCEPT"
    return 0
  catch error =>
    IO.eprintln s!"LEAN_KERNEL_REJECT: {error}"
    return 2
