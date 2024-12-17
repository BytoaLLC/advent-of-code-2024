from pathlib import Path
from typing import List, Set, Tuple, Dict

# Directions for movement: Left, Right, Up, Down
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def read_garden_map(file_path: Path) -> List[str]:
    """
    Returns garden map input as a list of strings.
    """
    grid = []
    with file_path.open(encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                grid.append(line)
    return grid

def get_neighbors(position: Tuple[int, int], grid: List[str]) -> List[Tuple[Tuple[int, int], str]]:
    """
    Returns the valid neighboring positions and their corresponding plant type.
    """
    x, y = position
    neighbors = []
    width, height = len(grid[0]), len(grid)
    
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            neighbors.append(((nx, ny), grid[ny][nx]))
    return neighbors

def calculate_region_sides(region: Set[Tuple[int, int]]) -> int:
    """
    Calculates the number of distinct sides for a given region.
    """
    up_sides = down_sides = left_sides = right_sides = 0
    
    for (x, y) in region:
        left = (x - 1, y) not in region
        right = (x + 1, y) not in region
        above = (x, y - 1) not in region
        below = (x, y + 1) not in region

        # Check ownership of edges based on neighbors
        if above and (right or (x + 1, y - 1) in region):
            up_sides += 1
        if below and (right or (x + 1, y + 1) in region):
            down_sides += 1
        if left and (below or (x - 1, y + 1) in region):
            left_sides += 1
        if right and (below or (x + 1, y + 1) in region):
            right_sides += 1

    return up_sides + down_sides + left_sides + right_sides

def flood_fill_region(start_pos: Tuple[int, int], grid: List[str], visited: Set[Tuple[int, int]]) -> Tuple[int, int, int]:
    """
    Performs a flood-fill algorithm to find the area, perimeter, and sides of a region.
    """
    stack = [start_pos]
    region = set()
    area = perimeter = 0
    plant_type = grid[start_pos[1]][start_pos[0]]

    while stack:
        x, y = stack.pop()
        if (x, y) in region:
            continue

        region.add((x, y))
        area += 1
        local_sides = 4  # Each cell has 4 potential sides

        for neighbor_pos, neighbor_type in get_neighbors((x, y), grid):
            if neighbor_type == plant_type:
                stack.append(neighbor_pos)
                local_sides -= 1  # Neighbor reduces the perimeter
        perimeter += local_sides

    sides = calculate_region_sides(region)
    visited.update(region)
    return area, perimeter, sides

def calculate_fencing_cost(grid: List[str], use_sides: bool = False) -> int:
    """
    Calculates the total cost of fencing all regions on the grid.
    """
    visited = set()
    total_cost = 0
    width, height = len(grid[0]), len(grid)

    for y in range(height):
        for x in range(width):
            if (x, y) not in visited:
                area, perimeter, sides = flood_fill_region((x, y), grid, visited)
                cost = area * (sides if use_sides else perimeter)
                total_cost += cost
    return total_cost

def main():
    """
    Puzzle Narrative Context:
        Calculate fence costs for garden plots where:
        - Each plot grows a single type of plant (indicated by letter)
        - Connected plots of same type form a region
        
    Part One:
        Price = area * perimeter
        - area is number of plots in region
        - perimeter counts all edges not shared with same plant
        
    Part Two:
        Price = area * number of sides
        - sides counts distinct fence sections
        - continuous straight lines count as one side
        
    Solution:
        - Use flood-fill to identify regions and calculate their area, perimeter, and sides
    """
    input_file = Path(__file__).parent / "input.txt"
    garden_map = read_garden_map(input_file)

    # Part 1: Total cost using area * perimeter
    part1_cost = calculate_fencing_cost(garden_map, use_sides=False)
    print(f"Total price (Part 1): {part1_cost}")

    # Part 2: Total cost using area * sides
    part2_cost = calculate_fencing_cost(garden_map, use_sides=True)
    print(f"Total price (Part 2): {part2_cost}")

if __name__ == "__main__":
    main()
