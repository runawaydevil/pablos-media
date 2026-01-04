@echo off
REM Script para atualizar o site no GitHub com os arquivos gerados
REM Execute este script após rodar list_filmes.py e list_series.py

echo ========================================
echo Atualizando site no GitHub
echo ========================================
echo.

REM Verificar se os arquivos existem
if not exist "lista_filmes.txt" (
    echo ERRO: lista_filmes.txt nao encontrado!
    echo Execute: python list_filmes.py
    pause
    exit /b 1
)

if not exist "lista_series.txt" (
    echo ERRO: lista_series.txt nao encontrado!
    echo Execute: python list_series.py
    pause
    exit /b 1
)

echo Arquivos encontrados:
if exist "lista_filmes.txt" echo   [OK] lista_filmes.txt
if exist "lista_series.txt" echo   [OK] lista_series.txt
if exist "lista_filmes.pdf" echo   [OK] lista_filmes.pdf
if exist "lista_series.pdf" echo   [OK] lista_series.pdf
echo.

REM Adicionar apenas os arquivos gerados
echo Adicionando arquivos ao git...
git add lista_filmes.txt lista_series.txt
if exist "lista_filmes.pdf" git add lista_filmes.pdf
if exist "lista_series.pdf" git add lista_series.pdf

REM Verificar se há mudanças
git diff --cached --quiet
if %errorlevel% == 0 (
    echo Nenhuma mudanca detectada nos arquivos.
    pause
    exit /b 0
)

REM Fazer commit
echo.
echo Fazendo commit...
git commit -m "Atualizar lista de filmes e series - %date% %time%"

REM Push para o GitHub
echo.
echo Enviando para o GitHub...
git push

echo.
echo ========================================
echo Atualizacao concluida!
echo ========================================
echo O site sera atualizado automaticamente no GitHub Pages.
pause

