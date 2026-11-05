# Relatório Técnico: Análise Exploratória e Pré-processamento de Dados (Dataset Titanic)

**Disciplina:** Análise e Visualização de Dados (UAs 01 e 02)  
**Autores:** Diogo Galrão Carvalho, Felipe Artur Macedo Lima, Luan Cavalcante Dias Rodrigues  
**Notebook de Referência:** [notebooks/01_analise_titanic.ipynb](../notebooks/01_analise_titanic.ipynb)  
**Data:** Novembro de 2026  

---

## 1. Introdução e Apresentação do Dataset

O naufrágio do navio de passageiros RMS Titanic ocorreu na madrugada de 15 de abril de 1912 no Oceano Atlântico Norte, após colisão com um iceberg durante a viagem inaugural entre Southampton e Nova York. A tragédia resultou na morte de mais de 1.500 das 2.224 pessoas a bordo, expondo falhas estruturais nos protocolos de segurança marítima da época, sobretudo a escassez de botes salva-vidas.

A base de dados analisada reúne registros de 891 passageiros na partição de treinamento, organizados em 12 variáveis que contemplam dados cadastrais, características socioeconômicas, distribuição de cabines e informações de sobrevivência. O propósito deste trabalho é investigar os fatores determinantes da taxa de sobrevivência dos passageiros, identificar padrões de vulnerabilidade e privilégio social na evacuação, e estruturar um fluxo reproduzível de limpeza, tratamento de inconsistências, engenharia de atributos e padronização para alimentar futuros algoritmos de aprendizado supervisionado.

<div class="page-break"></div>

## 2. Classificação Minuciosa das Variáveis e Papel Analítico

Cada coluna do conjunto de dados foi classificada a partir de sua natureza matemática e de sua função operacional no estudo:

| Variável | Tipo Estatístico | Subtipo | Descrição | Papel Analítico no Estudo |
| :--- | :--- | :--- | :--- | :--- |
| `PassengerId` | Quantitativa | Discreta | Identificador numérico sequencial (1 a 891) | Chave primária cadastral sem relevância preditiva; excluída do pipeline |
| `Survived` | Qualitativa | Nominal (Binária) | Indicador de sobrevivência (0 = óbito, 1 = sobreviveu) | Variável alvo dependente da modelagem preditiva |
| `Pclass` | Qualitativa | Ordinal | Classe da passagem (1 = 1ª, 2 = 2ª, 3 = 3ª) | Estrato socioeconômico e proximidade física aos conveses superiores |
| `Name` | Qualitativa | Nominal | Nome completo do passageiro com pronome de tratamento | Identificação de laços familiares e extração de títulos honoríficos |
| `Sex` | Qualitativa | Nominal | Sexo biológico (female, male) | Preditivo central associado ao protocolo de evacuação |
| `Age` | Quantitativa | Contínua | Idade em anos (0,42 a 80 anos) | Identificação de grupos de vulnerabilidade física (crianças e idosos) |
| `SibSp` | Quantitativa | Discreta | Quantidade de cônjuges e irmãos a bordo (0 a 8) | Componente horizontal da estrutura do núcleo familiar |
| `Parch` | Quantitativa | Discreta | Quantidade de pais e filhos a bordo (0 a 6) | Componente vertical da estrutura do núcleo familiar |
| `Ticket` | Qualitativa | Nominal | Código alfanumérico da passagem | Detecção de bilhetes compartilhados e contagem de passageiros por grupo |
| `Fare` | Quantitativa | Contínua | Tarifa impressa no bilhete (0 a 512,33 libras) | Indicador financeiro que requer ajuste pelo tamanho do grupo |
| `Cabin` | Qualitativa | Nominal | Identificador da cabine e convés (ex: C85) | Registro físico da acomodação; transformado em indicador de presença |
| `Embarked` | Qualitativa | Nominal | Porto de embarque (C = Cherbourg, Q = Queenstown, S = Southampton) | Ponto logístico de partida; correlacionado à distribuição de classes |

A distinção entre variáveis conceituais e operacionais orienta o tratamento analítico. `Pclass`, apesar de registrada numericamente como 1, 2 e 3, possui ordenação hierárquica qualitativa. `Fare` e `Age` operam como métricas contínuas que exigem inspeção de distribuições de probabilidade e tratamento de escala.

<div class="page-break"></div>

## 3. Inconsistências Iniciais nos Registros e Decisões Metodológicas

A fase inicial de auditoria nos dados revelou três inconsistências que exigiram tratamento metodológico específico:

1. **Tarifas com valor zero (`Fare == 0.0`):** Foram localizados 15 passageiros com tarifa nula no registro. A inspeção nominal confirmou que se tratava de cortesias operacionais da companhia White Star Line e passagens concedidas a engenheiros da construtora naval Harland and Wolff (grupo de garantia responsável pelo acompanhamento técnico da embarcação). Como faziam parte legítima dos viajantes, essas observações foram preservadas na amostra.
2. **Bilhetes compartilhados e distorção da tarifa:** O dataset conta com 681 códigos de bilhete distintos para 891 pessoas. Vários passageiros da mesma família ou grupo compartilham o mesmo código de bilhete com o mesmo valor registrado em `Fare`. O valor de `Fare` representa a soma total do grupo e não o preço individual. Para evitar que passageiros de 3ª classe viajando em grupos numerosos aparentassem riqueza desproporcional, calculou-se a tarifa per capita `FarePorPessoa = Fare / GroupSize`.
3. **Idades fracionárias:** Sete bebês com menos de 1 ano apresentam idades decimais registradas no manifesto original (0,42 ano para 5 meses; 0,67 ano para 8 meses; 0,83 ano para 10 meses; 0,92 ano para 11 meses). Confirmou-se a veracidade histórica dos registros censitários navais britânicos, mantendo-se os números decimais sem arredondamento artificial.

<div class="page-break"></div>

## 4. Distribuição da Variável Alvo e Impacto do Desbalanceamento

A variável dependente `Survived` divide o dataset entre 549 passageiros que morreram (61,62%) e 342 passageiros que sobreviveram (38,38%).

![Distribuição da Variável Alvo](figures/titanic_target_dist.png)

A proporção observada é de aproximadamente 1,6 óbito para cada passageiro resgatado. O desbalanceamento moderado acarreta consequências metodológicas para o aprendizado de máquina:

- **Falácia da acurácia:** Um classificador ingênuo que preveja a classe majoritária (óbito) para todas as instâncias atinge 61,6% de acurácia sem extrair nenhum padrão explicativo real.
- **Seleção de métricas de avaliação:** A acurácia global torna-se insuficiente. A validação de algoritmos preditivos deve priorizar a revocação (recall) da classe minoritária, a precisão balanceada, o F1-Score harmônico e a área sob a curva ROC (ROC-AUC).
- **Ponderação de erros na função de perda:** Algoritmos como Regressão Logística, Random Forest e Support Vector Machines devem ser parametrizados com compensação de pesos (`class_weight='balanced'`), aplicando penalidades superiores aos falsos negativos.

<div class="page-break"></div>

## 5. Relações Bivariadas e Multivariadas com a Sobrevivência

A análise das variáveis explicativas comprova a influência determinante do gênero e da classe socioeconômica no resgate:

- **Sobrevivência por sexo:** As mulheres registraram taxa de sobrevivência de 74,20% (233 resgatadas em 314), enquanto os homens alcançaram 18,89% (109 resgatados em 577). A priorização feminina no carregamento dos botes operou de forma homogênea.
- **Sobrevivência por classe socioeconômica:** A 1ª classe registrou taxa de resgate de 62,96% (136 sobreviventes em 216 passageiros); a 2ª classe atingiu 47,28% (87 sobreviventes em 184 passageiros); e a 3ª classe computou apenas 24,24% (119 sobreviventes em 491 passageiros).

![Sobrevivência por Sexo e Classe](figures/titanic_survival_by_sex_pclass.png)

A interação conjunta entre sexo e classe detalha disparidades ainda mais expressivas:

- **Mulheres da 1ª classe:** 96,8% de sobrevivência (91 sobreviventes em 94).
- **Mulheres da 2ª classe:** 92,1% de sobrevivência (70 sobreviventes em 76).
- **Mulheres da 3ª classe:** 50,0% de sobrevivência (72 sobreviventes em 144).
- **Homens da 1ª classe:** 36,9% de sobrevivência (45 sobreviventes em 122).
- **Homens da 2ª classe:** 15,7% de sobrevivência (17 sobreviventes em 108).
- **Homens da 3ª classe:** 13,5% de sobrevivência (47 sobreviventes em 347).

Mesmo submetidas à diretriz de prioridade feminina, as passageiras da 3ª classe tiveram chances de resgate sensivelmente menores do que as mulheres das classes superiores, decorrência do isolamento físico das cabines nos conveses inferiores e da lentidão no acesso aos conveses de botes.

Em relação ao porto de embarque, passageiros que embarcaram em Cherbourg (C) apresentaram taxa média de sobrevivência de 55,36%, superior a Southampton (S) com 33,70% e Queenstown (Q) com 38,96%. Esse desvio é decorrente da composição socioeconômica: 50,6% dos passageiros de Cherbourg viajaram na 1ª classe, contra 19,7% de Southampton e apenas 3,9% de Queenstown.

A dinâmica dos grupos familiares (`TamanhoFamilia = SibSp + Parch + 1`) revelou que passageiros solitários (n = 1) tiveram 30,35% de sobrevivência; famílias pequenas (2 a 4 pessoas) atingiram 57,88%; e famílias extensas (5 ou mais pessoas) sofreram queda acentuada para 16,13%, refletindo o obstáculo de reunir todos os membros durante a evacuação.

![Matriz de Correlação Linear](figures/titanic_correlation_matrix.png)

<div class="page-break"></div>

## 6. Tratamento Técnico de Dados Ausentes

Apenas 3 das 12 colunas originais continham campos nulos:

- `Cabin`: 687 registros nulos (77,10% da amostra).
- `Age`: 177 registros nulos (19,87% da amostra).
- `Embarked`: 2 registros nulos (0,22% da amostra).

As estratégias de tratamento adotadas seguiram critérios técnicos fundamentados:

1. **Gestão de `Cabin`:** A exclusão da coluna original é mandatória em razão da carência de 77% dos dados. Contudo, a ausência de registro de cabine não decorre de perda aleatória; representa informação estrutural. Passageiros com cabine registrada pertenciam em sua maioria à 1ª classe e registraram taxa de sobrevivência de 66,67%, contra 29,98% daqueles sem registro. Criou-se a variável binária `TemCabine` (1 se preenchido, 0 se ausente), preservando o sinal informativo da acomodação.
2. **Gestão de `Embarked`:** As duas ausências (passageiras da 1ª classe no bilhete 113572 com tarifa 80) foram imputadas pela moda estatística `S` (Southampton, responsável por 72,4% dos embarques totais), preservando as instâncias no dataset.
3. **Gestão de `Age`:** A remoção de 177 observações provocaria o descarte de 20% do volume amostral. A imputação pela mediana geral (28 anos) achataria a variância e ignoraria que a mediana etária feminina da 1ª classe é de 35 anos (40 anos para homens), enquanto na 3ª classe é de 21,5 anos para mulheres (25 anos para homens). Aplicou-se a imputação pela mediana condicional estratificada por sexo e classe (`Sex` e `Pclass`). Adicionalmente, gerou-se o atributo `IdadeImputada` para sinalizar quais valores foram estimados.

<div class="page-break"></div>

## 7. Análise de Outliers e Engenharia de Atributos Numéricos

A inspeção da dispersão e das caixas interquartis evidenciou valores extremos na variável financeira:

![Boxplots de Detecção de Outliers](figures/titanic_boxplots_outliers.png)

O valor máximo de 512,33 libras correspondia a três bilhetes da suíte presidencial ocupada pela família Cardeza e seus assistentes. Como se tratava de registro factual verídico, os dados não foram descartados.

Para mitigar a influência das caudas longas e corrigir o viés de bilhetes familiares, realizaram-se duas transformações:

1. **Tarifa individual per capita:** `FarePorPessoa = Fare / GroupSize`, dividindo o custo pelo total de viajantes que usavam o mesmo código de bilhete.
2. **Transformação logarítmica estabilizadora:** Aplicação de `FarePorPessoa_log = np.log1p(FarePorPessoa)`. A assimetria da curva foi reduzida de 4,79 para 0,44, aproximando a variável de uma distribuição normal e eliminando a distorção de escala em modelos lineares.

Atributos de controle puramente cadastrais (`PassengerId`, `Name`, `Ticket`) foram descartados após a extração das variáveis derivadas, prevenindo sobreajuste e memorização espúria.

<div class="page-break"></div>

## 8. Codificação de Variáveis Categóricas e Fundamentação Matemática

A conversão de representações textuais em matrizes numéricas exige rigor conceitual na escolha do método:

- **Limitações do Label Encoding:** A codificação por rótulos numéricos atribui inteiros sequenciais às categorias (exemplo: Cherbourg = 0, Queenstown = 1, Southampton = 2). Essa abordagem cria uma métrica euclidiana fictícia ($2 - 0 = 2 \times (1 - 0)$), forçando o algoritmo a pressupor que a distância entre Southampton e Cherbourg seja o dobro da distância para Queenstown. Em modelos lineares, regressões logísticas e redes neurais, essa relação arbitrária corrompe a geometria do hiperplano de separação.
- **Propriedades do One-Hot Encoding:** O método projeta as $k$ categorias nominais em vetores de base canônica ortogonais no espaço $\mathbb{R}^k$, assegurando equidistância geométrica entre todos os estados qualitativos. Para evitar a armadilha das variáveis fictícias (dummy variable trap) e a colinearidade estrita na matriz de planejamento, adota-se o descarte da primeira categoria (`drop_first=True`), gerando $k-1$ colunas indicadoras binárias.

Aplicou-se One-Hot Encoding sobre `Sex` (gerando `Sex_male`), `Embarked` (gerando `Embarked_Q` e `Embarked_S`, com Cherbourg como referência) e `TipoFamilia` (gerando `TipoFamilia_Pequena` e `TipoFamilia_Sozinho`, com Família Grande como categoria base).

<div class="page-break"></div>

## 9. Normalização e Padronização Contínua

A escala das variáveis quantitativas contínuas (`Age` e `FarePorPessoa_log`) afeta diretamente algoritmos dependentes de otimização por gradiente ou cálculo de distâncias métricas (como KNN, SVM e redes neurais):

- **Min-Max Scaling:** Transforma os limites para o intervalo $[0, 1]$. Em distribuições com observações extremas, a fórmula comprime a maioria das instâncias em intervalos ínfimos, reduzindo a variância explicativa.
- **Padronização Z-Score (`StandardScaler`):** Centra a distribuição na média zero com desvio padrão unitário ($z = \frac{x - \mu}{\sigma}$). Esse procedimento assegura que o gradiente descendente avance com passos proporcionais em todos os eixos, prevenindo oscilações numéricas e dominância de variáveis com magnitudes absolutas elevadas.

<div class="page-break"></div>

## 10. Síntese do Processamento e Evidências Consolidadas

O pipeline consolidado transformou os dados originais em uma matriz inteiramente numérica com 891 registros, 11 colunas e nenhuma inconsistência ou dado ausente.

A tabela a seguir apresenta os indicadores consolidados calculados na base:

<!-- titanic_metrics:start -->
<!-- titanic_metrics:end -->

O dataset processado foi exportado para o caminho `data/processed/titanic_clean.csv`, apto a alimentar etapas de validação cruzada e treinamento preditivo.

<div class="page-break"></div>

## 11. Conclusão Metodológica

A investigação exploratória do naufrágio do Titanic comprovou que as chances individuais de sobrevivência foram condicionadas prioritariamente pelo gênero do passageiro e por sua classe socioeconômica, refletindo normas institucionais de evacuação combinadas com barreiras arquitetônicas de acesso aos conveses superiores.

O processo de engenharia de dados implementado demonstrou a importância de contextualizar decisões técnicas com conhecimento histórico: o cálculo da tarifa per capita corrigiu a distorção de bilhetes compartilhados; a retenção do registro de cabines por meio de indicador binário capturou o padrão não aleatório das omissões; e a imputação condicional da idade pela mediana de sexo e classe preservou a heterogeneidade demográfica da população original.

<div class="page-break"></div>

## 12. Referências Bibliográficas

DE COCK, Dean. Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project. *Journal of Statistics Education*, v. 19, n. 3, p. 1-14, 2011.

HASTIE, Trevor; TIBSHIRANI, Robert; FRIEDMAN, Jerome. *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*. 2. ed. New York: Springer, 2009.

JAMES, Gareth; WITTEN, Daniela; HASTIE, Trevor; TIBSHIRANI, Robert. *An Introduction to Statistical Learning: with Applications in Python*. New York: Springer, 2023.

PEDREGOSA, Fabian et al. Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, v. 12, p. 2825-2830, 2011.

WICKHAM, Hadley. Tidy Data. *Journal of Statistical Software*, v. 59, n. 10, p. 1-23, 2014.
