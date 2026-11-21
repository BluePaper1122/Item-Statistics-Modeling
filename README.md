# Item Statistics Modeling

A Flask starter for a Wynncraft item roll calculator. The forms, validation,
plot rendering, and Render configuration are ready. Each calculation displays
its first unfinished exercise until you implement it.

## Run locally

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m flask --app app run
```

Open http://127.0.0.1:5000.

## Start in modeling.py

Replace the `raise NotImplementedError(...)` line in each numbered function
with your implementation. Start with TODOs 1–3 and use **Calculate odds** with
the default inputs. The expected result is 40% across five integer outcomes.

| TODO | Function | Quick check |
| --- | --- | --- |
| 1 | `integer_support` | 1 through 5 contains five integers. A range from 7 to 7 contains one. |
| 2 | `uniform_probabilities` | Five masses of 0.2 sum to 1. |
| 3 | `event_probability` | At least 4 gives 40%. Exactly 8 gives 0%. Between 2 and 4 gives 60%. |
| 4 | `normal_curve` | Mean 0 and SD 1 give a symmetric curve peaking near 0.399. |
| 5 | `sample_rolls` | All ten samples are in range. Repeating a seed repeats the sequence. |
| 6 | `amplified_probabilities` | Each supported tier returns nonnegative masses totaling 1. |
| 7 | `insulator_outcomes` | An eligible locked stat always returns its supplied current value. |

The base exercise assumes every integer in the range is equally likely. If
Wynncraft rolls underlying multipliers and rounds several into the same displayed
stat, count those underlying outcomes and combine their mass before calculating
displayed odds. Verify the current game rules for amplifiers, lock eligibility,
and how modifiers interact before encoding them. The normal viewer plots a
continuous density as a separate exercise. Both exact odds and simulated rolls
use the same discrete probability mass function in `item_distribution`.

## Deploy to Render

In the [Render dashboard](https://dashboard.render.com/), choose **New → Blueprint**,
select this GitHub repository, and deploy the supplied `render.yaml`. The
Blueprint defines a free Python web service, a Gunicorn startup command, and a
health check. Alternatively, create a Web Service and copy the build and start
commands from that file. The dashboard shows the assigned `onrender.com` URL.

[Render Flask deployment guide](https://render.com/docs/deploy-flask)
