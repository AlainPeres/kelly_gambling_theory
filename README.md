# Kelly Gambling Theory

Simulations Monte Carlo autour des stratégies de mise en pari répété (pile ou
face biaisé) :

- [main.py](main.py) — critère de Kelly (croissance optimale du capital à
  long terme) comparé à une mise plus agressive.
- [martingale.py](martingale.py) — stratégie de Martingale (doublement de la
  mise après chaque perte).

Référence théorique : `2006-thorp.pdf` (Edward Thorp, *The Kelly Criterion in
Blackjack, Sports Betting, and the Stock Market*).

## Principe

À chaque pari, on mise une fraction `f` du capital courant. Avec probabilité
`p` de gain et un ratio gain/perte `b`, la fraction de Kelly qui maximise la
croissance géométrique espérée du capital est :

```text
f* = p - (1 - p) / b
```

`main.py` simule des trajectoires de capital sur `n` paris, répète la
simulation sur `nruns` tirages indépendants, puis calcule :

- le capital final moyen et son écart-type,
- la probabilité de ruine (capital final sous un seuil `ruin_threshold`),

pour la fraction de Kelly et pour une fraction "agressive" (2.5x Kelly, par
défaut) à titre de comparaison.

## Installation

Le projet utilise [uv](https://docs.astral.sh/uv/) et Python ≥ 3.13.

```bash
uv sync
```

## Utilisation

```bash
uv run main.py
uv run martingale.py
```

Les paramètres (`p`, `b`, `n`, `nruns`, `ruin_threshold`) sont définis dans le
bloc `if __name__ == "__main__":` en bas du fichier et peuvent être modifiés
directement.

Le script affiche dans la console les statistiques (capital moyen, écart-type,
probabilité de ruine) pour Kelly et pour la stratégie alternative, puis ouvre
trois graphiques matplotlib :

1. évolution du capital pour la fraction de Kelly,
2. évolution du capital pour la fraction alternative,
3. courbe du taux de croissance `g(f)` en fonction de la fraction misée `f`.

## Structure de `main.py`

| Fonction                    | Rôle                                                            |
| --------------------------- | ---------------------------------------------------------------- |
| `kelly_ratio(p, b)`         | Calcule la fraction de Kelly optimale, bornée entre 0 et 1       |
| `step(bet, p, b)`           | Simule le résultat (gain/perte) d'un seul pari                   |
| `simulate(f, p, b, n)`      | Simule l'évolution du capital sur `n` paris successifs           |
| `final_stats(...)`          | Moyenne/écart-type du capital final sur `nruns` simulations      |
| `ruin_probability(...)`     | Probabilité que le capital final passe sous `ruin_threshold`     |
| `visualize(capital, text)`  | Trace l'évolution du capital dans le temps                       |
| `visualize_g(p, b)`         | Trace le taux de croissance `g(f) = p·ln(1+fb) + (1-p)·ln(1-f)`  |

Les fonctions de simulation sont compilées via `numba.jit(nopython=True)`
pour accélérer les boucles Monte Carlo.

## Structure de `martingale.py`

La Martingale consiste à doubler la mise après chaque perte, afin de
récupérer les pertes cumulées dès la première victoire (mise remise à sa
valeur initiale après un gain).

| Fonction | Rôle |
| --- | --- |
| `martingale_strategy(bankroll, bet_size, win_probability)` | Simule la stratégie jusqu'à ruine (`bankroll <= 0`) et renvoie l'historique du capital et de la mise |
| `martingale_with_stop(bankroll, bet_size, win_probability)` | Simule une série de pertes jusqu'à la première victoire et renvoie `(duration, bankroll_final, bet_size_final)` |
| `main_martigale_strategy()` | Trace l'évolution du capital et de la mise courante pour une simulation de `martingale_strategy` |
| `main_martingale_with_stop()` | Lance une simulation unique de `martingale_with_stop` (bankroll initial nul) et renvoie `(duration, bankroll_final, bet_size_final)` |
| `stat_with_stop()` | Sur `N = 10000` répétitions de `main_martingale_with_stop`, calcule la moyenne et le maximum de `duration`, `bankroll_final` et `bet_size_final` |

Le point d'entrée `if __name__ == "__main__":` appelle `stat_with_stop()` et
affiche, pour une série de pertes avant la première victoire, la durée
moyenne/maximale, le capital final moyen/maximal et la mise finale
moyenne/maximale.
