"""PDF report builder for hands-on-eda technical reports.

Parses Markdown with markdown-it-py (commonmark + tables), injects dynamic
evidence tables from JSON files, and compiles publication-quality A4 PDFs
using WeasyPrint and clean CSS typography.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
EVIDENCE_DIR = REPORTS_DIR / "evidence"

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

REPORT_TARGETS = [
    ("Entrega_1_UA1_UA2_Relatorio_Tecnico.md", "Entrega_1_UA1_UA2_Relatorio_Tecnico.pdf"),
    ("Entrega_2_UA3_UA4_Relatorio_Tecnico.md", "Entrega_2_UA3_UA4_Relatorio_Tecnico.pdf"),
]

CSS_STYLE = """
@page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
    @bottom-center {
        content: counter(page);
        font-size: 9pt;
        font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
        color: #555555;
    }
    @top-right {
        content: "Hands-on EDA | Relatório Técnico";
        font-size: 8pt;
        font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
        color: #777777;
    }
}

body {
    font-family: 'Liberation Serif', 'DejaVu Serif', serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #222222;
    text-align: justify;
    hyphens: auto;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    color: #1a1a1a;
    page-break-after: avoid;
    break-after: avoid;
    font-weight: 600;
}

h1 {
    font-size: 18pt;
    border-bottom: 2px solid #204a87;
    padding-bottom: 4px;
    margin-top: 0;
    margin-bottom: 14px;
}

h2 {
    font-size: 13.5pt;
    border-bottom: 1px solid #d0d7de;
    padding-bottom: 3px;
    margin-top: 18px;
    margin-bottom: 10px;
}

h3 {
    font-size: 11pt;
    margin-top: 14px;
    margin-bottom: 6px;
}

p {
    margin-top: 0;
    margin-bottom: 8px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9pt;
    font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif;
    page-break-inside: avoid;
    break-inside: avoid;
}

th, td {
    border: 1px solid #d0d7de;
    padding: 6px 9px;
    text-align: left;
    vertical-align: top;
}

th {
    background-color: #f6f8fa;
    font-weight: 600;
    color: #1f2328;
}

tr:nth-child(even) td {
    background-color: #fafbfc;
}

code {
    font-family: 'DejaVu Sans Mono', monospace;
    font-size: 8.5pt;
    background-color: #f6f8fa;
    padding: 1px 4px;
    border-radius: 3px;
    border: 1px solid #e1e4e8;
}

pre {
    font-family: 'DejaVu Sans Mono', monospace;
    font-size: 8pt;
    line-height: 1.4;
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 4px;
    padding: 8px 12px;
    overflow-x: auto;
    white-space: pre-wrap;
    word-wrap: break-word;
    page-break-inside: avoid;
    break-inside: avoid;
    margin: 10px 0;
}

pre code {
    background-color: transparent;
    padding: 0;
    border: none;
}

blockquote {
    border-left: 3px solid #204a87;
    margin: 10px 0;
    padding: 6px 12px;
    color: #444444;
    background-color: #f0f4f8;
    page-break-inside: avoid;
    break-inside: avoid;
}

img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 12px auto;
    page-break-inside: avoid;
    break-inside: avoid;
}

hr {
    border: 0;
    border-top: 1px solid #d0d7de;
    margin: 16px 0;
}

.page-break {
    page-break-after: always;
    break-after: always;
}
"""


def _generate_titanic_metrics_table(evidence_path: Path) -> str:
    """Generate Markdown table from titanic_metrics.json."""
    if not evidence_path.is_file():
        return ""
    with open(evidence_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = data.get("total_passengers", 0)
    survivors = data.get("survivors", 0)
    non_survivors = data.get("non_survivors", 0)
    rate = data.get("survival_rate", 0.0) * 100
    by_sex = data.get("survival_by_sex", {})
    by_pclass = data.get("survival_by_pclass", {})
    missing = data.get("missing_counts_before", {})
    shape = data.get("processed_shape", [0, 0])

    rows = [
        "| Métrica Analítica | Valor Observado |",
        "| :--- | :--- |",
        f"| Total de Passageiros Analisados | {total} |",
        f"| Sobreviventes | {survivors} ({rate:.2f}%) |",
        f"| Não Sobreviventes (Óbitos) | {non_survivors} ({100 - rate:.2f}%) |",
        f"| Taxa de Sobrevivência Feminina | {by_sex.get('female', 0.0) * 100:.2f}% |",
        f"| Taxa de Sobrevivência Masculina | {by_sex.get('male', 0.0) * 100:.2f}% |",
        f"| Taxa Sobrevivência - 1ª Classe | {by_pclass.get('1', 0.0) * 100:.2f}% |",
        f"| Taxa Sobrevivência - 2ª Classe | {by_pclass.get('2', 0.0) * 100:.2f}% |",
        f"| Taxa Sobrevivência - 3ª Classe | {by_pclass.get('3', 0.0) * 100:.2f}% |",
        f"| Nulos Iniciais em Cabine (Cabin) | {missing.get('Cabin', 0)} |",
        f"| Nulos Iniciais em Idade (Age) | {missing.get('Age', 0)} |",
        f"| Nulos Iniciais em Embarque (Embarked) | {missing.get('Embarked', 0)} |",
        f"| Dimensão do Dataset Limpo | {shape[0]} linhas × {shape[1]} colunas |",
    ]
    return "\n" + "\n".join(rows) + "\n"


def _generate_house_prices_metrics_table(evidence_path: Path) -> str:
    """Generate Markdown table from house_prices_metrics.json."""
    if not evidence_path.is_file():
        return ""
    with open(evidence_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = data.get("total_records", 0)
    mean_price = data.get("saleprice_mean", 0.0)
    med_price = data.get("saleprice_median", 0.0)
    std_price = data.get("saleprice_std", 0.0)
    skew = data.get("saleprice_skew", 0.0)
    top_corr = data.get("top_correlations", {})
    top_feat = data.get("top_15_features", {})
    pca_var = data.get("pca_explained_variance_ratio", [0.0, 0.0])
    shape = data.get("processed_shape", [0, 0])

    pc1_pct = (pca_var[0] if len(pca_var) > 0 else 0.0) * 100
    pc2_pct = (pca_var[1] if len(pca_var) > 1 else 0.0) * 100
    pca_total = pc1_pct + pc2_pct

    rows = [
        "| Indicador Metodológico | Valor Calculado |",
        "| :--- | :--- |",
        f"| Total de Imóveis no Registro | {total} |",
        f"| Preço Médio de Venda (SalePrice) | US$ {mean_price:,.2f} |",
        f"| Preço Mediano de Venda (SalePrice) | US$ {med_price:,.2f} |",
        f"| Desvio Padrão (SalePrice) | US$ {std_price:,.2f} |",
        f"| Assimetria da Distribuição Original | {skew:.4f} (Positiva acentuada) |",
        f"| Maior Correlação Linear com Preço | OverallQual (r = {top_corr.get('OverallQual', 0.0):.4f}) |",
        f"| Segunda Maior Correlação com Preço | GrLivArea (r = {top_corr.get('GrLivArea', 0.0):.4f}) |",
        f"| Variável Mais Importante (Random Forest) | TotalArea ({top_feat.get('TotalArea', 0.0) * 100:.2f}%) |",
        f"| Segunda Variável Mais Importante | OverallQual ({top_feat.get('OverallQual', 0.0) * 100:.2f}%) |",
        f"| Variância Explicada pelo PC1 | {pc1_pct:.2f}% (Tamanho e Construtora) |",
        f"| Variância Explicada pelo PC2 | {pc2_pct:.2f}% (Idade vs Conservação) |",
        f"| Variância Retida no Plano (PC1 + PC2) | {pca_total:.2f}% |",
        f"| Dimensões do Dataset com Features | {shape[0]} linhas × {shape[1]} colunas |",
    ]
    return "\n" + "\n".join(rows) + "\n"


def _generate_generic_json_table(evidence_path: Path) -> str:
    """Generate generic Markdown table from any JSON dictionary."""
    if not evidence_path.is_file():
        return ""
    with open(evidence_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        return ""

    rows = ["| Chave | Valor |", "| :--- | :--- |"]
    for k, v in data.items():
        if isinstance(v, (int, float, str, bool)):
            rows.append(f"| {k} | {v} |")
        elif isinstance(v, list):
            rows.append(f"| {k} | {', '.join(str(x) for x in v)} |")
    return "\n" + "\n".join(rows) + "\n"


def inject_evidence(markdown_text: str, evidence_dir: Path | str | None = None) -> str:
    """Inject dynamic evidence tables into markdown comments.

    Replaces blocks like:
        <!-- section_name:start -->
        ...
        <!-- section_name:end -->
    with formatted evidence content if available.
    """
    ev_dir = Path(evidence_dir).resolve() if evidence_dir else EVIDENCE_DIR

    pattern = re.compile(
        r"<!--\s*([a-zA-Z0-9_-]+):start\s*-->(.*?)<!--\s*\1:end\s*-->",
        re.DOTALL,
    )

    def replacer(match: re.Match) -> str:
        section = match.group(1).strip()
        original_body = match.group(2)

        if section == "titanic_metrics":
            content = _generate_titanic_metrics_table(ev_dir / "titanic_metrics.json")
            if content:
                return f"<!-- {section}:start -->\n{content}\n<!-- {section}:end -->"

        elif section == "house_prices_metrics":
            content = _generate_house_prices_metrics_table(ev_dir / "house_prices_metrics.json")
            if content:
                return f"<!-- {section}:start -->\n{content}\n<!-- {section}:end -->"

        elif (ev_dir / f"{section}.json").is_file():
            content = _generate_generic_json_table(ev_dir / f"{section}.json")
            if content:
                return f"<!-- {section}:start -->\n{content}\n<!-- {section}:end -->"

        return f"<!-- {section}:start -->{original_body}<!-- {section}:end -->"

    return pattern.sub(replacer, markdown_text)


def markdown_to_html(markdown_content: str) -> str:
    """Render Markdown content to HTML using markdown-it-py with tables."""
    from markdown_it import MarkdownIt

    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    return md.render(markdown_content)


def normalize_image_paths(html: str) -> str:
    """Ensure image src references resolve properly relative to reports directory.

    Replaces src='figures/...' with src='evidence/figures/...' if evidence/figures exists.
    """
    pattern = re.compile(r'src=["\']figures/([^"\']+)["\']')
    return pattern.sub(r'src="evidence/figures/\1"', html)


def build_html_document(body_html: str, title: str = "Relatório Técnico", css: str | None = None) -> str:
    """Wrap body HTML into a complete HTML document with A4 CSS."""
    used_css = css if css is not None else CSS_STYLE
    normalized_body = normalize_image_paths(body_html)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
{used_css}
</style>
</head>
<body>
{normalized_body}
</body>
</html>"""


def compile_markdown_to_pdf(
    markdown_path: Path | str,
    pdf_path: Path | str | None = None,
    evidence_dir: Path | str | None = None,
) -> Path:
    """Compile Markdown file to PDF with dynamic injection and WeasyPrint."""
    md_file = Path(markdown_path).resolve()
    if not md_file.is_file():
        raise FileNotFoundError(f"Arquivo Markdown não encontrado: {md_file}")

    target_pdf = Path(pdf_path).resolve() if pdf_path else md_file.with_suffix(".pdf")

    # Read markdown and inject evidence
    raw_md = md_file.read_text(encoding="utf-8")
    injected_md = inject_evidence(raw_md, evidence_dir=evidence_dir)

    # Convert to HTML and wrap
    body_html = markdown_to_html(injected_md)
    title = md_file.stem.replace("_", " ")
    full_html = build_html_document(body_html, title=title)

    # Compile with WeasyPrint
    import weasyprint

    html_obj = weasyprint.HTML(string=full_html, base_url=str(md_file.parent))
    html_obj.write_pdf(target=str(target_pdf))

    return target_pdf


def build_all_reports(reports_dir: Path | str | None = None) -> list[Path]:
    """Find and compile canonical reports if they exist."""
    rep_dir = Path(reports_dir).resolve() if reports_dir else REPORTS_DIR
    compiled: list[Path] = []

    print("[build_reports] Iniciando compilação de relatórios técnicos...")
    for md_name, pdf_name in REPORT_TARGETS:
        md_file = rep_dir / md_name
        pdf_file = rep_dir / pdf_name
        if md_file.is_file():
            print(f" -> Compilando {md_name} para {pdf_name}...")
            out_pdf = compile_markdown_to_pdf(md_file, pdf_file)
            size_kb = out_pdf.stat().st_size / 1024
            print(f"    Gerado com sucesso: {pdf_name} ({size_kb:.1f} KB)")
            compiled.append(out_pdf)
        else:
            print(f" -- Arquivo de relatório não encontrado, ignorado: {md_name}")

    return compiled


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compila relatórios técnicos em Markdown para PDF via WeasyPrint."
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        default=None,
        help="Arquivo Markdown específico a compilar.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Caminho do PDF de saída.",
    )
    parser.add_argument(
        "--dir",
        "-d",
        type=str,
        default=None,
        help="Diretório dos relatórios (padrão: reports/).",
    )

    args = parser.parse_args()

    try:
        if args.file:
            md_path = Path(args.file)
            out_pdf = compile_markdown_to_pdf(md_path, args.output)
            print(f"[build_reports] PDF compilado: {out_pdf}")
        else:
            compiled = build_all_reports(args.dir)
            if not compiled:
                print("[build_reports] Nenhum relatório foi compilado (arquivos fonte ainda não existem).")
            else:
                print(f"[build_reports] Total de {len(compiled)} relatório(s) compilado(s).")
        return 0
    except Exception as exc:
        print(f"[build_reports] Erro durante compilação: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
