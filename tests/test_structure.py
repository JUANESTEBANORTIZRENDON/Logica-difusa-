from pathlib import Path


def test_required_project_structure_exists():
    root = Path(__file__).resolve().parents[1]
    required = [
        "app.py", "model/config.py", "model/membership.py", "model/inference.py",
        "services/reporting.py", "ui/plots.py", "ui/pages.py", "docs/contenido.md",
        ".streamlit/config.toml", "requirements.txt", "README.md",
    ]
    assert all((root / item).is_file() for item in required)


def test_engine_does_not_import_streamlit():
    root = Path(__file__).resolve().parents[1]
    for filename in ("config.py", "membership.py", "inference.py"):
        assert "streamlit" not in (root / "model" / filename).read_text(encoding="utf-8").lower()
