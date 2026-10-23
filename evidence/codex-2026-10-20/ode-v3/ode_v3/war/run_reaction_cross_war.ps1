$ErrorActionPreference = "Stop"
$workRoot = "<WIN_HOME>\nse-audit-20261020\ode-v3-f118929e"
$python = "<WIN_HOME>\nse-audit-20261020\simulation-venv\Scripts\python.exe"
$runner = Join-Path $workRoot "scripts\run_ode_scenario.py"
$expected = @{
    "scripts\run_ode_scenario.py" = "f118929e692f90ff86cc9bda0f1e3a5288abd0191dceaae432eafaf0c00db9a8"
    "scripts\run_scenario.py" = "cc9259992eee682d9ebb7c368e0cb91454b3f777d4b41ae3a87baf72e19094b9"
    "references\contratos-ode-v3.md" = "cee74957ddab6f5fa196d06840cfa642f5c08c15eb7b70540eb7e56c9bf5ed06"
}
foreach ($relative in $expected.Keys) {
    if ((Get-FileHash (Join-Path $workRoot $relative) -Algorithm SHA256).Hash.ToLower() -ne $expected[$relative]) { throw "Hash incorrecto: $relative" }
}
$resultRoot = Join-Path $workRoot "results_cross_reaction"
if (Test-Path $resultRoot) { throw "Los resultados ya existen; no sobrescribir." }
New-Item -ItemType Directory -Path $resultRoot | Out-Null
$records = @()
$started = [DateTime]::UtcNow.ToString("o")
$timer = [Diagnostics.Stopwatch]::StartNew()
$failure = $null
try {
    foreach ($scenario in @("rxn07", "rxn08", "rxn09")) {
        $baseline = Join-Path $resultRoot "$scenario\baseline\run.json"
        foreach ($mutant in @("baseline", "reverse_sign", "forward_coefficient", "mass_leak", "frozen")) {
            if ($timer.Elapsed.TotalSeconds -gt 600) { throw "Presupuesto de campaña agotado." }
            $output = Join-Path $resultRoot "$scenario\$mutant"
            $arguments = @($runner, "--case", "reaction", "--scenario", $scenario, "--mutant", $mutant, "--output", $output)
            if ($mutant -ne "baseline") { $arguments += @("--baseline", $baseline) }
            $runStarted = [DateTime]::UtcNow.ToString("o")
            $lines = & $python @arguments 2>&1
            $exitCode = $LASTEXITCODE
            $lines | Out-File -FilePath (Join-Path $workRoot "$scenario-$mutant-cross-launch.log") -Encoding utf8
            $lines | Write-Output
            $report = Get-Content (Join-Path $output "run.json") -Raw -Encoding utf8 | ConvertFrom-Json
            $records += [ordered]@{command=@($python)+$arguments;started_utc=$runStarted;finished_utc=[DateTime]::UtcNow.ToString("o");returncode=$exitCode;status=$report.status;scenario=$scenario;mutant=$mutant}
            if ($exitCode -ne 0) { throw "Runner fallido: $scenario $mutant, $exitCode" }
            if ($mutant -eq "baseline" -and $report.status -ne "BASELINE_PASS") { throw "Referencia no válida: $scenario" }
        }
    }
} catch {
    $failure = $_.Exception.Message
    throw
} finally {
    [ordered]@{started_utc=$started;finished_utc=[DateTime]::UtcNow.ToString("o");wall_seconds=$timer.Elapsed.TotalSeconds;hostname=$env:COMPUTERNAME;case="reaction";campaign_role="cross_host_replication";expected_runs=15;completed_runs=$records.Count;failure=$failure;source_hashes=$expected;runs=$records} | ConvertTo-Json -Depth 8 | Out-File -FilePath (Join-Path $workRoot "campaign_cross_execution.json") -Encoding utf8
}
