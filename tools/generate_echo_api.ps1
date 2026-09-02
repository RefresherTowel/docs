param(
    [Parameter(Mandatory=$true)]
    [string]$EchoRoot
)

python tools\generate_api.py `
    --manifest api-manifests\echo.yml `
    --source-root $EchoRoot `
    --output echo\api-reference.md
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python tools\generate_api.py `
    --manifest api-manifests\echo-chamber.yml `
    --source-root $EchoRoot `
    --output echo-chamber\api-reference.md
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python tools\generate_api.py `
    --manifest api-manifests\echo-chamber-styles.yml `
    --source-root $EchoRoot `
    --output echo-chamber\style-api-reference.md
exit $LASTEXITCODE
