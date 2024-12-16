from pathlib import Path
from collections import deque
from dataclasses import dataclass
from typing import List, Set, Tuple, Dict

@dataclass
class Point:
    """
    Represents a position on the topographic map.
    
    Attributes:
        row (int): The vertical position in the grid.
        col (int): The horizontal position in the grid.
    """
    row: int
    col: int
    
    def __hash__(self):
        return hash((self.row, self.col))
        
    def neighbors(self, height: int, width: int) -> List['Point']:
        """
        Returns valid neighboring points within grid bounds.
        
        Args:
            height (int): The total number of rows in the grid.
            width (int): The total number of columns in the grid.
            
        Returns:
            List[Point]: List of valid adjacent points (up, down, left, right).
            
        Notes:
            Hiking trails only allow orthogonal movement (no diagonals).
        """
        deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        points = []
        for dr, dc in deltas:
            new_row, new_col = self.row + dr, self.col + dc
            if 0 <= new_row < height and 0 <= new_col < width:
                points.append(Point(new_row, new_col))
        return points

def load_grid() -> List[List[int]]:
    """
    Loads and parses the topographic map
    
    Returns:
        List[List[int]]: 2D grid where each cell contains a height value (0-9).
        
    Notes:
        Each character in the input represents a height from 0 (lowest) to 9 (highest).
    """
    input_file = Path(__file__).parent / 'input.txt'
    with open(input_file) as f:
        return [[int(char) for char in line.strip()] for line in f]

def find_trailheads(grid: List[List[int]]) -> List[Point]:
    """
    Identifies all potential trailhead positions on the map.
    
    Args:
        grid (List[List[int]]): The 2D topographic map grid.
        
    Returns:
        List[Point]: List of all positions with height 0 (potential trailheads).
        
    Notes:
        A trailhead is any position with height 0 that can start hiking trails.
    """
    height, width = len(grid), len(grid[0])
    return [
        Point(row, col)
        for row in range(height)
        for col in range(width)
        if grid[row][col] == 0
    ]

def count_reachable_peaks(grid: List[List[int]], start: Point) -> int:
    """
    Counts height-9 positions reachable via valid hiking trails from a trailhead.
    
    Args:
        grid (List[List[int]]): The 2D topographic map grid.
        start (Point): Starting trailhead position.
        
    Returns:
        int: Number of unique height-9 positions reachable from this trailhead.
        
    Notes:
        A valid hiking trail must:
        - Start at height 0
        - Increase by exactly 1 at each step
        - Only move orthogonally (up, down, left, right)
        - Reach a position of height 9
    """
    height, width = len(grid), len(grid[0])
    visited = set()
    peaks = set()
    
    def dfs(point: Point, current_height: int) -> None:
        """
        Recursive DFS helper that explores valid hiking trails.
        
        Args:
            point (Point): Current position being explored.
            current_height (int): Expected height at this position.
            
        Notes:
            Updates the global visited and peaks sets.
            Backtracks if current position doesn't match expected height.
        """
        if point in visited:
            return
            
        visited.add(point)
        grid_height = grid[point.row][point.col]
        
        if grid_height != current_height:
            return
            
        if grid_height == 9:
            peaks.add(point)
            
        for neighbor in point.neighbors(height, width):
            if grid[neighbor.row][neighbor.col] == current_height + 1:
                dfs(neighbor, current_height + 1)
    
    dfs(start, 0)
    return len(peaks)

def count_distinct_paths(grid: List[List[int]], start: Point) -> int:
    """
    Counts distinct possible hiking trails from a trailhead to any height-9 position.
    
    Args:
        grid (List[List[int]]): The 2D topographic map grid.
        start (Point): Starting trailhead position.
        
    Returns:
        int: Total number of unique valid paths from this trailhead to any height-9 position.
        
    Notes:
        A distinct path:
        - Must follow valid hiking trail rules (increment by 1, orthogonal moves only)
        - Is counted separately even if it reaches the same peak as another path
        - Is defined by its unique sequence of moves
        
        Uses BFS with path counting to track all possible routes efficiently.
    """
    height, width = len(grid), len(grid[0])
    paths_to = {start: 1}  # Maps points to number of distinct paths reaching them
    queue = deque([(start, 0)])  # Tracks points to explore and their current height
    
    while queue:
        point, current_height = queue.popleft()
        paths_here = paths_to[point]
        
        for neighbor in point.neighbors(height, width):
            neighbor_height = grid[neighbor.row][neighbor.col]
            
            if neighbor_height != current_height + 1:
                continue
                
            if neighbor not in paths_to:
                queue.append((neighbor, neighbor_height))
                paths_to[neighbor] = 0
            paths_to[neighbor] += paths_here
    
    return sum(
        paths_to[Point(row, col)]
        for row in range(height)
        for col in range(width)
        if grid[row][col] == 9 and Point(row, col) in paths_to
    )

def main():
    """
    Puzzle Narrative Context:
        A reindeer at a Lava Production Facility needs help mapping hiking trails 
        on a topographic map. The map shows heights from 0 (lowest) to 9 (highest),
        and we need to analyze possible hiking trails.
    
    Part One:
        For each trailhead (height 0), count how many height-9 positions can be reached 
        via valid hiking trails. A valid trail always increases by exactly 1 in height 
        at each step and only moves up, down, left, or right. The sum of these counts 
        gives us the total score for all trailheads.
    
    Part Two:
        Instead of counting reachable peaks, count distinct possible paths from each 
        trailhead. Each unique sequence of moves that reaches a height-9 position 
        counts as a separate path. The sum of these path counts gives us the total 
        rating for all trailheads.
    
    Process:
        1. Loads the topographic map from input.txt
        2. Identifies all trailhead positions (height 0)
        3. For each trailhead:
            - Part 1: Counts reachable height-9 positions (score)
            - Part 2: Counts distinct possible paths to any height-9 position (rating)
        4. Outputs the sum of all trailhead scores and ratings
    """
    grid = load_grid()
    trailheads = find_trailheads(grid)
    
    # Part 1: Sum of scores (reachable peaks per trailhead)
    total_score = sum(count_reachable_peaks(grid, start) for start in trailheads)
    print(f"Part 1: {total_score}")
    
    # Part 2: Sum of ratings (distinct paths per trailhead)
    total_rating = sum(count_distinct_paths(grid, start) for start in trailheads)
    print(f"Part 2: {total_rating}")

if __name__ == '__main__':
    main()