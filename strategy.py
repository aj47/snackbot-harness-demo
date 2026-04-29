"""SnackBot route strategy.

The harness allows editing this file only.

Implement:
    plan_route(city: dict, orders: list[dict]) -> list[str]

Return a list of order IDs in the order SnackBot should deliver them.
"""


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def blocked_crossings(a, b, blocked):
    x, y = a
    bx, by = b
    hits = 0

    step_x = 1 if bx >= x else -1
    while x != bx:
        x += step_x
        if (x, y) in blocked:
            hits += 1

    step_y = 1 if by >= y else -1
    while y != by:
        y += step_y
        if (x, y) in blocked:
            hits += 1

    return hits


def build_scorer(city, orders):
    start = tuple(city["start"])
    max_steps = int(city["max_steps"])
    travel_cost = int(city.get("travel_cost", 1))
    late_penalty = int(city.get("late_penalty", 6))
    deadline_bonus = int(city.get("deadline_bonus", 3))
    blocked = {tuple(cell) for cell in city.get("blocked", [])}
    order_by_id = {order["id"]: order for order in orders}

    def score_route(route):
        position = start
        travel_steps = 0
        score = 0

        for order_id in route:
            order = order_by_id[order_id]
            destination = tuple(order["location"])
            leg = distance(position, destination)
            travel_steps += leg
            score -= leg * travel_cost
            score -= blocked_crossings(position, destination, blocked) * 4

            if travel_steps <= max_steps:
                score += int(order["tip"])
                if travel_steps <= int(order["deadline"]):
                    score += deadline_bonus
                else:
                    score -= late_penalty
            else:
                score -= 8

            position = destination

        if travel_steps > max_steps:
            score -= (travel_steps - max_steps) * 2

        return score

    return score_route


def plan_route(city, orders):
    """Deterministic best-insertion route with local search improvements."""
    remaining_ids = [order["id"] for order in orders]
    route = []
    score_route = build_scorer(city, orders)
    best_score = score_route(route)

    # Grow the route by repeatedly applying the best positive insertion.
    while True:
        best_delta = 0
        best_candidate = None

        for order_id in remaining_ids:
            for index in range(len(route) + 1):
                candidate = route[:index] + [order_id] + route[index:]
                candidate_score = score_route(candidate)
                delta = candidate_score - best_score
                if delta > best_delta:
                    best_delta = delta
                    best_candidate = (candidate, order_id, candidate_score)

        if best_candidate is None:
            break

        route, chosen_id, best_score = best_candidate
        remaining_ids.remove(chosen_id)

    # Improve ordering with deterministic local search.
    improved = True
    while improved:
        improved = False
        current_score = best_score
        n = len(route)

        # 1) Remove low-value stops if deletion improves score.
        for i in range(n):
            candidate = route[:i] + route[i + 1 :]
            candidate_score = score_route(candidate)
            if candidate_score > current_score:
                route = candidate
                best_score = candidate_score
                improved = True
                break
        if improved:
            continue

        # 2) Relocate one stop to a better position.
        for i in range(n):
            moved = route[i]
            base = route[:i] + route[i + 1 :]
            for j in range(n):
                candidate = base[:j] + [moved] + base[j:]
                candidate_score = score_route(candidate)
                if candidate_score > current_score:
                    route = candidate
                    best_score = candidate_score
                    improved = True
                    break
            if improved:
                break
        if improved:
            continue

        # 3) Swap two stops.
        for i in range(n):
            for j in range(i + 1, n):
                candidate = route[:]
                candidate[i], candidate[j] = candidate[j], candidate[i]
                candidate_score = score_route(candidate)
                if candidate_score > current_score:
                    route = candidate
                    best_score = candidate_score
                    improved = True
                    break
            if improved:
                break
        if improved:
            continue

        # 4) Reverse a segment (2-opt style adjustment).
        for i in range(n):
            for j in range(i + 2, n + 1):
                candidate = route[:i] + list(reversed(route[i:j])) + route[j:]
                candidate_score = score_route(candidate)
                if candidate_score > current_score:
                    route = candidate
                    best_score = candidate_score
                    improved = True
                    break
            if improved:
                break

    return route
