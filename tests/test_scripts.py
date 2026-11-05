"""Tests for automated execution scripts and PDF report builder."""

from __future__ import annotations

import os
from pathlib import Path
import sys
import tempfile
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

from scripts import build_reports, run_notebooks


class TestRunNotebooksScript(unittest.TestCase):
    def test_discover_notebooks_in_project(self):
        notebooks = run_notebooks.discover_notebooks()
        names = [nb.name for nb in notebooks]
        self.assertIn("01_analise_titanic.ipynb", names)
        self.assertIn("02_engenharia_recursos_house_prices.ipynb", names)
        self.assertEqual(names, sorted(names))

    def test_discover_notebooks_non_existent_dir(self):
        result = run_notebooks.discover_notebooks(PROJECT_ROOT / "non_existent_directory_xyz")
        self.assertEqual(result, [])

    def test_run_all_notebooks_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            results = run_notebooks.run_all_notebooks(notebooks_dir=tmpdir)
            self.assertEqual(results, [])

    def test_execute_notebook_minimal(self):
        import nbformat

        with tempfile.TemporaryDirectory() as tmpdir:
            nb_path = Path(tmpdir) / "test_dummy.ipynb"
            nb = nbformat.v4.new_notebook()
            nb.cells.append(nbformat.v4.new_code_cell("result = 7 * 6\nprint(result)"))
            with open(nb_path, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)

            elapsed = run_notebooks.execute_notebook(
                nb_path,
                project_root=tmpdir,
                timeout=60,
                kernel_name="python3",
            )
            self.assertGreater(elapsed, 0.0)

            # Re-read notebook to verify output execution
            with open(nb_path, "r", encoding="utf-8") as f:
                executed_nb = nbformat.read(f, as_version=4)

            self.assertEqual(len(executed_nb.cells[0].outputs), 1)
            self.assertIn("42", executed_nb.cells[0].outputs[0].text)


class TestBuildReportsScript(unittest.TestCase):
    def test_css_styling_structure(self):
        css = build_reports.CSS_STYLE
        self.assertIn("@page", css)
        self.assertIn("size: A4", css)
        self.assertIn("counter(page)", css)
        self.assertIn("Liberation Serif", css)
        self.assertIn("DejaVu Sans", css)
        self.assertIn("DejaVu Sans Mono", css)
        self.assertIn("page-break-inside: avoid", css)
        self.assertIn(".page-break", css)

    def test_markdown_to_html_rendering(self):
        md_text = (
            "# Título Principal\n\n"
            "Parágrafo introdutório com **ênfase**.\n\n"
            "| Item | Valor |\n"
            "| :--- | :--- |\n"
            "| Alpha | 100 |\n"
        )
        html = build_reports.markdown_to_html(md_text)
        self.assertIn("<h1>Título Principal</h1>", html)
        self.assertIn("<p>Parágrafo introdutório", html)
        self.assertIn("<table>", html)
        self.assertIn(">Item</th>", html)
        self.assertIn(">Alpha</td>", html)

    def test_inject_evidence_titanic(self):
        template = (
            "Antes\n"
            "<!-- titanic_metrics:start -->\n"
            "Original\n"
            "<!-- titanic_metrics:end -->\n"
            "Depois"
        )
        injected = build_reports.inject_evidence(template)
        self.assertIn("Total de Passageiros Analisados", injected)
        self.assertIn("891", injected)
        self.assertIn("Taxa de Sobrevivência Feminina", injected)
        self.assertIn("74.20%", injected)

    def test_inject_evidence_house_prices(self):
        template = (
            "Antes\n"
            "<!-- house_prices_metrics:start -->\n"
            "Original\n"
            "<!-- house_prices_metrics:end -->\n"
            "Depois"
        )
        injected = build_reports.inject_evidence(template)
        self.assertIn("Preço Médio de Venda (SalePrice)", injected)
        self.assertIn("US$ 180,921.20", injected)
        self.assertIn("OverallQual", injected)
        self.assertIn("Variância Explicada pelo PC1", injected)
        self.assertIn("35.79%", injected)

    def test_normalize_image_paths(self):
        raw_html = '<img src="figures/grafico.png" alt="Grafico">'
        normalized = build_reports.normalize_image_paths(raw_html)
        self.assertEqual(normalized, '<img src="evidence/figures/grafico.png" alt="Grafico">')

    def test_build_html_document(self):
        doc = build_reports.build_html_document("<p>Conteúdo</p>", title="Teste")
        self.assertIn("<!DOCTYPE html>", doc)
        self.assertIn("<title>Teste</title>", doc)
        self.assertIn("<style>", doc)
        self.assertIn("<p>Conteúdo</p>", doc)

    def test_compile_markdown_to_pdf_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = Path(tmpdir) / "test_report.md"
            pdf_path = Path(tmpdir) / "test_report.pdf"

            md_content = (
                "# Relatório de Teste\n\n"
                "Verificação da compilação de PDF com WeasyPrint.\n\n"
                "<!-- titanic_metrics:start -->\n"
                "Placeholder\n"
                "<!-- titanic_metrics:end -->\n\n"
                "| Indicador | Avaliação |\n"
                "| :--- | :--- |\n"
                "| Status | Aprovado |\n"
            )
            md_path.write_text(md_content, encoding="utf-8")

            compiled_pdf = build_reports.compile_markdown_to_pdf(md_path, pdf_path)
            self.assertTrue(compiled_pdf.is_file())
            self.assertGreater(compiled_pdf.stat().st_size, 2000)

            # Check PDF binary header
            header = compiled_pdf.read_bytes()[:5]
            self.assertEqual(header, b"%PDF-")

    def test_build_all_reports_empty_when_no_reports(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            compiled = build_reports.build_all_reports(reports_dir=tmpdir)
            self.assertEqual(compiled, [])


if __name__ == "__main__":
    unittest.main()
