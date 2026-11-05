import VersoManual
import VersoBlueprint.PreviewManifest
import ABEISBlueprint.Assembly

open Verso Doc
open Verso.Genre Manual

-- The no-preview-data mode still includes the official page-runtime module.
-- Emit its dependency closure without claiming a manifest or cached previews.
private def emitPageRuntime : Informal.PreviewManifest.BlueprintExtraStep := fun prepared => do
  let directory := match prepared.mode with
    | .single => "html-single"
    | .multi => "html-multi"
  Informal.PreviewManifest.writeBlueprintRuntimeModules
    (prepared.config.toConfig.destination / directory / "-verso-data")

def main (args : List String) : IO UInt32 :=
  if args.contains "--without-preview-data" then
    let options := args.filter (· != "--without-preview-data")
    Informal.PreviewManifest.blueprintMain
      ABEISBlueprint.assembledBlueprint
      (extensionImpls := by exact extension_impls%)
      options
      (config := Informal.PreviewManifest.withBlueprintAssets {})
      (extraSteps := [emitPageRuntime])
  else
    Informal.PreviewManifest.blueprintMainWithPreviewData
      ABEISBlueprint.assembledBlueprint
      args
      (extensionImpls := by exact extension_impls%)
