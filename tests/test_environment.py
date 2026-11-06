import pathlib
import unittest

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent


class TestEnvironmentConfig(unittest.TestCase):
    def test_requirements_file(self):
        req_path = ROOT_DIR / "requirements.txt"
        self.assertTrue(req_path.is_file(), "requirements.txt must exist")
        content = req_path.read_text(encoding="utf-8")
        required_packages = [
            "pandas",
            "numpy",
            "matplotlib",
            "seaborn",
            "scikit-learn",
            "markdown-it-py",
            "weasyprint",
            "nbformat",
            "nbconvert",
            "ipykernel",
        ]
        for package in required_packages:
            self.assertIn(package, content, f"{package} must be in requirements.txt")

    def test_pyproject_toml(self):
        pyproject_path = ROOT_DIR / "pyproject.toml"
        self.assertTrue(pyproject_path.is_file(), "pyproject.toml must exist")
        content = pyproject_path.read_text(encoding="utf-8")
        self.assertIn('requires-python = ">=3.12"', content)
        required_deps = [
            "pandas",
            "numpy",
            "matplotlib",
            "seaborn",
            "scikit-learn",
            "markdown-it-py",
            "weasyprint",
            "nbformat",
            "nbconvert",
            "ipykernel",
        ]
        for dep in required_deps:
            self.assertIn(dep, content, f"{dep} must be in pyproject.toml dependencies")

    def test_gitignore(self):
        gitignore_path = ROOT_DIR / ".gitignore"
        self.assertTrue(gitignore_path.is_file(), ".gitignore must exist")
        content = gitignore_path.read_text(encoding="utf-8")
        required_patterns = [
            "__pycache__",
            ".venv",
            ".ipynb_checkpoints",
            ".superpowers",
            ".DS_Store",
        ]
        for pattern in required_patterns:
            self.assertIn(pattern, content, f"{pattern} must be in .gitignore")

    def test_makefile_targets(self):
        makefile_path = ROOT_DIR / "Makefile"
        self.assertTrue(makefile_path.is_file(), "Makefile must exist")
        content = makefile_path.read_text(encoding="utf-8")
        expected_targets = [
            "all",
            "run",
            "test",
            "reports",
            "notebooks",
            "venv",
            "clean",
        ]
        for target in expected_targets:
            self.assertIn(target, content, f"Target {target} must be in Makefile")


if __name__ == "__main__":
    unittest.main()
