import fileinput


def main():
    res = 0
    pos = 50
    with fileinput.input() as f:
        for line in f:
            direction = line[:1]
            distance = int(line[1:])
            # First step count where we land on zero
            first_hit = 100 - pos if direction == "R" else pos
            # Edge case: We are on zero already. In that case, 100 clicks in either direction needed for the next hit
            first_hit = 100 if first_hit == 0 else first_hit

            if distance >= first_hit:
                # Count the first hit + amount of full wraps after that
                res += 1 + (distance - first_hit) // 100

            pos = (pos + distance) % 100 if direction == "R" else (pos - distance) % 100

    print(res)


if __name__ == "__main__":
    main()
