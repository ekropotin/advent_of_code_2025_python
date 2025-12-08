import fileinput


def calc_timelines(grid: list[str]):
    R, C = len(grid), len(grid[0])
    s_c = grid[0].find("S")
    curr_row_memo = [0] * C
    curr_row_memo[s_c] = 1
    res = 0

    for r in range(1, R):
        next_row_memo = [0] * C
        for c in range(C):
            n = curr_row_memo[c]
            if n == 0:
                # there are no paths leading here
                continue

            ch = grid[r][c]
            if ch == ".":
                # Empty cell
                if r == R - 1:
                    # Path reached OOB of the field
                    # No more splitting to happen for this column. Flush the result
                    res += n
                else:
                    next_row_memo[c] += n
            else:
                # Splitter
                if r == R - 1:
                    res += 2 * n
                    continue
                if c not in range(0, C):
                    # we reached OOB, flush amount of paths
                    res += n
                    continue
                if c - 1 >= 0:
                    next_row_memo[c - 1] += n
                if c + 1 < C:
                    next_row_memo[c + 1] += n

        curr_row_memo = next_row_memo

    return res


def main():
    lines = []
    with fileinput.input() as f:
        for line in f:
            lines.append(line.rstrip("\n"))
    print(calc_timelines(lines))


if __name__ == "__main__":
    main()
