from pathlib import Path

def read_input(file_path):
    """
    Reads the input map from the given file path and returns it as a 2D grid.
    """
    input_path = Path(file_path)
    with input_path.open() as file:
        return [list(line.strip()) for line in file.readlines()]

def find_guard_initial_state(grid):
    """
    Finds the guard's initial position and direction.
    Directions:
    '^' -> 0 (Up), '>' -> 1 (Right), 'v' -> 2 (Down), '<' -> 3 (Left)
    Returns: (row, col, direction)
    """
    direction_map = {'^': 0, '>': 1, 'v': 2, '<': 3}
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell in direction_map:
                return r, c, direction_map[cell]
    raise ValueError("Guard's starting position not found.")

def simulate_guard_path_fast(grid):
    """
    Simulates the guard's path through the map and calculates the number of unique
    positions visited. Optimized for speed and terminates on loop detection.
    """
    movement_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
    current_row, current_col, current_direction = find_guard_initial_state(grid)
    visited_positions = set()
    seen_states = set()  # Track state (row, col, direction)
    rows, cols = len(grid), len(grid[0])

    while True:
        # If the guard exits the grid, terminate
        if not (0 <= current_row < rows and 0 <= current_col < cols):
            break

        # Mark the current position as visited
        visited_positions.add((current_row, current_col))

        # Detect loops
        state = (current_row, current_col, current_direction)
        if state in seen_states:
            break
        seen_states.add(state)

        # Calculate next position
        delta_row, delta_col = movement_directions[current_direction]
        next_row, next_col = current_row + delta_row, current_col + delta_col

        # If next move is valid, proceed; otherwise, turn right
        if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row][next_col] != '#':
            current_row, current_col = next_row, next_col
        else:
            current_direction = (current_direction + 1) % 4

    return len(visited_positions)

def main():
    """
    Main function to read input, simulate the guard's path, and print the result.
    """
    input_file_path = Path(__file__).parent/"input.txt"  # Replace with your input file path if needed
    grid = read_input(input_file_path)
    result = simulate_guard_path_fast(grid)
    print(f"Number of distinct positions visited: {result}")

if __name__ == "__main__":
    main()
