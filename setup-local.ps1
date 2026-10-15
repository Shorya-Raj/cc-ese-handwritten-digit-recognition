# One-time setup on this Windows computer. Run from PowerShell:
#   & '.\setup-local.ps1'
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

$python = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'
$pythonArgs = @()
if (-not (Test-Path -LiteralPath $python)) {
    $pythonLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($null -eq $pythonLauncher) {
        throw 'Python 3.12 was not found. Install it from python.org or make the py launcher available.'
    }
    $python = $pythonLauncher.Source
    $pythonArgs = @('-3.12')
}

$awsCommand = Get-Command aws -ErrorAction SilentlyContinue
if ($awsCommand) {
    $aws = $awsCommand.Source
} else {
    $aws = Join-Path $env:LOCALAPPDATA 'Programs\Amazon\AWSCLIV2\aws.exe'
    if (-not (Test-Path -LiteralPath $aws)) {
        throw 'AWS CLI v2 was not found. Add aws to PATH or install AWS CLI v2 from AWS.'
    }
}

& $python @pythonArgs -m pip install --user -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Python package installation failed.' }
& $python @pythonArgs -c "import importlib.util; names=['streamlit','tensorflow','PIL','numpy','matplotlib','requests']; missing=[n for n in names if importlib.util.find_spec(n) is None]; print('Missing:', missing) if missing else print('All application packages are available'); raise SystemExit(bool(missing))"
if ($LASTEXITCODE -ne 0) { throw 'One or more application packages could not be imported.' }
& $aws --version
if ($LASTEXITCODE -ne 0) { throw 'AWS CLI is installed but failed to start.' }

if (Test-Path -LiteralPath '.streamlit\secrets.toml') {
    Write-Output 'AWS app settings are present. The Streamlit demo can call the existing AWS endpoint.'
} else {
    Write-Output 'AWS app settings are absent. The app will use the included local model.'
}
Write-Output 'Setup complete. Start the app with: & .\start-demo.ps1'
