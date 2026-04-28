"""Bad example: this is exactly what the harness contract forbids.

Do not copy this pattern. It mentions eval order IDs and memorizes a route instead
of implementing a general routing strategy. eval.py should reject this.
"""


def plan_route(city, orders):
    return [
        "E01", "E02", "E07", "E24", "E13", "E12", "E18", "E23",
        "E19", "E11", "E09", "E20", "E27", "E08", "E25", "E10",
    ]
