import csv
import hashlib
import json
import pathlib
import unittest

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DATA_DIR = ROOT_DIR / "data" / "processed"
EVIDENCE_DIR = ROOT_DIR / "reports" / "evidence"
FIGURES_DIR = EVIDENCE_DIR / "figures"

TITANIC_PATH = RAW_DATA_DIR / "titanic.csv"
HOUSE_PRICES_PATH = RAW_DATA_DIR / "house_prices.csv"
README_PATH = RAW_DATA_DIR / "README.md"

TITANIC_CLEAN_PATH = PROCESSED_DATA_DIR / "titanic_clean.csv"
TITANIC_METRICS_PATH = EVIDENCE_DIR / "titanic_metrics.json"

HOUSE_PRICES_FEATURES_PATH = PROCESSED_DATA_DIR / "house_prices_features.csv"
HOUSE_PRICES_METRICS_PATH = EVIDENCE_DIR / "house_prices_metrics.json"

TITANIC_SHA256 = "4a437fde05fe5264e1701a7387ac6fb75393772ba38bb2c9c566405af5af4bd7"
HOUSE_PRICES_SHA256 = "1e18addf81e5e4d347cc17ee6075bbe4a42b7fa26b9e5b063e8f692a5f929d41"


class TestRawDatasets(unittest.TestCase):
    def test_raw_directory_and_readme_exist(self):
        self.assertTrue(RAW_DATA_DIR.is_dir(), "data/raw directory must exist")
        self.assertTrue(README_PATH.is_file(), "data/raw/README.md must exist")

    def test_titanic_dataset_integrity(self):
        self.assertTrue(TITANIC_PATH.is_file(), "data/raw/titanic.csv must exist")

        content = TITANIC_PATH.read_bytes()
        calculated_hash = hashlib.sha256(content).hexdigest()
        self.assertEqual(
            calculated_hash,
            TITANIC_SHA256,
            f"Titanic SHA-256 mismatch: expected {TITANIC_SHA256}, got {calculated_hash}",
        )

        with open(TITANIC_PATH, mode="r", encoding="utf-8") as f:
            reader = list(csv.reader(f))

        header = reader[0]
        data_rows = reader[1:]

        self.assertEqual(len(header), 12, "Titanic dataset must have 12 columns")
        self.assertIn("Survived", header, "Titanic header must contain 'Survived' column")
        self.assertEqual(len(data_rows), 891, "Titanic dataset must have 891 rows")

    def test_house_prices_dataset_integrity(self):
        self.assertTrue(HOUSE_PRICES_PATH.is_file(), "data/raw/house_prices.csv must exist")

        content = HOUSE_PRICES_PATH.read_bytes()
        calculated_hash = hashlib.sha256(content).hexdigest()
        self.assertEqual(
            calculated_hash,
            HOUSE_PRICES_SHA256,
            f"House prices SHA-256 mismatch: expected {HOUSE_PRICES_SHA256}, got {calculated_hash}",
        )

        with open(HOUSE_PRICES_PATH, mode="r", encoding="utf-8") as f:
            reader = list(csv.reader(f))

        header = reader[0]
        data_rows = reader[1:]

        self.assertEqual(len(header), 81, "House prices dataset must have 81 columns")
        self.assertIn("SalePrice", header, "House prices header must contain 'SalePrice' column")
        self.assertEqual(len(data_rows), 1460, "House prices dataset must have 1460 rows")


class TestProcessedTitanicDataset(unittest.TestCase):
    def test_processed_titanic_file_integrity(self):
        self.assertTrue(TITANIC_CLEAN_PATH.is_file(), "data/processed/titanic_clean.csv must exist")
        with open(TITANIC_CLEAN_PATH, mode="r", encoding="utf-8") as f:
            reader = list(csv.reader(f))

        header = reader[0]
        data_rows = reader[1:]

        self.assertEqual(len(data_rows), 891, "titanic_clean.csv must contain exactly 891 rows")
        self.assertEqual(len(header), 11, "titanic_clean.csv must contain exactly 11 columns")
        self.assertIn("Survived", header, "titanic_clean.csv must retain the target column 'Survived'")

        # Ensure no null/empty string cells exist
        for row_idx, row in enumerate(data_rows):
            for col_idx, val in enumerate(row):
                self.assertTrue(
                    val != "" and val.lower() != "nan" and val.lower() != "null",
                    f"Empty or NaN cell found at row {row_idx}, column {header[col_idx]}",
                )

    def test_titanic_metrics_and_figures(self):
        self.assertTrue(TITANIC_METRICS_PATH.is_file(), "reports/evidence/titanic_metrics.json must exist")
        with open(TITANIC_METRICS_PATH, mode="r", encoding="utf-8") as f:
            metrics = json.load(f)

        self.assertEqual(metrics.get("total_passengers"), 891)
        self.assertEqual(metrics.get("survivors"), 342)
        self.assertEqual(metrics.get("non_survivors"), 549)
        self.assertAlmostEqual(metrics.get("survival_rate"), 342 / 891, places=3)
        self.assertIn("survival_by_sex", metrics)
        self.assertIn("survival_by_pclass", metrics)
        self.assertIn("missing_counts_before", metrics)
        self.assertIn("processed_shape", metrics)

        expected_figures = [
            "titanic_target_dist.png",
            "titanic_survival_by_sex_pclass.png",
            "titanic_correlation_matrix.png",
            "titanic_boxplots_outliers.png",
        ]
        for fig_name in expected_figures:
            fig_path = FIGURES_DIR / fig_name
            self.assertTrue(fig_path.is_file(), f"Figure {fig_name} must exist")
            self.assertGreater(fig_path.stat().st_size, 1000, f"Figure {fig_name} must not be empty")


class TestProcessedHousePricesDataset(unittest.TestCase):
    def test_processed_house_prices_file_integrity(self):
        self.assertTrue(
            HOUSE_PRICES_FEATURES_PATH.is_file(),
            "data/processed/house_prices_features.csv must exist",
        )
        with open(HOUSE_PRICES_FEATURES_PATH, mode="r", encoding="utf-8") as f:
            reader = list(csv.reader(f))

        header = reader[0]
        data_rows = reader[1:]

        self.assertEqual(len(data_rows), 1460, "house_prices_features.csv must contain exactly 1460 rows")
        self.assertEqual(len(header), 89, "house_prices_features.csv must contain exactly 89 columns")
        self.assertIn("SalePrice", header, "Must contain target column 'SalePrice'")

        engineered_cols = [
            "HouseAge",
            "TotalArea",
            "IsRemodeled",
            "ExterQual_Num",
            "BsmtQual_Num",
            "KitchenQual_Num",
            "PC1",
            "PC2",
        ]
        for col in engineered_cols:
            self.assertIn(col, header, f"Must contain engineered column '{col}'")

        structural_cols = ["Alley", "PoolQC", "Fence", "FireplaceQu", "GarageType"]
        for col in structural_cols:
            self.assertIn(col, header, f"Must contain structural column '{col}'")

    def test_house_prices_metrics_and_figures(self):
        self.assertTrue(
            HOUSE_PRICES_METRICS_PATH.is_file(),
            "reports/evidence/house_prices_metrics.json must exist",
        )
        with open(HOUSE_PRICES_METRICS_PATH, mode="r", encoding="utf-8") as f:
            metrics = json.load(f)

        self.assertEqual(metrics.get("total_records"), 1460)
        self.assertAlmostEqual(metrics.get("saleprice_mean"), 180921.2, places=1)
        self.assertEqual(metrics.get("saleprice_median"), 163000.0)
        self.assertAlmostEqual(metrics.get("saleprice_skew"), 1.8829, places=2)

        self.assertIn("top_correlations", metrics)
        self.assertIn("OverallQual", metrics["top_correlations"])

        self.assertIn("top_15_features", metrics)
        self.assertIn("TotalArea", metrics["top_15_features"])
        self.assertIn("OverallQual", metrics["top_15_features"])
        self.assertIn("HouseAge", metrics["top_15_features"])

        self.assertIn("pca_explained_variance_ratio", metrics)
        self.assertEqual(len(metrics["pca_explained_variance_ratio"]), 2)

        self.assertEqual(metrics.get("processed_shape"), [1460, 89])

        expected_figures = [
            "house_prices_target_dist.png",
            "house_prices_correlation_heatmap.png",
            "house_prices_engineered_features.png",
            "house_prices_overall_qual_boxplot.png",
            "house_prices_feature_importance.png",
            "house_prices_pca_scatter.png",
        ]
        for fig_name in expected_figures:
            fig_path = FIGURES_DIR / fig_name
            self.assertTrue(fig_path.is_file(), f"Figure {fig_name} must exist")
            self.assertGreater(fig_path.stat().st_size, 1000, f"Figure {fig_name} must not be empty")


if __name__ == "__main__":
    unittest.main()

