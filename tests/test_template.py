"""Tests for the cookiecutter template itself."""

import json
import tempfile
import unittest
from pathlib import Path

from cookiecutter.main import cookiecutter

TEMPLATE_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = TEMPLATE_ROOT / "{{cookiecutter.project_name}}"

REQUIRED_PROMPTS = {
    "full_name",
    "email",
    "project_short_description",
    "organization_name",
    "project_name",
}


class TestTemplateFiles(unittest.TestCase):
    """The template structure is intact."""

    def test_cookiecutter_json_is_valid(self) -> None:
        """cookiecutter.json parses and exposes the required prompts."""
        config = json.loads((TEMPLATE_ROOT / "cookiecutter.json").read_text())
        missing = REQUIRED_PROMPTS - set(config)
        self.assertEqual(missing, set())

    def test_expected_template_files_exist(self) -> None:
        """The files every generated project relies on are present."""
        expected = [
            TEMPLATE_DIR / "pyproject.toml",
            TEMPLATE_DIR / ".github" / "workflows" / "tests.yml",
            TEMPLATE_DIR / ".github" / "workflows" / "release.yml",
            TEMPLATE_DIR / "src" / "{{cookiecutter.project_slug}}" / "__init__.py",
            TEMPLATE_DIR / "src" / "{{cookiecutter.project_slug}}" / "dependencies.py",
        ]
        for path in expected:
            with self.subTest(path=str(path)):
                self.assertTrue(path.is_file(), f"missing: {path}")

    def test_no_tests_generated(self) -> None:
        """Generated projects no longer include a tests directory."""
        self.assertFalse((TEMPLATE_DIR / "tests").exists())


class TestTemplateRender(unittest.TestCase):
    """The template renders into a valid project."""

    def render(self, tmp: Path) -> Path:
        """Render the template with no input and return the project path."""
        project = cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            extra_context={
                "full_name": "Test User",
                "email": "test@example.com",
                "project_short_description": "A test package",
                "organization_name": "test-org",
                "project_name": "Test Package",
                "generate_into_current_dir": "no",
            },
            output_dir=str(tmp),
        )
        return Path(project)

    def test_render_produces_expected_files(self) -> None:
        """Rendering yields pyproject.toml, package and workflows."""
        with tempfile.TemporaryDirectory() as tmp:
            project = self.render(Path(tmp))
            self.assertTrue((project / "pyproject.toml").is_file())
            self.assertTrue((project / "src" / "test_package" / "__init__.py").is_file())
            self.assertTrue((project / "src" / "test_package" / "dependencies.py").is_file())
            self.assertTrue((project / ".github" / "workflows" / "tests.yml").is_file())
            self.assertFalse((project / "tests").exists())

    def test_render_substitutes_values(self) -> None:
        """Template variables are replaced in the rendered output."""
        with tempfile.TemporaryDirectory() as tmp:
            project = self.render(Path(tmp))
            pyproject = (project / "pyproject.toml").read_text()
            self.assertIn('name = "Test Package"', pyproject)
            self.assertIn("test-org/Test Package", pyproject)
            self.assertNotIn("{{ cookiecutter", pyproject)
            self.assertNotIn("{{", (project / "src" / "test_package" / "__init__.py").read_text())

if __name__ == "__main__":
    unittest.main()
