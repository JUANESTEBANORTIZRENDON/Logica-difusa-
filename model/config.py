"""Fuente única de verdad del modelo difuso académico."""

MODEL_VERSION = "modelo_v1"

VARIABLES = {
    "peso": {
        "label": "Peso",
        "unit": "kg",
        "range": (0.0, 200.0),
        "sets": {
            "ligero": ("trap", (0.0, 0.0, 50.0, 70.0)),
            "intermedio": ("tri", (50.0, 75.0, 100.0)),
            "elevado": ("trap", (80.0, 110.0, 200.0, 200.0)),
        },
    },
    "edad": {
        "label": "Edad",
        "unit": "años",
        "range": (0.0, 120.0),
        "sets": {
            "joven": ("trap", (0.0, 0.0, 25.0, 40.0)),
            "adulta": ("tri", (30.0, 50.0, 70.0)),
            "mayor": ("trap", (60.0, 80.0, 120.0, 120.0)),
        },
    },
    "salida": {
        "label": "Índice académico de propensión al infarto",
        "unit": "puntos",
        "range": (0.0, 100.0),
        "sets": {
            "bajo": ("trap", (0.0, 0.0, 20.0, 40.0)),
            "medio": ("tri", (30.0, 50.0, 70.0)),
            "alto": ("trap", (60.0, 80.0, 100.0, 100.0)),
        },
    },
}

RULES = (
    ("R1", "ligero", "joven", "bajo", 1.0),
    ("R2", "ligero", "adulta", "medio", 1.0),
    ("R3", "ligero", "mayor", "alto", 1.0),
    ("R4", "intermedio", "joven", "bajo", 1.0),
    ("R5", "intermedio", "adulta", "medio", 1.0),
    ("R6", "intermedio", "mayor", "alto", 1.0),
    ("R7", "elevado", "joven", "medio", 1.0),
    ("R8", "elevado", "adulta", "alto", 1.0),
    ("R9", "elevado", "mayor", "alto", 1.0),
)

OUTPUT_POINTS = 1001
TIE_PRIORITY = ("alto", "medio", "bajo")


def validate_rule_base() -> None:
    """Garantiza una regla única para cada uno de los nueve cruces."""
    weight_sets = set(VARIABLES["peso"]["sets"])
    age_sets = set(VARIABLES["edad"]["sets"])
    expected = {(weight, age) for weight in weight_sets for age in age_sets}
    actual = [(rule[1], rule[2]) for rule in RULES]
    if len(RULES) != 9 or len(set(actual)) != 9 or set(actual) != expected:
        raise RuntimeError("La base debe contener exactamente los nueve cruces únicos")
    output_sets = set(VARIABLES["salida"]["sets"])
    if any(rule[3] not in output_sets or rule[4] != 1.0 for rule in RULES):
        raise RuntimeError("Consecuente desconocido o peso de regla distinto de 1")


validate_rule_base()
