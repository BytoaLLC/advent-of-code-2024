from pathlib import Path
from typing import Set, Tuple, List, Optional

def get_next_position(x: int, y: int, direction: str) -> Tuple[int, int]:
    """Returns coordinates of next position based on current direction."""
    moves = {
        '^': (0, -1),  # Up
        'v': (0, 1),   # Down
        '<': (-1, 0),  # Left
        '>': (1, 0)    # Right
    }
    dx, dy = moves[direction]
    return (x + dx, y + dy)

def turn_right(direction: str) -> str:
    """Handles 90-degree clockwise rotation of guard's direction."""
    return {'^': '>', '>': 'v', 'v': '<', '<': '^'}[direction]

def simulate_guard(grid: List[str], block_pos: Optional[Tuple[int, int]] = None) -> Tuple[Set[Tuple[int, int]], bool]:
    """
    Simulates guard's movement through the grid with path and loop detection.
    Uses set-based state tracking to identify loops and exits.
    
    Performance optimizations:
    - Uses sets for O(1) position lookups
    - Tracks complete state (position + direction) to detect loops
    - Avoids unnecessary path exploration
    
    Returns:
    - Set of all positions visited by guard
    - Boolean indicating if guard got stuck in loop (True) or exited map (False)
    """
    width = len(grid[0])
    height = len(grid)
    
    # Find guard's starting position and direction
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
    
    # Track visited positions and complete states for loop detection
    visited_positions = {(start_x, start_y)}
    state_history = {(start_x, start_y, start_dir)}
    
    x, y = start_x, start_y
    direction = start_dir
    
    while True:
        next_x, next_y = get_next_position(x, y, direction)
        
        # Exit if guard would leave map boundaries
        if not (0 <= next_x < width and 0 <= next_y < height):
            return visited_positions, False
        
        # Check both existing and optional new obstacles
        is_blocked = (
            grid[next_y][next_x] == '#' or
            (block_pos and (next_x, next_y) == block_pos)
        )
        
        if is_blocked:
            direction = turn_right(direction)
            new_state = (x, y, direction)
            if new_state in state_history:  # Loop detected
                return visited_positions, True
            state_history.add(new_state)
        else:
            x, y = next_x, next_y
            visited_positions.add((x, y))
            new_state = (x, y, direction)
            if new_state in state_history:  # Loop detected
                return visited_positions, True
            state_history.add(new_state)

def find_loop_positions(grid: List[str]) -> int:
    """
    Identifies positions where placing an obstacle creates a patrol loop.
    
    Key optimizations:
    - Only tests positions the guard actually visited in original path
    - Uses efficient state tracking to quickly identify loops
    - Avoids testing invalid positions (outside grid, existing obstacles)
    """
    width = len(grid[0])
    height = len(grid)
    
    # Get guard's original patrol path
    original_visited, _ = simulate_guard(grid)
    
    # Find guard's starting position (can't place obstacle here)
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
    
    # Build set of potential obstacle positions
    # Only consider positions adjacent to guard's path
    for x, y in original_visited:
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            test_x = x + dx
            test_y = y + dy
            if (0 <= test_x < width and 0 <= test_y < height and
                grid[test_y][test_x] != '#' and
                (test_x, test_y) != start_pos):
                positions_to_check.add((test_x, test_y))
    
    # Only test positions the guard can actually reach
    for test_pos in positions_to_check:
        if test_pos in original_visited:
            _, creates_loop = simulate_guard(grid, test_pos)
            if creates_loop:
                loop_count += 1
    
    return loop_count

def solve_puzzle(input_path: Path) -> Tuple[int, int]:
    """
    Solves both parts of the patrol puzzle.
    Part 1: Count positions in original patrol
    Part 2: Find positions that would create patrol loops
    """
    grid = input_path.read_text().strip().splitlines()
    visited_positions, _ = simulate_guard(grid)
    part1 = len(visited_positions)
    part2 = find_loop_positions(grid)
    return part1, part2

def main() -> None:
    PROJECT_DIR = Path(__file__).parent

    part1, part2 = solve_puzzle(PROJECT_DIR/'input.txt')
    print(f"Part 1: The guard visits {part1} distinct positions")
    print(f"Part 2: {part2} positions would create a patrol loop")

if __name__ == "__main__":
    main()