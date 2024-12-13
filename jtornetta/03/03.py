from pathlib import Path
import re

def parse_instructions(data):
    """
    Parses the given data string and returns a list of instructions found.

    Each instruction is represented as a tuple indicating which instruction was matched:
    - ("do",)
    - ("don't",)
    - ("mul", x, y)  where x and y are integers

    Only correctly formatted instructions are returned; all other text is ignored.
    """
    regex = r"(do\(\))|(don't\(\))|(mul\((\d+),(\d+)\))"
    instructions = []

    for match in re.findall(regex, data):
        if match[0]:
            # Found "do()"
            instructions.append(("do",))
        elif match[1]:
            # Found "don't()"
            instructions.append(("don't",))
        else:
            # Found "mul(X,Y)" with X and Y in match[3] and match[4]
            x = int(match[3])
            y = int(match[4])
            instructions.append(("mul", x, y))

    return instructions

def process_instructions(instructions):
    """
    Processes a list of instructions and returns a list of results.

    - Initially, mul instructions are enabled (valid = 1).
    - "do()" sets valid to 1 (enabled).
    - "don't()" sets valid to 0 (disabled).
    - "mul(X,Y)" adds X*Y to the total sum of all multiplications, and also to the "enabled" sum 
      if currently enabled.

    Returns:
    - res: A list [sum_all, sum_enabled]
      sum_all: Sum of all mul(...) results.
      sum_enabled: Sum of mul(...) results that occurred while mul was enabled.
    """
    res = [0, 0]
    valid = 1  # Initially enabled

    for instruction in instructions:
        if instruction[0] == "do":
            valid = 1
        elif instruction[0] == "don't":
            valid = 0
        elif instruction[0] == "mul":
            x, y = instruction[1], instruction[2]
            product = x * y
            res[0] += product
            if valid:
                res[1] += product

    return res

def main():
    PROJECT_DIR = Path(__file__).parent
    input_file = PROJECT_DIR / 'input.txt'

    with open(input_file, 'r') as f:
        data = f.read()

    # Parse instructions from the data
    instructions = parse_instructions(data)

    # Process the parsed instructions to get the results
    results = process_instructions(instructions)

    # Print the results: [sum_all, sum_enabled]
    print(results)

if __name__ == "__main__":
    main()
