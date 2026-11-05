# Design Doc: Estruturação e Entregas do Hands-on EDA

## 1. Contexto e Motivação
Este projeto integra o curso de pós-graduação na disciplina de Análise e Visualização de Dados, desenvolvido pelos integrantes Diogo Galrão Carvalho, Felipe Artur Macedo Lima e Luan Cavalcante Dias Rodrigues.

O repositório `hands-on-eda` consolida duas entregas acadêmicas obrigatórias baseadas nos roteiros oficiais da pós-graduação:
1. **Entrega 1 (UA 01 e UA 02):** Análise exploratória e pré-processamento de dados com o dataset Titanic (Passos 1 a 11 do material impresso).
2. **Entrega 2 (UA 03 e UA 04):** Engenharia de recursos e visualização de dados com o dataset House Prices do Kaggle (Passos 1 a 22 do material impresso).

O repositório deve espelhar o rigor de engenharia de software e reprodutibilidade do projeto de referência `bigdata_datascience`: automação com Makefile, relatórios técnicos canônicos em Markdown compilados para PDF com WeasyPrint, suíte de testes de integridade, notebooks estruturados e documentação abrangente no README.

## 2. Metas, Não Metas e Anti-Metas

### Metas (Goals)
- **Cobertura Integral dos Roteiros:** Cumprir todos os passos metodológicos de ambas as unidades de aprendizagem (Passos 1-11 da Entrega 1 e Passos 1-22 da Entrega 2) com justificativas estatísticas e de negócio aprofundadas.
- **Relatórios Técnicos Executivos:** Produzir `Entrega_1_UA1_UA2_Relatorio_Tecnico.pdf` e `Entrega_2_UA3_UA4_Relatorio_Tecnico.pdf` a partir de fontes canônicas em Markdown (`reports/`), no padrão visual A4 corporativo com paginação, tipografia sóbria e tabelas consolidadas.
- **Notebooks Canônicos:** Disponibilizar `notebooks/01_analise_titanic.ipynb` e `notebooks/02_engenharia_recursos_house_prices.ipynb` reprodutíveis do início ao fim com saídas salvas e gráficos em alta resolução.
- **Automação Completa via Makefile:** Comandos `make run`, `make test`, `make reports` e `make notebooks` para orquestrar execução de ponta a ponta sem intervenção manual.
- **Suíte de Testes:** Validar existência e integridade dos dados brutos e processados, geração de evidências JSON e integridade dos PDFs gerados.

### Não Metas (Non-goals)
- Treinamento extensivo de múltiplos modelos de machine learning em grade de hiperparâmetros (o foco do roteiro é EDA, pré-processamento, engenharia de atributos, importância via Random Forest e PCA).
- Submissão ao Kaggle ou deploy de modelos em nuvem.

### Anti-Metas (Anti-goals)
- Códigos soltos sem documentação ou células de notebook desordenadas.
- Relatórios em PDF gerados manualmente via impressão de navegador com formatação quebrada.
- Omissão de justificativas técnicas exigidas na rubrica de avaliação (ex: omitir a fundamentação entre One-Hot vs Label Encoding ou a análise de tarifas de grupos no Titanic).

## 3. Restrições e Padrões
- **Python:** Ambiente configurado com suporte a virtualenv e `pyproject.toml` / `requirements.txt`.
- **Bibliotecas:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `markdown-it-py`, `weasyprint`, `nbformat`, `nbconvert`.
- **Dados:** Armazenados em `data/raw/` e `data/processed/`, com hashes SHA-256 e proveniência documentada.
- **Estilo de Escrita:** Texto revisado de acordo com as diretrizes do Humanizer, sem jargões artificiais, sem travessões decorativos e com linguagem técnica direta e fundamentada.

## 4. Abordagens Consideradas
- **Abordagem A (Apenas Notebooks no Git):** Manter apenas notebooks jupyter com as saídas.
  *Trade-off:* Falha no critério de entrega da pós (exige envio de PDF com relatório executivo) e descumpre a diretriz de seguir o padrão do `bigdata_datascience`. Descartada.
- **Abordagem B (Arquitetura Canônica bigdata_datascience - Escolhida):**
  Estrutura desacoplada:
  - `data/raw/` e `data/processed/`
  - `notebooks/` com narrativa e análises
  - `scripts/` para automações (`run_notebooks.py`, `build_reports.py`)
  - `reports/` com fontes Markdown, evidências e PDFs oficiais
  - `tests/` com testes automatizados
  - `Makefile` e `README.md` completos.
  *Vantagem:* Reprodutibilidade total, atende à rubrica com nota máxima e segue fielmente a lógica solicitada pelo usuário.

## 5. Estrutura de Arquivos
```text
hands-on-eda/
├── Makefile
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   │   ├── titanic.csv
│   │   └── house_prices.csv
│   └── processed/
│       ├── titanic_clean.csv
│       └── house_prices_features.csv
├── notebooks/
│   ├── 01_analise_titanic.ipynb
│   └── 02_engenharia_recursos_house_prices.ipynb
├── reports/
│   ├── Entrega_1_UA1_UA2_Relatorio_Tecnico.md
│   ├── Entrega_1_UA1_UA2_Relatorio_Tecnico.pdf
│   ├── Entrega_2_UA3_UA4_Relatorio_Tecnico.md
│   ├── Entrega_2_UA3_UA4_Relatorio_Tecnico.pdf
│   └── evidence/
│       ├── titanic_metrics.json
│       ├── house_prices_metrics.json
│       └── figures/
├── scripts/
│   ├── run_notebooks.py
│   └── build_reports.py
└── tests/
    ├── test_data.py
    └── test_reports.py
```
