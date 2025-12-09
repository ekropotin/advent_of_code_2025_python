import fileinput


def main():
    tiles = []
    with fileinput.input() as f:
        for line in f:
            c, r = line.split(",")
            tiles.append((int(r), int(c)))

    max_area = 0
    for i in range(0, len(tiles)):
        r1, c1 = tiles[i]
        for j in range(0, len(tiles)):
            r2, c2 = tiles[j]
            area = (abs(r2 - r1) + 1) * (abs(c2 - c1) + 1)
            # print(f"({c1},{r1}) and ({c2},{r2}), area {area}")
            max_area = max(max_area, area)

    print(max_area)


if __name__ == "__main__":
    main()
