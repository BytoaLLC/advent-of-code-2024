from pathlib import Path
from typing import Tuple, Optional, NamedTuple

class ButtonMovements(NamedTuple):
    """ Store x and y movements for a button press """
    x_movement: int
    y_movement: int

class PrizeLocation(NamedTuple):
    """ Store x and y coordinates of prize """
    x_coordinate: int
    y_coordinate: int

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Settled on algebra and the Euclidean Algorithm to find the numers we need.
    Tried brute forcing first, but that was a silly choice.
    
    1. Takes two numbers for button movements (e.g., 6 and 15)
    2. Keeps dividing the bigger by the smaller and keeping track of remainders:
       Example with 15 and 6:
       - 15 divided by 6 = 2 remainder 3
       - 6 divided by 3 = 2 remainder 0
       - When we get remainder 0, we've found our GCD (3)
    3. Works backwards through these divisions to find the solution
    
    The function uses recursion:
    1. First call:  extended_gcd(6, 15)
       - Gets remainder: 15 % 6 = 3
       - Calls: extended_gcd(3, 6)
    
    2. Second call: extended_gcd(3, 6)
       - Gets remainder: 6 % 3 = 0
       - Calls: extended_gcd(0, 3)
    
    3. Final call:  extended_gcd(0, 3)
       - When a=0, we've found the GCD (it's b=3)
       - Return (3, 0, 1) as starting point
       Then work backwards to find final numbers
    
    Args:
        a: First number (like how far button A moves)
        b: Second number (like how far button B moves)
    
    Returns:
        Tuple of (gcd, x, y) where:
        - gcd is the Greatest Common Divisor (tells us if solution is possible)
        - x, y are numbers that satisfy: ax + by = gcd
        Example: for 6 and 15, returns (3, -2, 1) because:
        6 * (-2) + 15 * 1 = 3
    """
    # Base case - we've divided down until remainder is 0
    if a == 0:
        return b, 0, 1
        
    # Get result from next division
    # Pass in: (remainder from b÷a, original a)
    gcd_value, coeff_x, coeff_y = extended_gcd(b % a, a)
    
    # Calculate and return our solution based on recursive call's results
    # These calculations work backwards through our divisions 
    # to find numbers that satisfy: ax + by = gcd
    return gcd_value, coeff_y - (b // a) * coeff_x, coeff_x


def parse_button_line(line: str) -> ButtonMovements:
    """
    Parse button movement line from input.
    Example input: "Button A: X+94, Y+34"
    Returns: ButtonMovements(x_movement=94, y_movement=34)
    """
    x_start = line.find('+') + 1
    x_end = line.find(',')
    y_start = line.rfind('+') + 1
    
    x_movement = int(line[x_start:x_end])
    y_movement = int(line[y_start:])
    
    return ButtonMovements(x_movement, y_movement)

def parse_prize_line(line: str) -> PrizeLocation:
    """
    Parse prize location line from input.
    Example input: "Prize: X=8400, Y=5400"
    Returns: PrizeLocation(x_coordinate=8400, y_coordinate=5400)
    """
    x_start = line.find('=') + 1
    x_end = line.find(',')
    y_start = line.rfind('=') + 1
    
    x_coordinate = int(line[x_start:x_end])
    y_coordinate = int(line[y_start:])
    
    return PrizeLocation(x_coordinate, y_coordinate)

def solve_machine(button_a: ButtonMovements, button_b: ButtonMovements, 
                 prize: PrizeLocation, max_presses: Optional[int] = None) -> Optional[int]:
    """Calculate minimum tokens needed to win prize on a machine."""
    # Find base solution
    gcd_result, base_a, base_b = extended_gcd(button_a.x_movement, button_b.x_movement)
    if prize.x_coordinate % gcd_result != 0:
        return None

    # Scale solution to match target x
    scaling = prize.x_coordinate // gcd_result
    base_a *= scaling
    base_b *= scaling
    
    # Calculate step sizes
    step_a = button_b.x_movement // gcd_result
    step_b = -button_a.x_movement // gcd_result
    
    # Check y-coordinate
    current_y = button_a.y_movement * base_a + button_b.y_movement * base_b
    if current_y != prize.y_coordinate:
        y_step = button_a.y_movement * step_a + button_b.y_movement * step_b
        if y_step == 0:
            return None
        steps_needed = (prize.y_coordinate - current_y) // y_step
        if (prize.y_coordinate - current_y) % y_step != 0:
            return None
        
        base_a += step_a * steps_needed
        base_b += step_b * steps_needed

    # Validate solution
    if base_a < 0 or base_b < 0:
        return None
    if max_presses and (base_a > max_presses or base_b > max_presses):
        return None

    return 3 * base_a + base_b

def main():
    """
    Calculate minimum tokens needed for both scenarios:
    
    Part 1: Original coordinates, max 100 button presses
    Part 2: Offset coordinates, unlimited presses
    """
    total_tokens_part1 = 0
    total_tokens_part2 = 0
    coordinate_offset = 10_000_000_000_000
    
    with open(Path(__file__).parent/'input.txt') as f:
        # Read all lines and split into non-empty groups
        lines = f.read().strip().split('\n')
        
        # Process lines in groups of 4 (3 data lines + 1 blank)
        for i in range(0, len(lines), 4):
            # Parse machine configuration
            button_a = parse_button_line(lines[i])
            button_b = parse_button_line(lines[i + 1])
            prize = parse_prize_line(lines[i + 2])
            
            # Solve Part 1 (max 100 presses)
            solution_part1 = solve_machine(button_a, button_b, prize, 100)
            if solution_part1 is not None:
                total_tokens_part1 += solution_part1
            
            # Solve Part 2 (add offset, no press limit)
            prize_with_offset = PrizeLocation(
                prize.x_coordinate + coordinate_offset,
                prize.y_coordinate + coordinate_offset
            )
            solution_part2 = solve_machine(button_a, button_b, prize_with_offset)
            if solution_part2 is not None:
                total_tokens_part2 += solution_part2
    
    print(f"Part 1: {total_tokens_part1}")
    print(f"Part 2: {total_tokens_part2}")

if __name__ == "__main__":
    main()