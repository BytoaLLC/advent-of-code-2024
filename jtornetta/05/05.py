from pathlib import Path

def parse_input(input_text: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    """
    Parse the input text into rules and updates.
    Example rule: '61|32' means page 61 must come before page 32
    Example update: '62,33,12,19,48,99,14,98,29,82,72,37,51'
    
    Returns tuple of (rules, updates) where:
    - rules is list of (before, after) page number tuples
    - updates is list of lists containing page numbers to be printed
    """
    rules_text, updates_text = input_text.strip().split('\n\n')
    
    # Parse rules into list of tuples (before_page, after_page)
    rules = [tuple(map(int, rule.split('|'))) for rule in rules_text.splitlines()]
    
    # Parse updates into list of lists of page numbers
    updates = [list(map(int, update.split(','))) for update in updates_text.splitlines()]
    
    return rules, updates

def is_valid_order(pages: list[int], rules: list[tuple[int, int]]) -> bool:
    """
    Check if a sequence of pages satisfies all applicable rules.
    Example: if pages=[62,33,12] and we have a rule (62|33), this checks that
    62 appears before 33 in the list.
    
    A rule only matters if both pages exist in the update list.
    """
    page_set = set(pages)
    
    # For each rule, check if both pages are present and in correct order
    for before, after in rules:
        if before in page_set and after in page_set:
            if pages.index(before) >= pages.index(after):
                return False
    return True

def build_dependency_graph(rules: list[tuple[int, int]], pages: set[int]) -> dict[int, list[int]]:
    """
    Create a directed graph showing which pages must come before others.
    For example, with rule '61|32', the graph would show that 61 points to 32,
    meaning 61 must be printed before 32.
    """
    graph = {}
    for before, after in rules:
        if before in pages and after in pages:
            if before not in graph:
                graph[before] = []
            graph[before].append(after)
    return graph

def topological_sort(graph: dict[int, list[int]], pages: set[int]) -> list[int]:
    """
    Determine correct page order using topological sort.
    For example, if rules require:
        61 before 32
        32 before 12
    The sort would give us [61, 32, 12]
    
    This ensures all "must come before" relationships are satisfied.
    """
    result = []
    visited = set()
    temp_visited = set()  # For cycle detection
    
    def visit(page: int):
        if page in temp_visited:
            return  # Skip if in temporary set (handles cycles)
        if page in visited:
            return  # Skip if already processed
        
        temp_visited.add(page)
        
        # Process all pages that need to come after this one
        for next_page in graph.get(page, []):
            visit(next_page)
            
        temp_visited.remove(page)
        visited.add(page)
        result.append(page)
    
    # Start with pages that have dependencies (appear in graph)
    for page in pages:
        if page not in visited:
            visit(page)
            
    # Reverse to get correct order (since we built it backwards)
    corrected_order = result[::-1]
    
    # Add any remaining pages that had no dependencies
    remaining = pages - set(corrected_order)
    return corrected_order + list(remaining)

def solve_both_parts(input_path: Path) -> tuple[int, int]:
    """
    Process input and solve both parts:
    Part 1: Find sum of middle pages from valid updates
    Part 2: Find sum of middle pages from corrected invalid updates
    """
    # Read and parse input
    input_text = input_path.read_text()
    rules, updates = parse_input(input_text)
    
    part1_middle_pages = []  # Middle pages from already-valid updates
    part2_middle_pages = []  # Middle pages from fixed invalid updates
    
    # Process each update
    for update in updates:
        if is_valid_order(update, rules):
            # Part 1: Store middle page of valid updates
            middle_idx = len(update) // 2
            part1_middle_pages.append(update[middle_idx])
        else:
            # Part 2: Fix invalid updates and find their middle pages
            pages = set(update)
            graph = build_dependency_graph(rules, pages)
            correct_order = topological_sort(graph, pages)
            
            middle_idx = len(correct_order) // 2
            part2_middle_pages.append(correct_order[middle_idx])
    
    return sum(part1_middle_pages), sum(part2_middle_pages)

def main():
    input_path = Path(__file__).parent / 'input.txt'
    part1_answer, part2_answer = solve_both_parts(input_path)
    
    print(f"Part 1 - Sum of middle pages from valid updates: {part1_answer}")
    print(f"Part 2 - Sum of middle pages from corrected invalid updates: {part2_answer}")

if __name__ == '__main__':
    main()