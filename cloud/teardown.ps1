# Delete only the course demo's named Lambda, execution role, log group, and ZIP bucket.
# Run from the repository root after the evaluation: .\cloud\teardown.ps1
$ErrorActionPreference = 'Stop'
$awsCommand = Get-Command aws -ErrorAction SilentlyContinue
if ($awsCommand) {
    $aws = $awsCommand.Source
} else {
    $aws = Join-Path $env:LOCALAPPDATA 'Programs\Amazon\AWSCLIV2\aws.exe'
    if (-not (Test-Path -LiteralPath $aws)) {
        throw 'AWS CLI v2 was not found. Add aws to PATH or install AWS CLI v2 from AWS.'
    }
}
$env:AWS_DEFAULT_REGION = 'ap-southeast-2'
$env:AWS_PAGER = ''
$account = (& $aws sts get-caller-identity --query Account --output text).Trim()
if ($LASTEXITCODE -ne 0) { throw 'AWS sign-in is required before teardown.' }
$bucket = "cc-ese-digit-lambda-artifacts-$account-ap-southeast-2"

& $aws lambda delete-function --function-name cc-ese-digit-inference
if ($LASTEXITCODE -ne 0) { throw 'Could not delete the Lambda function.' }
& $aws logs delete-log-group --log-group-name '/aws/lambda/cc-ese-digit-inference'
if ($LASTEXITCODE -ne 0) { throw 'Could not delete its CloudWatch log group.' }
& $aws s3api delete-object --bucket $bucket --key digit_lambda.zip | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Could not delete the deployment ZIP.' }
& $aws s3api delete-bucket --bucket $bucket
if ($LASTEXITCODE -ne 0) { throw 'Could not delete the deployment bucket; check for other objects.' }
& $aws iam detach-role-policy --role-name cc-ese-digit-inference-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
if ($LASTEXITCODE -ne 0) { throw 'Could not detach the Lambda role policy.' }
& $aws iam delete-role --role-name cc-ese-digit-inference-role
if ($LASTEXITCODE -ne 0) { throw 'Could not delete the Lambda role.' }
Write-Output 'Demo AWS resources deleted. Remove .streamlit/secrets.toml to return the app to local mode.'
