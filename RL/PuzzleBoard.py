import json
import numpy as np
import random

with open("words_dictionary.json", "r") as read_file:
    words = json.load(read_file)

class PuzzleBoard:
    # THIS CLASS IS A WORK IN PROGRESS
    # This board uses a one-hot-encoding for letters and is therefore more complicated
    # We should master everything on the string-based board before working on this

    _letters = list(map(chr, range(65, 91))) + ["E"] #Change to / after testing solving done

    def __init__(self, height, width=None):
        if width is None:
            width = height
        self.width = width
        self.height = height
        self.board = np.zeros((height, width, 27))

        for i in range(height):
            for j in range(width):
                square_value = random.randint(0, 26)
                self.board[i, j, square_value] = 1

    def __str__(self):
        board_string = ""
        for i in range(self.height):
            for j in range(self.width):
                #square_value = self.board[row, column, :].argmax()
                #board_string += PuzzleBoard._letters[square_value]
                board_string += self.get_letter(i, j)
                board_string += " "
            board_string += "\n"
        return (board_string)

    def mutate_one_square(self):
        #Maybe can be made faster if we don't delete whole col and replace
        while True:
            square_row = random.randint(0, self.height-1)
            square_column = random.randint(0, self.width-1)
            if self.board[square_row, square_column, 26] == 1:
                continue
            square_value = random.randint(0, 25)
            self.board[square_row, square_column, :] = np.zeros(27)
            self.board[square_row, square_column, square_value] = 1
            break

    def get_letter(self, row, column):
        square_value = self.board[row, column, :].argmax()
        letter = PuzzleBoard._letters[square_value]
        return(letter)

    def is_puzzle_solved(self):
        #Will need to take into account blank squares
        putative_words = set()
        for i in range(self.height):
            word = ""
            for j in range(self.width):
                word += self.get_letter(i, j).lower()
            putative_words.add(word)
        for j in range(self.width):
            word = ""
            for i in range(self.height):
                word += self.get_letter(i, j).lower()
            putative_words.add(word)
        if putative_words.issubset(words):
            return (True)
        else:
            return (False)

    def solve_puzzle_randomly(self):
        #Took a long time for even a 3x3 puzzle
        for i in range(10000):
            if self.is_puzzle_solved():
                return (self, i)
            else:
                self.mutate_one_square()
        return (self, -1)
