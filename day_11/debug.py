import fileinput
from collections import defaultdict, deque

def main():
    adj_list = defaultdict(list)
    with fileinput.input() as f:
        for line in f:
            parts = line.rstrip("\n").split(" ")
            adj_list[parts[0][:-1]] = parts[1:]

    # Check for svr, dac, fft, out in graph
    print(f"Number of nodes: {len(adj_list)}")
    print(f"svr exists: {'svr' in adj_list}")
    print(f"svr -> {adj_list.get('svr', [])}")
    print(f"dac exists: {'dac' in adj_list}")
    print(f"dac -> {adj_list.get('dac', [])}")
    print(f"fft exists: {'fft' in adj_list}")
    print(f"fft -> {adj_list.get('fft', [])}")

    # Find all nodes that lead to 'out'
    leads_to_out = [node for node, neighbors in adj_list.items() if 'out' in neighbors]
    print(f"\nNodes that lead to 'out': {leads_to_out}")

    # Check if there's a simple path from svr to out
    def can_reach(start, end, graph, max_depth=10):
        """BFS to check reachability with depth limit"""
        queue = deque([(start, 0, {start})])
        while queue:
            node, depth, visited = queue.popleft()
            if depth > max_depth:
                continue
            if node == end:
                return True, depth
            for next_node in graph.get(node, []):
                if next_node not in visited:
                    queue.append((next_node, depth + 1, visited | {next_node}))
        return False, -1

    reachable, depth = can_reach('svr', 'out', adj_list, max_depth=20)
    print(f"\nCan reach 'out' from 'svr': {reachable}, min depth: {depth}")

    reachable, depth = can_reach('svr', 'dac', adj_list, max_depth=20)
    print(f"Can reach 'dac' from 'svr': {reachable}, depth: {depth}")

    reachable, depth = can_reach('svr', 'fft', adj_list, max_depth=20)
    print(f"Can reach 'fft' from 'svr': {reachable}, depth: {depth}")

    reachable, depth = can_reach('dac', 'out', adj_list, max_depth=20)
    print(f"Can reach 'out' from 'dac': {reachable}, depth: {depth}")

    reachable, depth = can_reach('fft', 'out', adj_list, max_depth=20)
    print(f"Can reach 'out' from 'fft': {reachable}, depth: {depth}")

if __name__ == "__main__":
    main()
