param(
    [string]$msg = "atualizacao automatica"
)

Write-Host "Rodando pipeline..."
poetry run python -m projeto_python.pipeline

Write-Host "Enviando para o Git..."
git add .
git commit -m $msg
git push

Write-Host "Tudo concluido!"