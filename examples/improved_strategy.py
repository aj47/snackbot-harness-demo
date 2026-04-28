"""Example improved SnackBot strategy.

Generic heuristic: prefer high value, nearby, urgent orders and stop before the
step budget gets too expensive. This is intentionally not optimal.
"""


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def plan_route(city, orders):
    position = tuple(city["start"])
    max_steps = int(city.get("max_steps", 10**9))
    remaining = [dict(order) for order in orders]
    route = []
    elapsed = 0

    while remaining:
        best_order = None
        best_score = None
        best_arrival = None

        for order in remaining:
            location = tuple(order["location"])
            travel = distance(position, location)
            arrival = elapsed + travel
            lateness = max(0, arrival - int(order["deadline"]))
            slack = int(order["deadline"]) - arrival
            urgency = 10 / max(1, slack + 8) if slack >= -5 else 0

            # Main tradeoff: high tips are good, travel and lateness are bad.
            score = int(order["tip"]) - 4 * travel - lateness + urgency

            # Avoid routes that run beyond the budget unless the order is amazing.
            if arrival > max_steps:
                score -= 100

            if best_score is None or score > best_score:
                best_score = score
                best_order = order
                best_arrival = arrival

        if best_order is None or best_score is None or best_score < -40:
            break

        route.append(best_order["id"])
        position = tuple(best_order["location"])
        elapsed = best_arrival
        remaining.remove(best_order)

    return route
