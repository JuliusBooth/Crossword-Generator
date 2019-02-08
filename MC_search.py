from PuzzleBoard import PuzzleBoard
import copy
import random
import numpy as np
import logging

logger = logging.getLogger('monte_carlo')
logger.setLevel(logging.INFO)

def monte_carlo_search(root_puzzle, depth=1, breadth=1000, iterations=1000, change_method="random", choice_method="random"):
    # At each iteration we copy the root_puzzle breadth times
    # We then make depth changes to each puzzle and throw out the invalid puzzles
    # One of the altered puzzles becomes the new root_puzzle
    original_puzzle = root_puzzle
    root_puzzle_value = root_puzzle.get_board_value()
    lengths = []
    if change_method == "network":
        from Model import Network
        network = Network(restore="saved_model")
        network.run_network()

    for iteration in range(iterations):

        puzzles = []

        #if not root_puzzle.validate_board():
         #   raise("Root Puzzle Invalid")

        if change_method == "network":
            cloned_puzzles = [copy.deepcopy(root_puzzle) for i in range(breadth)]

            for step in range(depth):
                x_train = np.array([cloned_puzzle.get_matrix()[:, :, :26] for cloned_puzzle in cloned_puzzles])
                output = network.predict(x_train)
                for num, prediction in enumerate(output):

                    probabilities = softmax(prediction)
                    i, j, k = sample(probabilities)

                    cloned_puzzles[num].change_square(i, j, k)
            puzzles = [cloned_puzzle for cloned_puzzle in cloned_puzzles if cloned_puzzle.is_puzzle_solved()]

        else:
            for branch in range(breadth):
                # this creates a deepcopy of the object
                # (ie. changes to its properties do not affect the original)
                cloned_puzzle = copy.deepcopy(root_puzzle)
                for step in range(depth):
                    cloned_puzzle.mutate_one_square()

                if cloned_puzzle.is_puzzle_solved():
                    puzzles.append(cloned_puzzle)
        lengths.append(len(puzzles))
        #print(len(puzzles))
        if len(puzzles) == 0:
            continue
        else:

            if choice_method == "distance":
                distances = [hamming_distance(cloned_puzzle, original_puzzle) for cloned_puzzle in puzzles]
                root_puzzle = puzzles[distances.index(max(distances))]

            elif choice_method == "value":
                for cloned_puzzle in puzzles:
                    value = cloned_puzzle.get_board_value()

                    if value >= root_puzzle_value:
                        root_puzzle = cloned_puzzle
                        root_puzzle_value = value
                print(root_puzzle_value)
            else:
                root_puzzle = random.choice(puzzles)
            print("Iteration: ", iteration)
            print(root_puzzle)
    print(sum(lengths)/iterations)
    return root_puzzle


def hamming_distance(puzzle1, puzzle2):
    distance = 0
    for i, j in puzzle1.iterate_board():
        if puzzle1.get_letter(i, j) != puzzle2.get_letter(i, j):
            distance += 1
    return distance


def softmax(x):
    return np.exp(x)/np.sum(np.exp(x))


def sample(x):
    flat_x = x.flatten()
    index = random.choice(list(enumerate(flat_x)))[0]
    i, j, k = np.unravel_index(index, x.shape)
    return(i, j, k)

if __name__ == "__main__":

    puzzle = PuzzleBoard(file_name="Valid_Boards/15x15_v1.txt", target_file_name="Valid_Boards/15x15_v1_target.txt")
    print(puzzle)

    puzzle = monte_carlo_search(puzzle, depth=2, iterations=1000000, breadth=10, choice_method="random", change_method="random")


