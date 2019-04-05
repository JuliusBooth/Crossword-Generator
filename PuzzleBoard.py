import json
import csv
import random
from math import exp, log

#DICTIONARY = 'Dictionaries/words_dictionary.json'
DICTIONARY = "Dictionaries/master_dictionary.json"
with open(DICTIONARY, "r") as read_file:
    words = json.load(read_file)
    words = dict([(k.upper(),v) for (k,v) in words.items()])
    # Don't store words in PuzzleBoard or it's too slow using copy.deepcopy

    with open("Dictionaries/dbcluesunique.txt") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            word = line[0].upper()
            appearance_count = int(line[1])
            if len(word) <= 5 and appearance_count <= 5:
                words.pop(word, None)
    #x_l_words = [k for (k, v) in words.items() if len(k) == x]


class PuzzleBoard:

    _BLANK = "-"
    _letters = list(map(chr, range(65, 91))) + [_BLANK]
    _num_letters = len(_letters)-1

    _letter_values = {'A': 1, 'C': 3, 'B': 3, 'E': 1, 'D': 2, 'G': 2, 'F': 4, 'I': 1, 'H': 4,
                        'K': 5, 'J': 8, 'M': 3, 'L': 1, 'O': 1, 'N': 1, 'Q': 10, 'P': 3, 'S': 1,
                            'R': 1, 'U': 1, 'T': 1, 'W': 4, 'V': 4, 'Y': 4, 'X': 8, 'Z': 10, _BLANK: 0}

    def __init__(self, puzzle=None, target_puzzle=None, file_name=None, target_file_name=None, total_iterations=1000, override_fail=False):

        if puzzle:
            self.board = puzzle
        elif file_name:
            self.board = self.read_from_txt(file_name)
        else:
            raise("No starting board supplied")

        if target_puzzle:
            self.target_board = target_puzzle
        elif target_file_name:
            self.target_board = self.read_from_txt(target_file_name)
        else:
            self.target_board = None

        self.num_rows = len(self.board)
        self.num_cols = len(self.board[0])
        self.num_letters = self.num_rows * self.num_cols

        if not self.validate_board() and not override_fail:
            raise("Initiating with invalid puzzle!")

        self.change_history = []
        self.board_value = self.get_board_value()
        self.total_iterations = total_iterations
        self.iteration = 1

    def __str__(self):
        # String representation of board

        board_string = ""
        for row in self.board:
            for letter in row:
                board_string += letter
                board_string += " "
            board_string += "\n"
        #print(self.board)
        return board_string

    def read_from_txt(self, file_name):
        puzzle = []
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                puzzle.append([letter.upper() for letter in line])
        return puzzle

    def write_to_txt(self, file_name):
        with open(file_name, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(self.board)

    def iterate_board(self):
        # Creates iterator of all board positions

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                yield(i, j)

    def validate_board(self):
        # Checks every position on board to see if valid words
        # takes time O(num_rows*num_cols*(num_rows+num_cols))
        # This is too long and shouldn't be used to check every time
        # Use IsPuzzleSolved() for quick checks

        for i, j in self.iterate_board():
            if not self.check_words_ok(i, j):
                return False
        return True

    def get_board_value(self):
        # board value is average of letter values

        value = 0
        for i, j in self.iterate_board():
            value += PuzzleBoard._letter_values[self.get_letter(i, j)]
        return value/self.num_letters

    def update_board_value(self, new_letter, old_letter):
        # Updates the board value in O(1)

        new_val = PuzzleBoard._letter_values[new_letter]/self.num_letters
        old_val = PuzzleBoard._letter_values[old_letter]/self.num_letters
        self.board_value += (new_val - old_val)

    def get_words(self):
        words = []
        for i in range(self.num_rows):
            # Check the row

            start = 0
            row_letters = [self.get_letter(i, col_num) for col_num in range(self.num_cols)]
            for index, letter in enumerate(row_letters):
                if letter == PuzzleBoard._BLANK:
                    word = "".join(row_letters[start:index])
                    if word != PuzzleBoard._BLANK and len(word) > 0:
                        words.append(word)
                    start = index + 1
            if row_letters[-1] != PuzzleBoard._BLANK:
                word = "".join(row_letters[start:])
                words.append(word)

        for j in range(self.num_cols):
            # Check the column
            start = 0
            col_letters = [self.get_letter(row_num, j) for row_num in range(self.num_rows)]
            for index, letter in enumerate(col_letters):
                if letter == PuzzleBoard._BLANK:
                    word = "".join(col_letters[start:index])
                    if word != PuzzleBoard._BLANK and len(word) > 0 :
                        words.append(word)
                    start = index + 1
            if col_letters[-1] != PuzzleBoard._BLANK:
                word = "".join(col_letters[start:])
                words.append(word)
        return words

    def change_square(self, i, j, k):
        #MIGHT NEED TO ADD TARGET_FILE STUFF
        # Change one square of your choice
        old_letter = self.get_letter(i, j)
        if old_letter == PuzzleBoard._BLANK:
            print("Can't change a blank square")
            return False
        new_letter = PuzzleBoard._letters[k]
        self.board[i][j] = new_letter
        self.update_board_value(new_letter, old_letter)
        self.change_history.append((i, j))

    def mutate_one_square(self):
        # Randomly changes one square. Not allowed to change blank squares
        # This should interact with the change history

        while True:
            square_row = random.randint(0, self.num_rows-1)
            square_column = random.randint(0, self.num_cols-1)
            old_letter = self.get_letter(square_row, square_column)
            if old_letter == PuzzleBoard._BLANK:
                continue
            if self.target_board:
                if old_letter == self.target_board[square_row][square_column] and self.is_annealed(old_letter):
                    continue
            new_letter = PuzzleBoard._letters[random.randint(0, PuzzleBoard._num_letters-1)]
            self.board[square_row][square_column] = new_letter
            self.update_board_value(new_letter, old_letter)
            self.change_history.append((square_row, square_column))
            break

    def is_annealed(self, letter):
        #Freeze after quarter mark
        if self.iteration > self.total_iterations/4:
            return True
        energy = PuzzleBoard._letter_values[letter]**2
        temperature = self.total_iterations/self.iteration
        k = 20
        annealing_likelihood = 1 - exp(-energy*k/temperature)
        if random.random() < annealing_likelihood:
            return True
        else:
            return False

    def get_letter(self, row, col):
        return self.board[row][col]

    def check_words_ok(self, i, j):
        # Returns True if the two words that use cell (i, j) are legitimate
        # Returns False otherwise
        # TODO: This could be made more elegant and possibly faster
        # TODO: get rid of one of the check_words_ok functions
        # (doesn't need to check the whole row and column just between BLANKS)

        if self.get_letter(i, j) == PuzzleBoard._BLANK:
            return True
        row = "".join([self.get_letter(i, col_num) for col_num in range(self.num_cols)])
        row_split = row.split(PuzzleBoard._BLANK)
        num_letters_seen = 0
        for row_word in row_split:
            num_letters_seen += len(row_word) + 1
            if num_letters_seen > j:
                break

        if row_word.upper() not in words:
            return False

        col = "".join([self.get_letter(row_num, j) for row_num in range(self.num_rows)])
        col_split = col.split(PuzzleBoard._BLANK)

        num_letters_seen = 0
        for col_word in col_split:
            num_letters_seen += len(col_word) + 1
            if num_letters_seen > i:
                break

        if col_word.upper() not in words:
            return False

        return True

    def check_words_ok2(self, i, j):
        # Returns True if the two words that use cell (i, j) are legitimate UNLESS the word is a target word
        # Returns False otherwise
        # TODO: This could be made more elegant and possibly faster
        # (doesn't need to check the whole row and column just between BLANKS)

        if self.get_letter(i, j) == PuzzleBoard._BLANK:
            return True

        # Check the row
        row_indices = []
        start = 0
        row_letters = [self.get_letter(i, col_num) for col_num in range(self.num_cols)]
        for index, letter in enumerate(row_letters):
            if letter == PuzzleBoard._BLANK:
                word = row_letters[start:index]
                if word != PuzzleBoard._BLANK and len(word) > 0:
                    row_indices.append((start, index))
                start = index + 1
        if row_letters[-1] != PuzzleBoard._BLANK:
            row_indices.append((start, index+1))

        if self.target_board:
            target_row = [self.target_board[i][col_num] for col_num in range(self.num_cols)]

        for start, end in row_indices:
            word = "".join(row_letters[start:end])
            if word.upper() not in words:
                if self.target_board:
                    target_word = "".join(target_row[start:end])
                    if PuzzleBoard._BLANK not in target_word:
                        continue
                return False

        # Check the column
        col_indices = []
        start = 0
        col_letters = [self.get_letter(row_num, j) for row_num in range(self.num_rows)]
        for index, letter in enumerate(col_letters):
            if letter == PuzzleBoard._BLANK:
                word = col_letters[start:index]
                if word != PuzzleBoard._BLANK and len(word) > 0:
                    col_indices.append((start, index))
                start = index + 1
        if col_letters[-1] != PuzzleBoard._BLANK:
            col_indices.append((start, index+1))

        if self.target_board:
            target_col = [self.target_board[row_num][j] for row_num in range(self.num_rows)]

        for start, end in col_indices:
            word = "".join(col_letters[start:end])
            if word.upper() not in words:
                if self.target_board:
                    target_word = "".join(target_col[start:end])
                    if PuzzleBoard._BLANK not in target_word:
                        continue
                return False

        return True

    def is_puzzle_solved(self):
        # This should be used to check if the previous changes invalidated puzzle

        for change in self.change_history:
            changed_row, changed_col = change
            if not self.check_words_ok2(changed_row, changed_col):
                return False
        self.change_history = []
        return True



if __name__ == "__main__":
    puzzle = [['-', 'R', 'A', 'D'], ['L', 'A', 'T', 'E'], ['E', 'T', 'O', 'N'], ['D', 'A', 'P', '-']]




