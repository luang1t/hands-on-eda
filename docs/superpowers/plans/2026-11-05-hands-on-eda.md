# Hands-on EDA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the `hands-on-eda` repository into a fully reproducible postgraduate project following the architecture of `bigdata_datascience`, implementing both deliveries (Titanic EDA/preprocessing and House Prices feature engineering/PCA) with automated reports, tests, and Makefile orchestration.

**Architecture:** Decouple pipeline into raw/processed datasets (`data/`), comprehensive Jupyter notebooks (`notebooks/`), headless execution and PDF report builder scripts (`scripts/`), canonical Markdown reports compiled to A4 PDFs with WeasyPrint (`reports/`), and automated regression tests (`tests/`).

**Tech Stack:** Python 3.12+, pandas, numpy, scikit-learn, matplotlib, seaborn, markdown-it-py, weasyprint, nbformat, nbconvert, make.

**Spec:** `docs/superpowers/specs/2026-11-05-hands-on-eda-design.md`

## Global Constraints

- Preserve and credit group members: Diogo Galrão Carvalho, Felipe Artur Macedo Lima e Luan Cavalcante Dias Rodrigues.
- Cover 100% of the rubric criteria from `material.pdf` (Passos 1 a 11) and `material (1).pdf` (Passos 1 a 22).
- Generate clean A4 executive PDFs matching the typography, styling, and evidence tables of `bigdata_datascience`.
- Ensure deterministic and headless execution through `Makefile` (`make run`, `make test`, `make reports`, `make notebooks`).
- All written Portuguese prose must strictly follow Humanizer guidelines (no artificial fillers, no unwarranted em-dashes, direct technical clarity).

## Review Focus

- Missing values in `Age` (19.9%) and `Fare` group tickets in Titanic must be documented with clear rationale rather than naive deletion.
- Structural absence in House Prices (`Alley`, `PoolQC`, `Fence`) must be converted to explicit 'No*' categories rather than treated as random missing data.
- Feature importance in House Prices must compare original vs engineered variables (`TotalArea`, `HouseAge`, `IsRemodeled`).
- PCA projection must evaluate whether PC1 and PC2 separate houses by quality clusters (`OverallQual`).
- PDF compilation must succeed gracefully in standard environments, generating non-empty valid documents.

---

### Task 1: Environment Setup, Dependencies and Makefile Configuration

**Files:**
- Create: `Makefile`
- Create: `requirements.txt`
- Modify: `pyproject.toml`
- Create: `.gitignore`

**Interfaces:**
- Consumes: Project configuration and dependency specifications.
- Produces: Standard build and execution commands (`make run`, `make test`, `make reports`, `make notebooks`, `make clean`).

- [ ] **Step 1: Create requirements.txt with all required packages**
- [ ] **Step 2: Update pyproject.toml to reflect standard python floor (>=3.12) and all dependencies**
- [ ] **Step 3: Create .gitignore ignoring __pycache__, .venv, .ipynb_checkpoints, .DS_Store, and temporary build outputs**
- [ ] **Step 4: Create Makefile with standard targets matching bigdata_datascience**
- [ ] **Step 5: Verify make targets with dry-run (`make -n test`)**
- [ ] **Step 6: Commit changes**

---

### Task 2: Data Acquisition and Raw Datasets Storage

**Files:**
- Create: `data/raw/titanic.csv`
- Create: `data/raw/house_prices.csv`
- Create: `data/raw/README.md`
- Create: `tests/test_data.py`

**Interfaces:**
- Consumes: Kaggle Titanic dataset and Ames House Prices dataset.
- Produces: Persistent raw datasets with known row/column counts and SHA-256 provenance.

- [ ] **Step 1: Write test in tests/test_data.py verifying existence, row counts, and columns of raw datasets**
- [ ] **Step 2: Run test to verify it fails (files do not exist yet)**
- [ ] **Step 3: Extract/download titanic.csv (891 rows, 12 cols) and house_prices.csv (1460 rows, 81 cols) to data/raw/**
- [ ] **Step 4: Document data origin, dates, and SHA-256 hashes in data/raw/README.md**
- [ ] **Step 5: Run tests/test_data.py and verify PASS**
- [ ] **Step 6: Commit changes**

---

### Task 3: Notebook 01: Complete Titanic EDA and Preprocessing (UA 01 e UA 02)

**Files:**
- Move & Enhance: `src/analise_titanic.ipynb` -> `notebooks/01_analise_titanic.ipynb`
- Create: `data/processed/titanic_clean.csv`
- Create: `reports/evidence/titanic_metrics.json`
- Create: `reports/evidence/figures/titanic_*.png`

**Interfaces:**
- Consumes: `data/raw/titanic.csv`.
- Produces: Executed notebook covering Steps 1 to 11, processed dataset, JSON metrics, and high-res figures.

- [ ] **Step 1: Integrate Luan's existing Steps 1-3 into notebooks/01_analise_titanic.ipynb**
- [ ] **Step 2: Implement Steps 4 to 6 (Target distribution, grouped bar plots by Sex, Pclass, Embarked, multivariate analysis)**
- [ ] **Step 3: Implement Step 7 (Missing data analysis, quantification, and technical justification for imputation/retention)**
- [ ] **Step 4: Implement Step 8 (Outliers, Fare per person adjustment for group tickets, justification for dropping non-informative IDs)**
- [ ] **Step 5: Implement Step 9 (Categorical encoding comparing One-Hot vs Label Encoding with technical justification)**
- [ ] **Step 6: Implement Step 10 (Scaling with StandardScaler/MinMaxScaler and export data/processed/titanic_clean.csv)**
- [ ] **Step 7: Implement Step 11 & Export evidence (generate reports/evidence/figures/ and titanic_metrics.json)**
- [ ] **Step 8: Execute notebook and verify all cells run cleanly with saved outputs**
- [ ] **Step 9: Commit changes**

---

### Task 4: Notebook 02: House Prices Feature Engineering and Visualization (UA 03 e UA 04)

**Files:**
- Create: `notebooks/02_engenharia_recursos_house_prices.ipynb`
- Create: `data/processed/house_prices_features.csv`
- Create: `reports/evidence/house_prices_metrics.json`
- Create: `reports/evidence/figures/house_prices_*.png`

**Interfaces:**
- Consumes: `data/raw/house_prices.csv`.
- Produces: Executed notebook covering Steps 1 to 22, processed dataset, JSON metrics, and high-res figures.

- [ ] **Step 1: Implement Steps 1 to 4 (Load, info, describe, SalePrice distribution, skewness, correlation heatmap)**
- [ ] **Step 2: Implement Steps 5 to 8 (Create HouseAge, TotalArea, IsRemodeled, visual scatter/boxplots, and real estate hypotheses)**
- [ ] **Step 3: Implement Steps 9 to 13 (Ordinal mapping for ExterQual, BsmtQual, KitchenQual, OverallQual_Num boxplot, structural missing data handling)**
- [ ] **Step 4: Implement Steps 14 to 15 (Random Forest feature_importances_ ranking, top 15 features bar plot, PCA fit)**
- [ ] **Step 5: Implement Steps 16 to 18 (PC1 vs PC2 scatterplot colored by OverallQual, interpretation of dimensionality reduction)**
- [ ] **Step 6: Implement Steps 19 to 22 (Export house_prices_features.csv, synthesize conclusions, actionable business recommendations, export metrics and figures)**
- [ ] **Step 7: Execute notebook and verify all cells run cleanly with saved outputs**
- [ ] **Step 8: Commit changes**

---

### Task 5: Automation Scripts (run_notebooks.py and build_reports.py)

**Files:**
- Create: `scripts/run_notebooks.py`
- Create: `scripts/build_reports.py`
- Modify: `tests/test_data.py` (add processed data validation)

**Interfaces:**
- Consumes: `notebooks/`, `reports/*.md`, `reports/evidence/`.
- Produces: Executed notebooks and compiled `reports/*.pdf`.

- [ ] **Step 1: Write scripts/run_notebooks.py to execute notebooks deterministically via nbconvert/nbformat**
- [ ] **Step 2: Write scripts/build_reports.py with WeasyPrint and Markdown-it using bigdata_datascience A4 styling**
- [ ] **Step 3: Test running scripts/run_notebooks.py and scripts/build_reports.py**
- [ ] **Step 4: Commit changes**

---

### Task 6: Technical Reports in Markdown and PDF Compilation

**Files:**
- Create: `reports/Entrega_1_UA1_UA2_Relatorio_Tecnico.md`
- Create: `reports/Entrega_1_UA1_UA2_Relatorio_Tecnico.pdf`
- Create: `reports/Entrega_2_UA3_UA4_Relatorio_Tecnico.md`
- Create: `reports/Entrega_2_UA3_UA4_Relatorio_Tecnico.pdf`
- Create: `tests/test_reports.py`

**Interfaces:**
- Consumes: `reports/*.md`, `reports/evidence/`.
- Produces: Polished executive PDF reports matching academic rubrics.

- [ ] **Step 1: Write tests/test_reports.py verifying existence, non-empty status, and minimum size of reports and PDFs**
- [ ] **Step 2: Write reports/Entrega_1_UA1_UA2_Relatorio_Tecnico.md covering Titanic analysis with all rubrics for 5.0 pts**
- [ ] **Step 3: Write reports/Entrega_2_UA3_UA4_Relatorio_Tecnico.md covering House Prices with all rubrics for 5.0 pts**
- [ ] **Step 4: Compile PDFs via python -m scripts.build_reports**
- [ ] **Step 5: Run tests/test_reports.py and verify PASS**
- [ ] **Step 6: Commit changes**

---

### Task 7: Comprehensive README.md and Final Integration

**Files:**
- Modify: `README.md`
- Clean: Remove redundant files (e.g. initial placeholder `src/`)

**Interfaces:**
- Consumes: Complete project state and evidence.
- Produces: Professional documentation and clean Git repository.

- [ ] **Step 1: Write README.md matching bigdata_datascience format and structure**
- [ ] **Step 2: Clean up obsolete files from original scaffold**
- [ ] **Step 3: Run full verification suite (make test, make reports)**
- [ ] **Step 4: Final commit and status check**
