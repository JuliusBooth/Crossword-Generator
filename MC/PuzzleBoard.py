import json
import random
import csv



with open("../Dictionaries/master_dictionary.json", "r") as read_file:
    words = json.load(read_file)
    # Don't store words in PuzzleBoard or it's too slow using copy.deepcopy


class PuzzleBoard:

    _BLANK = "-"
    _letters = list(map(chr, range(65, 91))) + [_BLANK]
    #_letters = ["A","E","I","O","U","C","D","L","N","P","R","S","T","B",BLANK]
    _num_letters = len(_letters)-1

    _letter_values = {'A': 1, 'C': 3, 'B': 3, 'E': 1, 'D': 2, 'G': 2, 'F': 4, 'I': 1, 'H': 4,
                        'K': 5, 'J': 8, 'M': 3, 'L': 1, 'O': 1, 'N': 1, 'Q': 10, 'P': 3, 'S': 1,
                        'R': 1, 'U': 1, 'T': 1, 'W': 4, 'V': 4, 'Y': 4, 'X': 8, 'Z': 10, _BLANK: 0}

    def __init__(self, puzzle=None, file_name=None):

        if puzzle:
            self.board = puzzle
        elif file_name:
            self.read_from_txt(file_name)
        else:
            raise("No starting board supplied")

        self.num_rows = len(self.board)
        self.num_cols = len(self.board[0])
        self.num_letters = self.num_rows * self.num_cols

        if not self.validate_board():
            raise("Initiating with invalid puzzle!")

        self.change_history = []
        self.board_value = self.get_board_value()

    def __str__(self):
        # String representation of board

        board_string = ""
        for row in self.board:
            for letter in row:
                board_string += letter
                board_string += " "
            board_string += "\n"
        print(self.board)
        return board_string

    def read_from_txt(self, file_name):
        puzzle = []
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                puzzle.append([letter.upper() for letter in line])
        self.board = puzzle

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

    def mutate_one_square(self):
        # Randomly changes one square. Not allowed to change blank squares
        # This should interact with the change history

        while True:
            square_row = random.randint(0, self.num_rows-1)
            square_column = random.randint(0, self.num_cols-1)
            old_letter = self.get_letter(square_row, square_column)
            if old_letter == PuzzleBoard._BLANK:
                continue
            new_letter = PuzzleBoard._letters[random.randint(0, PuzzleBoard._num_letters-1)]
            self.board[square_row][square_column] = new_letter
            self.update_board_value(new_letter, old_letter)
            self.change_history.append((square_row, square_column))
            break

    def get_letter(self, row, col):
        return self.board[row][col]

    def check_words_ok(self, i, j):
        # Returns True if the two words that use cell (i, j) are legitimate
        # Returns False otherwise
        # This could be made more elegant and possibly faster
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

    def is_puzzle_solved(self):
        # This should be used to check if the previous changes invalidated puzzle

        for change in self.change_history:
            changed_row, changed_col = change
            if not self.check_words_ok(changed_row, changed_col):
                return False
        self.change_history = []
        return True

    def solve_puzzle_randomly(self):
        # Randomly makes changes until puzzle is valid

        for i in range(1000000):
            if self.validate_board():
                return (i)
            else:
                self.mutate_one_square()
        return "Could not solve"


if __name__ == "__main__":
    puzzle = [['-', 'R', 'A', 'D'], ['L', 'A', 'T', 'E'], ['E', 'T', 'O', 'N'], ['D', 'A', 'P', '-']]



