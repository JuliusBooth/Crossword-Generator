from PuzzleBoard import PuzzleBoard


def write2file(board, file_name):
    puzzle = PuzzleBoard(puzzle=board, override_fail=True)
    puzzle.write_to_txt(file_name)


board = [['E', 'D', 'D', 'O', 'S', '-', 'C', 'A', 'B', 'E', 'D', '-', 'A', 'N', 'C'], ['S', 'O', 'O', 'P', 'A', '-', 'R', 'E', 'E', 'D', 'Y', '-', 'L', 'Y', 'S'], ['S', 'U', 'P', 'E', 'R', 'S', 'U', 'N', 'D', 'A', 'Y', '-', 'P', 'A', 'T'], ['O', 'M', 'E', 'N', '-', 'A', 'S', 'I', 'T', '-', 'D', 'R', 'E', 'S', 'S'], ['-', '-', '-', 'M', 'A', 'L', 'T', '-', 'I', 'D', 'E', 'A', 'N', '-', '-'], ['-', 'F', 'R', 'I', 'D', 'A', 'Y', 'I', 'M', 'I', 'N', 'L', 'O', 'V', 'E'], ['P', 'L', 'A', 'C', 'A', '-', '-', 'N', 'E', 'E', '-', 'E', 'M', 'E', 'R'], ['E', 'O', 'N', '-', 'W', 'H', 'A', 'S', 'S', 'U', 'P', '-', 'E', 'S', 'N'], ['R', 'O', 'S', 'I', '-', 'O', 'T', 'A', '-', '-', 'R', 'A', 'G', 'E', 'S'], ['C', 'R', 'A', 'S', 'H', 'W', 'E', 'D', 'N', 'E', 'S', 'D', 'A', 'Y', '-'], ['-', '-', 'C', 'H', 'O', 'E', 'L', '-', 'A', 'T', 'E', 'D', '-', '-', '-'], ['M', 'O', 'K', 'E', 'S', '-', 'U', 'P', 'S', 'Y', '-', 'O', 'A', 'C', 'T'], ['U', 'R', 'E', '-', 'M', 'A', 'N', 'I', 'C', 'M', 'O', 'N', 'D', 'A', 'Y'], ['S', 'A', 'R', '-', 'E', 'S', 'C', 'A', 'S', '-', 'S', 'T', 'R', 'A', 'P'], ['T', 'E', 'S', '-', 'R', 'E', 'S', 'O', 'R', '-', 'T', 'O', 'A', 'N', 'Y']]
file_name = "Valid_Boards/failed_boards/15x15_1.txt"
write2file(board, file_name)