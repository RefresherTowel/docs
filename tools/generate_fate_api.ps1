param(
	[Parameter(Mandatory = $true)]
	[string]$FateRoot
)

$SiteRoot = Split-Path -Parent $PSScriptRoot
$Manifest = Join-Path $SiteRoot "api-manifests\fate.yml"
$Output = Join-Path $SiteRoot "fate\api-reference.md"

python (Join-Path $PSScriptRoot "generate_api.py") `
	--manifest $Manifest `
	--source-root $FateRoot `
	--output $Output

if ($LASTEXITCODE -ne 0) {
	exit $LASTEXITCODE
}

Write-Host "Generated Fate API reference: $Output"
