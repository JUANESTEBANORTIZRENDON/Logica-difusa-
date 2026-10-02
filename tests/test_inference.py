import copy

import numpy as np
import pytest

from model.config import RULES, VARIABLES, validate_rule_base
from model.inference import evaluar


CASES = [
    (55, 25, 16.5384, "bajo", {"R1": 0.75, "R4": 0.2}),
    (75, 50, 50.0, "medio", {"R5": 1.0}),
    (130, 80, 84.4445, "alto", {"R9": 1.0}),
    (90, 50, 65.4664, "alto", {"R5": 0.4, "R8": 1 / 3}),
]


@pytest.mark.parametrize("weight,age,target,level,alphas", CASES)
def test_reference_cases(weight, age, target, level, alphas):
    result = evaluar(weight, age)
    assert result["indice"] == pytest.approx(target, abs=0.02)
    assert result["nivel"] == level
    trace = {row["id"]: row["alpha"] for row in result["reglas"]}
    for identifier, alpha in alphas.items():
        assert trace[identifier] == pytest.approx(alpha)
    assert len(result["reglas"]) == 9
    assert len(result["curvas_recortadas"]) == 9
    assert result["universo_salida"].shape == (1001,)


def test_rule_base_has_all_nine_unique_crosses():
    validate_rule_base()
    crosses = {(rule[1], rule[2]) for rule in RULES}
    assert len(RULES) == len(crosses) == 9
    assert crosses == {(p, e) for p in VARIABLES["peso"]["sets"] for e in VARIABLES["edad"]["sets"]}


@pytest.mark.parametrize("weight,age", [(0, 0), (0, 120), (200, 0), (200, 120)])
def test_four_domain_corners_produce_finite_bounded_output(weight, age):
    result = evaluar(weight, age)
    assert np.isfinite(result["indice"])
    assert 0 <= result["indice"] <= 100


@pytest.mark.parametrize("weight,age", [(-0.1, 20), (200.1, 20), (70, -0.1), (70, 120.1), (70, 20.5), (True, 20), (70, False), ("70", 20), (70, "20"), (None, 20), (70, None), (np.nan, 20), (np.inf, 20), (70, -np.inf), ([70], 20)])
def test_invalid_inputs_are_rejected_in_spanish(weight, age):
    with pytest.raises(ValueError, match="(Peso|Edad).*(número|finito|entre)"):
        evaluar(weight, age)


def test_decimal_weight_integer_age_and_full_result_contract():
    result = evaluar(81.25, 43)
    assert result["entrada"] == {"peso": 81.25, "edad": 43}
    assert set(result["grados_entrada"]) == {"peso", "edad"}
    assert set(result["grados_salida"]) == {"bajo", "medio", "alto"}
    assert np.isfinite(result["curva_agregada"]).all()


def test_engine_does_not_mutate_configuration_between_queries():
    before_variables = copy.deepcopy(VARIABLES)
    before_rules = copy.deepcopy(RULES)
    for values in [(55, 25), (90, 50), (130, 80), (0, 120)]:
        evaluar(*values)
    assert VARIABLES == before_variables
    assert RULES == before_rules
