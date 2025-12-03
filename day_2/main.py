import fileinput


def main():
    res = 0
    with fileinput.input() as f:
        line = f.readline()
        ranges = line.split(",")
        for r in ranges:
            start, end = r.split("-")
            print(f"processing range: {start} - {end}")
            for i in range(int(start), int(end) + 1):
                i_str = str(i)
                if len(i_str) % 2 != 0:
                    continue
                split_idx = len(i_str) // 2
                first_half = i_str[:split_idx]
                second_half = i_str[split_idx:]
                if first_half == second_half:
                    res += i
    print(res)


if __name__ == "__main__":
    main()
