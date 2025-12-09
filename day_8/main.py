import fileinput
import heapq
from scipy.cluster.hierarchy import DisjointSet


def main():
    coordinates = []
    with fileinput.input() as f:
        for i, line in enumerate(f):
            coordinates.append([int(coord) for coord in line.rstrip("\n").split(",")])

    BOX_COUNT = len(coordinates)
    disjoint_set = DisjointSet(range(0, BOX_COUNT))

    # minheap of distances
    heap = []
    for i in range(0, BOX_COUNT):
        x1, y1, z1 = coordinates[i]
        for j in range(i + 1, BOX_COUNT):
            x2, y2, z2 = coordinates[j]
            dist = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
            heapq.heappush(heap, (dist, i, j))

    while True:
        _, box1, box2 = heapq.heappop(heap)
        disjoint_set.merge(box1, box2)
        if disjoint_set.subset_size(box1) == BOX_COUNT:
            print(coordinates[box1][0] * coordinates[box2][0])
            break


if __name__ == "__main__":
    main()
