from collections import defaultdict


def main():
    with open("test.txt") as f:
        lines = f.readlines()
        operators = lines[-1].split()
        cols = defaultdict(list)
        for line in lines[:-1]:
            for i, num in enumerate(line.split()):
                cols[i].append(num)

        res = 0
        cols_len = len(cols[0])
        print(f"cols: {cols_len}")
        for i, nums in cols.items():
            op = operators[i]
            tmp_res = 1 if op == "*" else 0
            curr_pos = 0
            padded_count = 0
            print(f"processing {nums} with {op}")
            while padded_count < cols_len:
                for num_str in nums:
                    if curr_pos >= len(num_str):
                        padded_count += 1
                        continue
                    digit = int(num_str[curr_pos])
                    print(f"digit {digit} at pos {curr_pos}")
                    if op == "+":
                        tmp_res += digit
                    else:
                        tmp_res *= digit

                # print(f"padded: {padded_count}")
                if padded_count >= cols_len:
                    break
                padded_count = 0
                curr_pos += 1
            res += tmp_res
        print(res)


if __name__ == "__main__":
    main()
