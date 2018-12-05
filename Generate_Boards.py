import sys

from PuzzleBoard import PuzzleBoard
from MC_search import monte_carlo_search

def generate_valid_boards(height=4, width=4):
    puzzle = PuzzleBoard(file_name="Valid_Boards/4x4_v1.txt")
    for i in range(1000,1001):
        print(puzzle)
        puzzle=monte_carlo_search(puzzle, depth=4, breadth=500, iterations=400)
        if puzzle.validate_board():
            file_name = "Valid_Boards/4x4/Board#" + str(i)
            puzzle.write_to_txt(file_name)
        else:
            raise

generate_valid_boards()