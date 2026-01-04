#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para listar todos os filmes de um diretório e exportar para PDF e TXT.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Formatos de vídeo suportados
FORMATOS_VIDEO = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.ts', '.m2ts'}


def is_arquivo_video(arquivo):
    """Verifica se o arquivo é um vídeo baseado na extensão."""
    return Path(arquivo).suffix.lower() in FORMATOS_VIDEO


def escanear_filmes(diretorio_base):
    """
    Escaneia o diretório e retorna um dicionário com pastas e seus filmes.
    
    Retorna: dict {nome_pasta: [lista_arquivos_video]}
    """
    filmes_por_pasta = defaultdict(list)
    diretorio = Path(diretorio_base)
    
    if not diretorio.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {diretorio_base}")
    
    print(f"Escaneando diretório: {diretorio_base}")
    
    # Percorre todas as pastas no diretório base
    for item in diretorio.iterdir():
        if item.is_dir():
            nome_pasta = item.name
            arquivos_video = []
            
            # Procura arquivos de vídeo na pasta
            try:
                for arquivo in item.iterdir():
                    if arquivo.is_file() and is_arquivo_video(arquivo):
                        arquivos_video.append(arquivo.name)
                
                # Se encontrou vídeos, adiciona à lista
                if arquivos_video:
                    filmes_por_pasta[nome_pasta] = sorted(arquivos_video)
                    print(f"  [OK] {nome_pasta}: {len(arquivos_video)} arquivo(s) de video")
            
            except PermissionError:
                print(f"  [ERRO] Erro de permissao ao acessar: {nome_pasta}")
            except Exception as e:
                print(f"  [ERRO] Erro ao processar {nome_pasta}: {e}")
    
    return dict(sorted(filmes_por_pasta.items()))


def exportar_txt(filmes_por_pasta, arquivo_saida='lista_filmes.txt'):
    """Exporta a lista de filmes para um arquivo TXT."""
    print(f"\nGerando arquivo TXT: {arquivo_saida}")
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("LISTA DE FILMES\n")
        f.write("=" * 80 + "\n")
        f.write(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Total de filmes: {len(filmes_por_pasta)}\n")
        f.write("=" * 80 + "\n\n")
        
        for indice, (nome_pasta, arquivos) in enumerate(filmes_por_pasta.items(), 1):
            f.write(f"{indice}. {nome_pasta}\n")
            f.write("-" * 80 + "\n")
            
            for arquivo in arquivos:
                f.write(f"   • {arquivo}\n")
            
            f.write("\n")
        
        f.write("=" * 80 + "\n")
        f.write(f"Total: {len(filmes_por_pasta)} filme(s) listado(s)\n")
        f.write("=" * 80 + "\n")
    
    print(f"  [OK] Arquivo TXT criado com sucesso!")


def exportar_pdf(filmes_por_pasta, arquivo_saida='lista_filmes.pdf'):
    """Exporta a lista de filmes para um arquivo PDF compacto."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        print(f"\nGerando arquivo PDF: {arquivo_saida}")
        
        # Criar documento PDF com margens reduzidas
        doc = SimpleDocTemplate(
            arquivo_saida,
            pagesize=A4,
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1*cm,
            bottomMargin=1*cm
        )
        
        # Estilos compactos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=12,
            textColor='#1a1a1a',
            spaceAfter=8,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Normal'],
            fontSize=9,
            textColor='#2c3e50',
            spaceAfter=2,
            spaceBefore=4,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=7,
            textColor='#34495e',
            spaceAfter=1,
            leftIndent=10
        )
        
        info_style = ParagraphStyle(
            'CustomInfo',
            parent=styles['Normal'],
            fontSize=7,
            textColor='#7f8c8d',
            alignment=TA_CENTER,
            spaceAfter=6
        )
        
        # Conteúdo do PDF
        story = []
        
        # Título compacto
        story.append(Paragraph("LISTA DE FILMES", title_style))
        
        # Informações compactas
        info_text = f"{datetime.now().strftime('%d/%m/%Y %H:%M')} | Total: {len(filmes_por_pasta)} filme(s)"
        story.append(Paragraph(info_text, info_style))
        story.append(Spacer(1, 0.2*cm))
        
        # Lista de filmes compacta
        for indice, (nome_pasta, arquivos) in enumerate(filmes_por_pasta.items(), 1):
            # Nome do filme (pasta) - compacto
            filme_text = f"{indice}. {nome_pasta}"
            story.append(Paragraph(filme_text, heading_style))
            
            # Arquivos de vídeo - compactos
            for arquivo in arquivos:
                arquivo_text = f"  • {arquivo}"
                story.append(Paragraph(arquivo_text, normal_style))
        
        # Gerar PDF
        doc.build(story)
        print(f"  [OK] Arquivo PDF criado com sucesso!")
        
    except ImportError:
        print("  [ERRO] Erro: Biblioteca 'reportlab' nao instalada.")
        print("  Execute: pip install reportlab")
        raise


def main():
    """Função principal."""
    diretorio_filmes = r"Y:\Mídia\Filmes"
    
    print("=" * 80)
    print("LISTADOR DE FILMES")
    print("=" * 80)
    
    try:
        # Escanear filmes
        filmes_por_pasta = escanear_filmes(diretorio_filmes)
        
        if not filmes_por_pasta:
            print("\n[AVISO] Nenhum filme encontrado no diretorio especificado.")
            return
        
        print(f"\n[OK] Total de filmes encontrados: {len(filmes_por_pasta)}")
        
        # Exportar para TXT
        exportar_txt(filmes_por_pasta)
        
        # Exportar para PDF
        try:
            exportar_pdf(filmes_por_pasta)
        except ImportError:
            print("\n[AVISO] PDF nao foi gerado. Instale reportlab para gerar PDFs.")
        
        print("\n" + "=" * 80)
        print("Processo concluído!")
        print("=" * 80)
        
    except FileNotFoundError as e:
        print(f"\n[ERRO] Erro: {e}")
    except Exception as e:
        print(f"\n[ERRO] Erro inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

