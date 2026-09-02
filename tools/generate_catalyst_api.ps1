param(
    [Parameter(Mandatory=$true)]
    [string]$CatalystRoot
)

python tools\generate_api.py `
    --manifest api-manifests\catalyst.yml `
    --source-root $CatalystRoot `
    --output catalyst\api-reference.md
exit $LASTEXITCODE
