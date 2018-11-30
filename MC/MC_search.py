from PuzzleBoard import PuzzleBoard
import copy
import random


def monte_carlo_search(root_puzzle, depth=1, breadth=1000, iterations=1000, choice_method="random"):
    # At each iteration we copy the root_puzzle breadth times
    # We then make depth changes to each puzzle and throw out the invalid puzzles
    # One of the altered puzzles becomes the new root_puzzle
    root_puzzle_value = root_puzzle.get_board_value()
    for iteration in range(iterations):
        puzzles = []

        for branch in range(breadth):
            # this creates a deepcopy of the object
            # (ie. changes to its properties do not affect the original)
            cloned_puzzle = copy.deepcopy(root_puzzle)

            for step in range(depth):
                cloned_puzzle.mutate_one_square()
            if cloned_puzzle.is_puzzle_solved():
                puzzles.append(cloned_puzzle)

        if len(puzzles) == 0:
            continue
        else:
            if choice_method == "random":
                root_puzzle = random.choice(puzzles)

            else:
                for cloned_puzzle in puzzles:
                    value = cloned_puzzle.get_board_value()

                    if value >= root_puzzle_value:
                        root_puzzle = cloned_puzzle
                        root_puzzle_value = value

            print(root_puzzle)
            print(root_puzzle_value)
    return root_puzzle

if __name__ == "__main__":
    board = [['-', 'G', 'R', 'O', 'S'], ['B', 'R', 'E', 'D', 'E'], ['R', 'E', 'M', 'O', 'P'],
             ['A', 'C', 'O', 'R', 'N'], ['T', 'O', 'P', 'S', '-']]
    #board = [['-', 'G', 'L', 'A', 'R'], ['B', 'R', 'E', 'D', 'E'], ['R', 'E', 'M', 'O', 'P'],
            # ['A', 'B', 'O', 'R', 'T'], ['D', 'O', 'N', 'N', '-']]

    puzzle = PuzzleBoard(board)
    print(puzzle)
    puzzle = monte_carlo_search(puzzle, depth=1)
    print(puzzle)