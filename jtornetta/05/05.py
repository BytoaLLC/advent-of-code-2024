from pathlib import Path

def parse_input(input_text: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    """
    Parse the input text into rules and updates.
    
    The input consists of two sections separated by a blank line:
    - The first section defines ordering rules, one per line, in the form "X|Y".
      Each rule means: if both page X and page Y are in an update, then X must come before Y.
    - The second section defines the updates, one per line, as a comma-separated list of page numbers.
    
    Returns:
    - rules: A list of (before_page, after_page) tuples extracted from the rules section.
    - updates: A list of lists, where each sub-list contains page numbers for that update.
    """
    rules_text, updates_text = input_text.strip().split('\n\n')
    rules = [tuple(map(int, rule.split('|'))) for rule in rules_text.splitlines()]
    updates = [list(map(int, update.split(','))) for update in updates_text.splitlines()]
    return rules, updates

def is_valid_order(pages: list[int], rules: list[tuple[int, int]]) -> bool:
    """
    Checks if a given sequence of pages (one update) obeys all the relevant rules.
    Relevant rules are those for which both pages appear in the given update.
    
    Returns True if the update is valid under the given ordering rules, False otherwise.
    """
    page_set = set(pages)
    for before, after in rules:
        if before in page_set and after in page_set:
            # If the 'before' page does not appear before the 'after' page, order is invalid
            if pages.index(before) >= pages.index(after):
                return False
    return True

def build_dependency_graph(rules: list[tuple[int, int]], pages: set[int]) -> dict[int, list[int]]:
    """
    Builds a directed graph representing the dependencies between pages.
    For each rule 'X|Y' that applies to the current update's pages, create an edge X -> Y,
    indicating X must come before Y.
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
    Performs a topological sort on the pages according to the dependency graph.
    This gives a correct ordering of pages that respects all 'must come before' rules.
    
    If some pages have no dependencies, they'll appear at the end of the result in arbitrary order.
    """
    result = []
    visited = set()
    temp_visited = set()

    def visit(page: int):
        if page in temp_visited:
            return
        if page in visited:
            return
        
        temp_visited.add(page)
        for next_page in graph.get(page, []):
            visit(next_page)
        temp_visited.remove(page)
        visited.add(page)
        result.append(page)
    
    # Process all pages, ensuring that those with dependencies are handled first
    for page in pages:
        if page not in visited:
            visit(page)

    # The result list is built in reverse order, so reverse it to get correct order
    corrected_order = result[::-1]
    # Add any pages not in the graph (no dependencies)
    remaining = pages - set(corrected_order)
    return corrected_order + list(remaining)

def solve_both_parts(input_path: Path) -> tuple[int, int]:
    """
    Reads the input, determines which updates are already valid, and which need reordering.
    
    - For each valid update, find the "middle" page and accumulate its sum for Part 1.
    - For each invalid update, reorder the pages using topological sort and then find the "middle" page
      from this corrected sequence, accumulating its sum for Part 2.
      
    Returns (part1_sum, part2_sum).
    """
    # Parse the input into rules and updates
    input_text = input_path.read_text()
    rules, updates = parse_input(input_text)
    
    part1_middle_pages = []
    part2_middle_pages = []

    for update in updates:
        if is_valid_order(update, rules):
            # Already in correct order: take the middle page for Part 1
            middle_idx = len(update) // 2
            part1_middle_pages.append(update[middle_idx])
        else:
            # Not in correct order: fix it by topological sorting, then take the middle page for Part 2
            pages = set(update)
            graph = build_dependency_graph(rules, pages)
            correct_order = topological_sort(graph, pages)
            middle_idx = len(correct_order) // 2
            part2_middle_pages.append(correct_order[middle_idx])
    
    return sum(part1_middle_pages), sum(part2_middle_pages)

def main():
    """
    Puzzle Narrative:
    With the Chief Historian still missing, you find yourself in a busy North Pole printing department.
    Here, strict ordering rules govern how new pages for safety manuals must be printed. 
    Each rule "X|Y" says that if an update includes both pages X and Y, X must appear before Y in that update.

    You’re given:
    - A list of rules defining these page order constraints.
    - A series of updates, each one specifying which pages need printing.

    Task for Part One:
    - Identify which updates already follow all the relevant ordering rules as-is.
    - For each such correctly ordered update, determine its "middle" page and sum these middle pages together.

    Task for Part Two:
    - For the updates that don't follow the rules, reorder them correctly according to the rules using 
      a topological sort (a way to line up pages so all constraints are met).
    - Once corrected, take the middle page from each fixed update and add these up.
    
    You then print both sums:
    - The sum of middle pages from the already-valid updates (Part 1).
    - The sum of middle pages from the newly fixed updates (Part 2).
    """

    input_path = Path(__file__).parent / 'input.txt'
    part1_answer, part2_answer = solve_both_parts(input_path)
    
    print(f"Part 1 - Sum of middle pages from valid updates: {part1_answer}")
    print(f"Part 2 - Sum of middle pages from corrected invalid updates: {part2_answer}")

if __name__ == '__main__':
    main()
