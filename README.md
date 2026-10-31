# Pricer Black-Scholes-Merton (Tkinter)

Application Python avec interface graphique Tkinter calculant le prix d'une option
européenne **Call** ou **Put** par la formule fermée de Black-Scholes-Merton,
avec rendement continu des dividendes.

## Le modèle

Le modèle de Black-Scholes-Merton suppose que le prix du sous-jacent suit un mouvement
brownien géométrique sous la probabilité risque-neutre :

```
dS = (r - q) S dt + sigma S dW
```

Hypothèses principales :

- option **européenne** (exercice uniquement à la maturité T) ;
- taux sans risque `r`, volatilité `sigma` et rendement des dividendes `q` constants (taux continus) ;
- marché sans frictions (pas de coûts de transaction ni d'impôts), ventes à découvert autorisées ;
- absence d'opportunité d'arbitrage, négociation en continu.

Notations :

| Symbole | Signification | Unité |
|---|---|---|
| `S0` | Prix actuel du sous-jacent | devise |
| `K` | Prix d'exercice (strike) | devise |
| `T` | Maturité | années |
| `r` | Taux sans risque continu | décimal (0.05 = 5 %) |
| `sigma` | Volatilité annualisée | décimal |
| `q` | Rendement continu des dividendes | décimal |

## Formules

```
d1 = [ln(S0/K) + (r - q + sigma²/2) T] / (sigma √T)
d2 = d1 - sigma √T

Call : C = S0 e^(-qT) N(d1) - K e^(-rT) N(d2)
Put  : P = K e^(-rT) N(-d2) - S0 e^(-qT) N(-d1)
```

`N` est la fonction de répartition de la loi normale centrée réduite (`scipy.stats.norm.cdf`).

## Structure

| Fichier | Rôle |
|---|---|
| `black_scholes.py` | Moteur de calcul (`bsm_price`, `d1_d2`) |
| `main.py` | Interface graphique Tkinter |
| `test_black_scholes.py` | Tests unitaires (pytest) |
| `requirements.txt` | Dépendances |

## Installation

Prérequis : Python 3.9 ou plus récent, avec Tkinter (inclus dans l'installateur
officiel Windows/macOS ; sous Debian/Ubuntu : `sudo apt install python3-tk`).

```powershell
git clone <url-du-depot>
cd BlackScholes
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

(Linux/macOS : `source .venv/bin/activate`.)

## Utilisation

```powershell
python main.py
```

Paramètres par défaut : S0 = 100, K = 100, T = 1 an, r = 5 %, sigma = 20 %, q = 0 %.
Choisir Call ou Put puis cliquer sur **Calculer** (ou appuyer sur Entrée).
Le prix est affiché avec six décimales : Call = 10.450584, Put = 5.573526.

Dans l'interface, r, sigma et q sont saisis en pourcentage ; la virgule est acceptée
comme séparateur décimal.

Utilisation directe du moteur (taux en décimal) :

```python
from black_scholes import bsm_price
bsm_price(S0=100, K=100, T=1, r=0.05, sigma=0.20, q=0.0, option_type="call")
```

## Exemple numérique

Paramètres : S0 = 100, K = 100, T = 1, r = 5 %, sigma = 20 %, q = 0.

```
d1 = [ln(100/100) + (0.05 + 0.20²/2) × 1] / (0.20 × 1) = 0.07 / 0.20 = 0.35
d2 = 0.35 - 0.20 = 0.15

N(d1)  = 0.636831     N(d2)  = 0.559618
N(-d1) = 0.363169     N(-d2) = 0.440382
K e^(-rT) = 100 × e^(-0.05) = 95.122942

Call = 100 × 0.636831 - 95.122942 × 0.559618 = 10.450584
Put  = 95.122942 × 0.440382 - 100 × 0.363169 = 5.573526
```

Vérification par la parité call-put : `C - P = 10.450584 - 5.573526 = 4.877058`
et `S0 - K e^(-rT) = 100 - 95.122942 = 4.877058`.

Avec un rendement des dividendes q = 3 % (autres paramètres inchangés), le Call baisse
à 8.652529 et le Put monte à 6.730918.

## Validation

- S0, K, T et sigma doivent être strictement positifs (sinon `ValueError`, affichée en rouge dans l'interface).
- r et q peuvent être négatifs.

## Tests

```powershell
python -m pytest -v
```

Les tests couvrent des valeurs de référence (cas par défaut, exemple de Hull),
la parité call-put `C - P = S0 e^(-qT) - K e^(-rT)` sur plusieurs jeux de paramètres
(y compris des taux négatifs), des propriétés de monotonie et de bornes, et la validation des entrées.

## Hors périmètre

Pas de Greeks, de Monte Carlo ni de graphiques.
