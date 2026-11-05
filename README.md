# Análise Exploratória, Pré-processamento e Engenharia de Recursos

Repositório acadêmico da disciplina de Análise e Visualização de Dados do curso de pós-graduação em Ciência de Dados e Big Data. O projeto reúne duas entregas obrigatórias estruturadas em pipelines analíticos reproduzíveis, relatórios técnicos canônicos, suíte de testes de integridade e automação via Makefile:
- **Entrega 1 (UAs 01 e 02):** Análise exploratória e pré-processamento de dados com o conjunto de dados Titanic.
- **Entrega 2 (UAs 03 e 04):** Engenharia de recursos, seleção de preditores e visualização multidimensional com o conjunto de dados House Prices.

---

## Equipe
- Diogo Galrão Carvalho
- Felipe Artur Macedo Lima
- Luan Cavalcante Dias Rodrigues

---

## Execução e Automação

O projeto conta com automação via Makefile para orquestrar a execução sequencial dos notebooks, a compilação dos relatórios técnicos em PDF e a validação por testes automatizados.

### Comandos principais

```bash
# Executa os notebooks analíticos e compila os relatórios técnicos em PDF
make run

# Executa a suíte de testes automatizados (32 testes de dados, ambiente e relatórios)
make test

# Compila os relatórios técnicos em PDF a partir dos arquivos canônicos em Markdown
make reports

# Executa os notebooks Jupyter e atualiza as saídas salvas
make notebooks

# Configura o ambiente virtual Python (.venv) e instala as dependências
make venv

# Remove arquivos temporários de compilação e caches do projeto
make clean
```

### Pré-requisitos de ambiente
- Python >= 3.12
- Dependências Python declaradas em `requirements.txt` (`pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `markdown-it-py`, `weasyprint`, `nbformat`, `nbconvert`, `ipykernel`)
- Bibliotecas de sistema do WeasyPrint (Pango, Cairo, GObject e fontes TrueType)

---

## Entregas e Evidências

Todos os artefatos de entrega estão disponíveis no repositório com rastreabilidade entre código, dados intermediários e documentos finais compilados:

### Relatórios Técnicos Oficiais
- **Entrega 1 (UAs 01 e 02 - Titanic):**
  - [Relatório Técnico em PDF](reports/Entrega_1_UA1_UA2_Relatorio_Tecnico.pdf)
  - [Fonte canônica em Markdown](reports/Entrega_1_UA1_UA2_Relatorio_Tecnico.md)
- **Entrega 2 (UAs 03 e 04 - House Prices):**
  - [Relatório Técnico em PDF](reports/Entrega_2_UA3_UA4_Relatorio_Tecnico.pdf)
  - [Fonte canônica em Markdown](reports/Entrega_2_UA3_UA4_Relatorio_Tecnico.md)

### Notebooks Reprodutíveis
- [notebooks/01_analise_titanic.ipynb](notebooks/01_analise_titanic.ipynb): Análise exploratória, tratamento de inconsistências, imputação estratificada de idade por sexo e classe, transformação logarítmica de tarifas per capita e One-Hot Encoding.
- [notebooks/02_engenharia_recursos_house_prices.ipynb](notebooks/02_engenharia_recursos_house_prices.ipynb): Análise da distribuição de SalePrice, engenharia de atributos (HouseAge, TotalArea, IsRemodeled), tratamento de ausências estruturais, ranking de importância via Random Forest e redução de dimensionalidade com PCA.

### Evidências Estruturadas e Gráficos
- [reports/evidence/titanic_metrics.json](reports/evidence/titanic_metrics.json): Métricas consolidadas de sobrevivência, proporções demográficas e dimensões do conjunto processado do Titanic.
- [reports/evidence/house_prices_metrics.json](reports/evidence/house_prices_metrics.json): Estatísticas descritivas de SalePrice, matriz de correlação, ranking de importância de variáveis e proporção de variância explicada do PCA.
- [reports/evidence/figures/](reports/evidence/figures/): Figuras analíticas em alta resolução geradas diretamente pelos pipelines.

---

## Dados e Resultados Analíticos

### Entrega 1: Dataset Titanic (891 registros, 12 atributos originais)
- **Taxa geral de sobrevivência:** 38,38% (342 sobreviventes e 549 óbitos), resultando em uma proporção de 1,6 óbito por sobrevivente. O desbalanceamento moderado inviabiliza o uso da acurácia simples como métrica isolada, exigindo avaliação por F1-Score, precisão, revocação e área sob a curva ROC (ROC-AUC).
- **Disparidade por gênero:** O protocolo naval de evacuação determinou taxa de sobrevivência de 74,20% entre mulheres contra 18,89% entre homens (razão de chances aproximada de 12:1).
- **Estratificação socioeconômica:** A classe da passagem apresentou correlação direta com as chances de salvamento: 62,96% na 1ª classe, 47,28% na 2ª classe e 24,24% na 3ª classe.
- **Interação cruzada Sexo x Classe:** Mulheres da 1ª classe registraram taxa de sobrevivência de 96,80% contra 50,00% entre mulheres da 3ª classe. Homens da 1ª classe alcançaram 36,89% de resgate contra 13,54% na 3ª classe.
- **Estrutura familiar:** Passageiros em famílias de pequeno porte (2 a 4 pessoas) obtiveram taxa de 57,88%, superando passageiros solitários (30,35%) e integrantes de famílias numerosas com 5 ou mais pessoas (16,13%).
- **Auditoria de bilhetes e tarifas de grupo:** Identificou-se que a coluna `Fare` continha o valor acumulado do grupo em passagens compartilhadas (681 códigos de bilhete distintos para 891 viajantes). O cálculo da tarifa per capita (`FarePorPessoa = Fare / GroupSize`) eliminou distorções contábeis que superestimavam o poder aquisitivo de passageiros de 3ª classe. Registros com tarifa zero (15 ocorrências) foram preservados por corresponderem a cortesias operacionais da White Star Line e integrantes da equipe de garantia técnica dos estaleiros Harland and Wolff.
- **Tratamento de ausências e codificação:** A variável `Cabin` (77,10% nulos) foi convertida no indicador estrutural `TemCabine` (sobrevivência de 66,67% com registro contra 29,98% sem registro). A coluna `Age` (19,87% nulos) recebeu imputação estratificada pela mediana do cruzamento entre `Sex` e `Pclass`, acompanhada da flag `IdadeImputada`. Variáveis categóricas nominais foram codificadas via One-Hot Encoding com exclusão da primeira categoria (`drop_first=True`), evitando multicolinearidade perfeita.

### Entrega 2: Dataset House Prices (1.460 registros, 79 atributos originais)
- **Distribuição de SalePrice:** Média de US$ 180.921,20, mediana de US$ 163.000,00, desvio padrão de US$ 79.442,50, assimetria positiva de 1,8829 e curtose de 6,5362. A assimetria acentuada reflete a presença de residências de alto padrão que elevam a média em relação ao centro da distribuição amostral.
- **Preditores com maior correlação linear:** `OverallQual` (r = 0,7910), `GrLivArea` (r = 0,7086), `GarageCars` (r = 0,6404), `GarageArea` (r = 0,6234), `TotalBsmtSF` (r = 0,6136) e `1stFlrSF` (r = 0,6059).
- **Engenharia de recursos:**
  - `HouseAge` (`YrSold - YearBuilt`): quantifica o envelhecimento e a obsolescência funcional na data da transação, exibindo correlação linear negativa com o preço (r = -0,5229).
  - `TotalArea` (`TotalBsmtSF + 1stFlrSF + 2ndFlrSF`): agrega a metragem utilizável do subsolo aos pavimentos térreo e superior, atingindo coeficiente de correlação linear de r = 0,7821 com `SalePrice` (superior a qualquer medida de área individual).
  - `IsRemodeled` (`YearRemodAdd != YearBuilt`): identifica intervenções de reforma ou ampliação presentes em 47,81% dos imóveis da amostra.
- **Importância de atributos via Random Forest:** O modelo Random Forest Regressor apontou `TotalArea` como a característica mais relevante (43,18% de redução média de impureza), superando `OverallQual` (33,91%). Combinados, os dois preditores acumulam 77,09% da importância global do modelo.
- **Análise de Componentes Principais (PCA):** As duas primeiras componentes principais retêm 48,32% da variância amostral total (35,79% em PC1, ligada a porte físico e padrão geral; 12,53% em PC2, ligada a conservação e contraste temporal). A projeção bidimensional demonstra segregação clara de grupos conforme a pontuação de `OverallQual`.

---

## Estrutura do Repositório

```text
hands-on-eda/
├── Makefile                 # Automação de tarefas (run, test, reports, notebooks, venv, clean)
├── README.md                # Documentação técnica e guia de execução do projeto
├── pyproject.toml           # Metadados do projeto e especificação de dependências Python
├── requirements.txt         # Lista de pacotes para instalação via pip
├── .gitignore               # Padrões de arquivos e diretórios ignorados pelo Git
├── data/
│   ├── raw/                 # Bases de dados brutas imutáveis e metadados
│   │   ├── titanic.csv      # Conjunto de dados bruto do Titanic (891 linhas, 12 colunas)
│   │   ├── house_prices.csv # Conjunto de dados bruto de House Prices (1460 linhas, 81 colunas)
│   │   └── README.md        # Documentação, dicionário e hashes SHA-256 das bases brutas
│   └── processed/           # Conjuntos de dados processados pelos pipelines
│       ├── titanic_clean.csv          # Base tratada do Titanic (891 linhas, 11 colunas)
│       └── house_prices_features.csv  # Base tratada de House Prices (1460 linhas, 89 colunas)
├── notebooks/               # Notebooks Jupyter com análises e saídas pré-computadas
│   ├── 01_analise_titanic.ipynb                # Análise exploratória e pré-processamento (UAs 01/02)
│   └── 02_engenharia_recursos_house_prices.ipynb # Engenharia de recursos, RF e PCA (UAs 03/04)
├── reports/                 # Relatórios técnicos canônicos e artefatos visuais
│   ├── Entrega_1_UA1_UA2_Relatorio_Tecnico.md  # Fonte canônica em Markdown da Entrega 1
│   ├── Entrega_1_UA1_UA2_Relatorio_Tecnico.pdf # Relatório técnico oficial em PDF da Entrega 1
│   ├── Entrega_2_UA3_UA4_Relatorio_Tecnico.md  # Fonte canônica em Markdown da Entrega 2
│   ├── Entrega_2_UA3_UA4_Relatorio_Tecnico.pdf # Relatório técnico oficial em PDF da Entrega 2
│   └── evidence/            # Métricas estruturadas e figuras analíticas
│       ├── titanic_metrics.json                # Métricas consolidadas em JSON do Titanic
│       ├── house_prices_metrics.json           # Métricas consolidadas em JSON de House Prices
│       └── figures/                            # Gráficos em alta resolução exportados pelos notebooks
├── scripts/                 # Utilitários Python de suporte e compilação
│   ├── run_notebooks.py     # Execução sequencial dos notebooks Jupyter
│   └── build_reports.py     # Compilação dos relatórios Markdown para PDF via WeasyPrint
└── tests/                   # Suíte de testes automatizados com unittest
    ├── test_data.py         # Validação de integridade de dados brutos, tratados e evidências
    ├── test_environment.py  # Verificação de dependências, Makefile e configurações
    ├── test_reports.py      # Verificação estrutural e textual dos relatórios e PDFs
    └── test_scripts.py      # Testes unitários dos utilitários de execução e compilação
```

---

## Verificação e Qualidade

O projeto dispõe de 32 testes automatizados baseados em `unittest`, cobrindo as seguintes dimensões:
1. **Integridade de dados:** verificação de hashes SHA-256 das fontes brutas, consistência de dimensões, inexistência de registros nulos nos conjuntos processados e conformidade das métricas JSON.
2. **Ambiente e configuração:** presença e completude das metas do Makefile, alinhamento de dependências e regras de exclusão no `.gitignore`.
3. **Conformidade dos relatórios:** verificação de autoria, estrutura formal das seções de rubrica, referências bibliográficas e validação da compilação dos PDFs executivos.
4. **Scripts de automação:** validação da descoberta de notebooks, compilação de CSS executivo A4 e injeção dinâmica de métricas.

Comando de verificação:
```bash
make test
```
