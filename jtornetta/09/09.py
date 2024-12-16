import sys
from collections import deque
from pathlib import Path

def read_input(file_path):
    """
    Reads the input from the file and returns the disk map as a string.
    """
    with open(file_path, 'r') as file:
        return file.read().strip()

def parse_disk_map(disk_map, part2):
    """
    Parses the disk map into file blocks and free space.

    Args:
        disk_map (str): The compact representation of the disk.
        part2 (bool): If True, allows files to be moved into free space.

    Returns:
        tuple: A deque of file blocks and free spaces, and the final layout.
    """
    files = deque()
    free_spaces = deque()
    final_layout = []
    file_id = 0
    position = 0

    # Parse the disk map
    for index, char in enumerate(disk_map):
        length = int(char)

        if index % 2 == 0:  # File blocks
            if part2:
                files.append((position, length, file_id))
            for _ in range(length):
                final_layout.append(file_id)
                if not part2:
                    files.append((position, 1, file_id))
                position += 1
            file_id += 1
        else:  # Free spaces
            free_spaces.append((position, length))
            for _ in range(length):
                final_layout.append(None)
                position += 1

    return files, free_spaces, final_layout

def compact_files(files, free_spaces, final_layout):
    """
    Simulates moving file blocks to the leftmost available free spaces.

    Args:
        files (deque): A deque of file block tuples (position, size, file_id).
        free_spaces (deque): A deque of free space tuples (position, size).
        final_layout (list): The current layout of the disk.

    Returns:
        list: The updated layout after compacting the files.
    """
    for pos, size, file_id in reversed(files):
        for space_index, (space_pos, space_size) in enumerate(free_spaces):
            if space_pos < pos and size <= space_size:
                # Move the file blocks to the free space
                for i in range(size):
                    assert final_layout[pos + i] == file_id, f"Unexpected block at {pos + i}"
                    final_layout[pos + i] = None
                    final_layout[space_pos + i] = file_id
                # Update the free space
                free_spaces[space_index] = (space_pos + size, space_size - size)
                break

    return final_layout

def calculate_checksum(final_layout):
    """
    Calculates the filesystem checksum based on the compacted layout.

    Args:
        final_layout (list): The compacted layout of the disk.

    Returns:
        int: The calculated checksum.
    """
    checksum = 0
    for position, block in enumerate(final_layout):
        if block is not None:
            checksum += position * block
    return checksum

def solve(disk_map, part2):
    """
    Solves the problem for a given part (compact or not).

    Args:
        disk_map (str): The compact representation of the disk.
        part2 (bool): If True, files can be moved into free space.

    Returns:
        int: The checksum of the compacted layout.
    """
    files, free_spaces, final_layout = parse_disk_map(disk_map, part2)
    final_layout = compact_files(files, free_spaces, final_layout)
    return calculate_checksum(final_layout)

def main():
    """
    Puzzle Narrative Context:
    We are helping an amphipod compact its hard drive to make contiguous free space.
    The disk map is represented as a string of alternating numbers, where:
    - Even-indexed numbers represent file sizes.
    - Odd-indexed numbers represent free space sizes.

    Part One Scenario:
    Each file block is compacted into the first available free space strictly to the left.
    The checksum is calculated as the sum of the product of each block's position 
    and its file ID.

    Part Two Scenario:
    Files are compacted in larger chunks, potentially freeing more space earlier in the process.
    The checksum calculation remains the same.

    This program:
    - Reads the disk map from an input file.
    - Parses it into file blocks and free spaces.
    - Compacts the files according to the rules of each part.
    - Calculates the checksum of the final disk layout for both parts.
    """

    #might not need, but increases the recursion depth limit in Python for 
    #large recursive operations
    sys.setrecursionlimit(10**6)
    input_file_path = Path(__file__).parent / "input.txt"
    disk_map = read_input(input_file_path)

    # Solve for part 1 and part 2
    part1_result = solve(disk_map, part2=False)
    part2_result = solve(disk_map, part2=True)

    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
