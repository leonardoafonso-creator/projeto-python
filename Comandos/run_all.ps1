param(
    [string]$msg = "atualizacao automatica"
)

Write-Host "Rodando pipeline..."
poetry run python -m projeto_python.pipeline

if ($LASTEXITCODE -ne 0) {
    Write-Host "Pipeline falhou. Git nao sera atualizado."
    exit 1
}

Write-Host "Enviando para o Git..."
git add .
git commit -m $msg
git push

Write-Host "Tudo concluido!"