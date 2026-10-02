from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_streamlit_five_sections_calculation_and_downloads():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(app_path, default_timeout=20).run()
    assert not app.exception
    assert app.radio[0].options == [
        "Simulador",
        "Diseño y documentación",
        "Matriz y reglas",
        "Validaciones",
        "Evidencias",
    ]
    assert len(app.number_input) == 2
    app.button[0].click().run()
    assert not app.exception
    assert any("50.00 puntos" in item.value for item in app.metric)
    assert any("Riesgo medio" in item.value for item in app.metric)

    for page in app.radio[0].options[1:]:
        app.radio[0].set_value(page).run()
        assert not app.exception, page
        assert page in app.header[0].value

    assert len(app.get("download_button")) == 3
