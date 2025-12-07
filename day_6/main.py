import math


def main():
    lines = []
    max_line_len = 0
    res = 0

    with open("input.txt") as f:
        for line in f:
            lines.append(line[:-1])
            max_line_len = max(max_line_len, len(line) - 1)

    col_idx = max_line_len - 1
    batch = []
    while col_idx >= 0:
        tmp_num = ""
        for line_idx, line in enumerate(lines):
            if line_idx == len(lines) - 1:
                # Last line
                batch.append(tmp_num)
                if col_idx < len(line) and line[col_idx] in set(["+", "*"]):
                    # we landed of + or *
                    # Perform calculation and move to the next batch
                    if line[col_idx] == "+":
                        res += sum([int(num) for num in batch])
                    else:
                        res += math.prod([int(num) for num in batch])
                    batch = []
                    # skip delim between batches
                    col_idx -= 1
            else:
                if col_idx < len(line) and line[col_idx]:
                    tmp_num += line[col_idx]

        col_idx -= 1

    print(res)


if __name__ == "__main__":
    main()
