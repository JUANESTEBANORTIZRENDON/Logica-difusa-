import csv
import io
import json
import zipfile

from model.inference import evaluar
from services.reporting import result_csv, result_json, simulation_docx, teacher_docx


def test_json_and_csv_include_all_rules_and_model_version():
    result = evaluar(90, 50)
    payload = json.loads(result_json(result))
    assert payload["version_modelo"] == "modelo_v1"
    assert "-05:00" in payload["fecha_zona_horaria"]
    assert len(payload["reglas"]) == 9
    rows = list(csv.DictReader(io.StringIO(result_csv(result).decode("utf-8-sig"))))
    assert [row["regla"] for row in rows] == [f"R{i}" for i in range(1, 10)]
    assert all(row["version_modelo"] == "modelo_v1" for row in rows)


def test_generated_docx_files_are_valid_office_archives():
    for content in (simulation_docx(evaluar(75, 50)), teacher_docx()):
        assert content.startswith(b"PK")
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            assert "word/document.xml" in archive.namelist()
