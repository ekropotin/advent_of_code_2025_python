import fileinput
from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np


# Solve the problem via ILP
def calculate(buttons: list[list[int]], targets: list[int]):
    n_buttons = len(buttons)
    n_counters = len(targets)

    # Build constraint matrix A where A[j][i] = 1 if button i affects counter j
    A_eq = np.zeros((n_counters, n_buttons))
    for button_idx, button in enumerate(buttons):
        for counter_idx in button:
            A_eq[counter_idx][button_idx] = 1

    # Objective: minimize sum of button presses (all coefficients = 1)
    c = np.ones(n_buttons)

    # Constraints: A_eq @ x = b_eq (each counter must equal its target)
    constraints = LinearConstraint(A_eq, lb=targets, ub=targets)

    # Bounds: all button presses must be non-negative integers
    bounds = Bounds(lb=0, ub=np.inf)

    # Specify that all variables are integers
    integrality = np.ones(n_buttons)  # 1 means integer variable

    return milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)


def parse(line: str):
    part1_end = line.index("]")
    part1_parsed = line[1:part1_end]
    part2_end = line.index("{")
    part2 = line[part1_end + 1 : part2_end]
    part2_parsed = [
        list(map(int, part[1:-1].split(","))) for part in part2.split(" ") if part
    ]
    part3_parsed = tuple(int(num) for num in line[part2_end + 1 : -2].split(","))
    return (part1_parsed, part2_parsed, part3_parsed)


def main():
    res = 0
    with fileinput.input() as f:
        for line in f:
            parsed = parse(line)
            res += calculate(parsed[1], parsed[2])
    print(res)


if __name__ == "__main__":
    main()
