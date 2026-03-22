param(
    [string]$msg = ""
)

Write-Host "Rodando pipeline do estudo..."
poetry run python -m projeto_python.pipeline

if ($LASTEXITCODE -ne 0) {
    Write-Host "Pipeline falhou. Interrompendo."
    exit 1
}

Write-Host "Pipeline concluido com sucesso."

if ($msg -ne "") {
    Write-Host "Atualizando Git..."
    git add .
    git commit -m $msg
    git push
    Write-Host "Git atualizado."
}