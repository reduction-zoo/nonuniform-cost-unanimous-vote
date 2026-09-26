"""Independent exact oracles for Partition and fixed-order Unanimous Vote."""

import argparse
import json
import subprocess
import sys
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path


def legal_source(source):
    return (isinstance(source, dict) and isinstance(source.get("weights"), list)
            and all(type(weight) is int and weight > 0 for weight in source["weights"]))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal Partition instance")
    weights = source["weights"]
    total = sum(weights)
    if total % 2:
        return {"status": "NO-SOLUTION"}
    for mask in range(1 << len(weights)):
        subset = [index for index in range(len(weights)) if mask & (1 << index)]
        if sum(weights[index] for index in subset) * 2 == total:
            return {"subset": subset}
    return {"status": "NO-SOLUTION"}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    subset = output.get("subset")
    weights = source["weights"]
    return (set(output) == {"subset"} and isinstance(subset, list)
            and all(type(index) is int and 0 <= index < len(weights) for index in subset)
            and len(set(subset)) == len(subset)
            and 2 * sum(weights[index] for index in subset) == sum(weights))


def rational_pair(value):
    return (isinstance(value, list) and len(value) == 2
            and all(type(part) is int for part in value) and value[1] > 0)


def legal_target(target):
    if not isinstance(target, dict):
        return False
    probabilities, costs, bound = (target.get(key) for key in ("probabilities", "costs", "bound"))
    return (isinstance(probabilities, list) and isinstance(costs, list)
            and len(probabilities) == len(costs) and rational_pair(bound)
            and all(rational_pair(probability) and 0 < Fraction(*probability) < 1 for probability in probabilities)
            and all(rational_pair(cost) and Fraction(*cost) > 0 for cost in costs))


def expected_cost(target, order):
    probabilities = [Fraction(*pair) for pair in target["probabilities"]]
    costs = [Fraction(*pair) for pair in target["costs"]]
    heads = tails = Fraction(1)
    total = Fraction(0)
    for position, index in enumerate(order):
        total += costs[index] * (1 if position == 0 else heads + tails)
        heads *= probabilities[index]
        tails *= 1 - probabilities[index]
    return total


def target_solutions(target, limit=3):
    if not legal_target(target):
        raise ValueError("Illegal Unanimous Vote instance")
    bound = Fraction(*target["bound"])
    answers = []
    for order in permutations(range(len(target["probabilities"]))):
        if expected_cost(target, order) <= bound:
            answers.append({"order": list(order)})
            if len(answers) >= limit:
                break
    return answers or [{"status": "NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target, limit=1)[0]


def valid_target(target, output):
    if not legal_target(target) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_target(target) == output
    order = output.get("order")
    n = len(target["probabilities"])
    return (set(output) == {"order"} and isinstance(order, list)
            and len(order) == n and all(type(index) is int for index in order)
            and set(order) == set(range(n))
            and expected_cost(target, order) <= Fraction(*target["bound"]))


def direct_expected_cost(target, order):
    probabilities = [Fraction(*pair) for pair in target["probabilities"]]
    costs = [Fraction(*pair) for pair in target["costs"]]
    total = Fraction(0)
    for outcomes in product((False, True), repeat=len(order)):
        chance = Fraction(1)
        for index, outcome in enumerate(outcomes):
            chance *= probabilities[index] if outcome else 1 - probabilities[index]
        spent = Fraction(0)
        first = None
        for index in order:
            spent += costs[index]
            if first is None:
                first = outcomes[index]
            elif outcomes[index] != first:
                break
        total += chance * spent
    return total


def self_test():
    from generate_cases import EDGE_CASES, random_source

    root = Path(__file__).resolve().parents[3]
    cases_path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable, str(root / "research/validate_preparation.py"), str(cases_path)], check=True, cwd=root)
    cases = json.loads(cases_path.read_text())
    for weights, expected_satisfiable in EDGE_CASES:
        assert ("subset" in solve_source({"weights": weights})) == expected_satisfiable
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current, expected = solve_source(source), case["expected"]
        reachable = {0}
        for weight in source["weights"]:
            reachable |= {sum_so_far + weight for sum_so_far in reachable}
        total = sum(source["weights"])
        assert ("subset" in current) == (total % 2 == 0 and total // 2 in reachable)
        assert ("subset" in current) == ("subset" in expected)
        assert valid_source(source, expected)
        assert valid_source(source, current)

    even = {"weights": [1, 1]}
    odd = {"weights": [1, 2]}
    assert valid_source(even, {"subset": [0]})
    assert not valid_source(even, {"subset": []})
    assert valid_source(even, solve_source(even))
    assert solve_source(odd) == {"status": "NO-SOLUTION"}
    assert not valid_source(even, {"subset": [0, 0]})

    feasible = {"probabilities": [[1, 2], [1, 2], [1, 2]],
                "costs": [[1, 1], [2, 1], [3, 1]], "bound": [9, 2]}
    infeasible = {**feasible, "bound": [4, 1]}
    assert valid_target(feasible, {"order": [0, 1, 2]})
    assert not valid_target(feasible, {"order": [2, 1, 0]})
    assert valid_target(feasible, solve_target(feasible))
    assert solve_target(infeasible) == {"status": "NO-SOLUTION"}
    assert valid_target(infeasible, {"status": "NO-SOLUTION"})
    assert not valid_target(feasible, {"order": [0, 0, 1]})
    assert not legal_target({"probabilities": [[0, 1]], "costs": [[1, 1]], "bound": [1, 1]})

    target_cases = 0
    for n in range(5):
        for pattern in ((0,) if n == 0 else (0, 1)):
            probabilities = [[1 + (index + pattern) % 3, 4] for index in range(n)]
            costs = [[1 + (index * 2 + pattern) % 4, 1] for index in range(n)]
            target = {"probabilities": probabilities, "costs": costs, "bound": [0, 1]}
            costs_by_order = [direct_expected_cost(target, order) for order in permutations(range(n))]
            for order, direct in zip(permutations(range(n)), costs_by_order):
                assert expected_cost(target, order) == direct
            optimum = min(costs_by_order)
            for bound, should_exist in ((optimum, True), (optimum - Fraction(1, 6), False)):
                target["bound"] = [bound.numerator, bound.denominator]
                assert ("order" in solve_target(target)) == should_exist
                target_cases += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {target_cases} exact target threshold checks")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable, str(path)], input=json.dumps(source), text=True, capture_output=True, check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Candidate produced an illegal target from {source}")
        for target_output in target_solutions(target):
            if not valid_target(target, target_output):
                raise AssertionError(f"Target oracle returned an invalid output: {target_output}")
            payload = {"source": source, "target_solution": target_output}
            extraction = subprocess.run([sys.executable, str(path), "--extract"], input=json.dumps(payload), text=True, capture_output=True, check=True)
            source_output = json.loads(extraction.stdout)
            if not valid_source(source, source_output):
                raise AssertionError(f"Invalid recovery from {target_output}: {source_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} independently solved target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
