import fileinput
from collections import defaultdict

def main():
    adj_list = defaultdict(list)
    all_nodes = set()
    with fileinput.input() as f:
        for line in f:
            parts = line.rstrip("\n").split(" ")
            node = parts[0][:-1]
            neighbors = parts[1:]
            adj_list[node] = neighbors
            all_nodes.add(node)
            all_nodes.update(neighbors)

    print(f"Total nodes: {len(all_nodes)}")
    print(f"Nodes with outgoing edges: {len(adj_list)}")

    # Check for key nodes
    print(f"\nsvr in graph: {'svr' in adj_list}")
    if 'svr' in adj_list:
        print(f"  svr -> {adj_list['svr']}")

    print(f"dac in graph: {'dac' in adj_list}")
    if 'dac' in adj_list:
        print(f"  dac -> {adj_list['dac']}")

    print(f"fft in graph: {'fft' in adj_list}")
    if 'fft' in adj_list:
        print(f"  fft -> {adj_list['fft']}")

    # Count edges
    total_edges = sum(len(neighbors) for neighbors in adj_list.values())
    print(f"\nTotal edges: {total_edges}")
    print(f"Average out-degree: {total_edges / len(adj_list):.2f}")

    # Find max out-degree
    max_out = max((len(neighbors), node) for node, neighbors in adj_list.items())
    print(f"Max out-degree: {max_out[0]} (node: {max_out[1]})")

    # Nodes leading to 'out'
    to_out = [node for node, neighbors in adj_list.items() if 'out' in neighbors]
    print(f"\nNodes that directly connect to 'out': {len(to_out)}")
    print(f"Sample: {to_out[:5]}")

if __name__ == "__main__":
    main()
