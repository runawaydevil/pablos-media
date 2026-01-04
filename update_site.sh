#!/bin/bash
# Script para atualizar o site no GitHub com os arquivos gerados
# Execute este script após rodar list_filmes.py e list_series.py

echo "========================================"
echo "Atualizando site no GitHub"
echo "========================================"
echo ""

# Verificar se os arquivos existem
if [ ! -f "lista_filmes.txt" ]; then
    echo "ERRO: lista_filmes.txt não encontrado!"
    echo "Execute: python list_filmes.py"
    exit 1
fi

if [ ! -f "lista_series.txt" ]; then
    echo "ERRO: lista_series.txt não encontrado!"
    echo "Execute: python list_series.py"
    exit 1
fi

echo "Arquivos encontrados:"
[ -f "lista_filmes.txt" ] && echo "  [OK] lista_filmes.txt"
[ -f "lista_series.txt" ] && echo "  [OK] lista_series.txt"
[ -f "lista_filmes.pdf" ] && echo "  [OK] lista_filmes.pdf"
[ -f "lista_series.pdf" ] && echo "  [OK] lista_series.pdf"
echo ""

# Adicionar apenas os arquivos gerados
echo "Adicionando arquivos ao git..."
git add lista_filmes.txt lista_series.txt
[ -f "lista_filmes.pdf" ] && git add lista_filmes.pdf
[ -f "lista_series.pdf" ] && git add lista_series.pdf

# Verificar se há mudanças
if git diff --cached --quiet; then
    echo "Nenhuma mudança detectada nos arquivos."
    exit 0
fi

# Fazer commit
echo ""
echo "Fazendo commit..."
git commit -m "Atualizar lista de filmes e séries - $(date '+%Y-%m-%d %H:%M:%S')"

# Push para o GitHub
echo ""
echo "Enviando para o GitHub..."
git push

echo ""
echo "========================================"
echo "Atualização concluída!"
echo "========================================"
echo "O site será atualizado automaticamente no GitHub Pages."

