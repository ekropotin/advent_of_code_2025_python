import fileinput
from collections import defaultdict
import functools


# DFS on DAG with memoization
def main():
    adj = defaultdict(list)
    for line in fileinput.input():
        left, *right = line.strip().replace(":", "").split()
        adj[left] = right

    # dp[node][state] = sum(dp[child][updated_state])
    @functools.lru_cache(None)
    def count_paths(node, state):
        # 0b01 -> seen fft
        # 0b10 -> seen dac
        if node == "fft":
            state |= 1
        elif node == "dac":
            state |= 2

        if node == "out":
            # only count if both bits set
            return 1 if state == 3 else 0

        total = 0
        for nxt in adj[node]:
            total += count_paths(nxt, state)
        return total

    print(count_paths("svr", 0))


if __name__ == "__main__":
    main()
