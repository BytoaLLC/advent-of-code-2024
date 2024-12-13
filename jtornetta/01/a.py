from pathlib import Path

def part_one(values_first_column, values_second_column):
    """
    Computes the sum of the absolute differences between corresponding elements 
    of two sorted lists. Both lists are assumed to have the same length.

    Parameters:
    - values_first_column: List[int]
    - values_second_column: List[int]

    Returns:
    - int: The sum of the absolute differences between corresponding elements.
    """
    # Calculate the absolute difference for each pair of corresponding elements
    # and sum them up. Using zip allows us to iterate over both lists in parallel.
    differences = [abs(b - a) for a, b in zip(values_first_column, values_second_column)]
    return sum(differences)


def part_two(values_first_column, values_second_column):
    """
    For each value in the first list, this function computes how many times 
    that value appears in the second list and multiplies this count by the value itself.
    Finally, it sums these results for all elements in the first list.

    Parameters:
    - values_first_column: List[int]
    - values_second_column: List[int]

    Returns:
    - int: The sum of each element multiplied by its frequency of occurrence in the second list.
    """
    # For each element in the first list, count how many times it appears in the second list.
    # Multiply the element by its occurrence count and add these values together.
    total_weighted_occurrences = 0
    for value in values_first_column:
        occurrence_count = values_second_column.count(value)
        total_weighted_occurrences += occurrence_count * value

    return total_weighted_occurrences


def main():
    """
    The input file is expected to have two columns of integers per line, 
    separated by whitespace. For example:
    
        1 3
        2 5
        4 4

    Each line is read, and the first integer goes into 'values_first_column' 
    and the second integer goes into 'values_second_column'.

    After reading, both lists are sorted and then processed by 'part_one' and 'part_two'.
    """
    project_directory = Path(__file__).parent
    values_first_column = []
    values_second_column = []

    # Read data from input file
    with open(project_directory / 'input.txt', 'r') as file:
        for line in file:
            # Split line into two integers and append to respective lists
            first_val_str, second_val_str = line.split()
            values_first_column.append(int(first_val_str))
            values_second_column.append(int(second_val_str))

    # Sort the input lists
    values_first_column.sort()
    values_second_column.sort()

    # Compute results
    result_part_one = part_one(values_first_column, values_second_column)
    result_part_two = part_two(values_first_column, values_second_column)

    # Print results
    print(result_part_one)
    print(result_part_two)


if __name__ == "__main__":
    main()
