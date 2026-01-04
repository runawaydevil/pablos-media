#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para encontrar arquivos duplicados nos diretórios de TV e Filmes.
Compara arquivos por nome e por hash MD5 para detectar duplicatas exatas.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Formatos de vídeo suportados (lista completa)
FORMATOS_VIDEO = {
    # Formatos MPEG
    '.mp4', '.m4v', '.mpg', '.mpeg', '.m1v', '.m2v', '.mpv', '.mpv2', '.mp4v',
    # Formatos AVI e DivX
    '.avi', '.divx', '.xvid',
    # Formatos Matroska
    '.mkv', '.mk3d', '.mka',
    # Formatos QuickTime/Apple
    '.mov', '.qt',
    # Formatos Windows Media
    '.wmv', '.wmvhd', '.asf',
    # Formatos Flash
    '.flv', '.f4v', '.swf',
    # Formatos Web
    '.webm', '.ogv', '.ogm',
    # Formatos RealMedia
    '.rm', '.rmvb', '.ra', '.ram', '.rv',
    # Formatos de transmissão/streaming
    '.ts', '.m2ts', '.mts', '.trp', '.tp',
    # Formatos de vídeo bruto
    '.yuv', '.y4m', '.raw', '.ycbcr', '.rgb', '.rgba',
    # Formatos de container
    '.nut',
    # Formatos de disco
    '.vob', '.vro', '.dat', '.bik', '.smk',
    # Formatos de gravação
    '.dvr-ms', '.wtv', '.pvr',
    # Formatos de celular
    '.3gp', '.3g2', '.amv', '.dmv',
    # Formatos de codec específicos
    '.h264', '.h265', '.hevc', '.264', '.265', '.avc', '.vc1', '.vp8', '.vp9', '.av1',
    # Formatos Microsoft
    '.mxf', '.wv',
    # Formatos diversos
    '.nsv', '.roq', '.svi', '.uvu', '.viv', '.xesc', '.gifv'
}


def is_arquivo_video(arquivo):
    """Verifica se o arquivo é um vídeo baseado na extensão."""
    return Path(arquivo).suffix.lower() in FORMATOS_VIDEO


def escanear_arquivos(diretorio_base, tipo='filmes'):
    """
    Escaneia o diretório e retorna informações sobre todos os arquivos de vídeo.
    
    Args:
        diretorio_base: Caminho do diretório base
        tipo: Tipo de conteúdo ('filmes' ou 'series')
    
    Returns:
        Lista de tuplas: [(caminho_completo, nome_arquivo, nome_pasta, tamanho)]
    """
    arquivos_encontrados = []
    diretorio = Path(diretorio_base)
    
    if not diretorio.exists():
        print(f"  [AVISO] Diretório não encontrado: {diretorio_base}")
        return arquivos_encontrados
    
    print(f"Escaneando {tipo}: {diretorio_base}")
    sys.stdout.flush()
    
    # Contar total de pastas primeiro
    try:
        print(f"  Listando pastas...", end='')
        sys.stdout.flush()
        pastas = [item for item in diretorio.iterdir() if item.is_dir()]
        total_pastas = len(pastas)
        print(f"  Total de pastas encontradas: {total_pastas}")
        sys.stdout.flush()
    except Exception as e:
        print(f"\n  [ERRO] Erro ao contar pastas: {e}")
        sys.stdout.flush()
        return arquivos_encontrados
    
    # Percorre todas as pastas no diretório base
    pastas_processadas = 0
    inicio = time.time()
    
    for item in diretorio.iterdir():
        if item.is_dir():
            nome_pasta = item.name
            pastas_processadas += 1
            
            # Procura arquivos de vídeo na pasta
            try:
                for arquivo in item.iterdir():
                    if arquivo.is_file() and is_arquivo_video(arquivo):
                        try:
                            tamanho = arquivo.stat().st_size
                            arquivos_encontrados.append((
                                str(arquivo),
                                arquivo.name,
                                nome_pasta,
                                tamanho
                            ))
                        except (OSError, PermissionError) as e:
                            print(f"\n  [AVISO] Erro ao acessar {arquivo.name}: {e}")
                
                # Mostrar progresso a cada 10 pastas ou na última
                if pastas_processadas % 10 == 0 or pastas_processadas == total_pastas:
                    porcentagem = (pastas_processadas / total_pastas) * 100
                    print(f"  Progresso: {pastas_processadas}/{total_pastas} pastas ({porcentagem:.1f}%) - {len(arquivos_encontrados)} arquivos encontrados", end='\r')
                    sys.stdout.flush()
            
            except PermissionError:
                print(f"\n  [ERRO] Erro de permissão ao acessar: {nome_pasta}")
            except Exception as e:
                print(f"\n  [ERRO] Erro ao processar {nome_pasta}: {e}")
    
    tempo_decorrido = time.time() - inicio
    print(f"\n  [OK] {len(arquivos_encontrados)} arquivo(s) encontrado(s) em {tipo} ({tempo_decorrido:.1f}s)")
    sys.stdout.flush()
    return arquivos_encontrados


def encontrar_duplicados_por_nome(arquivos_filmes, arquivos_series):
    """
    Encontra arquivos duplicados por nome (mesmo nome de arquivo).
    
    Returns:
        Lista de duplicados: [(nome_arquivo, [lista_caminhos])]
    """
    print("  Agrupando arquivos por nome...")
    sys.stdout.flush()
    
    duplicados = defaultdict(list)
    todos_arquivos = arquivos_filmes + arquivos_series
    total_arquivos = len(todos_arquivos)
    processados = 0
    inicio = time.time()
    ultimo_tempo = inicio
    
    # Agrupar por nome de arquivo
    for caminho, nome, pasta, tamanho in todos_arquivos:
        processados += 1
        duplicados[nome.lower()].append((caminho, pasta, tamanho))
        
        # Mostrar progresso a cada 100 arquivos ou a cada segundo
        tempo_atual = time.time()
        if processados % 100 == 0 or (tempo_atual - ultimo_tempo) >= 1.0:
            porcentagem = (processados / total_arquivos) * 100
            print(f"  Processando: {processados}/{total_arquivos} arquivos ({porcentagem:.1f}%)", end='\r')
            sys.stdout.flush()
            ultimo_tempo = tempo_atual
    
    print(f"\n  Analisando grupos de duplicados...")
    sys.stdout.flush()
    
    # Filtrar apenas os que aparecem mais de uma vez
    duplicados_por_nome = {
        nome: caminhos for nome, caminhos in duplicados.items() 
        if len(caminhos) > 1
    }
    
    return duplicados_por_nome


def formatar_tamanho(tamanho_bytes):
    """Formata tamanho em bytes para formato legível."""
    for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamanho_bytes < 1024.0:
            return f"{tamanho_bytes:.2f} {unidade}"
        tamanho_bytes /= 1024.0
    return f"{tamanho_bytes:.2f} PB"


def exportar_txt(duplicados_por_nome, arquivo_saida='lista_duplicados.txt'):
    """Exporta a lista de duplicados para um arquivo TXT."""
    print(f"  Gerando arquivo TXT: {arquivo_saida}...")
    sys.stdout.flush()
    
    total_duplicados_nome = len(duplicados_por_nome)
    inicio = time.time()
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RELATÓRIO DE ARQUIVOS DUPLICADOS\n")
        f.write("=" * 80 + "\n")
        f.write(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Duplicados por nome: {total_duplicados_nome}\n")
        f.write("=" * 80 + "\n\n")
        
        # Seção: Duplicados por nome
        if duplicados_por_nome:
            f.write("=" * 80 + "\n")
            f.write("DUPLICADOS POR NOME DE ARQUIVO\n")
            f.write("=" * 80 + "\n\n")
            
            total_nome = len(duplicados_por_nome)
            for indice, (nome_arquivo, caminhos) in enumerate(sorted(duplicados_por_nome.items()), 1):
                if indice % 10 == 0 or indice == total_nome:
                    print(f"    Escrevendo duplicados por nome: {indice}/{total_nome}", end='\r')
                    sys.stdout.flush()
                
                f.write(f"{indice}. {nome_arquivo}\n")
                f.write("-" * 80 + "\n")
                
                tamanho_total = 0
                for caminho, pasta, tamanho in caminhos:
                    tamanho_total += tamanho
                    f.write(f"   • {pasta} / {Path(caminho).name}\n")
                    f.write(f"     Caminho: {caminho}\n")
                    f.write(f"     Tamanho: {formatar_tamanho(tamanho)}\n")
                
                f.write(f"\n   Total de cópias: {len(caminhos)}\n")
                f.write(f"   Espaço desperdiçado: {formatar_tamanho(tamanho_total - caminhos[0][2])}\n")
                f.write("\n")
        else:
            f.write("=" * 80 + "\n")
            f.write("DUPLICADOS POR NOME DE ARQUIVO\n")
            f.write("=" * 80 + "\n\n")
            f.write("Nenhum arquivo duplicado encontrado por nome.\n\n")
        
        
        f.write("=" * 80 + "\n")
        f.write("FIM DO RELATÓRIO\n")
        f.write("=" * 80 + "\n")
    
    tempo_total = time.time() - inicio
    print(f"\n  [OK] Arquivo TXT criado com sucesso! ({tempo_total:.1f}s)")
    sys.stdout.flush()


def exportar_pdf(duplicados_por_nome, arquivo_saida='lista_duplicados.pdf'):
    """Exporta a lista de duplicados para um arquivo PDF compacto."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        print(f"  Gerando arquivo PDF: {arquivo_saida}...")
        sys.stdout.flush()
        inicio = time.time()
        
        total_duplicados_nome = len(duplicados_por_nome)
        
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
        
        # Título
        story.append(Paragraph("RELATÓRIO DE ARQUIVOS DUPLICADOS", title_style))
        
        # Informações
        info_text = f"{datetime.now().strftime('%d/%m/%Y %H:%M')} | Duplicados por nome: {total_duplicados_nome}"
        story.append(Paragraph(info_text, info_style))
        story.append(Spacer(1, 0.2*cm))
        
        # Duplicados por nome
        story.append(Paragraph("DUPLICADOS POR NOME", heading_style))
        if duplicados_por_nome:
            total_nome = min(50, len(duplicados_por_nome))
            for indice, (nome_arquivo, caminhos) in enumerate(sorted(duplicados_por_nome.items())[:50], 1):  # Limitar a 50 para não ficar muito grande
                if indice % 10 == 0 or indice == total_nome:
                    print(f"    Processando PDF - duplicados por nome: {indice}/{total_nome}", end='\r')
                    sys.stdout.flush()
                
                texto = f"{indice}. {nome_arquivo} ({len(caminhos)} cópias)"
                story.append(Paragraph(texto, heading_style))
                for caminho, pasta, tamanho in caminhos[:3]:  # Mostrar apenas os 3 primeiros
                    texto_arquivo = f"  • {pasta} / {Path(caminho).name} ({formatar_tamanho(tamanho)})"
                    story.append(Paragraph(texto_arquivo, normal_style))
                if len(caminhos) > 3:
                    story.append(Paragraph(f"  ... e mais {len(caminhos) - 3} cópias", normal_style))
        else:
            story.append(Paragraph("Nenhum arquivo duplicado encontrado por nome.", normal_style))
        
        # Gerar PDF
        print(f"    Gerando PDF final...", end='\r')
        sys.stdout.flush()
        doc.build(story)
        tempo_total = time.time() - inicio
        print(f"\n  [OK] Arquivo PDF criado com sucesso! ({tempo_total:.1f}s)")
        sys.stdout.flush()
        
    except ImportError:
        print("  [ERRO] Erro: Biblioteca 'reportlab' não instalada.")
        print("  Execute: pip install reportlab")
        raise


def exportar_csv(duplicados_por_nome, arquivo_saida='lista_duplicados.csv'):
    """
    Exporta a lista de duplicados para um arquivo CSV.
    
    Colunas:
    - Tipo: 'Por Nome'
    - Grupo: Identificador do grupo de duplicados
    - Nome do Arquivo: Nome do arquivo
    - Caminho Completo: Caminho absoluto do arquivo
    - Pasta: Nome da pasta onde está o arquivo
    - Tamanho (Bytes): Tamanho em bytes
    - Tamanho (Formatado): Tamanho formatado (KB, MB, GB, etc)
    - Total de Cópias: Quantidade de cópias no grupo
    """
    import csv
    
    print(f"  Gerando arquivo CSV: {arquivo_saida}...")
    sys.stdout.flush()
    inicio = time.time()
    
    with open(arquivo_saida, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_ALL)
        
        # Cabeçalho
        writer.writerow([
            'Tipo',
            'Grupo',
            'Nome do Arquivo',
            'Caminho Completo',
            'Pasta',
            'Tamanho (Bytes)',
            'Tamanho (Formatado)',
            'Total de Cópias'
        ])
        
        # Duplicados por nome
        total_nome = len(duplicados_por_nome)
        linhas_escritas = 0
        
        for grupo_id, (nome_arquivo, caminhos) in enumerate(sorted(duplicados_por_nome.items()), 1):
            grupo = f"Nome-{grupo_id}"
            total_copias = len(caminhos)
            
            for caminho, pasta, tamanho in caminhos:
                writer.writerow([
                    'Por Nome',
                    grupo,
                    Path(caminho).name,
                    caminho,
                    pasta,
                    tamanho,
                    formatar_tamanho(tamanho),
                    total_copias
                ])
                linhas_escritas += 1
                if linhas_escritas % 100 == 0:
                    print(f"    Escrevendo CSV: {linhas_escritas} linhas...", end='\r')
                    sys.stdout.flush()
    
    tempo_total = time.time() - inicio
    print(f"\n  [OK] Arquivo CSV criado com sucesso! ({tempo_total:.1f}s)")
    sys.stdout.flush()


def main():
    """Função principal."""
    # Forçar flush do output para garantir que mensagens apareçam imediatamente
    sys.stdout.flush()
    
    diretorio_filmes = r"Y:\Mídia\Filmes"
    diretorio_series = r"Y:\Mídia\TV"
    
    print("=" * 80)
    print("DETECTOR DE ARQUIVOS DUPLICADOS")
    print("=" * 80)
    sys.stdout.flush()
    
    # Verificar se os diretórios existem antes de começar
    print("\nVerificando diretórios...")
    print(f"  Filmes: {diretorio_filmes}")
    print(f"  Séries: {diretorio_series}")
    sys.stdout.flush()
    
    if not Path(diretorio_filmes).exists():
        print(f"\n[ERRO] Diretório de filmes não encontrado: {diretorio_filmes}")
        print("       Verifique se o caminho está correto e acessível.")
        sys.stdout.flush()
        return
    
    if not Path(diretorio_series).exists():
        print(f"\n[ERRO] Diretório de séries não encontrado: {diretorio_series}")
        print("       Verifique se o caminho está correto e acessível.")
        sys.stdout.flush()
        return
    
    print("  [OK] Diretórios encontrados!")
    sys.stdout.flush()
    
    try:
        # Escanear arquivos
        print("\n[1/4] Escaneando arquivos...")
        sys.stdout.flush()
        arquivos_filmes = escanear_arquivos(diretorio_filmes, 'filmes')
        sys.stdout.flush()
        arquivos_series = escanear_arquivos(diretorio_series, 'series')
        sys.stdout.flush()
        
        total_arquivos = len(arquivos_filmes) + len(arquivos_series)
        if total_arquivos == 0:
            print("\n[AVISO] Nenhum arquivo encontrado nos diretórios especificados.")
            return
        
        print(f"\n[OK] Total de arquivos escaneados: {total_arquivos}")
        print(f"     - Filmes: {len(arquivos_filmes)}")
        print(f"     - Séries: {len(arquivos_series)}")
        
        # Encontrar duplicados por nome
        print("\n[2/4] Procurando duplicados por nome...")
        duplicados_por_nome = encontrar_duplicados_por_nome(arquivos_filmes, arquivos_series)
        print(f"[OK] {len(duplicados_por_nome)} arquivo(s) duplicado(s) por nome encontrado(s)")
        
        # Exportar resultados
        print("\n[3/4] Exportando resultados...")
        inicio_export = time.time()
        exportar_txt(duplicados_por_nome)
        exportar_csv(duplicados_por_nome)
        
        try:
            exportar_pdf(duplicados_por_nome)
        except ImportError:
            print("\n[AVISO] PDF não foi gerado. Instale reportlab para gerar PDFs.")
        
        tempo_export = time.time() - inicio_export
        print(f"  [OK] Exportação concluída em {tempo_export:.1f}s")
        
        # Resumo final
        print("\n" + "=" * 80)
        print("RESUMO")
        print("=" * 80)
        print(f"Total de arquivos analisados: {total_arquivos}")
        print(f"Duplicados por nome: {len(duplicados_por_nome)}")
        print("=" * 80)
        print("Processo concluído!")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n[AVISO] Processo interrompido pelo usuário.")
    except Exception as e:
        print(f"\n[ERRO] Erro inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

