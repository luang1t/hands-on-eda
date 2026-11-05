"""Headless Jupyter notebook execution module.

Discovers and executes notebooks in place using nbformat and nbconvert's
ExecutePreprocessor, ensuring deterministic execution from PROJECT_ROOT.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Ensure virtualenv site-packages and binaries are prioritized if running in system python
venv_lib = PROJECT_ROOT / ".venv" / "lib"
if venv_lib.exists():
    for sp in venv_lib.glob("python*/site-packages"):
        if sp.exists() and str(sp) not in sys.path:
            sys.path.insert(0, str(sp))

VENV_BIN = PROJECT_ROOT / ".venv" / "bin"
if VENV_BIN.is_dir():
    existing_path = os.environ.get("PATH", "")
    if str(VENV_BIN) not in existing_path:
        os.environ["PATH"] = f"{VENV_BIN}:{existing_path}"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def discover_notebooks(directory: Path | str | None = None) -> list[Path]:
    """Discover all .ipynb files in target directory, excluding checkpoints."""
    search_dir = Path(directory).resolve() if directory else NOTEBOOKS_DIR
    if not search_dir.is_dir():
        return []
    notebooks = [
        path
        for path in search_dir.glob("*.ipynb")
        if not path.name.startswith(".") and ".ipynb_checkpoints" not in str(path)
    ]
    return sorted(notebooks, key=lambda p: p.name)


def execute_notebook(
    notebook_path: Path | str,
    project_root: Path | str | None = None,
    timeout: int = 600,
    kernel_name: str = "python3",
) -> float:
    """Execute a single notebook headlessly and save it in place with outputs."""
    nb_path = Path(notebook_path).resolve()
    if not nb_path.is_file():
        raise FileNotFoundError(f"Notebook file not found: {nb_path}")

    root = Path(project_root).resolve() if project_root else PROJECT_ROOT

    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor

    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=timeout, kernel_name=kernel_name)
    start_time = time.time()
    ep.preprocess(nb, {"metadata": {"path": str(root)}})
    elapsed = time.time() - start_time

    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    return elapsed


def run_all_notebooks(
    notebooks_dir: Path | str | None = None,
    project_root: Path | str | None = None,
    timeout: int = 600,
    kernel_name: str = "python3",
) -> list[tuple[Path, float]]:
    """Discover and execute all notebooks in order, returning timing stats."""
    notebooks = discover_notebooks(notebooks_dir)
    if not notebooks:
        print("[run_notebooks] Nenhum notebook encontrado.")
        return []

    results: list[tuple[Path, float]] = []
    print(f"[run_notebooks] Executando {len(notebooks)} notebook(s)...")

    for nb_path in notebooks:
        print(f" -> Executando: {nb_path.name}...")
        elapsed = execute_notebook(
            nb_path,
            project_root=project_root,
            timeout=timeout,
            kernel_name=kernel_name,
        )
        print(f"    Concluído em {elapsed:.2f}s")
        results.append((nb_path, elapsed))

    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Executa notebooks Jupyter do projeto hands-on-eda de forma automatizada."
    )
    parser.add_argument(
        "--notebook",
        "-n",
        type=str,
        default=None,
        help="Caminho para um notebook específico a executar.",
    )
    parser.add_argument(
        "--dir",
        "-d",
        type=str,
        default=None,
        help="Diretório contendo os notebooks (padrão: notebooks/).",
    )
    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        default=600,
        help="Timeout máximo por célula em segundos (padrão: 600).",
    )
    parser.add_argument(
        "--kernel",
        "-k",
        type=str,
        default="python3",
        help="Nome do kernel do Jupyter (padrão: python3).",
    )

    args = parser.parse_args()

    try:
        if args.notebook:
            target = Path(args.notebook)
            print(f"[run_notebooks] Executando notebook individual: {target.name}...")
            elapsed = execute_notebook(
                target,
                timeout=args.timeout,
                kernel_name=args.kernel,
            )
            print(f"[run_notebooks] Concluído em {elapsed:.2f}s")
        else:
            run_all_notebooks(
                notebooks_dir=args.dir,
                timeout=args.timeout,
                kernel_name=args.kernel,
            )
        return 0
    except Exception as exc:
        print(f"[run_notebooks] Erro durante execução: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
