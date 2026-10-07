param(
    [Parameter(Mandatory=$true)]
    [string]$SundialRoot
)

python tools\generate_api.py `
    --manifest api-manifests\sundial.yml `
    --source-root $SundialRoot `
    --output sundial\api-reference.md
exit $LASTEXITCODE
