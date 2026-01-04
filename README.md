# Filmes e Séries do Pablo

Repositório contendo scripts Python para listar filmes e séries, além de um site web estático hospedado no GitHub Pages.

## 🌐 Site Web

O site está disponível em: **https://runawaydevil.github.io/pablos-media/**

O site exibe automaticamente os filmes e séries lendo os arquivos TXT gerados pelos scripts Python. Possui:
- Página inicial com navegação
- Página de filmes com lista completa
- Página de séries com lista completa e contagem de episódios
- Design moderno e responsivo
- Links para download dos PDFs

### Atualizar o Site

**Workflow:** Os scripts Python rodam localmente, apenas os resultados (TXT e PDF) são enviados para o GitHub.

#### Opção 1: Usando o script automatizado (Windows)
```bash
# 1. Execute os scripts Python localmente
python list_filmes.py
python list_series.py

# 2. Execute o script de atualização
update_site.bat
```

#### Opção 2: Usando o script automatizado (Linux/Mac)
```bash
# 1. Execute os scripts Python localmente
python list_filmes.py
python list_series.py

# 2. Execute o script de atualização
chmod +x update_site.sh
./update_site.sh
```

#### Opção 3: Manualmente
```bash
# 1. Execute os scripts Python localmente
python list_filmes.py
python list_series.py

# 2. Adicione apenas os arquivos gerados
git add lista_filmes.txt lista_series.txt
git add lista_filmes.pdf lista_series.pdf  # se existirem

# 3. Commit e push
git commit -m "Atualizar lista de filmes e séries"
git push
```

O GitHub Pages atualizará automaticamente o site após o push.

## 📝 Scripts Python

Scripts Python para listar filmes e séries de diretórios, encontrar duplicados e exportar para arquivos PDF e TXT.

## Requisitos

- Python 3.6 ou superior
- Biblioteca `reportlab` (para geração de PDF)

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Listar Filmes

Execute o script:
```bash
python list_filmes.py
```

O script irá:
1. Escanear o diretório `Y:\Mídia\Filmes`
2. Identificar todos os arquivos de vídeo em cada pasta
3. Gerar `lista_filmes.txt` com a lista formatada
4. Gerar `lista_filmes.pdf` com a lista formatada em PDF (compacto)

### Listar Séries

Execute o script:
```bash
python list_series.py
```

O script irá:
1. Escanear o diretório `Y:\Mídia\TV`
2. Identificar todos os episódios (arquivos de vídeo) em cada pasta de série
3. Gerar `lista_series.txt` com a lista formatada
4. Gerar `lista_series.pdf` com a lista formatada em PDF (compacto)

### Encontrar Arquivos Duplicados

Execute o script:
```bash
python find_duplicados.py
```

O script irá:
1. Escanear os diretórios `Y:\Mídia\Filmes` e `Y:\Mídia\TV`
2. Identificar arquivos duplicados por **nome** (mesmo nome de arquivo)
3. Identificar arquivos duplicados por **conteúdo** (mesmo hash MD5)
4. Calcular o espaço desperdiçado por duplicatas
5. Gerar `lista_duplicados.txt` com relatório detalhado
6. Gerar `lista_duplicados.csv` com dados estruturados (caminhos completos, tamanhos, etc.)
7. Gerar `lista_duplicados.pdf` com relatório em PDF (compacto)

**Nota:** O cálculo de hash MD5 pode levar alguns minutos dependendo da quantidade de arquivos. O script mostra o progresso durante o processamento.

**CSV:** O arquivo CSV contém todas as informações dos duplicados em formato tabular, incluindo:
- Tipo de duplicado (por nome ou por conteúdo)
- Grupo de duplicados
- Nome do arquivo
- Caminho completo
- Pasta
- Tamanho em bytes e formatado
- Hash MD5 (para duplicados por conteúdo)
- Total de cópias no grupo

## Formatos de Vídeo Suportados

Os scripts identificam uma ampla gama de formatos de vídeo, incluindo:

**Formatos Comuns:**
- MPEG: `.mp4`, `.m4v`, `.mpg`, `.mpeg`, `.m1v`, `.m2v`, `.mpv`, `.mpv2`, `.mp4v`
- AVI/DivX: `.avi`, `.divx`, `.xvid`
- Matroska: `.mkv`, `.mk3d`, `.mka`
- QuickTime: `.mov`, `.qt`
- Windows Media: `.wmv`, `.wmvhd`, `.asf`
- Flash: `.flv`, `.f4v`, `.swf`
- Web: `.webm`, `.ogv`, `.ogm`

**Formatos de Transmissão/Streaming:**
- `.ts`, `.m2ts`, `.mts`, `.trp`, `.tp`

**Formatos de Disco:**
- `.vob`, `.vro`, `.dat`, `.bik`, `.smk`

**Formatos de Gravação:**
- `.dvr-ms`, `.wtv`, `.pvr`

**Formatos de Celular:**
- `.3gp`, `.3g2`, `.amv`, `.dmv`

**Formatos de Codec Específicos:**
- `.h264`, `.h265`, `.hevc`, `.264`, `.265`, `.avc`, `.vc1`, `.vp8`, `.vp9`, `.av1`

**Outros Formatos:**
- RealMedia: `.rm`, `.rmvb`, `.ra`, `.ram`, `.rv`
- Microsoft: `.mxf`, `.wv`
- Vídeo bruto: `.yuv`, `.y4m`, `.raw`, `.ycbcr`, `.rgb`, `.rgba`
- Container: `.nut`
- Diversos: `.nsv`, `.roq`, `.svi`, `.uvu`, `.viv`, `.xesc`, `.gifv`

**Total:** Mais de 70 formatos de vídeo suportados!

## Estrutura de Saída

### Filmes
A lista é organizada por pasta (nome do filme), mostrando:
- Número sequencial
- Nome da pasta (nome do filme)
- Arquivos de vídeo dentro de cada pasta

### Séries
A lista é organizada por pasta (nome da série), mostrando:
- Número sequencial
- Nome da pasta (nome da série) e quantidade de episódios
- Lista de episódios (arquivos de vídeo) dentro de cada pasta

## 📁 Estrutura do Projeto

```
.
├── index.html          # Página inicial do site
├── filmes.html         # Página de filmes
├── series.html         # Página de séries
├── style.css           # Estilos do site
├── script.js           # JavaScript para processar TXT
├── list_filmes.py      # Script para listar filmes (roda localmente)
├── list_series.py      # Script para listar séries (roda localmente)
├── find_duplicados.py  # Script para encontrar arquivos duplicados (roda localmente)
├── update_site.bat     # Script para atualizar site (Windows)
├── update_site.sh      # Script para atualizar site (Linux/Mac)
├── requirements.txt    # Dependências Python
└── README.md          # Este arquivo
```

## 🚀 Configuração do GitHub Pages

**⚠️ IMPORTANTE:** Se você está vendo erro 404, siga o guia completo: **[SETUP_GITHUB_PAGES.md](SETUP_GITHUB_PAGES.md)**

### Passos Rápidos:

1. **Configurar GitHub Pages:**
   - Vá em **Settings** > **Pages** no repositório
   - Selecione **GitHub Actions** como source (NÃO "Deploy from a branch")
   - Salve

2. **Executar o Workflow:**
   - Vá em **Actions** > **Deploy GitHub Pages**
   - Clique em **Run workflow** > **Run workflow**
   - Aguarde o deploy completar (alguns minutos)

3. **Acessar o site:**
   - `https://runawaydevil.github.io/pablos-media/`

### GitHub Actions

O workflow `.github/workflows/deploy.yml` está configurado para:
- Disparar automaticamente em qualquer push para a branch main
- Validar que todos os arquivos necessários existem
- Fazer deploy automático para o GitHub Pages
- Pode ser executado manualmente via **Actions** > **Deploy GitHub Pages** > **Run workflow**

## 📝 Notas

- **Scripts rodam localmente**: Os scripts Python (`list_filmes.py`, `list_series.py` e `find_duplicados.py`) devem ser executados na sua máquina local
- **Apenas resultados no GitHub**: Apenas os arquivos TXT e PDF gerados são enviados para o repositório
- Os scripts usam o nome da pasta como nome do filme/série
- Apenas arquivos de vídeo são listados (legendas e outros arquivos são ignorados)
- Os scripts tratam erros de permissão e acesso a diretórios de rede
- Os PDFs são gerados em formato compacto para economizar espaço
- O site lê os arquivos TXT via JavaScript (fetch API)
- Os arquivos TXT e PDF devem estar no repositório para o site funcionar
- O script `find_duplicados.py` detecta duplicados por nome e por conteúdo (hash MD5), calculando também o espaço desperdiçado

