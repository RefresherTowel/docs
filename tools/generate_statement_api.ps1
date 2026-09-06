param(
    [Parameter(Mandatory=$true)]
    [string]$StatementRoot
)

python tools\generate_api.py `
    --manifest api-manifests\statement.yml `
    --source-root $StatementRoot `
    --output statement\api-reference.md
exit $LASTEXITCODE
