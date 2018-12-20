import sys

from PuzzleBoard import PuzzleBoard
from MC_search import monte_carlo_search

def generate_valid_boards():
    puzzle = PuzzleBoard(file_name="Valid_Boards/5x5/Board#30")
    for i in range(33,1001):
        print(puzzle)
        puzzle=monte_carlo_search(puzzle, depth=3, breadth=10, iterations=300000)
        if puzzle.validate_board():
            file_name = "Valid_Boards/5x5/Board#" + str(i)
            puzzle.write_to_txt(file_name)
        else:
            raise

generate_valid_boards()