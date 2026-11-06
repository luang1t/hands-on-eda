# Análise exploratória e engenharia de recursos

Projeto da disciplina Análise e Visualização de Dados da pós-graduação em Ciência de Dados e Big Data. A equipe é formada por Diogo Galrão Carvalho, Felipe Artur Macedo Lima e Luan Cavalcante Dias Rodrigues.

As duas atividades são:

- Titanic: classificação de variáveis, análise de sobrevivência e pré-processamento.
- House Prices: engenharia de atributos, seleção de características e visualização com PCA.

## Executar

Requisitos: Python 3.12 ou superior, bibliotecas de sistema do WeasyPrint (Pango, Cairo e fontes) e acesso à internet para instalar os pacotes. Na raiz do repositório:

```bash
make venv
make run
make test
```

Execute apenas notebooks e relatórios de fontes confiáveis: notebooks podem executar código e relatórios podem carregar recursos locais.

`make run` executa os notebooks em ordem, atualiza dados e figuras e compila os relatórios em PDF. A execução sobrescreve esses arquivos. Para etapas individuais, use `make notebooks` ou `make reports`. O Makefile usa `.venv/bin/python` quando o ambiente existe.

## Entregas

Cada integrante deve entregar no AVA o PDF correspondente a cada atividade:

- [Relatório Titanic](reports/Entrega_1_UA1_UA2_Relatorio_Tecnico.pdf) e [notebook](notebooks/01_analise_titanic.ipynb).
- [Relatório House Prices](reports/Entrega_2_UA3_UA4_Relatorio_Tecnico.pdf) e [notebook](notebooks/02_engenharia_recursos_house_prices.ipynb).

As fontes dos relatórios estão em `reports/` em Markdown. Os links dos PDFs apontam para os notebooks na branch `main` do repositório GitHub; eles só refletirão as alterações depois de publicadas. Os arquivos brutos e sua origem estão em [data/raw](data/raw/README.md). Os resultados ficam em `data/processed/` e `reports/evidence/`.

## Resultados e limites

No Titanic, 342 dos 891 passageiros (38,38%) sobreviveram. As taxas variam entre grupos de sexo e classe. A base processada tem 891 linhas e 11 colunas numéricas. A tarifa dividida pela quantidade de registros de um bilhete é uma aproximação, pois a amostra pode não conter todos os passageiros do grupo.

Em House Prices, `TotalArea` e `HouseAge` têm correlação de 0,782 e -0,523 com o preço, respectivamente. A floresta ranqueia variáveis originais e criadas, com categorias agregadas por coluna. O PCA retém 48,32% da variância nas duas primeiras componentes. São resultados exploratórios da amostra, sem estimativa de causalidade ou desempenho em dados novos. O CSV enriquecido mantém valores ausentes em parte das colunas originais.

Para avaliar modelos preditivos, separe treino e teste antes de ajustar imputação, codificação, escala, seleção ou PCA. Os artefatos aqui foram gerados usando a amostra completa.
