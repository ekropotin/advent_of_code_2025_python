import fileinput
import math

from scipy.cluster.hierarchy import DisjointSet


def main():
    box_to_pos = {}
    with fileinput.input() as f:
        for i, line in enumerate(f):
            box_to_pos[i] = [int(coord) for coord in line.rstrip("\n").split(",")]

    boxes_count = len(box_to_pos)

    disjoint_set = DisjointSet(range(0, boxes_count))

    def calc_distance(id1: int, id2: int):
        pos1 = box_to_pos[id1]
        pos2 = box_to_pos[id2]
        return math.sqrt(
            (pos1[0] - pos2[0]) ** 2
            + (pos1[1] - pos2[1]) ** 2
            + (pos1[2] - pos2[2]) ** 2
        )

    connects_done = 0
    CONN_LIMIT = 1000
    while connects_done < CONN_LIMIT - 1:
        closest_pair = None
        best_distance = math.inf
        for i in range(boxes_count):
            for j in range(boxes_count):
                if disjoint_set.connected(i, j):
                    continue
                dist = calc_distance(i, j)
                if dist < best_distance:
                    best_distance = dist
                    closest_pair = (i, j)
        if closest_pair:
            connects_done += 1
            print(f"connecting {closest_pair[0]} and {closest_pair[1]}")
            disjoint_set.merge(closest_pair[0], closest_pair[1])
            # print(disjoint_set.subsets())
        else:
            break

    lens = [len(subs) for subs in disjoint_set.subsets()]
    lens.sort(reverse=True)
    acc = 1
    for i in range(0, min(len(lens), 3)):
        acc *= lens[i]
    print(acc)


if __name__ == "__main__":
    main()
