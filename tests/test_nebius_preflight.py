import pytest

from nebius_preflight import DEFAULT_BASE_URL, DEFAULT_MODEL_ID, evaluate, require_live_config


def approved_env(**overrides):
    env = {
        "NEBIUS_BASE_URL": DEFAULT_BASE_URL,
        "NEBIUS_MODEL_ID": DEFAULT_MODEL_ID,
        "NEBIUS_API_KEY": "test-key-not-real",
        "ALLOW_LIVE_NEBIUS_TEST": "YES",
        "NEBIUS_PROMO_COVERAGE_CONFIRMED": "YES",
    }
    env.update(overrides)
    return env


def test_approved_configuration_is_ready():
    result = evaluate(approved_env())
    assert result["ready_for_single_live_call"] is True
    assert all(result["checks"].values())


def test_rejects_non_nebius_endpoint():
    result = evaluate(approved_env(NEBIUS_BASE_URL="https://api.openai.com/v1"))
    assert result["ready_for_single_live_call"] is False
    assert result["checks"]["nebius_https_endpoint"] is False


def test_rejects_non_nvidia_model():
    result = evaluate(approved_env(NEBIUS_MODEL_ID="other/model"))
    assert result["ready_for_single_live_call"] is False
    assert result["checks"]["nvidia_model_requested"] is False


def test_gate_stays_closed_without_credit_confirmation():
    with pytest.raises(RuntimeError, match="promo_coverage_confirmed"):
        require_live_config(approved_env(NEBIUS_PROMO_COVERAGE_CONFIRMED="NO"))
