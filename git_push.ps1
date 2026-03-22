param(
    [string]$msg = "update do projeto"
)

Write-Host "Adicionando arquivos..."
git add .

Write-Host "Commitando..."
git commit -m $msg

Write-Host "Enviando para o GitHub..."
git push

Write-Host "Concluido!"