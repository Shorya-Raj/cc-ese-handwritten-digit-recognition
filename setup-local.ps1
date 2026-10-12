# One-time setup on this Windows computer. Run from PowerShell:
#   & '.\setup-local.ps1'
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

$python = 'C:\Users\shory\AppData\Local\Programs\Python\Python312\python.exe'
$aws = 'C:\Users\shory\AppData\Local\Programs\Amazon\AWSCLIV2\aws.exe'
if (-not (Test-Path -LiteralPath $python)) {
    throw "Python 3.12 was not found at $python. Install Python 3.12 from python.org first."
}
if (-not (Test-Path -LiteralPath $aws)) {
    throw "AWS CLI was not found at $aws. Install AWS CLI v2 from AWS first."
}

& $python -m pip install --user -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Python package installation failed.' }
& $python -c "import importlib.util; names=['streamlit','tensorflow','PIL','numpy','matplotlib','requests']; missing=[n for n in names if importlib.util.find_spec(n) is None]; print('Missing:', missing) if missing else print('All application packages are available'); raise SystemExit(bool(missing))"
if ($LASTEXITCODE -ne 0) { throw 'One or more application packages could not be imported.' }
& $aws --version
if ($LASTEXITCODE -ne 0) { throw 'AWS CLI is installed but failed to start.' }

if (Test-Path -LiteralPath '.streamlit\secrets.toml') {
    Write-Output 'AWS app settings are present. The Streamlit demo can call the existing AWS endpoint.'
} else {
    Write-Output 'AWS app settings are absent. The app will use the included local model.'
}
Write-Output 'Setup complete. Start the app with: & .\start-demo.ps1'
