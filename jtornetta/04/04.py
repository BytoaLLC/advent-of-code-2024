from pathlib import Path

def is_valid(grid, row, col):
    """
    - Returns True if (row, col) is a valid position in the grid, False otherwise.
    - Essentially a boundary check to prevent indexing outside the grid.
    """
    return 0 <= col < len(grid[0]) and 0 <= row < len(grid)

def check_xmas(grid, start_position, direction):
    """
    - Checks whether starting from 'X' at start_position, we can read 'XMAS' 
    straight through in the specified direction (horizontal, vertical, or diagonal).
    - If the subsequent cells align to form 'M', 'A', 'S' in that order, 
    we consider it a match.
    """
    start_x, start_y = start_position
    step_x, step_y = direction

    return all(
        is_valid(grid, start_y + step_y * (1 + i), start_x + step_x * (1 + i)) and
        grid[start_y + step_y * (1 + i)][start_x + step_x * (1 + i)] == c
        for i, c in enumerate("MAS")
    )

def part1(grid):
    """
    Part One:
    - We scan the entire grid for every possible occurrence of the word "XMAS".
    - The word can appear in all eight directions from each 'X' we find.
    - Each time we confirm 'XMAS' is formed in a line, we increment our count.
    - Prints the total number found after checking the entire grid.
    """
    count_occurrences = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "X":
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        if check_xmas(grid, (col, row), (dx, dy)):
                            count_occurrences += 1
    print(count_occurrences)

def check_xmas_2(grid, center_x, center_y):
    """
    Part Two Check:
    Here 'A' sits at the center of an 'X' shape made by 'M' and 'S'.
    To qualify as an "X-MAS" shape:
    - Look at the four diagonals around the 'A'.
    - They must contain exactly two 'M's and two 'S's arranged in a certain pattern.

    If these conditions are True, it counts as a valid "X-MAS".
    """
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            if not is_valid(grid, center_y + dy, center_x + dx):
                return False

    diagonal_chars = [
        grid[center_y + 1][center_x + 1],
        grid[center_y - 1][center_x - 1],
        grid[center_y - 1][center_x + 1],
        grid[center_y + 1][center_x - 1],
    ]

    return (diagonal_chars.count("S") == 2 
            and diagonal_chars.count("M") == 2 
            and diagonal_chars[0] != diagonal_chars[1])

def part2(grid):
    """
    Part Two:
    We're looking for "X-MAS" patterns, not just the word "XMAS".
    A valid "X-MAS" is formed by placing 'A' at the center and arranging 
    'M' and 'S' characters diagonally around it in a specific manner.
    
    For each 'A' found in the grid, we check if it meets the "X-MAS" criteria.
    We sum up all occurrences and print the total count.
    """
    count_x_mas = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "A":
                if check_xmas_2(grid, col, row):
                    count_x_mas += 1
    print(count_x_mas)

def main():
    """
    Puzzle Narrative:
    After failing to find the Chief Historian at the last location, you and the Historians 
    arrive at a new place where a local Elf needs help with a peculiar word search. 
    The Elf's puzzle focuses on the string "XMAS" hidden in a large grid. 
    "XMAS" might be spelled out in any direction—backwards, diagonally, you name it.

    In Part One:
    - We look through every cell of the grid and try to locate the sequence "XMAS" 
      in all possible directions. Each successful find is counted.

   In Part Two:
    - We're not just looking for the linear word "XMAS" anymore. Instead, we’re searching 
      for a special "X-MAS" formation where 'A' sits at the center of an 'X' made by 'M' and 'S'.
    
    Steps:
    1. Read the input from 'input.txt' and construct a grid of characters.
    2. Run part1 to count all straight-line occurrences of "XMAS".
    3. Run part2 to count all "X-MAS" patterns, a more complex arrangement.
    
    Once both parts are done, their totals are printed.
    """

    PROJECT_DIR = Path(__file__).parent
    with open(PROJECT_DIR / "input.txt", 'r') as f:
        grid = [list(line.strip()) for line in f]

    part1(grid)
    part2(grid)

if __name__ == "__main__":
    main()
