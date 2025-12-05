import fileinput


def create_matrix():
    res = []
    with fileinput.input() as f:
        for line in f:
            res.append([ch for ch in line[:-1]])
    return res


def remove_rolls(matrix: list[list]):
    res = 0
    rows, cols = len(matrix), len(matrix[0])
    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ]
    for r in range(0, rows):
        for c in range(0, cols):
            if matrix[r][c] != "@":
                continue
            adj_count = 0
            for d in directions:
                new_r = r + d[0]
                new_c = c + d[1]
                if (
                    new_r in range(0, rows)
                    and new_c in range(0, cols)
                    and matrix[new_r][new_c] == "@"
                ):
                    adj_count += 1
            if adj_count < 4:
                matrix[r][c] = "."
                res += 1
    return res


def main():
    matrix = create_matrix()
    res = 0
    tmp = remove_rolls(matrix)
    while tmp > 0:
        res += tmp
        tmp = remove_rolls(matrix)
    print(res)


if __name__ == "__main__":
    main()
