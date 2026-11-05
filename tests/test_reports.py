"""Tests for technical reports and PDF compilation."""

from __future__ import annotations

import os
from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Prioritize virtualenv site-packages if running with system python
VENV_SITE_PACKAGES = (
    PROJECT_ROOT
    / ".venv"
    / "lib"
    / f"python{sys.version_info.major}.{sys.version_info.minor}"
    / "site-packages"
)
VENV_BIN = PROJECT_ROOT / ".venv" / "bin"

if VENV_SITE_PACKAGES.is_dir():
    if str(VENV_SITE_PACKAGES) not in sys.path:
        sys.path.insert(0, str(VENV_SITE_PACKAGES))
    existing_pp = os.environ.get("PYTHONPATH", "")
    if str(VENV_SITE_PACKAGES) not in existing_pp:
        os.environ["PYTHONPATH"] = (
            f"{VENV_SITE_PACKAGES}:{existing_pp}" if existing_pp else str(VENV_SITE_PACKAGES)
        )

if VENV_BIN.is_dir():
    existing_path = os.environ.get("PATH", "")
    if str(VENV_BIN) not in existing_path:
        os.environ["PATH"] = f"{VENV_BIN}:{existing_path}"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

REPORTS_DIR = PROJECT_ROOT / "reports"


class TestTitanicTechnicalReport(unittest.TestCase):
    """Validation suite for Entrega 1 (Titanic UA1/UA2) report."""

    md_path = REPORTS_DIR / "Entrega_1_UA1_UA2_Relatorio_Tecnico.md"
    pdf_path = REPORTS_DIR / "Entrega_1_UA1_UA2_Relatorio_Tecnico.pdf"

    def test_markdown_file_exists_and_not_empty(self):
        self.assertTrue(self.md_path.is_file(), f"Arquivo não encontrado: {self.md_path}")
        size = self.md_path.stat().st_size
        self.assertGreater(size, 2000, f"Arquivo Markdown muito pequeno ({size} bytes)")

    def test_markdown_metadata_and_authors(self):
        if not self.md_path.is_file():
            self.skipTest("Arquivo Markdown ainda não existe.")
        content = self.md_path.read_text(encoding="utf-8")
        self.assertIn("Diogo Galrão Carvalho", content)
        self.assertIn("Felipe Artur Macedo Lima", content)
        self.assertIn("Luan Cavalcante Dias Rodrigues", content)
        self.assertIn("notebooks/01_analise_titanic.ipynb", content)

    def test_markdown_rubric_sections(self):
        if not self.md_path.is_file():
            self.skipTest("Arquivo Markdown ainda não existe.")
        content = self.md_path.read_text(encoding="utf-8")
        required_terms = [
            "Introdução",
            "Classificação",
            "Survived",
            "titanic_survival_by_sex_pclass",
            "Cabin",
            "Age",
            "Embarked",
            "One-Hot",
            "StandardScaler",
            "<!-- titanic_metrics:start -->",
            "<!-- titanic_metrics:end -->",
            "Referências",
        ]
        for term in required_terms:
            self.assertIn(term, content, f"Termo obrigatório '{term}' ausente no relatório Titanic.")

    def test_pdf_exists_and_valid(self):
        self.assertTrue(self.pdf_path.is_file(), f"PDF não encontrado: {self.pdf_path}")
        size_kb = self.pdf_path.stat().st_size / 1024
        self.assertGreater(size_kb, 15.0, f"PDF menor que 15 KB ({size_kb:.1f} KB)")
        with open(self.pdf_path, "rb") as f:
            header = f.read(5)
        self.assertEqual(header, b"%PDF-", "Cabeçalho binário do PDF inválido")


class TestHousePricesTechnicalReport(unittest.TestCase):
    """Validation suite for Entrega 2 (House Prices UA3/UA4) report."""

    md_path = REPORTS_DIR / "Entrega_2_UA3_UA4_Relatorio_Tecnico.md"
    pdf_path = REPORTS_DIR / "Entrega_2_UA3_UA4_Relatorio_Tecnico.pdf"

    def test_markdown_file_exists_and_not_empty(self):
        self.assertTrue(self.md_path.is_file(), f"Arquivo não encontrado: {self.md_path}")
        size = self.md_path.stat().st_size
        self.assertGreater(size, 2000, f"Arquivo Markdown muito pequeno ({size} bytes)")

    def test_markdown_metadata_and_authors(self):
        if not self.md_path.is_file():
            self.skipTest("Arquivo Markdown ainda não existe.")
        content = self.md_path.read_text(encoding="utf-8")
        self.assertIn("Diogo Galrão Carvalho", content)
        self.assertIn("Felipe Artur Macedo Lima", content)
        self.assertIn("Luan Cavalcante Dias Rodrigues", content)
        self.assertIn("notebooks/02_engenharia_recursos_house_prices.ipynb", content)

    def test_markdown_rubric_sections(self):
        if not self.md_path.is_file():
            self.skipTest("Arquivo Markdown ainda não existe.")
        content = self.md_path.read_text(encoding="utf-8")
        required_terms = [
            "SalePrice",
            "HouseAge",
            "TotalArea",
            "IsRemodeled",
            "OverallQual",
            "Random Forest",
            "PCA",
            "<!-- house_prices_metrics:start -->",
            "<!-- house_prices_metrics:end -->",
            "Recomendações",
            "Referências",
        ]
        for term in required_terms:
            self.assertIn(term, content, f"Termo obrigatório '{term}' ausente no relatório House Prices.")

    def test_pdf_exists_and_valid(self):
        self.assertTrue(self.pdf_path.is_file(), f"PDF não encontrado: {self.pdf_path}")
        size_kb = self.pdf_path.stat().st_size / 1024
        self.assertGreater(size_kb, 15.0, f"PDF menor que 15 KB ({size_kb:.1f} KB)")
        with open(self.pdf_path, "rb") as f:
            header = f.read(5)
        self.assertEqual(header, b"%PDF-", "Cabeçalho binário do PDF inválido")


if __name__ == "__main__":
    unittest.main()
