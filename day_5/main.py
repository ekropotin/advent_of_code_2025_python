import fileinput


def merge_ranges(ranges: list[tuple]):
    ranges.sort()
    res = []
    curr = ranges[0]
    i = 1
    while i < len(ranges):
        next = ranges[i]
        if next[0] <= curr[1]:
            # merge if the ranges overlap
            curr[1] = max(curr[1], next[1])
        else:
            # Flush current if no overlap
            res.append(curr)
            curr = next
        i += 1

    res.append(curr)
    return res


def main():
    ranges = []
    with fileinput.input() as f:
        line = ""
        while True:
            line = f.readline()
            if line == "\n":
                break
            splitted = line.split("-")
            ranges.append([int(splitted[0]), int(splitted[1][:-1])])

    merged = merge_ranges(ranges)

    res = 0
    for interval in merged:
        res += interval[1] - interval[0] + 1

    print(res)


if __name__ == "__main__":
    main()
