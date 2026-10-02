"""Funciones de membresía triangulares y trapezoidales."""

from __future__ import annotations

import numpy as np


def membership(x, kind: str, points: tuple[float, ...]):
    """Evalúa una membresía conservando correctamente los hombros."""
    values = np.asarray(x, dtype=float)
    if kind == "tri" and len(points) == 3:
        a, b, d = points
        c = b
    elif kind == "trap" and len(points) == 4:
        a, b, c, d = points
    else:
        raise ValueError("Definición de función de membresía inválida")
    rising = np.ones_like(values) if a == b else (values - a) / (b - a)
    falling = np.ones_like(values) if c == d else (d - values) / (d - c)
    result = np.clip(np.minimum(rising, falling), 0.0, 1.0)
    result = np.where((values < a) | (values > d), 0.0, result)
    return float(result) if result.ndim == 0 else result


def memberships(x: float, set_definitions: dict) -> dict[str, float]:
    return {
        name: float(membership(x, kind, tuple(points)))
        for name, (kind, points) in set_definitions.items()
    }
