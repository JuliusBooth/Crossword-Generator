import sys
sys.path.insert(0, 'MC/')
from PuzzleBoard import PuzzleBoard
from MC_search import monte_carlo_search

def generate_valid_boards(height=4, width=4):
    puzzle = PuzzleBoard(file_name="Valid_Boards/4x4_v1.txt")
    for i in range(171,1000):
        print(puzzle)
        puzzle=monte_carlo_search(puzzle, depth=4, breadth=400, iterations=200)
        if puzzle.validate_board():
            file_name = "Valid_Boards/4x4/Board#" + str(i)
            puzzle.write_to_txt(file_name)
        else:
            raise

generate_valid_boards()