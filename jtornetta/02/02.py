from pathlib import Path

def is_safe(lst):
    return sorted(lst) in [lst, lst[::-1]] \
       and all(1 <= abs(a-b) <= 3 for a, b in zip(lst, lst[1:]))

def main():
    PROJECT_DIR = Path(__file__).parent

    full_safe, one_bad_level_safe = 0, 0
    for line in open(PROJECT_DIR/'input.txt'):
        data = [int(x) for x in line.split()]
        if is_safe(data):
            full_safe += 1
        elif any(is_safe(data[:i] + data[i+1:]) for i in range(len(data))):
            one_bad_level_safe += 1

    print('Part 1 safe:', full_safe)
    print('Part 2 safe:', full_safe + one_bad_level_safe)


if __name__=="__main__":
    main() 