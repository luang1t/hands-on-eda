import csv
import hashlib
import pathlib
import unittest

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"

TITANIC_PATH = RAW_DATA_DIR / "titanic.csv"
HOUSE_PRICES_PATH = RAW_DATA_DIR / "house_prices.csv"
README_PATH = RAW_DATA_DIR / "README.md"

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


if __name__ == "__main__":
    unittest.main()
