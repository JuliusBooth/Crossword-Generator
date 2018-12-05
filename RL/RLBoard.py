import json
import numpy as np
import sys
sys.path.insert(0, '../MC')
from PuzzleBoard import PuzzleBoard
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "../Dictionaries/master_dictionary.json"
abs_file_path = os.path.join(script_dir, rel_path)


with open(abs_file_path, "r") as read_file:
    words = json.load(read_file)
    # Don't store words in PuzzleBoard or it's too slow using copy.deepcopy

class RLBoard(PuzzleBoard):
    # THIS CLASS IS A WORK IN PROGRESS
    # This board uses a one-hot-encoding for letters and is therefore more complicated
    # We should master everything on the string-based board before working on this


    def __init__(self, puzzle=None, file_name=None):
        PuzzleBoard.__init__(self, puzzle, file_name)
        self.matrix = self.get_matrix()


    def get_matrix(self):
        matrix = np.zeros((self.num_rows, self.num_cols, 27))
        for i, j in self.iterate_board():
            letter = self.get_letter(i, j)
            index = PuzzleBoard._letters.index(letter)
            matrix[i, j, index] = 1
        return matrix

    # TODO: I'd like an update_matrix function that efficiently updates the matrix based on change_list



if __name__ == "__main__":
    puzzle = RLBoard(file_name="../Valid_Boards/4x4_v1.txt")
    print(puzzle)
    print(puzzle.matrix)
