import math

import pytest

from black_scholes import CALL, PUT, bsm_price, d1_d2


def parity_gap(S0, K, T, r, sigma, q):
    """C - P - (S0 e^{-qT} - K e^{-rT}), doit être nul."""
    call = bsm_price(S0, K, T, r, sigma, q, CALL)
    put = bsm_price(S0, K, T, r, sigma, q, PUT)
    return call - put - (S0 * math.exp(-q * T) - K * math.exp(-r * T))


# --- Valeurs de référence -------------------------------------------------

def test_default_parameters_call():
    assert bsm_price(100, 100, 1, 0.05, 0.20, 0.0, CALL) == pytest.approx(10.450583572185565, abs=1e-9)


def test_default_parameters_put():
    assert bsm_price(100, 100, 1, 0.05, 0.20, 0.0, PUT) == pytest.approx(5.573526022256971, abs=1e-9)


def test_hull_example():
    # Hull, Options, Futures and Other Derivatives : S0=42, K=40, r=10 %, sigma=20 %, T=0.5
    assert bsm_price(42, 40, 0.5, 0.10, 0.20, 0.0, CALL) == pytest.approx(4.7594, abs=1e-4)
    assert bsm_price(42, 40, 0.5, 0.10, 0.20, 0.0, PUT) == pytest.approx(0.8086, abs=1e-4)


def test_d1_d2_default():
    d1, d2 = d1_d2(100, 100, 1, 0.05, 0.20)
    assert d1 == pytest.approx(0.35, abs=1e-12)
    assert d2 == pytest.approx(0.15, abs=1e-12)


def test_option_type_case_insensitive():
    assert bsm_price(100, 100, 1, 0.05, 0.2, 0, "CALL") == bsm_price(100, 100, 1, 0.05, 0.2, 0, "call")


# --- Parité call-put -----------------------------------------------------

@pytest.mark.parametrize(
    "S0, K, T, r, sigma, q",
    [
        (100, 100, 1, 0.05, 0.20, 0.0),
        (100, 120, 2, 0.03, 0.35, 0.02),
        (50, 40, 0.25, -0.01, 0.15, 0.04),
        (200, 180, 5, 0.08, 0.50, -0.01),
        (10, 15, 0.01, 0.0, 0.05, 0.0),
    ],
)
def test_put_call_parity(S0, K, T, r, sigma, q):
    assert parity_gap(S0, K, T, r, sigma, q) == pytest.approx(0.0, abs=1e-10)


# --- Propriétés et bornes ------------------------------------------------

def test_dividends_reduce_call_and_raise_put():
    assert bsm_price(100, 100, 1, 0.05, 0.2, 0.03, CALL) < bsm_price(100, 100, 1, 0.05, 0.2, 0.0, CALL)
    assert bsm_price(100, 100, 1, 0.05, 0.2, 0.03, PUT) > bsm_price(100, 100, 1, 0.05, 0.2, 0.0, PUT)


def test_negative_rates_accepted():
    price = bsm_price(100, 100, 1, -0.01, 0.2, -0.005, CALL)
    assert price > 0
    assert parity_gap(100, 100, 1, -0.01, 0.2, -0.005) == pytest.approx(0.0, abs=1e-10)


def test_deep_in_the_money_call_tends_to_forward_intrinsic():
    S0, K, T, r, q = 1000, 10, 1, 0.05, 0.01
    expected = S0 * math.exp(-q * T) - K * math.exp(-r * T)
    assert bsm_price(S0, K, T, r, 0.2, q, CALL) == pytest.approx(expected, abs=1e-8)
    assert bsm_price(S0, K, T, r, 0.2, q, PUT) == pytest.approx(0.0, abs=1e-8)


def test_price_increases_with_volatility():
    low = bsm_price(100, 100, 1, 0.05, 0.10, 0, CALL)
    high = bsm_price(100, 100, 1, 0.05, 0.40, 0, CALL)
    assert high > low


# --- Validation des entrées ---------------------------------------------

@pytest.mark.parametrize(
    "kwargs",
    [
        dict(S0=0, K=100, T=1, sigma=0.2),
        dict(S0=-1, K=100, T=1, sigma=0.2),
        dict(S0=100, K=0, T=1, sigma=0.2),
        dict(S0=100, K=100, T=0, sigma=0.2),
        dict(S0=100, K=100, T=-1, sigma=0.2),
        dict(S0=100, K=100, T=1, sigma=0),
        dict(S0=100, K=100, T=1, sigma=-0.2),
        dict(S0=float("nan"), K=100, T=1, sigma=0.2),
    ],
)
def test_invalid_inputs_raise(kwargs):
    with pytest.raises(ValueError):
        bsm_price(r=0.05, q=0.0, option_type=CALL, **kwargs)


def test_invalid_option_type_raises():
    with pytest.raises(ValueError):
        bsm_price(100, 100, 1, 0.05, 0.2, 0.0, "digital")
