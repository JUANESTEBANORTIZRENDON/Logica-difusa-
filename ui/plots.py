"""Gráficas generadas desde las funciones reales del motor."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from model.config import RULES, VARIABLES
from model.membership import membership

COLORS = {"ligero": "#B91C1C", "intermedio": "#7F1D1D", "elevado": "#F87171", "joven": "#B91C1C", "adulta": "#7F1D1D", "mayor": "#F87171", "bajo": "#991B1B", "medio": "#DC2626", "alto": "#450A0A"}
DASHES = {"bajo": "dot", "medio": "dash", "alto": "solid"}
RISK_LABELS = {"bajo": "Riesgo bajo", "medio": "Riesgo medio", "alto": "Riesgo alto"}


def membership_figure(variable: str, evaluated: float | None = None) -> go.Figure:
    definition = VARIABLES[variable]
    low, high = definition["range"]
    x = np.linspace(low, high, int(high - low) * 5 + 1)
    fig = go.Figure()
    for name, (kind, points) in definition["sets"].items():
        display_name = RISK_LABELS.get(name, name.capitalize())
        fig.add_trace(go.Scatter(x=x, y=membership(x, kind, points), name=display_name, line={"color": COLORS[name], "width": 3, "dash": DASHES.get(name, "solid")}))
    if evaluated is not None:
        fig.add_vline(x=evaluated, line_width=2, line_dash="dash", line_color="#1F2937", annotation_text=f"{evaluated:g} {definition['unit']}")
    fig.update_layout(title=definition["label"], xaxis_title=definition["unit"], yaxis_title="Grado μ", yaxis_range=[0, 1.05], template="plotly_white", legend_title="Conjuntos", margin=dict(l=30, r=20, t=55, b=35))
    return style_figure(fig)


def output_figure(result: dict) -> go.Figure:
    z = result["universo_salida"]
    fig = go.Figure()
    for consequent in VARIABLES["salida"]["sets"]:
        related = [result["curvas_recortadas"][rule[0]] for rule in RULES if rule[3] == consequent]
        combined = np.maximum.reduce(related)
        fig.add_trace(go.Scatter(x=z, y=combined, name=RISK_LABELS[consequent], line={"color": COLORS[consequent], "dash": DASHES[consequent], "width": 2}))
    fig.add_trace(go.Scatter(x=z, y=result["curva_agregada"], name="Agregada", fill="tozeroy", fillcolor="rgba(185,28,28,.15)", line={"color": "#111827", "width": 3}))
    fig.add_vline(x=result["indice"], line_width=3, line_color="#B91C1C", annotation_text=f"Centroide {result['indice']:.2f}")
    fig.update_layout(title="Consecuencias recortadas, agregado y centroide", xaxis_title="Índice (puntos)", yaxis_title="Grado μ", yaxis_range=[0, 1.05], template="plotly_white", legend_title="Curvas", margin=dict(l=30, r=20, t=55, b=35))
    return style_figure(fig)


def style_figure(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        font=dict(family="Segoe UI, sans-serif", color="#526071", size=12),
        title_font=dict(size=16, color="#33252D"),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        legend=dict(orientation="h", y=-0.22, x=0, title_text=""),
        margin=dict(l=35, r=20, t=65, b=100), height=380,
    )
    fig.update_xaxes(gridcolor="#EFF1F4", zerolinecolor="#DFE3E9")
    fig.update_yaxes(gridcolor="#EFF1F4", zerolinecolor="#DFE3E9")
    return fig
