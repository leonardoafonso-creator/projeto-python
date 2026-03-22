@echo off
poetry run python -m projeto_python.pipeline
git add .
git commit -m "update automatico"
git push
pause