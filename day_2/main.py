import fileinput


def has_repeats(s: str):
    for seq_len in range(1, len(s) // 2 + 1):
        if len(s) % seq_len != 0:
            continue
        match = s[0:seq_len]
        i = seq_len
        while True:
            if s[i : i + seq_len] != match:
                break
            if i + seq_len == len(s):
                return True
            i += seq_len


def main():
    res = 0
    with fileinput.input() as f:
        line = f.readline()
        ranges = line.split(",")
        for r in ranges:
            start, end = r.split("-")
            print(f"processing range: {start} - {end}")
            for i in range(int(start), int(end) + 1):
                print(f"processing {i}")
                if has_repeats(str(i)):
                    res += i
    print(res)


if __name__ == "__main__":
    main()
