import fileinput


def main():
    with fileinput.input() as f:
        res = 0
        for line in f:
            print(f"processing {line}")
            max_1, max_2 = -1, -1
            max_1_pos = -1
            for i in range(0, len(line) - 2):
                num = int(line[i])
                if num > max_1:
                    max_1 = num
                    max_1_pos = i
            for i in range(max_1_pos + 1, len(line) - 1):
                num = int(line[i])
                max_2 = max(num, max_2)
            res += 10 * max_1 + max_2
            print(f"biggest number: {10 * max_1 + max_2}")

    print(res)


if __name__ == "__main__":
    main()
