from PuzzleBoard import PuzzleBoard
import json
from collections import defaultdict
import random
import copy

#STANKY CODE IN THIS FILE

DICTIONARY = "Dictionaries/master_dictionary.json"
with open(DICTIONARY, "r") as read_file:
    words = json.load(read_file)
    word_length_dict = defaultdict(list)
    for word, value in words.items():
        word_length_dict[len(word)].append(word.upper())
    words = dict([(k.upper(), v) for (k, v) in words.items()])


def get_indices(puzzle):
    row_indices = set()
    col_indices = set()
    for i in range(puzzle.num_rows):
        # Check the row
        #row_indices = []
        start = 0
        row_letters = [puzzle.get_letter(i, col_num) for col_num in range(puzzle.num_cols)]
        for index, letter in enumerate(row_letters):
            if letter == PuzzleBoard._BLANK:
                word = row_letters[start:index]
                if word != PuzzleBoard._BLANK and len(word) > 0and index-start>2:

                    row_indices.add(((i, start),(i, index), "R"))
                start = index + 1
        if row_letters[-1] != PuzzleBoard._BLANK:

            row_indices.add(((i, start),(i, index+1), "R"))

    for j in range(puzzle.num_cols):
        # Check the column
        #col_indices = []
        start = 0
        col_letters = [puzzle.get_letter(row_num, j) for row_num in range(puzzle.num_rows)]
        for index, letter in enumerate(col_letters):
            if letter == PuzzleBoard._BLANK:
                word = col_letters[start:index]
                if word != PuzzleBoard._BLANK and len(word) > 0 and index-start>2:

                    col_indices.add(((start, j),(index, j), "C"))
                start = index + 1
        if col_letters[-1] != PuzzleBoard._BLANK:

            col_indices.add(((start, j),(index+1, j), "C"))

    return row_indices, col_indices


def insert_word(puzzle, word, start, direction):
    for index in range(len(word)):
        if direction == "R":
            puzzle.board[start[0]][start[1]+index] = word[index]
        else:
            puzzle.board[start[0] + index][start[1]] = word[index]


def recurse(puzzle_frame,remaining_word_indices):
    print(puzzle_frame, len(remaining_word_indices))
    if not remaining_word_indices:
        return puzzle_frame
    start, end, direction = remaining_word_indices.pop()

    if direction == "R":
        length = end[1] - start[1]
    else:
        length = end[0] - start[0]
    random.shuffle(word_length_dict[length])
    for word_attempt in word_length_dict[length]:
        insert_word(puzzle_frame, word_attempt, start, direction)
        if puzzle_frame.validate_board():
            result = recurse(puzzle_frame, remaining_word_indices)
            if not result:
                continue
            else:
                return result
    return False


def fit_words_in(puzzle_frame):
    row_indices, col_indices = get_indices(puzzle_frame)
    word_indices = row_indices.union(col_indices)
    for i, j in puzzle_frame.iterate_board():
        if puzzle_frame.get_letter(i, j) != PuzzleBoard._BLANK:
            puzzle_frame.board[i][j] = "-"

    for index,(start, end, direction) in enumerate(word_indices):

        if direction == "R":
            length = end[1] - start[1]
        else:
            length = end[0] - start[0]
        if index == 0:
            word_attempt = random.choice(word_length_dict[length])
            insert_word(puzzle_frame, word_attempt, start, direction)
        else:
            random.shuffle(word_length_dict[length])
            for word_attempt in word_length_dict[length]:
                insert_word(puzzle_frame, word_attempt, start, direction)
                if puzzle_frame.validate_board():
                    break
            if not puzzle_frame.validate_board():
                return False

    return puzzle_frame


def generate_targets(puzzle_skeleton, number_of_targets):
    puzzle = PuzzleBoard(file_name=puzzle_skeleton)

    for i, j in puzzle.iterate_board():
        if puzzle.get_letter(i, j) != PuzzleBoard._BLANK:
            puzzle.board[i][j] = "!"

    targets = []

    while len(targets) < number_of_targets:
        puzzle_frame = copy.deepcopy(puzzle)
        print(puzzle_frame)
        generated_target = fit_words_in(puzzle_frame)
        if generated_target:
            targets.append(generated_target)

    if number_of_targets == 1:
        return targets[0]
    for i, target_puzzle in enumerate(targets):
        file_name = "Valid_Boards/Targets/15x15_generated_target_" + str(i+14) + ".txt"
        target_puzzle.write_to_txt(file_name)
    return targets



#generate_targets("Valid_Boards/15x15_v1_target.txt", 2)
