import numpy as np
from scipy import stats


def integer_support(low: int, high: int) -> np.ndarray:
    # Return every integer from low through high.
    if low > high:
        raise ValueError("Minimum roll must be at most the maximum roll.")
    return np.arange(low, high + 1, dtype=np.int64)


def uniform_probabilities(values: np.ndarray) -> np.ndarray:
    # Give every value an equal probability.
    if values.size == 0:
        raise ValueError("At least one outcome is required.")
    return np.full(values.size, 1.0 / values.size)


def amplified_probabilities(
    raw_rolls: np.ndarray,
    probabilities: np.ndarray,
    tier: int,
) -> np.ndarray:
    # Remove rolls below the cutoff and rescale the remaining probabilities.
    if tier not in (0, 1, 2, 3, 4):
        raise ValueError("Choose an amplifier tier from 0 to 4.")

    cutoff = 5 * tier
    accepted = np.where(raw_rolls >= cutoff, probabilities, 0.0)
    total = accepted.sum()
    if total <= 0:
        raise ValueError("No rolls meet the amplifier cutoff.")
    return accepted / total


def insulator_outcomes(
    values: np.ndarray,
    locked_value: int,
) -> tuple[np.ndarray, np.ndarray]:
    # Give the locked value a probability of 1.
    if locked_value not in values:
        raise ValueError("The locked value must be a possible roll.")
    return np.array([locked_value]), np.array([1.0])


def item_distribution(
    low: int,
    high: int,
    tier: int,
    locked_value: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    # Build a uniform distribution for the existing min/max form.
    if tier not in (0, 1, 2, 3, 4):
        raise ValueError("Choose an amplifier tier from 0 to 4.")

    values = integer_support(low, high)
    if locked_value is not None:
        return insulator_outcomes(values, locked_value)

    if tier and low < high:
        # Treat higher values as better in the generic range calculator.
        cutoff = low + (5 * tier * (high - low) + 99) // 100
        values = values[values >= cutoff]

    return values, uniform_probabilities(values)


def displayed_rolls(
    base_value: int,
    raw_rolls: np.ndarray,
    roll_rule: str,
) -> np.ndarray:
    # Convert raw rolls to displayed stats using the chosen multiplier range.
    if roll_rule == "beneficial":
        numerator = base_value * (30 + raw_rolls)
        denominator = 100
    elif roll_rule == "harmful":
        numerator = base_value * (650 - 3 * raw_rolls)
        denominator = 500
    else:
        raise ValueError("Choose a beneficial or harmful roll rule.")

    # Round to the nearest integer, with exact halves toward positive infinity.
    return (numerator + denominator // 2) // denominator


def wynncraft_distribution(
    base_value: int,
    roll_rule: str,
    tier: int,
    locked_value: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    # Start with 101 equally likely raw rolls.
    if tier not in (0, 1, 2, 3, 4):
        raise ValueError("Choose an amplifier tier from 0 to 4.")

    raw_rolls = integer_support(0, 100)
    displayed = displayed_rolls(base_value, raw_rolls, roll_rule)
    if locked_value is not None:
        return insulator_outcomes(displayed, locked_value)

    probabilities = uniform_probabilities(raw_rolls)
    if tier and roll_rule == "beneficial":
        probabilities = amplified_probabilities(raw_rolls, probabilities, tier)

    # Add the probabilities of raw rolls that display the same value.
    values, indices = np.unique(displayed, return_inverse=True)
    masses = np.bincount(indices, weights=probabilities)
    possible = masses > 0
    return values[possible], masses[possible]


def event_probability(
    values: np.ndarray,
    probabilities: np.ndarray,
    event: str,
    target: int,
    upper: int | None = None,
) -> float:
    # Add the probabilities of all values that satisfy the event.
    if event == "eq":
        matches = values == target
    elif event == "le":
        matches = values <= target
    elif event == "ge":
        matches = values >= target
    elif event == "between":
        if upper is None or upper < target:
            raise ValueError("The upper target must be at least the lower target.")
        matches = (values >= target) & (values <= upper)
    else:
        raise ValueError("Choose a valid probability event.")

    return float(np.clip(probabilities[matches].sum(), 0.0, 1.0))


def normal_curve(mean: float, stddev: float) -> tuple[np.ndarray, np.ndarray]:
    # Generate 161 points for the normal density plot.
    if not np.isfinite(mean) or not np.isfinite(stddev) or stddev <= 0:
        raise ValueError("Enter a finite mean and a positive, finite standard deviation.")

    x = np.linspace(mean - 4 * stddev, mean + 4 * stddev, 161)
    return x, stats.norm.pdf(x, loc=mean, scale=stddev)


def sample_rolls(
    values: np.ndarray,
    probabilities: np.ndarray,
    count: int,
    seed: int | None,
) -> np.ndarray:
    # Draw random samples from the same distribution used for the odds.
    distribution = stats.rv_discrete(values=(values, probabilities))
    rng = np.random.default_rng(seed)
    return distribution.rvs(size=count, random_state=rng)