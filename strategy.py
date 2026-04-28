"""SnackBot route strategy.

The harness allows editing this file only.

Implement:
    plan_route(city: dict, orders: list[dict]) -> list[str]

Return a list of order IDs in the order SnackBot should deliver them.
"""


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def plan_route(city, orders):
    """Baseline: deliver nearest remaining order until no orders remain."""
    position = tuple(city["start"])
    remaining = [dict(order) for order in orders]
    route = []

    while remaining:
        nearest = min(
            remaining,
            key=lambda order: distance(position, tuple(order["location"])),
        )
        route.append(nearest["id"])
        position = tuple(nearest["location"])
        remaining.remove(nearest)

    return route
