# Raw datasets

This directory stores the immutable raw datasets used in the exploratory data analyses.

## Summary

| Dataset | File | Records | Columns | SHA-256 checksum |
|---|---|---|---|---|
| Titanic | titanic.csv | 891 | 12 | 4a437fde05fe5264e1701a7387ac6fb75393772ba38bb2c9c566405af5af4bd7 |
| Ames House Prices | house_prices.csv | 1460 | 81 | 1e18addf81e5e4d347cc17ee6075bbe4a42b7fa26b9e5b063e8f692a5f929d41 |

As URLs abaixo foram consultadas em 6 nov. 2026; os arquivos remotos tinham os mesmos hashes das cópias locais nessa data.

## Dataset provenance

### Titanic
- Source URL: https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
- Original notebook source: https://www.kaggle.com/datasets/yasserh/titanic-dataset
- Comparison on 6 Nov 2026: the Kaggle CSV and this copy have identical content after normalizing line endings. Kaggle uses CRLF and this copy uses LF; both contain the same 891 rows and 12 columns.
- SHA-256 of the Kaggle CSV: `7d118fef8b6ccf7f81111877bc388536f7b1e498a655e3d649d19aaa010e9f6f`.
- Target variable: Survived (binary classification)
- Dimensions: 891 observation rows, 12 feature columns

### Ames House Prices
- Source URL: https://raw.githubusercontent.com/krishnaik06/Advanced-House-Price-Prediction-/master/train.csv
- Background: Ames Housing, described by Dean De Cock: https://jse.amstat.org/v19n3/decock.pdf
- Target variable: SalePrice (continuous regression)
- Dimensions: 1460 observation rows, 81 feature columns
