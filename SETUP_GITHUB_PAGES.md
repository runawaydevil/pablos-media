# Configuração do GitHub Pages - Passo a Passo

## ⚠️ IMPORTANTE: Siga estes passos na ordem!

### Passo 1: Fazer Push do Workflow

Primeiro, certifique-se de que o workflow foi enviado para o GitHub:

```bash
git add .github/workflows/deploy.yml
git commit -m "Adicionar workflow de deploy"
git push
```

### Passo 2: Configurar GitHub Pages

1. Acesse seu repositório no GitHub: `https://github.com/runawaydevil/pablos-media`
2. Vá em **Settings** (Configurações)
3. No menu lateral, clique em **Pages**
4. Em **Source** (Fonte), selecione: **GitHub Actions** (NÃO selecione "Deploy from a branch")
5. Clique em **Save** (Salvar)

### Passo 3: Executar o Workflow pela Primeira Vez

1. Vá na aba **Actions** do repositório
2. Você verá o workflow "Deploy GitHub Pages"
3. Clique nele
4. Clique no botão **Run workflow** (Executar workflow)
5. Selecione a branch **main**
6. Clique em **Run workflow**

### Passo 4: Aguardar o Deploy

- O workflow levará alguns minutos para executar
- Você pode acompanhar o progresso na aba **Actions**
- Quando estiver completo, você verá um check verde ✓

### Passo 5: Verificar o Site

Após o deploy completo (pode levar 1-2 minutos após o workflow terminar):
- Acesse: `https://runawaydevil.github.io/pablos-media/`
- O site deve estar funcionando!

## 🔄 Atualizações Futuras

Após a configuração inicial, o workflow será executado automaticamente sempre que você:
- Fizer push de arquivos TXT/PDF atualizados
- Fazer push de mudanças nos arquivos HTML/CSS/JS

## ❌ Problemas Comuns

### Erro 404 ainda aparece

1. Verifique se o workflow foi executado com sucesso (Actions > Deploy GitHub Pages)
2. Verifique se o GitHub Pages está configurado para usar **GitHub Actions** (não branch)
3. Aguarde alguns minutos - o deploy pode levar tempo para propagar
4. Tente limpar o cache do navegador (Ctrl+F5)

### Workflow não está executando

1. Verifique se o arquivo `.github/workflows/deploy.yml` está no repositório
2. Vá em Actions e execute manualmente via "Run workflow"
3. Verifique se há erros no log do workflow

### Site não atualiza após push

1. Verifique se os arquivos TXT/PDF foram realmente commitados e enviados
2. Verifique o log do workflow em Actions para ver se houve erros
3. O workflow pode levar alguns minutos para executar

## 📞 Precisa de Ajuda?

Se ainda tiver problemas:
1. Verifique os logs do workflow em **Actions**
2. Verifique se todos os arquivos necessários estão no repositório
3. Certifique-se de que o GitHub Pages está configurado corretamente

