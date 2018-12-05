import json
import sys
sys.path.insert(0, 'RL/')
sys.path.insert(0, 'MC/')
from RLBoard import RLBoard
import numpy as np

with open("Dictionaries/master_dictionary.json", "r") as read_file:
    words = json.load(read_file)

def load_data():

    num_points = 120
    num_training_points = 100
    y_train = np.zeros([num_points, 4, 4, 26])
    x_train = np.zeros([num_points, 4, 4, 26])
    for p in range(num_points):
        puzzle = RLBoard(file_name="Valid_Boards/4x4/Board#" + str(p))
        for i, j in puzzle.iterate_board():
            original_letter = puzzle.board[i][j]
            for z, letter in enumerate(list(map(chr, range(65, 91)))):
                puzzle.board[i][j] = letter
                if puzzle.validate_board():
                    y_train[p, i, j, z] = 1
            puzzle.board[i][j] = original_letter

        x_train_i = puzzle.get_matrix()[:, :, :26]
        x_train[p, :, :, :] = x_train_i
    x_tr = x_train[:num_training_points, :, :, :]
    y_tr = y_train[:num_training_points, :, :, :]
    x_val = x_train[num_training_points:, :, :, :]
    y_val = y_train[num_training_points:, :, :, :]
    return(x_tr, y_tr, x_val, y_val)

