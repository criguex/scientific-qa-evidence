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
    if ((Get-FileHash (Join-Path $workRoot $relative) -Algorithm SHA256).Hash.ToLower() -ne $expected[$relative]) {
        throw "Hash incorrecto: $relative"
    }
}
$resultRoot = Join-Path $workRoot "results"
if (Test-Path $resultRoot) { throw "Los resultados ya existen; no sobrescribir." }
New-Item -ItemType Directory -Path $resultRoot | Out-Null
$records = @()
$started = [DateTime]::UtcNow.ToString("o")
$timer = [Diagnostics.Stopwatch]::StartNew()
$failure = $null
try {
    & $python $runner --self-check 2>&1 | Tee-Object -FilePath (Join-Path $workRoot "self-check.log")
    if ($LASTEXITCODE -ne 0) { throw "Autopruebas fallidas: $LASTEXITCODE" }
    foreach ($number in 1..9) {
        $scenario = "osc{0:D2}" -f $number
        $baseline = Join-Path $resultRoot "$scenario\baseline\run.json"
        foreach ($mutant in @("baseline", "spring_sign", "damping_sign", "spring_coefficient", "frozen")) {
            if ($timer.Elapsed.TotalSeconds -gt 900) { throw "Presupuesto de campaña agotado." }
            $output = Join-Path $resultRoot "$scenario\$mutant"
            $arguments = @($runner, "--case", "oscillator", "--scenario", $scenario, "--mutant", $mutant, "--output", $output)
            if ($mutant -ne "baseline") { $arguments += @("--baseline", $baseline) }
            $runStarted = [DateTime]::UtcNow.ToString("o")
            $lines = & $python @arguments 2>&1
            $exitCode = $LASTEXITCODE
            $lines | Out-File -FilePath (Join-Path $workRoot "$scenario-$mutant-launch.log") -Encoding utf8
            $lines | Write-Output
            $report = Get-Content (Join-Path $output "run.json") -Raw | ConvertFrom-Json
            $records += [ordered]@{
                command = @($python) + $arguments
                started_utc = $runStarted
                finished_utc = [DateTime]::UtcNow.ToString("o")
                returncode = $exitCode
                status = $report.status
                scenario = $scenario
                mutant = $mutant
            }
            if ($exitCode -ne 0) { throw "Runner fallido: $scenario $mutant, $exitCode" }
            if ($mutant -eq "baseline" -and $report.status -ne "BASELINE_PASS") {
                throw "Referencia no válida: $scenario"
            }
        }
    }
} catch {
    $failure = $_.Exception.Message
    throw
} finally {
    [ordered]@{
        started_utc = $started
        finished_utc = [DateTime]::UtcNow.ToString("o")
        wall_seconds = $timer.Elapsed.TotalSeconds
        hostname = $env:COMPUTERNAME
        case = "oscillator"
        expected_runs = 45
        completed_runs = $records.Count
        failure = $failure
        source_hashes = $expected
        runs = $records
    } | ConvertTo-Json -Depth 8 | Out-File -FilePath (Join-Path $workRoot "campaign_execution.json") -Encoding utf8
}
