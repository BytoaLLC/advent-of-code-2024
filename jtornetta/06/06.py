from pathlib import Path
from typing import Set, Tuple, List, Optional

def get_next_position(x: int, y: int, direction: str) -> Tuple[int, int]:
    """
    Given the current coordinates (x, y) and a direction character (^, v, <, >),
    determine the next position if the guard moves one step in that direction.
    
    Directions:
    '^' means up    (y-1)
    'v' means down  (y+1)
    '<' means left  (x-1)
    '>' means right (x+1)

    Returns:
    A tuple (new_x, new_y) for the position after a single step in that direction.
    """
    moves = {
        '^': (0, -1),  
        'v': (0, 1),
        '<': (-1, 0),
        '>': (1, 0)
    }
    dx, dy = moves[direction]
    return (x + dx, y + dy)

def turn_right(direction: str) -> str:
    """
    Rotates the guard's facing direction 90 degrees clockwise.
    
    Mapping:
    '^' -> '>'
    '>' -> 'v'
    'v' -> '<'
    '<' -> '^'

    Returns the new direction after turning right once.
    """
    return {'^': '>', '>': 'v', 'v': '<', '<': '^'}[direction]

def simulate_guard(grid: List[str], block_pos: Optional[Tuple[int, int]] = None) -> Tuple[Set[Tuple[int, int]], bool]:
    """
    Simulates the guard's movement through the given grid. The guard follows these rules:
    1. If there is an obstacle directly in front, turn right.
    2. Otherwise, move forward one step.
    
    Obstacles are represented by '#' in the grid, and block_pos (if provided) acts as an additional obstacle.
    
    This simulation also detects loops:
    - The guard's state (position + direction) is tracked in a set.
    - If a state repeats, the guard is stuck in a loop.
    
    Returns:
    - A set of all (x, y) positions the guard visits.
    - A boolean indicating whether the guard gets stuck in a loop (True) or eventually leaves the map (False).
    """
    width = len(grid[0])
    height = len(grid)
    
    # Identify guard's starting position and facing direction
    start_x = start_y = None
    start_dir = None
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char in '^>v<':
                start_x, start_y = x, y
                start_dir = char
                break
        if start_dir:
            break
    
    visited_positions = {(start_x, start_y)}
    state_history = {(start_x, start_y, start_dir)}

    x, y = start_x, start_y
    direction = start_dir

    while True:
        next_x, next_y = get_next_position(x, y, direction)
        
        # If next step goes off the grid, guard leaves the map
        if not (0 <= next_x < width and 0 <= next_y < height):
            return visited_positions, False
        
        # Check if the next position is blocked either by a '#' or the optional block_pos
        is_blocked = (grid[next_y][next_x] == '#') or (block_pos and (next_x, next_y) == block_pos)
        
        if is_blocked:
            # Turn right if blocked and check for loop
            direction = turn_right(direction)
            new_state = (x, y, direction)
            if new_state in state_history:
                return visited_positions, True
            state_history.add(new_state)
        else:
            # Move forward
            x, y = next_x, next_y
            visited_positions.add((x, y))
            new_state = (x, y, direction)
            if new_state in state_history:  # Loop detection
                return visited_positions, True
            state_history.add(new_state)

def find_loop_positions(grid: List[str]) -> int:
    """
    Determines how many positions in the grid, if turned into an obstacle, would cause the guard to loop.
    
    Strategy:
    - First, simulate the guard's original path to know which positions are visited.
    - Consider placing a new obstacle in positions adjacent to the guard's path (and not the starting spot).
    - For each candidate position, simulate again and check if it creates a loop.
    
    Returns:
    The count of such positions where a new obstacle creates a patrol loop.
    """
    width = len(grid[0])
    height = len(grid)
    
    # Guard's original patrol path
    original_visited, _ = simulate_guard(grid)

    # Find guard's start position
    start_pos = None
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char in '^>v<':
                start_pos = (x, y)
                break
        if start_pos:
            break

    loop_count = 0
    positions_to_check = set()

    # Consider positions around the guard's visited path
    # Only add positions that are within the grid, not obstacles, and not the start position.
    for x, y in original_visited:
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            test_x, test_y = x + dx, y + dy
            if (0 <= test_x < width and 0 <= test_y < height and
                grid[test_y][test_x] != '#' and
                (test_x, test_y) != start_pos):
                positions_to_check.add((test_x, test_y))

    # Test only those positions the guard actually could reach
    for test_pos in positions_to_check:
        if test_pos in original_visited:
            _, creates_loop = simulate_guard(grid, test_pos)
            if creates_loop:
                loop_count += 1

    return loop_count

def solve_puzzle(input_path: Path) -> Tuple[int, int]:
    """
    Processes the puzzle input to solve both parts:
    Part 1: Count how many distinct positions the guard visits before leaving the map.
    Part 2: Find how many positions would cause a loop if turned into a new obstacle.
    """
    grid = input_path.read_text().strip().splitlines()
    visited_positions, _ = simulate_guard(grid)
    part1 = len(visited_positions)
    part2 = find_loop_positions(grid)
    return part1, part2

def main() -> None:
    """
    Puzzle Narrative:
    You and The Historians have traveled back to 1518 to a North Pole lab where a single guard patrols.
    The guard moves according to a simple pattern:
    - If blocked by an obstacle directly ahead, turn right.
    - Otherwise, move straight forward.
    Using this logic, the guard navigates through a map filled with obstacles ('#').

    Part One:
    Determine how many unique positions in the lab the guard will step onto before leaving the mapped area.
    Each position visited, including the starting point, counts. By simulating the guard's path, 
    you can identify all these visited positions and count them.

    Part Two:
    The Historians want to safely search the lab without interference. 
    They consider placing a new obstacle somewhere that causes the guard to get stuck in a loop. 
    By testing potential obstacle placements adjacent to the guard's original path and re-simulating the route, 
    you can find out which positions would create such a loop. 
    Count how many such positions exist.

    In summary:
    - Part 1: Simulate the guard's patrol and count visited positions.
    - Part 2: Identify positions where adding a single obstacle causes a loop, 
      ensuring the guard never leaves.
    """

    PROJECT_DIR = Path(__file__).parent
    part1, part2 = solve_puzzle(PROJECT_DIR/'input.txt')
    print(f"Part 1: The guard visits {part1} distinct positions")
    print(f"Part 2: {part2} positions would create a patrol loop")

if __name__ == "__main__":
    main()
