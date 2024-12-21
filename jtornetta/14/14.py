from pathlib import Path
from typing import List, Tuple

WIDTH = 101
HEIGHT = 103

class Robot:
    def __init__(self, p_x: int, p_y: int, v_x: int, v_y: int):
        """
        Initialize a robot with its starting position (p_x, p_y) and velocity (v_x, v_y).
        
        Args:
            p_x (int): The robot's initial x-coordinate.
            p_y (int): The robot's initial y-coordinate.
            v_x (int): The robot's x-velocity.
            v_y (int): The robot's y-velocity.
        """
        self.p_x = p_x
        self.p_y = p_y
        self.v_x = v_x
        self.v_y = v_y

    def move(self, grid: List[int]) -> None:
        """
        Move the robot one step based on its velocity, wrapping around the grid edges.
        Update the grid counter at the new position to track robot density.
        
        Args:
            grid (List[int]): The grid representing the area where robots move.
        """
        self.p_x = (self.p_x + self.v_x) % WIDTH
        self.p_y = (self.p_y + self.v_y) % HEIGHT
        grid[self.p_y * WIDTH + self.p_x] += 1
        
    def get_position_at(self, time: int) -> Tuple[int, int]:
        """
        Calculate the robot's position at a specific future time without actually moving it.
        Accounts for grid wrapping.
        
        Args:
            time (int): The number of seconds in the future to calculate the position for.
            
        Returns:
            Tuple[int, int]: The robot's position (x, y) at the specified future time.
        """
        x = (self.p_x + (self.v_x * time)) % WIDTH
        y = (self.p_y + (self.v_y * time)) % HEIGHT
        return (x, y)

def parse_input(filename: str) -> List[Robot]:
    """
    Parse the input file containing each robot's initial position (p) and velocity (v).
    Create and return a list of Robot objects based on the input data.
    
    Args:
        filename (str): The name of the input file containing robot data.
        
    Returns:
        List[Robot]: A list of Robot objects initialized with the parsed input data.
    """
    robots = []
    with open(filename, 'r') as file:
        data = file.read().split("\n")
    for row in data:
        p_str, v_str = row.split(" ")
        p_x, p_y = (int(val) for val in p_str[2:].split(","))
        v_x, v_y = (int(val) for val in v_str[2:].split(","))
        robots.append(Robot(p_x, p_y, v_x, v_y))
    return robots

def print_grid(grid: List[int], width: int, height: int, seconds: int) -> None:
    """
    Print a visual representation of the current robot positions on the grid.
    Each cell in the grid represents the density of robots at that position.
    
    Args:
        grid (List[int]): The grid representing the area where robots move.
        width (int): The width of the grid.
        height (int): The height of the grid.
        seconds (int): The current time in seconds.
    """
    rows = 0
    cols = 0
    print("Seconds", seconds)
    for _ in range(width * height):
        val = grid[width * rows + cols]
        if val == 0:
            val = " "
        print(val, end="")
        cols += 1
        if cols == width:
            print()
            cols = 0
            rows += 1
    print("\n")

def solve_part1(robots: List[Robot]) -> int:
    """
    Calculate the safety factor after 100 seconds based on the number of robots in each quadrant.
    Robots on the exact midlines are excluded from the count.
    
    Args:
        robots (List[Robot]): The list of Robot objects representing the robots in the area.
        
    Returns:
        int: The safety factor, which is the product of the robot counts in each quadrant.
    """
    # Get positions at 100 seconds
    positions = [robot.get_position_at(100) for robot in robots]
    
    # Count robots in each quadrant
    mid_x = WIDTH // 2
    mid_y = HEIGHT // 2
    quadrants = [0, 0, 0, 0]  # TL, TR, BL, BR
    
    for x, y in positions:
        if x == mid_x or y == mid_y:
            continue
        quad_idx = (int(x > mid_x) + (2 * int(y > mid_y)))
        quadrants[quad_idx] += 1
    
    # Calculate safety factor
    safety_factor = 1
    for count in quadrants:
        safety_factor *= count
    return safety_factor

def solve_part2(robots:List[Robot]) -> int:
    """
    Determines the fewest number of seconds that must elapse for the easter egg to appear.
    This was hard and I didn't know what I was looking for. The first solution I printed out everything
    and manually reviewed to find the easter egg. Once I knew what to look for, I realized I could look
    for non-overlapping robots. I think I got lucky with this solution overall.

    Args:
        robots (List[Robot]): The list of Robot objects representing the robots in the area.
        
    Returns:
        int: The least number of seconds to elapse for the tree to appear
    """
    seconds = 0
    print("\nSearching for tree pattern...")
    while True:
        grid = [0 for i in range(WIDTH * HEIGHT)]
        for robot in robots:
            robot.move(grid)
        seconds += 1
        if max(grid) > 1:
            if seconds % 1000 == 0:
                print(f"Checking second {seconds}...")
            continue
        print_grid(grid, WIDTH, HEIGHT, seconds)
        break
    return seconds

def main():
    """
    Solve the Easter Bunny HQ bathroom security puzzle.
    Part 1: Calculate the safety factor after 100 seconds.
    Part 2: Find the time when robots briefly display a Christmas tree pattern.
    """
    # Parse input
    robots = parse_input(Path(__file__).parent/'input.txt')

    # Part 1
    safety_factor = solve_part1(robots)
    print(f"Part 1: {safety_factor}")  # Should be 224357412

    # Part 2
    easter_egg = solve_part2(robots)
    print("Easter egg found after", easter_egg, "seconds")

if __name__ == "__main__":
    main()