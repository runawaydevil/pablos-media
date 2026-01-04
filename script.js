/**
 * Funções para carregar e processar arquivos TXT de filmes e séries
 */

/**
 * Carrega e exibe a lista de filmes
 */
async function loadFilmes() {
    const container = document.getElementById('filmes-container');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const stats = document.getElementById('stats');
    const totalFilmes = document.getElementById('total-filmes');

    try {
        // Carregar arquivo TXT
        const response = await fetch('lista_filmes.txt');
        if (!response.ok) {
            throw new Error('Arquivo não encontrado');
        }

        const text = await response.text();
        const filmes = parseFilmesTxt(text);

        // Esconder loading
        loading.style.display = 'none';

        if (filmes.length === 0) {
            error.style.display = 'block';
            error.innerHTML = '<p>Nenhum filme encontrado no arquivo.</p>';
            return;
        }

        // Exibir filmes
        container.innerHTML = '';
        filmes.forEach((filme, index) => {
            const filmeDiv = createFilmeElement(filme, index + 1);
            container.appendChild(filmeDiv);
        });

        // Atualizar estatísticas
        totalFilmes.textContent = filmes.length;
        stats.style.display = 'block';

    } catch (err) {
        loading.style.display = 'none';
        error.style.display = 'block';
        console.error('Erro ao carregar filmes:', err);
    }
}

/**
 * Carrega e exibe a lista de séries
 */
async function loadSeries() {
    const container = document.getElementById('series-container');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const stats = document.getElementById('stats');
    const totalSeries = document.getElementById('total-series');
    const totalEpisodios = document.getElementById('total-episodios');

    try {
        // Carregar arquivo TXT
        const response = await fetch('lista_series.txt');
        if (!response.ok) {
            throw new Error('Arquivo não encontrado');
        }

        const text = await response.text();
        const series = parseSeriesTxt(text);

        // Esconder loading
        loading.style.display = 'none';

        if (series.length === 0) {
            error.style.display = 'block';
            error.innerHTML = '<p>Nenhuma série encontrada no arquivo.</p>';
            return;
        }

        // Exibir séries
        container.innerHTML = '';
        let totalEps = 0;
        series.forEach((serie, index) => {
            const serieDiv = createSerieElement(serie, index + 1);
            container.appendChild(serieDiv);
            totalEps += serie.episodios.length;
        });

        // Atualizar estatísticas
        totalSeries.textContent = series.length;
        totalEpisodios.textContent = totalEps;
        stats.style.display = 'block';

    } catch (err) {
        loading.style.display = 'none';
        error.style.display = 'block';
        console.error('Erro ao carregar séries:', err);
    }
}

/**
 * Parse do arquivo TXT de filmes
 */
function parseFilmesTxt(text) {
    const filmes = [];
    const lines = text.split('\n');
    
    let currentFilme = null;
    let inFilmeSection = false;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        // Ignorar linhas vazias, separadores e cabeçalhos
        if (!line || line.startsWith('=') || line.startsWith('-') || 
            line.includes('LISTA DE FILMES') || line.includes('Data de geração') || 
            line.includes('Total de filmes') || line.includes('Total:')) {
            continue;
        }

        // Detectar início de um filme (formato: "1. Nome do Filme")
        const filmeMatch = line.match(/^\d+\.\s+(.+)$/);
        if (filmeMatch) {
            // Salvar filme anterior se existir
            if (currentFilme) {
                filmes.push(currentFilme);
            }
            // Criar novo filme
            currentFilme = {
                nome: filmeMatch[1],
                arquivos: []
            };
            inFilmeSection = true;
            continue;
        }

        // Detectar arquivos de vídeo (formato: "   • arquivo.ext")
        if (inFilmeSection && currentFilme && line.startsWith('•')) {
            const arquivo = line.replace(/^[\s•]+/, '').trim();
            if (arquivo) {
                currentFilme.arquivos.push(arquivo);
            }
        }
    }

    // Adicionar último filme
    if (currentFilme) {
        filmes.push(currentFilme);
    }

    return filmes;
}

/**
 * Parse do arquivo TXT de séries
 */
function parseSeriesTxt(text) {
    const series = [];
    const lines = text.split('\n');
    
    let currentSerie = null;
    let inSerieSection = false;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        // Ignorar linhas vazias, separadores e cabeçalhos
        if (!line || line.startsWith('=') || line.startsWith('-') || 
            line.includes('LISTA DE SÉRIES') || line.includes('Data de geração') || 
            line.includes('Total de séries') || line.includes('Total de episódios') || 
            line.includes('Total:')) {
            continue;
        }

        // Detectar início de uma série (formato: "1. Nome da Série (X episódio(s))")
        const serieMatch = line.match(/^\d+\.\s+(.+?)\s*\((\d+)\s+episódio\(s\)\)$/);
        if (serieMatch) {
            // Salvar série anterior se existir
            if (currentSerie) {
                series.push(currentSerie);
            }
            // Criar nova série
            currentSerie = {
                nome: serieMatch[1],
                episodios: []
            };
            inSerieSection = true;
            continue;
        }

        // Detectar episódios (formato: "   • episodio.ext")
        if (inSerieSection && currentSerie && line.startsWith('•')) {
            const episodio = line.replace(/^[\s•]+/, '').trim();
            if (episodio) {
                currentSerie.episodios.push(episodio);
            }
        }
    }

    // Adicionar última série
    if (currentSerie) {
        series.push(currentSerie);
    }

    return series;
}

/**
 * Cria elemento HTML para um filme
 */
function createFilmeElement(filme, numero) {
    const div = document.createElement('div');
    div.className = 'filme-item';

    const h3 = document.createElement('h3');
    const numeroSpan = document.createElement('span');
    numeroSpan.className = 'numero';
    numeroSpan.textContent = numero;
    h3.appendChild(numeroSpan);
    h3.appendChild(document.createTextNode(filme.nome));

    div.appendChild(h3);

    if (filme.arquivos.length > 0) {
        const ul = document.createElement('ul');
        ul.className = 'arquivos-lista';
        filme.arquivos.forEach(arquivo => {
            const li = document.createElement('li');
            li.textContent = arquivo;
            ul.appendChild(li);
        });
        div.appendChild(ul);
    }

    return div;
}

/**
 * Cria elemento HTML para uma série
 */
function createSerieElement(serie, numero) {
    const div = document.createElement('div');
    div.className = 'serie-item';

    const h3 = document.createElement('h3');
    const numeroSpan = document.createElement('span');
    numeroSpan.className = 'numero';
    numeroSpan.textContent = numero;
    h3.appendChild(numeroSpan);
    
    const nomeSpan = document.createElement('span');
    nomeSpan.textContent = serie.nome;
    h3.appendChild(nomeSpan);

    const countSpan = document.createElement('span');
    countSpan.className = 'episodios-count';
    countSpan.textContent = `${serie.episodios.length} episódio(s)`;
    h3.appendChild(countSpan);

    div.appendChild(h3);

    if (serie.episodios.length > 0) {
        const ul = document.createElement('ul');
        ul.className = 'arquivos-lista';
        serie.episodios.forEach(episodio => {
            const li = document.createElement('li');
            li.textContent = episodio;
            ul.appendChild(li);
        });
        div.appendChild(ul);
    }

    return div;
}

