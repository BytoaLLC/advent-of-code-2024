import itertools
from math import gcd
from pathlib import Path

def collect_antennas_by_frequency(input_lines):
    """
    According to the puzzle narrative, each position in the grid may contain an antenna 
    represented by an alphanumeric character (0-9, A-Z, a-z), which indicates its frequency. 
    Different frequencies are considered completely distinct, e.g., 'A' vs 'a'.
    
    This function scans the grid (list of input lines) and groups the coordinates 
    of antennas by their frequency. For example, if 'a' appears at multiple grid positions, 
    all those positions are collected under frequency 'a'.
    
    Returns:
    - antennas_by_freq: A dictionary mapping each frequency character to a list of (row, col) positions.
    - total_rows: Total number of rows in the grid.
    - total_cols: Number of columns in the longest row of the grid.
    """
    antennas_by_freq = {}
    total_rows = len(input_lines)
    total_cols = max(len(line) for line in input_lines) if input_lines else 0
    
    for row_index, line in enumerate(input_lines):
        for col_index, char in enumerate(line):
            if char.isalnum():
                # Add this antenna's position under its frequency character
                antennas_by_freq.setdefault(char, []).append((row_index, col_index))
                
    return antennas_by_freq, total_rows, total_cols


def get_line_positions(row_start, col_start, row_end, col_end, total_rows, total_cols):
    """
    In the updated model (Part 2 of the puzzle), any position that lies on a straight line 
    defined by two antennas of the same frequency is considered an antinode position.
    
    This function finds every grid cell that lies on the infinite straight line passing 
    through two given points. The line is extended across the entire grid in both directions, 
    and all positions along that line are collected.
    
    Returns:
    A set of (row, col) positions on that line within the grid boundaries.
    """
    line_positions = set()
    delta_row = row_end - row_start
    delta_col = col_end - col_start
    
    # Determine the step increments by using the greatest common divisor
    step_divisor = gcd(delta_row, delta_col) or 1
    step_row = delta_row // step_divisor
    step_col = delta_col // step_divisor
    
    # Trace the line in both directions starting from one antenna
    for direction in (1, -1):
        current_row, current_col = row_start, col_start
        while 0 <= current_row < total_rows and 0 <= current_col < total_cols:
            line_positions.add((current_row, current_col))
            current_row += step_row * direction
            current_col += step_col * direction
            
    return line_positions


def compute_antinode_positions(antennas_by_freq, total_rows, total_cols, mode='part1'):
    """
    The puzzle describes two different criteria for identifying antinodes:

    Part 1:
    An antinode occurs for two antennas of the same frequency if one antenna is exactly twice as far 
    from a point as the other. In other words, given two antennas A and B of the same frequency, 
    the positions that line up as "2B - A" and "2A - B" relative to them are antinodes if they fall within the grid.

    Part 2:
    The resonant harmonics mean that now an antinode occurs at *any* position that lies on a straight line 
    defined by two antennas of the same frequency. This greatly increases the number of antinodes since 
    it's no longer just about being twice the distance; any position collinear with at least two same-frequency 
    antennas counts.

    Parameters:
    - mode='part1': Use the original rule (antinode where one antenna is double the distance of the other).
    - mode='part2': Use the updated rule (antinode at all collinear positions).

    Returns:
    A set of all unique antinode positions in the grid.
    """
    antinodes = set()
    
    for freq, antenna_positions in antennas_by_freq.items():
        # Consider all pairs of antennas with the same frequency
        for antenna_a, antenna_b in itertools.combinations(antenna_positions, 2):
            row_a, col_a = antenna_a
            row_b, col_b = antenna_b
            
            if mode == 'part1':
                # Compute the two potential antinodes from the pair A-B
                reflected_from_a = (2 * row_b - row_a, 2 * col_b - col_a)  # 2B - A
                reflected_from_b = (2 * row_a - row_b, 2 * col_a - col_b)  # 2A - B
                
                for candidate in [reflected_from_a, reflected_from_b]:
                    if 0 <= candidate[0] < total_rows and 0 <= candidate[1] < total_cols:
                        antinodes.add(candidate)
            
            elif mode == 'part2':
                # For the updated rule, include all positions on the line passing through A and B
                line_positions = get_line_positions(row_a, col_a, row_b, col_b, total_rows, total_cols)
                antinodes.update(line_positions)
    
    return antinodes


def main():
    """
    Puzzle Narrative Context:
    We have a grid filled with antennas of various frequencies. 
    Each frequency is represented by a single alphanumeric character.
    
    Part One Scenario:
    Antinodes appear only under the strict "twice the distance" condition. 
    For every pair of same-frequency antennas, we add the two antinode positions that result 
    if they fall within the grid boundaries.

    Part Two Scenario:
    After considering resonant harmonics, an antinode occurs at any position that lies 
    straight in line with at least two antennas of the same frequency, 
    no matter the distance. Thus, every collinear position with a frequency pair becomes an antinode.

    This program:
    - Reads the antenna map.
    - Identifies antennas by their frequencies and collects their coordinates.
    - Computes antinodes first under the original rule (Part 1).
    - Computes antinodes again under the updated rule (Part 2).
    
    It then prints the number of unique antinodes found for both parts. 
    """

    input_file = Path(__file__).parent / 'input.txt'
    
    with open(input_file, 'r') as file:
        input_lines = [line.rstrip('\n') for line in file]
    
    # Gather antenna positions by frequency
    antennas_by_freq, rows, cols = collect_antennas_by_frequency(input_lines)
    
    # Part 1: Original antinode calculation
    antinodes_part1 = compute_antinode_positions(antennas_by_freq, rows, cols, 'part1')
    print(f"Part1 - Unique antinode positions: {len(antinodes_part1)}")
    
    # Part 2: Updated antinode calculation with resonant harmonics
    antinodes_part2 = compute_antinode_positions(antennas_by_freq, rows, cols, 'part2')
    print(f"Part2 - Unique antinode positions: {len(antinodes_part2)}")
    

if __name__ == "__main__":
    main()
