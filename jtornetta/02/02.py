from pathlib import Path

def is_safe(lst):
    # Checks if a given list of levels (integers) is considered "safe" according to the puzzle rules:
    #
    # Part 1 of the puzzle:
    # - The report (list of levels) must be strictly increasing or strictly decreasing.
    #   This means when sorted, the list must match either the original list (already ascending)
    #   or the reversed original list (already descending).
    # - Any two adjacent levels must differ by at least 1 and at most 3.
    #
    # 1. Check if the list is sorted ascending or exactly sorted descending.
    #    If sorted(lst) == lst, it's ascending.
    #    If sorted(lst) == lst[::-1], it's descending.
    #    Otherwise, it's not strictly one direction.
    #
    # 2. Check all adjacent differences: For each pair of consecutive levels (a, b),
    #    verify that 1 <= abs(a - b) <= 3.
    #
    # If both checks pass, return True; otherwise, return False.

    return sorted(lst) in [lst, lst[::-1]] \
       and all(1 <= abs(a-b) <= 3 for a, b in zip(lst, lst[1:]))


def main():
    """
    Main function:
    
    Puzzle Narrative:
    You're helping engineers at a Red-Nosed Reindeer nuclear reactor analyze "reports."
    Each report consists of several levels (integers). The reactor's safety systems
    tolerate certain patterns of levels. Initially (Part 1), a report is considered safe
    only if it's entirely increasing or entirely decreasing and each step is between 1 and 3.
    
    After determining how many reports are safe by this standard, the engineers introduce
    the "Problem Dampener" (Part 2). With the Problem Dampener, a single "bad" level 
    (one that breaks the safety pattern) can be removed from the sequence. If removing 
    one level from an otherwise unsafe report makes it safe, that report now also counts 
    as safe.
    
    Steps for the code:
    - Read each line (a report) from 'input.txt'.
    - Convert it into a list of integers.
    - Check if it's safe by the original rules (Part 1).
      If it is, increment full_safe (the count of reports that need no modification).
    - If it's not safe under the original rules, check if removing one level 
      could make it safe (Part 2 scenario). 
      For each position in the list, try removing that level and check again if the resulting
      list is safe. If yes for any removal, increment one_bad_level_safe.
    
    In the end:
    - Part 1 safe count = Number of reports safe without any removal.
    - Part 2 safe count = Number of reports safe by either original rules 
      or by removing one level.
    
    Print both counts.
    """

    PROJECT_DIR = Path(__file__).parent

    full_safe, one_bad_level_safe = 0, 0
    for line in open(PROJECT_DIR/'input.txt'):
        # Convert each line into a list of integers representing levels in the report.
        data = [int(x) for x in line.split()]

        # Check if the report is safe under the original rules (no removals).
        if is_safe(data):
            full_safe += 1
        else:
            # If not safe, check if removing one level can make it safe.
            # The Problem Dampener allows for one problematic level to be removed.
            # If after removing one level the report becomes safe, then count it in one_bad_level_safe.
            if any(is_safe(data[:i] + data[i+1:]) for i in range(len(data))):
                one_bad_level_safe += 1

    # Part 1 safe: reports that were safe without modifications.
    print('Part 1 safe:', full_safe)

    # Part 2 safe: reports safe without modifications plus those that become safe 
    # by removing one "bad" level.
    print('Part 2 safe:', full_safe + one_bad_level_safe)


if __name__=="__main__":
    main()
