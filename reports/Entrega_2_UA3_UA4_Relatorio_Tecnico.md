# Relatório Técnico: Engenharia de Recursos e Visualização Multidimensional (Dataset House Prices)

**Disciplina:** Análise e Visualização de Dados (UAs 03 e 04)  
**Autores:** Diogo Galrão Carvalho, Felipe Artur Macedo Lima, Luan Cavalcante Dias Rodrigues  
**Notebook de Referência:** [notebooks/02_engenharia_recursos_house_prices.ipynb](../notebooks/02_engenharia_recursos_house_prices.ipynb)  
**Data:** Novembro de 2026  

---

## 1. Introdução e Contexto de Mercado Imobiliário

A valoração automatizada de imóveis residenciais (Automated Valuation Models - AVM) constitui um dos campos centrais da econometria aplicada e da ciência de dados. A precificação precisa de habitações depende da quantificação de fatores estruturais, espaciais, de conservação e de acabamento, frequentemente caracterizados por não linearidades, correlações cruzadas e variáveis latentes.

O presente estudo analisa a base de dados de Ames, Iowa, compilada pelo economista Dean De Cock para o Journal of Statistics Education (2011). O levantamento registra 1.460 transações imobiliárias ocorridas entre 2006 e 2010, descritas por 79 atributos originais que cobrem características de terreno, fundação, conveses de garagem, qualidade de cômodos e metragens por pavimento. O objetivo deste trabalho é executar uma análise exploratória aprofundada da variável dependente `SalePrice`, criar novos atributos orientados pelo conhecimento do setor, tratar ausências estruturais e ordinais, mensurar a importância dos preditores por meio de florestas aleatórias (Random Forest) e projetar a estrutura latente dos dados com Análise de Componentes Principais (PCA).

<div class="page-break"></div>

## 2. Distribuição da Variável Alvo (SalePrice) e Correlações Lineares

A variável de resposta `SalePrice` registra o preço final de comercialização dos imóveis em dólares (US$). A distribuição amostral possui as seguintes estatísticas descritivas:

- Preço médio: US$ 180.921,20
- Preço mediano: US$ 163.000,00
- Desvio padrão: US$ 79.442,50
- Valor mínimo: US$ 34.900,00
- Valor máximo: US$ 755.000,00
- Assimetria amostral (skewness): 1,8829
- Curtose amostral: 6,5362

![Distribuição de SalePrice](figures/house_prices_target_dist.png)

A assimetria positiva de 1,88 evidencia uma distribuição com cauda longa à direita, típica de mercados habitacionais nos quais a maioria das residências negocia em faixas intermediárias (o intervalo interquartil varia de US$ 129.975,00 a US$ 214.000,00), enquanto transações de mansões de alto luxo elevam a média em quase 11% acima da mediana.

A matriz de correlação de Pearson revela forte associação linear de `SalePrice` com dimensões físicas e indicadores de qualidade construtiva:

- `OverallQual` (r = 0,7910): qualidade geral do acabamento e materiais da edificação.
- `GrLivArea` (r = 0,7086): área habitável acima do nível do solo.
- `GarageCars` (r = 0,6404) e `GarageArea` (r = 0,6234): capacidade e metragem da garagem.
- `TotalBsmtSF` (r = 0,6136): metragem quadrada do subsolo.
- `1stFlrSF` (r = 0,6059): metragem do primeiro pavimento térreo.
- `FullBath` (r = 0,5607): quantidade de banheiros completos.
- `TotRmsAbvGrd` (r = 0,5337): quantidade total de cômodos acima do solo.
- `YearBuilt` (r = 0,5229): ano de construção original do imóvel.

![Mapa de Calor das Correlações](figures/house_prices_correlation_heatmap.png)

<div class="page-break"></div>

## 3. Engenharia de Recursos com Fundamentação de Negócio

Para enriquecer a capacidade explicativa dos modelos, desenvolveram-se três novos atributos embasados na dinâmica econômica da avaliação imobiliária:

1. **Idade do Imóvel no Momento da Venda (`HouseAge`):**  
   Fórmula: `HouseAge = YrSold - YearBuilt`.  
   O ano civil de construção isolado (`YearBuilt`) não captura a defasagem temporal exata na data do negócio, uma vez que as vendas ocorreram entre 2006 e 2010. A idade cronológica efetiva variou de 0 ano (casas negociadas no próprio ano de conclusão) até 136 anos, com mediana de 35 anos. Do ponto de vista econômico, esse atributo quantifica a depreciação física contínua, o desgaste estrutural e a obsolescência de plantas arquitetônicas antigas. Apresenta correlação linear negativa com o preço de venda (r = -0,523).

2. **Superfície Útil Total Agregada (`TotalArea`):**  
   Fórmula: `TotalArea = TotalBsmtSF + 1stFlrSF + 2ndFlrSF`.  
   A métrica original `GrLivArea` contabiliza unicamente os pavimentos superiores, ignorando o subsolo. Contudo, compradores e avaliadores precificam a área total utilizável do imóvel, pois o subsolo abriga frequentemente salas de lazer, depósitos organizados ou quartos extras. A nova variável `TotalArea` alcançou coeficiente de correlação linear de r = 0,782 com `SalePrice`, superando expressivamente os preditores parciais `GrLivArea` (r = 0,709) e `TotalBsmtSF` (r = 0,614).

3. **Indicador Binário de Reforma (`IsRemodeled`):**  
   Fórmula: `IsRemodeled = (YearRemodAdd != YearBuilt).astype(int)`.  
   Identifica residências que passaram por intervenções de reforma, modernização de instalações ou expansão após a edificação original. No mercado residencial, uma reforma atualiza revestimentos, isolamento térmico e instalações hidráulicas e elétricas, amortecendo a perda de valor decorrente da idade física. No dataset analisado, 47,8% dos imóveis possuem histórico de reforma comprovada.

![Atributos Sintéticos Criados](figures/house_prices_engineered_features.png)

<div class="page-break"></div>

## 4. Mapeamento de Variáveis Ordinais e Tratamento de Ausências Estruturais

A base de dados contém avaliações qualitativas graduadas segundo escalas padronizadas que exigem tratamento numérico adequado:

- **Codificação ordinal numérica monotônica:** As colunas de avaliação de acabamento `ExterQual` (qualidade externa), `BsmtQual` (altura e acabamento do subsolo) e `KitchenQual` (qualidade da cozinha) foram convertidas para uma escala inteira discreta de 0 a 5:
  - 5: Excelente (`Ex`)
  - 4: Bom (`Gd`)
  - 3: Típico ou Médio (`TA`)
  - 2: Fraco (`Fa`)
  - 1: Pobre (`Po`)
  - 0: Ausência física da instalação (`NA`)
  
  Diferentemente do One-Hot Encoding (que geraria redundância dimensional e diluição do sinal de ordenação), essa transformação respeita a monotonicidade estrita da hierarquia ($5 > 4 > 3 > 2 > 1 > 0$), permitindo que algoritmos capturem diretamente o valor marginal de cada elevação de padrão.

- **Comportamento de `OverallQual`:** A nota global de qualidade (de 1 a 10) mantém relação monotônica com o preço, exibindo comportamento não linear com aceleração exponencial para notas superiores a 7:

![Boxplot de OverallQual vs SalePrice](figures/house_prices_overall_qual_boxplot.png)

  Residências de padrão médio (notas 5 a 6) concentram preços medianos de US$ 140.000 a US$ 160.000, enquanto imóveis de alto luxo (notas 8 a 10) saltam para medianas de US$ 269.000, US$ 345.000 e US$ 432.000, demarcando a fronteira de residências de alto padrão.

- **Diferenciação entre ausência estrutural e perda aleatória:** Na maioria dos conjuntos de dados, valores nulos representam omissões ou falhas de coleta (MCAR/MAR). Contudo, em bases imobiliárias, campos nulos nas colunas `Alley`, `PoolQC`, `Fence`, `FireplaceQu` e `GarageType` indicam a inexistência física da instalação na propriedade (a casa não possui beco, piscina, cerca, lareira ou garagem). A imputação estatística genérica por média ou moda nestes casos corromperia a integridade do domínio. O tratamento correto consistiu na atribuição explícita de classes categóricas identificadoras (`NoAlley`, `NoPool`, `NoFence`, `NoFireplace`, `NoGarage`), preservando a informação de ausência como indicador imobiliário legítimo.

<div class="page-break"></div>

## 5. Seleção de Características Baseada em Árvores (Random Forest)

Para avaliar o poder explicativo de cada dimensão e quantificar a relevância dos novos atributos frente às variáveis originais, ajustou-se um modelo `RandomForestRegressor` (100 estimadores, critério de divisão por erro quadrático e semente controlada):

![Importância das Features via Random Forest](figures/house_prices_feature_importance.png)

O vetor de importância de variáveis (Mean Decrease in Impurity - MDI) produziu as seguintes constatações:

1. **Supremacia do atributo sintetizado `TotalArea`:** A metragem total criada conquistou a primeira colocação absoluta no ranking com 43,18% de importância total, superando o principal preditor isolado original (`OverallQual`, com 33,91%). Juntas, essas duas variáveis concentram mais de 77% da informação preditiva do modelo.
2. **Relevância do atributo `HouseAge`:** A idade cronológica derivada posicionou-se na 7ª posição geral com 1,32% de importância, superando métricas tradicionais consolidadas como `GrLivArea` (1,30%) e `GarageArea` (1,08%).
3. **Influência das variáveis ordinais codificadas:** O padrão de acabamento da cozinha (`KitchenQual_Num`, com 1,05%) e do subsolo (`BsmtQual_Num`, com 1,00%) figuraram entre os dez preditores mais importantes, demonstrando que cômodos funcionais geram impacto direto na precificação.

<div class="page-break"></div>

## 6. Redução de Dimensionalidade com Análise de Componentes Principais (PCA)

A Análise de Componentes Principais (PCA) calcula a decomposição espectral da matriz de covariância após a padronização das variáveis com média zero e variância unitária ($Z = \frac{X - \mu}{\sigma}$). O objetivo é encontrar vetores ortogonais que capturem a máxima dispersão informacional:

- **Primeiro Componente Principal (PC1):** Retém 35,79% da variância total do conjunto selecionado. Suas maiores cargas concentram-se nas variáveis de dimensão física e acabamento (`TotalArea`, `GrLivArea`, `GarageCars`, `OverallQual`), operando como um indicador sintético de escala e padrão habitacional.
- **Segundo Componente Principal (PC2):** Retém 12,53% da variância total, capturando o contraste temporal da residência (cargas negativas fortes para `HouseAge` e cargas positivas para `YearBuilt`).
- **Retenção acumulada:** O plano bidimensional (PC1 e PC2) retém conjuntamente 48,32% da variância total das variáveis avaliadas.

![Dispersão PCA Colorida por Qualidade](figures/house_prices_pca_scatter.png)

A dispersão dos imóveis no plano PC1 contra PC2 exibe um gradiente contínuo e ordenado de segregação qualitativa:

- Residências com notas inferiores de acabamento (`OverallQual` 2 a 4) agrupam-se estritamente na extremidade esquerda e inferior da projeção (baixo PC1 e PC2 negativo), correspondendo a imóveis compactos e antigos.
- À medida que se transita para a direita no eixo horizontal, observa-se a sucessão gradual das notas médias (5, 6 e 7).
- No quadrante superior direito, destacam-se com total separação as residências de excelência construtiva (notas 8, 9 e 10), confirmando que a combinação ortogonal de metragem e idade no PCA sintetiza a estratificação socioeconômica do mercado de Ames.

<div class="page-break"></div>

## 7. Recomendações Acionáveis de Negócio

Com base nos resultados estatísticos, nos rankings de árvores de decisão e nas projeções fatoriais, apresentam-se três diretrizes aplicáveis para tomadores de decisão:

1. **Incorporadoras e Construtoras:** A metragem total habitável integrada (`TotalArea`) exerce peso superior ao de qualquer acabamento isolado na formação de valor. Ao conceber projetos residenciais, deve-se maximizar o aproveitamento útil de subsolos, estruturando-os desde a fundação como áreas plenamente habitáveis com iluminação e pé-direito adequado. Ademais, na dotação de orçamentos para acabamentos internos, a priorização de cozinhas de padrão excelente (`KitchenQual`) oferece o maior retorno marginal por metro quadrado entre todos os cômodos internos.
2. **Empresas de Reforma e Investidores (Fix-and-Flip):** A estratégia ótima de aquisição para repaginação deve focar imóveis com idade cronológica entre 30 e 50 anos que ainda preservam características originais (`IsRemodeled == 0`), mas mantêm integridade estrutural básica (`OverallCond >= 5`). O investimento direcionado à modernização da cozinha e à climatização do subsolo promove um deslocamento imediato no indicador `OverallQual` e no vetor PC1, destravando o prêmio de valorização exponencial observado na transição das notas medianas (5 e 6) para os padrões superiores (7 e 8).
3. **Avaliadores Imobiliários e Analistas de Risco (AVM):** O pipeline de precificação automatizada deve rejeitar imputações genéricas para ausências estruturais. A inexistência de garagem ou subsolo precisa ser tratada como penalidade funcional explícita através de categorias próprias. Além disso, as coordenadas latentes extraídas pelo PCA (PC1 e PC2) oferecem métricas sintéticas de liquidez e garantia patrimonial, permitindo avaliar a homogeneidade de carteiras imobiliárias frente a riscos de desvalorização física.

<div class="page-break"></div>

## 8. Síntese dos Indicadores e Evidências Consolidadas

A matriz processada final foi exportada com 1.460 registros e 89 colunas, agregando as variáveis originais higienizadas, as transformações sintéticas (`HouseAge`, `TotalArea`, `IsRemodeled`), as escalas ordinais numéricas e os escores fatoriais (`PC1`, `PC2`).

A tabela a seguir consolida as métricas calculadas pelo fluxo analítico:

<!-- house_prices_metrics:start -->
<!-- house_prices_metrics:end -->

O conjunto final foi salvo no caminho `data/processed/house_prices_features.csv` para uso em pipelines de regressão e modelagem de séries espaciais.

<div class="page-break"></div>

## 9. Conclusão Metodológica

A exploração e a engenharia de recursos no conjunto habitacional de Ames demonstraram que transformações embasadas no conhecimento do setor imobiliário superam o emprego de variáveis brutas isoladas. A consolidação da área total no atributo sintético `TotalArea` e a mensuração precisa da defasagem temporal em `HouseAge` ampliaram a interpretabilidade e a relevância dos dados preditivos.

A convergência dos resultados do Random Forest com a decomposição do PCA confirmou que a precificação habitacional responde primariamente à escala física utilizável ponderada pela conservação ao longo do tempo. Esse diagnóstico orienta o desenvolvimento de modelos preditivos mais precisos e oferece subsídios concretos para investimentos construtivos e gestão de portfólios imobiliários.

<div class="page-break"></div>

## 10. Referências Bibliográficas

BREIMAN, Leo. Random Forests. *Machine Learning*, v. 45, n. 1, p. 5-32, 2001.

DE COCK, Dean. Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project. *Journal of Statistics Education*, v. 19, n. 3, p. 1-14, 2011.

HASTIE, Trevor; TIBSHIRANI, Robert; FRIEDMAN, Jerome. *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*. 2. ed. New York: Springer, 2009.

JOLLIFFE, Ian T.; CADIMA, Jorge. Principal component analysis: a review and recent developments. *Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences*, v. 374, n. 2065, p. 20150202, 2016.

PEDREGOSA, Fabian et al. Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, v. 12, p. 2825-2830, 2011.
