"""Flask form handling and display. Implement the math in modeling.py."""

from math import isfinite

from flask import Flask, render_template, request

import modeling

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16_384


@app.get("/health")
def health():
    return "OK"


def integer(name, label, minimum, maximum):
    try:
        value = int(request.form.get(name, ""))
    except ValueError:
        raise ValueError(f"{label} must be a whole number.") from None
    if not minimum <= value <= maximum:
        raise ValueError(f"{label} must be between {minimum} and {maximum}.")
    return value


def decimal(name, label, minimum, maximum):
    try:
        value = float(request.form.get(name, ""))
    except ValueError:
        raise ValueError(f"{label} must be a number.") from None
    if not isfinite(value) or not minimum <= value <= maximum:
        raise ValueError(f"{label} must be between {minimum} and {maximum}.")
    return value


def show_normal():
    mean = decimal("mean", "Mean", -1_000_000, 1_000_000)
    stddev = decimal("stddev", "Standard deviation", 0.000001, 1_000_000)
    x, density = modeling.normal_curve(mean, stddev)
    points = " ".join(
        f"{45 + 530 * fraction:.2f},{190 - 175 * height / max_density:.2f}"
        for fraction, height in zip((x - x[0]) / (x[-1] - x[0]), density)
    ) if (max_density := max(density)) > 0 else ""
    return {"points": points, "ticks": (float(x[0]), mean, float(x[-1]))}


def show_item(action):
    low = integer("low", "Minimum roll", -1_000_000, 1_000_000)
    high = integer("high", "Maximum roll", low, min(low + 9999, 1_000_000))
    tier = integer("tier", "Amplifier tier", 0, 3)
    locked = None
    if request.form.get("insulator") == "on":
        locked = integer("locked", "Locked stat value", low, high)

    if action == "sample":
        count = integer("count", "Number of samples", 1, 1000)
        seed = None
        if request.form.get("seed", "").strip():
            seed = integer("seed", "Random seed", 0, 2**32 - 1)
        values, weights = modeling.item_distribution(low, high, tier, locked)
        rolls = modeling.sample_rolls(values, weights, count, seed)
        return {"rolls": [int(roll) for roll in rolls]}

    event = request.form.get("event")
    if event not in {"eq", "le", "ge", "between"}:
        raise ValueError("Choose an event.")
    target = integer("target", "Target", -1_000_000, 1_000_000)
    upper = None
    if event == "between":
        upper = integer("upper", "Upper target", target, 1_000_000)
    values, weights = modeling.item_distribution(low, high, tier, locked)
    probability = modeling.event_probability(values, weights, event, target, upper)
    return {"probability": f"{float(probability):.6%}", "outcomes": len(values)}


@app.route("/", methods=["GET", "POST"])
def index():
    form = request.form
    action = form.get("action")
    result = {}
    message = ""
    if request.method == "POST":
        try:
            if action == "normal":
                result = show_normal()
            elif action in {"odds", "sample"}:
                result = show_item(action)
            else:
                raise ValueError("Choose a calculator action.")
        except (NotImplementedError, ValueError) as error:
            message = str(error)
    return render_template("index.html", form=form, action=action, message=message, **result)
