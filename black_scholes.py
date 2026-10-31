"""Moteur de calcul Black-Scholes-Merton pour options européennes."""

import math

from scipy.stats import norm

CALL = "call"
PUT = "put"


def _validate(S0, K, T, sigma, option_type):
    for name, value in (("S0", S0), ("K", K), ("T", T), ("sigma", sigma)):
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} doit être strictement positif (reçu : {value}).")
    if option_type not in (CALL, PUT):
        raise ValueError(f"Type d'option invalide : {option_type!r} (attendu 'call' ou 'put').")


def d1_d2(S0, K, T, r, sigma, q=0.0):
    """Retourne (d1, d2). Les taux r, q et sigma sont exprimés en décimal."""
    sqrt_T = math.sqrt(T)
    d1 = (math.log(S0 / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T
    return d1, d2


def bsm_price(S0, K, T, r, sigma, q=0.0, option_type=CALL):
    """Prix d'une option européenne selon la formule fermée de Black-Scholes-Merton.

    S0, K, T et sigma doivent être strictement positifs ; r et q peuvent être négatifs.
    r, sigma et q sont en décimal (0.05 pour 5 %).
    """
    option_type = option_type.lower()
    _validate(S0, K, T, sigma, option_type)
    if not (math.isfinite(r) and math.isfinite(q)):
        raise ValueError("r et q doivent être des nombres finis.")

    d1, d2 = d1_d2(S0, K, T, r, sigma, q)
    disc_S = S0 * math.exp(-q * T)
    disc_K = K * math.exp(-r * T)

    if option_type == CALL:
        return disc_S * norm.cdf(d1) - disc_K * norm.cdf(d2)
    return disc_K * norm.cdf(-d2) - disc_S * norm.cdf(-d1)
