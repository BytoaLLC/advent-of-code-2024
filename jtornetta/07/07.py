from pathlib import Path
from itertools import product
from typing import List, Tuple, Dict
from functools import lru_cache

def parse_input(file_path: Path) -> List[Tuple[int, List[int]]]:
    """Load and parse each line from our input file into a list of equations.
    
    For example, a line like "190: 10 19" gets converted into:
    - test_value = 190 (what we're trying to make)
    - numbers = (10, 19) (the numbers we can use)
    
    I use tuples instead of lists for the numbers because tuples are immutable,
    which lets me use them as dictionary keys and in caching."""
    equations = []
    with file_path.open() as f:
        for line in f:
            if line.strip():
                test_str, nums_str = line.split(': ')
                test_value = int(test_str)
                numbers = tuple(int(x) for x in nums_str.split())
                equations.append((test_value, numbers))
    return equations

@lru_cache(maxsize=10000)
def quick_concat(a: int, b: int) -> int:
    """Concatenate two numbers together using math operations.
    
    The @lru_cache decorator tells Python to remember the results of this function.
    If its called again with the same inputs, it returns the cached result instead
    of recalculating. This is to help improve the speed due to the repeated concatenations.
    
    How it works for quick_concat(12, 345):
    1. 345 has 3 digits
    2. 12 * 10^3 = 12000
    3. 12000 + 345 = 12345
    
    This should be faster than converting both numbers to strings, concatenating,
    and converting back to an integer."""
    b_str = str(b)  # Convert second number to string to count digits
    return a * (10 ** len(b_str)) + b

def evaluate(numbers: List[int], operators: List[str], target: int) -> bool:
    """Try to reach the target value by applying operators to numbers left-to-right.
    
    For example, with numbers [2, 3, 4] and operators ['+', '*']:
    1. Start with 2
    2. Apply '+' to get 2 + 3 = 5
    3. Apply '*' to get 5 * 4 = 20
    
    We return False early if our result gets too big (over 10^15) since our
    target values are never that large. This saves time by avoiding unnecessary
    calculations with huge numbers.
    
    Available operators:
    '+' : Addition
    '*' : Multiplication
    '||': Concatenation (for part 2)"""
    result = numbers[0]
    
    for i, op in enumerate(operators):
        # Exit early if number is getting huge
        if result > 10**15:
            return False
            
        num = numbers[i + 1]
        if op == '+':
            result += num
        elif op == '*':
            result *= num
        else:  # '||' (concatenation)
            result = quick_concat(result, num)
            
    return result == target

def check_equation(test_value: int, numbers: Tuple[int], use_concat: bool = False) -> bool:
    """Check if we can make the test value using our numbers and available operators.
    
    We try every possible combination of operators between the numbers. For example,
    with numbers [2, 3, 4] we might try:
    - 2 + 3 + 4
    - 2 + 3 * 4
    - 2 * 3 + 4
    - 2 * 3 * 4
    And in part 2, also:
    - 2 || 3 + 4
    - 2 + 3 || 4
    etc.
    
    Parameters:
        test_value: The number we're trying to make
        numbers: Tuple of numbers we can use
        use_concat: Whether to allow the || operator (True for part 2)"""
    if len(numbers) == 1:
        return numbers[0] == test_value
    
    # Build list of allowed operators
    ops = ['+', '*']
    if use_concat:
        ops.append('||')
    
    # Try every possible combination of operators
    num_slots = len(numbers) - 1  # We need one less operator than numbers
    for ops_combo in product(ops, repeat=num_slots):
        if evaluate(list(numbers), ops_combo, test_value):
            return True
    
    return False

def solve_parts(input_path: Path) -> Tuple[int, int]:
    """Solve both parts of the puzzle.
    
    Part 1: Using only + and * operators
    Part 2: Using +, *, and || operators
    
    1. Group equations by length (number of operands)
    2. Process all equations of the same length together
    3. If an equation works in part 1, reuse it for part 2)"""
    equations = parse_input(input_path)
    part1_sum = 0
    part2_sum = 0
    
    # Group equations by length for better cache usage
    by_length: Dict[int, List[Tuple[int, Tuple[int, ...]]]] = {}
    for test_value, numbers in equations:
        by_length.setdefault(len(numbers), []).append((test_value, numbers))
    
    # Process equations grouped by length
    for length in sorted(by_length.keys()):
        for test_value, numbers in by_length[length]:
            # Try part 1 first (no concatenation)
            if check_equation(test_value, numbers, False):
                part1_sum += test_value
                part2_sum += test_value
            # Only check part 2 if part 1 failed
            elif check_equation(test_value, numbers, True):
                part2_sum += test_value
    
    return part1_sum, part2_sum

def main():
    PROJ_DIR = Path(__file__).parent
    input_path = PROJ_DIR/'input.txt'
    part1, part2 = solve_parts(input_path)
    
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == "__main__":
    main()