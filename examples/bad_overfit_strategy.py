"""Bad example: optimizes one obvious idea too hard.

This greedily chases tips and ignores travel/deadlines, which often looks smart
but wastes the step budget and regresses the score.
"""


def plan_route(city, orders):
    return [order["id"] for order in sorted(orders, key=lambda o: o["tip"], reverse=True)]
