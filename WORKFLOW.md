# Workflow de Atualização

## Processo Completo

### 1. Executar Scripts Localmente

Execute os scripts Python na sua máquina local para gerar os arquivos:

```bash
python list_filmes.py
python list_series.py
```

Isso irá gerar:
- `lista_filmes.txt`
- `lista_filmes.pdf`
- `lista_series.txt`
- `lista_series.pdf`

### 2. Atualizar o Site no GitHub

#### Windows:
```bash
update_site.bat
```

#### Linux/Mac:
```bash
chmod +x update_site.sh
./update_site.sh
```

#### Manualmente:
```bash
git add lista_filmes.txt lista_series.txt lista_filmes.pdf lista_series.pdf
git commit -m "Atualizar lista de filmes e séries"
git push
```

### 3. Verificar

O GitHub Pages atualizará automaticamente em alguns minutos. Acesse:
**https://runawaydevil.github.io/pablos-media/**

## Importante

- ✅ Os scripts Python **NÃO** vão para o GitHub (só rodam localmente)
- ✅ Apenas os arquivos TXT e PDF são enviados
- ✅ O site lê os arquivos TXT automaticamente
- ✅ Os PDFs ficam disponíveis para download

## Estrutura no GitHub

```
pablos-media/
├── index.html
├── filmes.html
├── series.html
├── style.css
├── script.js
├── lista_filmes.txt    ← Gerado localmente, enviado para GitHub
├── lista_series.txt    ← Gerado localmente, enviado para GitHub
├── lista_filmes.pdf    ← Gerado localmente, enviado para GitHub
├── lista_series.pdf    ← Gerado localmente, enviado para GitHub
└── README.md
```

