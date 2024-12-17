from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

def load_stones(filename: str) -> List[int]:
    """
    Load initial stone values from input file.
    
    Args:
        filename (str): Name of input file in same directory
        
    Returns:
        List[int]: Initial stone values
    """
    return list(map(int, open(filename).readline().strip().split()))

def solve(stone: int, blinks: int, memory: Dict[Tuple[int, int], int], 
        depth: int = 0) -> int:
    """
    Recursively calculate resulting stones using memoization.
    
    Args:
        stone (int): Current stone value
        blinks (int): Number of blinks remaining
        memory: Cache of previously calculated results
        
    Returns:
        int: Number of stones that will result from this stone
        
    Note:
        Uses memoization with (stone, blinks) as cache key.
        Each subproblem is only calculated once, then cached.
    """
    # Base case: no more transformations
    if blinks == 0:
        return 1
        
    # Check memoization cache
    if (stone, blinks) in memory:
        return memory[(stone, blinks)]
    
    # Apply transformation rules
    if stone == 0:
        val = solve(1, blinks - 1, memory, depth + 1)
    elif len(str_stone := str(stone)) % 2 == 0:
        mid = len(str_stone) // 2
        left = solve(int(str_stone[:mid]), blinks - 1, memory, depth + 1)
        right = solve(int(str_stone[mid:]), blinks - 1, memory, depth + 1)
        val = left + right
    else:
        val = solve(stone * 2024, blinks - 1, memory, depth + 1)
        
    # Cache and return
    memory[(stone, blinks)] = val
    return val

def simulate_stones(stones: List[int], blinks: int) -> int:
    """
    Simulate stone transformations for all initial stones.
    
    Args:
        stones (List[int]): Initial stone values
        blinks (int): Number of blinks to simulate
        
    Returns:
        int: Total number of stones after all transformations
    """
    memory = {}
    
    result = sum(solve(stone, blinks, memory) for stone in stones)
        
    return result

def main():
    """
    Puzzle Narrative Context:
        On Pluto, physics-defying stones transform according to these rules:
        1. If stone is 0, it becomes 1
        2. If stone has even digits, splits into two stones (left/right halves)
        3. Otherwise, multiply by 2024
        
    Solution:
        Uses memoization to cache results for each unique (stone, blinks) combination.  
        Memoization is a technique where we store the results of expensive function calls and return the cached result 
        when the same inputs occur again. Without memoization, we'd have to track every stone and do every transformation, 
        leading to an exponential number of operations. With memoization, we only solve each unique subproblem once.
    """
    stones = load_stones(Path(__file__).parent/"input.txt")
    
    print("Part 1:", simulate_stones(stones, 25))
    print("Part 2:", simulate_stones(stones, 75))

if __name__ == '__main__':
    main()