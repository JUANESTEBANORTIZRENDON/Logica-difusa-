"""Cinco vistas de la aplicación académica."""

from __future__ import annotations

import inspect
import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from model import config
from model.inference import evaluar
from services.reporting import result_csv, result_json, simulation_docx, teacher_docx
from ui.plots import membership_figure, output_figure
from ui.design import notice, empty_result

ROOT = Path(__file__).resolve().parents[1]
RISK_LABELS = {
    "bajo": "Riesgo bajo",
    "medio": "Riesgo medio",
    "alto": "Riesgo alto",
}


def disclaimer() -> None:
    notice()


def _set_example(weight: float, age: float) -> None:
    st.session_state.weight_input = weight
    st.session_state.age_input = age
    st.session_state.result = evaluar(weight, age)


def _reset() -> None:
    st.session_state.weight_input = 75.0
    st.session_state.age_input = 50
    st.session_state.result = None


def _trace_frame(result: dict) -> pd.DataFrame:
    frame = pd.DataFrame(result["reglas"]).rename(
        columns={
            "id": "Regla",
            "peso_conjunto": "Peso",
            "edad_conjunto": "Edad",
            "consecuente": "Consecuente",
            "peso_regla": "Peso de regla",
            "alpha": "Fuerza α",
        }
    )
    frame["Consecuente"] = frame["Consecuente"].map(RISK_LABELS)
    frame["Estado"] = np.where(frame["Fuerza α"] > 0, "Activa", "Inactiva")
    return frame[["Regla", "Peso", "Edad", "Consecuente", "Fuerza α", "Estado"]]


def simulator_page() -> None:
    st.header("Simulador")
    st.caption("Completa los datos para explorar el índice académico de propensión al infarto.")

    with st.container(border=True, key="entry_card"):
        st.subheader("01 / Datos de la simulación")
        with st.form("formulario_simulacion"):
            cols = st.columns(2)
            with cols[0]:
                weight = st.number_input(
                    "Peso (kg)", min_value=0.0, max_value=200.0,
                    step=0.1, key="weight_input",
                )
            with cols[1]:
                age = st.number_input(
                    "Edad (años enteros)", min_value=0, max_value=120,
                    step=1, format="%d", key="age_input",
                )
            if st.form_submit_button("Calcular índice", type="primary", width="stretch"):
                st.session_state.result = evaluar(weight, age)

        with st.expander("Prueba un caso de ejemplo"):
            examples = st.columns(2)
            for index, values in enumerate([(55, 25), (75, 50), (130, 80), (90, 50)]):
                examples[index % 2].button(
                    f"{values[0]} kg / {values[1]} años",
                    on_click=_set_example, args=values, width="stretch",
                )
        st.button("Reiniciar simulación", on_click=_reset)

    result = st.session_state.result
    if result is None:
        empty_result()
        return

    active = [rule for rule in result["reglas"] if rule["alpha"] > 0]
    strongest = max(active, key=lambda rule: rule["alpha"])

    with st.container(border=True, key="result_card"):
        st.subheader("02 / Resultado académico")
        st.caption(f"Datos evaluados: {result['entrada']['peso']:g} kg · {result['entrada']['edad']:g} años")
        summary = st.columns(3)
        summary[0].metric("Índice académico", f"{result['indice']:.2f} puntos")
        summary[1].metric("Nivel resultante", RISK_LABELS[result["nivel"]])
        summary[2].metric("Reglas activas", f"{len(active)} de 9")
        st.caption("La palabra “riesgo” identifica el nivel interno del ejercicio; no representa riesgo clínico real.")

    summary_tab, charts_tab, rules_tab = st.tabs(
        ["Resumen del cálculo", "Gráficas", "Reglas y activaciones"]
    )
    with summary_tab:
        st.subheader("¿Por qué se obtuvo este resultado?")
        st.write(
            f"La regla con mayor fuerza fue **{strongest['id']} = {strongest['alpha']:.4f}**: "
            f"peso **{strongest['peso_conjunto']}** y edad **{strongest['edad_conjunto']}**, "
            f"con consecuente **{RISK_LABELS[strongest['consecuente']]}**. "
            "El motor recortó las salidas de todas las reglas, las agregó mediante el máximo "
            "y calculó el centroide de la curva final."
        )
        degree_cols = st.columns(2)
        with degree_cols[0]:
            st.markdown("**Pertenencias del peso**")
            st.dataframe(
                pd.DataFrame(
                    [(name.capitalize(), value) for name, value in result["grados_entrada"]["peso"].items()],
                    columns=["Conjunto", "Grado μ"],
                ).style.format({"Grado μ": "{:.4f}"}),
                width="stretch", hide_index=True,
            )
        with degree_cols[1]:
            st.markdown("**Pertenencias de la edad**")
            st.dataframe(
                pd.DataFrame(
                    [(name.capitalize(), value) for name, value in result["grados_entrada"]["edad"].items()],
                    columns=["Conjunto", "Grado μ"],
                ).style.format({"Grado μ": "{:.4f}"}),
                width="stretch", hide_index=True,
            )
        st.markdown("**Pertenencias del resultado**")
        st.dataframe(
            pd.DataFrame(
                [(RISK_LABELS[name], value) for name, value in result["grados_salida"].items()],
                columns=["Nivel", "Grado μ"],
            ).style.format({"Grado μ": "{:.4f}"}),
            width="stretch", hide_index=True,
        )

    with charts_tab:
        st.subheader("Fusificación de las entradas")
        left, right = st.columns(2)
        left.plotly_chart(
            membership_figure("peso", result["entrada"]["peso"]), width="stretch"
        )
        right.plotly_chart(
            membership_figure("edad", result["entrada"]["edad"]), width="stretch"
        )
        st.subheader("Agregación y centroide")
        st.plotly_chart(output_figure(result), width="stretch")

    with rules_tab:
        st.subheader("Traza completa de las nueve reglas")
        st.write("Una fuerza α mayor que cero indica que la regla participó en el resultado.")
        st.dataframe(
            _trace_frame(result).style.format({"Fuerza α": "{:.6f}"}),
            width="stretch", hide_index=True,
        )


def documentation_page() -> None:
    st.header("Diseño y documentación")
    st.caption("Consulta el fundamento del modelo, sus funciones y el informe académico completo.")
    with st.expander("Explorar las funciones de pertenencia"):
        for variable in ("peso", "edad", "salida"):
            st.plotly_chart(membership_figure(variable), width="stretch")
    content = (ROOT / "docs" / "contenido.md").read_text(encoding="utf-8")
    chapters = content.split("\n## ")
    with st.expander("Presentación del informe"):
        st.markdown(chapters[0])
    for chapter in chapters[1:]:
        title, _, body = chapter.partition("\n")
        with st.expander(title):
            st.markdown(body)
    with st.expander("Código ejecutable completo del motor"):
        for relative in ("model/config.py", "model/membership.py", "model/inference.py"):
            st.markdown(f"**{relative}**")
            st.code((ROOT / relative).read_text(encoding="utf-8"), language="python")
    st.download_button("Descargar informe docente (DOCX)", teacher_docx(), "Informe_docente_sistema_difuso.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")


def rules_page() -> None:
    st.header("Matriz y reglas")
    matrix = pd.DataFrame(index=["Ligero", "Intermedio", "Elevado"], columns=["Joven", "Adulta", "Mayor"])
    for identifier, weight, age, consequent, _ in config.RULES:
        matrix.loc[weight.capitalize(), age.capitalize()] = f"{identifier} · {RISK_LABELS[consequent]}"
    st.metric("Reglas cargadas desde el motor", len(config.RULES))
    st.dataframe(matrix, width="stretch")
    rows = [{"Regla": r[0], "Peso": r[1], "Edad": r[2], "Consecuente": RISK_LABELS[r[3]], "Peso de regla": r[4]} for r in config.RULES]
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    if st.session_state.result:
        st.subheader("Activaciones del caso vigente")
        st.dataframe(_trace_frame(st.session_state.result), width="stretch", hide_index=True)
    with st.expander("Ver configuración versionada"):
        st.code(json.dumps({"version": config.MODEL_VERSION, "variables": config.VARIABLES, "reglas": config.RULES}, ensure_ascii=False, indent=2), language="json")
    with st.expander("Ver código real del evaluador"):
        st.code(inspect.getsource(evaluar), language="python")


def validations_page() -> None:
    st.header("Validaciones")
    expected = [(55, 25, 16.5384, "bajo"), (75, 50, 50.0, "medio"), (130, 80, 84.4445, "alto"), (90, 50, 65.4664, "alto")]
    rows = []
    for weight, age, target, level in expected:
        result = evaluar(weight, age)
        rows.append({"Peso": weight, "Edad": age, "Esperado": target, "Obtenido": result["indice"], "Diferencia": abs(result["indice"] - target), "Nivel": RISK_LABELS[result["nivel"]], "Cumple ±0,02": abs(result["indice"] - target) <= 0.02 and result["nivel"] == level})
    st.dataframe(pd.DataFrame(rows).style.format({"Esperado": "{:.4f}", "Obtenido": "{:.4f}", "Diferencia": "{:.6f}"}), width="stretch", hide_index=True)
    st.info("Estas son pruebas de coherencia matemática del ejercicio, no una validación clínica.")


def evidence_page() -> None:
    st.header("Evidencias y descargas")
    st.write(f"Versión ejecutada: **{config.MODEL_VERSION}**. El historial existe solo durante esta sesión y ninguna descarga ocurre sin tu acción.")
    result = st.session_state.result
    if result is None:
        st.info("Calcula un caso en Simulador para habilitar sus evidencias.")
    else:
        st.download_button("Descargar JSON trazable", result_json(result), "simulacion.json", "application/json")
        st.download_button("Descargar CSV trazable", result_csv(result), "simulacion.csv", "text/csv")
        st.download_button("Descargar informe de simulación (DOCX)", simulation_docx(result), "informe_simulacion.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    evidence_file = ROOT / "evidencias" / "resumen.md"
    if evidence_file.exists():
        st.markdown(evidence_file.read_text(encoding="utf-8"))


PAGES = {
    "Simulador": simulator_page,
    "Diseño y documentación": documentation_page,
    "Matriz y reglas": rules_page,
    "Validaciones": validations_page,
    "Evidencias": evidence_page,
}
