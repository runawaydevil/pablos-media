#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para listar todas as séries e episódios de um diretório e exportar para PDF e TXT.
"""

import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Formatos de vídeo suportados
FORMATOS_VIDEO = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.ts', '.m2ts'}


def is_arquivo_video(arquivo):
    """Verifica se o arquivo é um vídeo baseado na extensão."""
    return Path(arquivo).suffix.lower() in FORMATOS_VIDEO


def escanear_series(diretorio_base):
    """
    Escaneia o diretório e retorna um dicionário com séries e seus episódios.
    
    Retorna: dict {nome_serie: [lista_episodios]}
    """
    series_por_pasta = defaultdict(list)
    diretorio = Path(diretorio_base)
    
    if not diretorio.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {diretorio_base}")
    
    print(f"Escaneando diretório: {diretorio_base}")
    
    # Percorre todas as pastas no diretório base
    for item in diretorio.iterdir():
        if item.is_dir():
            nome_serie = item.name
            episodios = []
            
            # Procura arquivos de vídeo na pasta
            try:
                for arquivo in item.iterdir():
                    if arquivo.is_file() and is_arquivo_video(arquivo):
                        episodios.append(arquivo.name)
                
                # Se encontrou vídeos, adiciona à lista
                if episodios:
                    series_por_pasta[nome_serie] = sorted(episodios)
                    print(f"  ✓ {nome_serie}: {len(episodios)} episódio(s)")
            
            except PermissionError:
                print(f"  ✗ Erro de permissão ao acessar: {nome_serie}")
            except Exception as e:
                print(f"  ✗ Erro ao processar {nome_serie}: {e}")
    
    return dict(sorted(series_por_pasta.items()))


def exportar_txt(series_por_pasta, arquivo_saida='lista_series.txt'):
    """Exporta a lista de séries para um arquivo TXT."""
    print(f"\nGerando arquivo TXT: {arquivo_saida}")
    
    total_episodios = sum(len(episodios) for episodios in series_por_pasta.values())
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("LISTA DE SÉRIES\n")
        f.write("=" * 80 + "\n")
        f.write(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Total de séries: {len(series_por_pasta)}\n")
        f.write(f"Total de episódios: {total_episodios}\n")
        f.write("=" * 80 + "\n\n")
        
        for indice, (nome_serie, episodios) in enumerate(series_por_pasta.items(), 1):
            f.write(f"{indice}. {nome_serie} ({len(episodios)} episódio(s))\n")
            f.write("-" * 80 + "\n")
            
            for episodio in episodios:
                f.write(f"   • {episodio}\n")
            
            f.write("\n")
        
        f.write("=" * 80 + "\n")
        f.write(f"Total: {len(series_por_pasta)} série(s) | {total_episodios} episódio(s) listado(s)\n")
        f.write("=" * 80 + "\n")
    
    print(f"  ✓ Arquivo TXT criado com sucesso!")


def exportar_pdf(series_por_pasta, arquivo_saida='lista_series.pdf'):
    """Exporta a lista de séries para um arquivo PDF compacto."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        print(f"\nGerando arquivo PDF: {arquivo_saida}")
        
        total_episodios = sum(len(episodios) for episodios in series_por_pasta.values())
        
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
        story.append(Paragraph("LISTA DE SÉRIES", title_style))
        
        # Informações compactas
        info_text = f"{datetime.now().strftime('%d/%m/%Y %H:%M')} | {len(series_por_pasta)} série(s) | {total_episodios} episódio(s)"
        story.append(Paragraph(info_text, info_style))
        story.append(Spacer(1, 0.2*cm))
        
        # Lista de séries compacta
        for indice, (nome_serie, episodios) in enumerate(series_por_pasta.items(), 1):
            # Nome da série - compacto
            serie_text = f"{indice}. {nome_serie} ({len(episodios)} episódio(s))"
            story.append(Paragraph(serie_text, heading_style))
            
            # Episódios - compactos
            for episodio in episodios:
                episodio_text = f"  • {episodio}"
                story.append(Paragraph(episodio_text, normal_style))
        
        # Gerar PDF
        doc.build(story)
        print(f"  ✓ Arquivo PDF criado com sucesso!")
        
    except ImportError:
        print("  ✗ Erro: Biblioteca 'reportlab' não instalada.")
        print("  Execute: pip install reportlab")
        raise


def main():
    """Função principal."""
    diretorio_series = r"Y:\Mídia\TV"
    
    print("=" * 80)
    print("LISTADOR DE SÉRIES")
    print("=" * 80)
    
    try:
        # Escanear séries
        series_por_pasta = escanear_series(diretorio_series)
        
        if not series_por_pasta:
            print("\n⚠ Nenhuma série encontrada no diretório especificado.")
            return
        
        total_episodios = sum(len(episodios) for episodios in series_por_pasta.values())
        print(f"\n✓ Total de séries encontradas: {len(series_por_pasta)}")
        print(f"✓ Total de episódios: {total_episodios}")
        
        # Exportar para TXT
        exportar_txt(series_por_pasta)
        
        # Exportar para PDF
        try:
            exportar_pdf(series_por_pasta)
        except ImportError:
            print("\n⚠ PDF não foi gerado. Instale reportlab para gerar PDFs.")
        
        print("\n" + "=" * 80)
        print("Processo concluído!")
        print("=" * 80)
        
    except FileNotFoundError as e:
        print(f"\n✗ Erro: {e}")
    except Exception as e:
        print(f"\n✗ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

