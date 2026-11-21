"""Start here. Replace each TODO's exception with its implementation."""

import numpy as np
from scipy import stats


def integer_support(low: int, high: int) -> np.ndarray:
    """TODO 1: Return a 1-D integer array containing both endpoints.

    Hint: np.arange excludes its stop. Try (-2, 2) and (7, 7).
    """
    raise NotImplementedError("TODO 1 in modeling.py: generate integer support.")


def uniform_probabilities(values: np.ndarray) -> np.ndarray:
    """TODO 2: Return one equal probability per value, summing to 1.

    Hint: try np.full. Five possible outcomes should each have mass 0.2.
    """
    raise NotImplementedError("TODO 2 in modeling.py: build a uniform PMF.")


def amplified_probabilities(
    values: np.ndarray, probabilities: np.ndarray, tier: int
) -> np.ndarray:
    """TODO 6: Return a PMF aligned to values for the chosen amplifier tier.

    Verify the game's rules for each tier. Think about whether to modify
    the underlying roll pool before projecting it onto displayed integers.
    If the support changes, return a tuple of new support and PMF and
    update item_distribution to unpack both. Never mutate the input arrays.
    """
    raise NotImplementedError("TODO 6 in modeling.py: model amplifier tiers.")


def insulator_outcomes(
    values: np.ndarray, probabilities: np.ndarray, locked_value: int
) -> tuple[np.ndarray, np.ndarray]:
    """TODO 7: Model the selected stat when the user locks its current value.

    The GUI passes an explicit current value, including zero. Research the
    in-game restrictions and interaction with amplifiers. Catch any unsupported
    combination with a ValueError whose message the form can display.
    """
    raise NotImplementedError("TODO 7 in modeling.py: model locked rolls.")


def item_distribution(
    low: int, high: int, tier: int, locked_value: int | None
) -> tuple[np.ndarray, np.ndarray]:
    """Connect the base model to the optional modifier exercises."""
    values = integer_support(low, high)
    probabilities = uniform_probabilities(values)
    if tier:
        probabilities = amplified_probabilities(values, probabilities, tier)
    if locked_value is not None:
        values, probabilities = insulator_outcomes(values, probabilities, locked_value)
    return values, probabilities


def event_probability(
    values: np.ndarray, probabilities: np.ndarray, event: str, target: int,
    upper: int | None = None,
) -> float:
    """TODO 3: Sum PMF entries using a NumPy Boolean mask.

    Events: eq, le, ge, between. Between includes both target and upper.
    Example: P(X >= 4) on uniform {1, 2, 3, 4, 5} should be 0.4.
    """
    raise NotImplementedError("TODO 3 in modeling.py: calculate event odds.")


def normal_curve(mean: float, stddev: float) -> tuple[np.ndarray, np.ndarray]:
    """TODO 4: Return (x, density) arrays, each with 161 points.

    Use np.linspace from mean - 4*stddev to mean + 4*stddev and
    stats.norm.pdf. The density curve should peak at the mean.
    """
    raise NotImplementedError("TODO 4 in modeling.py: generate the normal curve.")


def sample_rolls(
    values: np.ndarray, probabilities: np.ndarray, count: int, seed: int | None
) -> np.ndarray:
    """TODO 5: Return count simulated item rolls using SciPy's .rvs().

    Hint: stats.rv_discrete(values=(values, probabilities)) accepts a
    custom PMF. Pass size=count and use np.random.default_rng(seed) as
    random_state. Each result must be in values. Repeat a seed to check
    reproducibility. Sampling is with replacement.
    """
    raise NotImplementedError("TODO 5 in modeling.py: simulate rolls with .rvs().")
