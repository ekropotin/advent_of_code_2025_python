import fileinput


def calc_max_number(s: str):
    sum = 0
    pos = 0
    digits_left = 12
    while digits_left > 0:
        local_max = 0
        for i in range(pos, len(s) - digits_left + 1):
            d = int(s[i])
            if d > local_max:
                local_max = d
                pos = i + 1
        sum += 10 ** (digits_left - 1) * local_max
        digits_left -= 1
    return sum


def main():
    with fileinput.input() as f:
        res = 0
        for line in f:
            print(f"processing {line}")
            res += calc_max_number(line[:-1])  # strip \n from the line
    print(res)


if __name__ == "__main__":
    main()
