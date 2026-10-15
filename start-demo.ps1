# Run from PowerShell whenever you want to show the digit recognition app:
#   & '.\start-demo.ps1'
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

$python = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'
$pythonArgs = @()
if (-not (Test-Path -LiteralPath $python)) {
    $pythonLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($null -eq $pythonLauncher) { throw 'Python 3.12 is missing. Run setup-local.ps1.' }
    $python = $pythonLauncher.Source
    $pythonArgs = @('-3.12')
}
& $python @pythonArgs -c "import streamlit, numpy, requests, PIL"
if ($LASTEXITCODE -ne 0) { throw 'Application packages are missing. Run setup-local.ps1.' }

$url = 'http://127.0.0.1:8502/'
try {
    $response = Invoke-WebRequest -UseBasicParsing -Uri ('{0}_stcore/health' -f $url) -TimeoutSec 3
    if ($response.StatusCode -eq 200) {
        Write-Output "A Streamlit server is already running at $url. Open it in your browser."
        Start-Process $url
        return
    }
} catch {
    # No server is listening yet; start this project's app below.
}

Write-Output "Starting the app at $url. Keep this PowerShell window open during the demo."
Write-Output 'Press Ctrl+C in this window to stop it.'
& $python @pythonArgs -m streamlit run .\digit_recognition\step_08_app.py --server.address 127.0.0.1 --server.port 8502
exit $LASTEXITCODE
