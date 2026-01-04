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

Scripts Python para listar filmes e séries de diretórios e exportar para arquivos PDF e TXT.

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

## Formatos de Vídeo Suportados

Os scripts identificam os seguintes formatos:
- .mp4, .mkv, .avi, .mov, .wmv, .flv, .webm, .m4v
- .mpg, .mpeg, .3gp, .ts, .m2ts

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

- **Scripts rodam localmente**: Os scripts Python (`list_filmes.py` e `list_series.py`) devem ser executados na sua máquina local
- **Apenas resultados no GitHub**: Apenas os arquivos TXT e PDF gerados são enviados para o repositório
- Os scripts usam o nome da pasta como nome do filme/série
- Apenas arquivos de vídeo são listados (legendas e outros arquivos são ignorados)
- Os scripts tratam erros de permissão e acesso a diretórios de rede
- Os PDFs são gerados em formato compacto para economizar espaço
- O site lê os arquivos TXT via JavaScript (fetch API)
- Os arquivos TXT e PDF devem estar no repositório para o site funcionar

