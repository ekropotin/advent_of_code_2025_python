import fileinput
from collections import deque


def parse(line: str):
    part1_end = line.index("]")
    part1_parsed = line[1:part1_end]
    part2_end = line.index("{")
    part2 = line[part1_end + 1 : part2_end]
    part2_parsed = [
        list(map(int, part[1:-1].split(","))) for part in part2.split(" ") if part
    ]
    part3_parsed = [int(num) for num in line[part2_end + 1 : -2].split(",")]
    return (part1_parsed, part2_parsed, part3_parsed)


# Example: "...#." -> 0b1000
def state_mask(state: str):
    target_state_mask = 0
    for i, ch in enumerate(state):
        if ch == "#":
            target_state_mask |= 1 << i
    return target_state_mask


def button_flip_mask(button: list[int]):
    res = 0
    for light_num in button:
        res |= 1 << light_num
    return res


def calculate(target_state: str, buttons: list[int]):
    # Example: "...#." -> 0b1000
    target_state_mask = state_mask(target_state)
    button_masks = list(map(button_flip_mask, buttons))

    # Brute-force all state transitions via BFS, until we get into target state
    visited = set([0])
    queue = deque([(0, 0)])
    while queue:
        state, count = queue.popleft()
        if state == target_state_mask:
            return count
        for mask in button_masks:
            next_state = state ^ mask
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, count + 1))


def main():
    res = 0
    with fileinput.input() as f:
        for line in f:
            parsed = parse(line)
            res += calculate(parsed[0], parsed[1])
    print(res)


if __name__ == "__main__":
    main()
