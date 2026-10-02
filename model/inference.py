"""Inferencia Mamdani explícita para el modelo académico."""

from __future__ import annotations

from numbers import Real

import numpy as np

from .config import MODEL_VERSION, OUTPUT_POINTS, RULES, TIE_PRIORITY, VARIABLES
from .membership import membership, memberships


def _validate_input(value, variable: str) -> float | int:
    label = VARIABLES[variable]["label"].lower()
    if value is None or isinstance(value, (bool, str)) or not isinstance(value, Real):
        raise ValueError(f"{label.capitalize()}: se requiere un número real")
    numeric = float(value)
    if not np.isfinite(numeric):
        raise ValueError(f"{label.capitalize()}: el valor debe ser finito")
    if variable == "edad" and not numeric.is_integer():
        raise ValueError("Edad: se requiere un número entero de años")
    lower, upper = VARIABLES[variable]["range"]
    if not lower <= numeric <= upper:
        raise ValueError(f"{label.capitalize()}: debe estar entre {lower:g} y {upper:g}")
    return int(numeric) if variable == "edad" else numeric


def evaluar(peso, edad) -> dict:
    """Ejecuta fusificación, reglas, agregación y centroide sin redondeos."""
    weight = _validate_input(peso, "peso")
    age = _validate_input(edad, "edad")
    weight_mu = memberships(weight, VARIABLES["peso"]["sets"])
    age_mu = memberships(age, VARIABLES["edad"]["sets"])
    start, end = VARIABLES["salida"]["range"]
    universe = np.linspace(start, end, OUTPUT_POINTS)
    aggregated = np.zeros_like(universe)
    trace = []
    clipped_curves = {}

    for identifier, weight_set, age_set, consequent, rule_weight in RULES:
        alpha = min(weight_mu[weight_set], age_mu[age_set]) * rule_weight
        kind, points = VARIABLES["salida"]["sets"][consequent]
        clipped = np.minimum(alpha, membership(universe, kind, points))
        aggregated = np.maximum(aggregated, clipped)
        clipped_curves[identifier] = clipped
        trace.append(
            {
                "id": identifier,
                "peso_conjunto": weight_set,
                "edad_conjunto": age_set,
                "consecuente": consequent,
                "peso_regla": rule_weight,
                "alpha": float(alpha),
            }
        )

    area = float(np.trapezoid(aggregated, universe))
    if area <= 0:
        raise ValueError("Error de configuración: ninguna regla fue activada")
    centroid = float(np.trapezoid(universe * aggregated, universe) / area)
    output_mu = memberships(centroid, VARIABLES["salida"]["sets"])
    level = max(TIE_PRIORITY, key=lambda name: output_mu[name])
    return {
        "version_modelo": MODEL_VERSION,
        "entrada": {"peso": weight, "edad": age},
        "grados_entrada": {"peso": weight_mu, "edad": age_mu},
        "reglas": trace,
        "universo_salida": universe,
        "curvas_recortadas": clipped_curves,
        "curva_agregada": aggregated,
        "area": area,
        "indice": centroid,
        "nivel": level,
        "grados_salida": output_mu,
    }
