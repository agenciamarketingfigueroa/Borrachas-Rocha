param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$workspaceRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$finalFolder = Join-Path $workspaceRoot 'output/catalogo-pu-2026-por-montadora/final-2026'
$keep = @(
  'output/pdf/Catalogo-PU-2026-Final-A4.pdf',
  'output/pdf/Catalogo-PU-2026-Final-Clientes.pdf',
  'output/pdf/Catalogo-PU-2026-Final-Sangria-3mm.pdf',
  'output/pdf/Catalogo-Buchas-do-Amortecedor-2026-A4.pdf',
  'output/pdf/Catalogo-Buchas-do-Amortecedor-2026-Clientes.pdf',
  'output/pdf/Catalogo-Buchas-do-Amortecedor-2026-Sangria-3mm.pdf',
  'output/catalogo-pu-2026-por-montadora/fontes/capas-aprovadas.pdf'
) | ForEach-Object { (Resolve-Path -LiteralPath (Join-Path $workspaceRoot $_)).Path }
$searchRoots = @('output/pdf','output/catalogo-pu-2026','output/catalogo-pu-2026-por-montadora','catálogos de PU')
$candidates = @($searchRoots | ForEach-Object {
  Get-ChildItem -LiteralPath (Join-Path $workspaceRoot $_) -File -Recurse -Filter '*.pdf'
} | Where-Object { $_.FullName -notin $keep })
$extras = @(
  'catalogo-pu-a4.pdf', 'catalogo-pu-a4.html', 'catálogos de PU/catalogo-pu-impressao-2026.html',
  'output/catalogo-pu-2026/visao-geral.jpg',
  'output/catalogo-pu-2026-por-montadora/visao-geral.jpg',
  'output/catalogo-pu-2026-por-montadora/revisao-02/visao-geral.jpg',
  'output/catalogo-pu-2026-por-montadora/revisao-03/geral-visao-geral.jpg',
  'output/catalogo-pu-2026-por-montadora/revisao-03/amortecedor-visao-geral.jpg',
  'output/catalogo-pu-2026-por-montadora/revisao-04/visao-geral.jpg',
  'output/catalogo-pu-2026-por-montadora/revisao-03/previas',
  'output/catalogo-pu-2026-por-montadora/revisao-04/previas'
)
foreach ($relative in $extras) {
  $candidate = Join-Path $workspaceRoot $relative
  if (Test-Path -LiteralPath $candidate) { $candidates += Get-Item -LiteralPath $candidate }
}
$candidates = @($candidates | Sort-Object FullName -Unique)
$report = @()
foreach ($item in $candidates) {
  $resolved = (Resolve-Path -LiteralPath $item.FullName).Path
  if (-not $resolved.StartsWith($workspaceRoot + '\',[System.StringComparison]::OrdinalIgnoreCase)) { throw "Fora do projeto: $resolved" }
  if ($resolved -in $keep -or $resolved.StartsWith($finalFolder + '\',[System.StringComparison]::OrdinalIgnoreCase)) { throw "Arquivo vigente: $resolved" }
  if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Link inesperado: $resolved" }
  $files = if ($item.PSIsContainer) { @(Get-ChildItem -LiteralPath $resolved -File -Recurse) } else { @($item) }
  foreach ($file in $files) {
    if ($file.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Link inesperado: $($file.FullName)" }
  }
  $report += [PSCustomObject]@{path=$resolved.Substring($workspaceRoot.Length+1);directory=$item.PSIsContainer;files=$files.Count;bytes=($files | Measure-Object Length -Sum).Sum}
}
if ($Apply) {
  $validation = Get-Content -LiteralPath (Join-Path $finalFolder 'validacao.json') -Raw -Encoding UTF8 | ConvertFrom-Json
  if ($validation.recortes_transparentes -ne 15 -or -not $validation.mascaras_transparencia_no_pdf) { throw 'Valide os PDFs com recortes antes da limpeza.' }
  foreach ($item in $candidates) {
    if ($item.PSIsContainer) { Remove-Item -LiteralPath $item.FullName -Recurse -Force }
    else { Remove-Item -LiteralPath $item.FullName -Force }
  }
  [PSCustomObject]@{date='2026-10-21';removed=$report;kept=$keep;totalFiles=($report | Measure-Object files -Sum).Sum;totalBytes=($report | Measure-Object bytes -Sum).Sum} |
    ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $finalFolder 'limpeza.json') -Encoding UTF8
}
$report | Format-Table path,files,bytes -AutoSize
Write-Output "Arquivos: $(($report | Measure-Object files -Sum).Sum); MB: $([math]::Round((($report | Measure-Object bytes -Sum).Sum)/1MB,1)); aplicado: $Apply"
