from PuzzleBoard import PuzzleBoard
import copy
import logging
import multiprocessing as mp
import argparse
from GenerateTargetBoards import generate_targets
import random

def generate_new_board(root_puzzle, depth=1):
    # At each iteration we copy the root_puzzle breadth times
    # We then make depth changes to each puzzle and throw out the invalid puzzles
    # One of the altered puzzles becomes the new root_puzzle
    original_puzzle = copy.deepcopy(root_puzzle)
    logger.info(original_puzzle)
    iterations = original_puzzle.total_iterations
    for iteration in range(iterations):
        cloned_puzzle = copy.deepcopy(root_puzzle)

        for mutation in range(depth):
            cloned_puzzle.mutate_one_square()

        if cloned_puzzle.is_puzzle_solved():
            root_puzzle = cloned_puzzle

            logger.info("Current iteration: %d", iteration)
            logger.info(root_puzzle.board)
            logger.info(root_puzzle)
        root_puzzle.iteration += 1
        if root_puzzle.iteration % 1000 == 0 and root_puzzle.validate_board():
            return root_puzzle
    return root_puzzle


def run_parallel(func, num_processes, **kwargs):
    pool = mp.Pool(processes=num_processes)

    # Setup a list of processes that we want to run
    results = [pool.apply_async(func, (kwargs['starting_puzzle'], kwargs['depth'])) for p in range(num_processes)]

    # Get process results from the output queue
    generated_puzzles = [result.get() for result in results]

    return generated_puzzles


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Puzzle Generation Options.')
    parser.add_argument('-p', '--processes', default=1, type=int,
                        help="number of processes/puzzles made")
    parser.add_argument('-d', '--depth', default=2, type=int,
                        help="steps per iteration (depth)")
    parser.add_argument('-i', '--iterations', default=1000, type=int,
                        help="iterations")
    puzzle_options = parser.parse_args()

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.WARNING, format='%(message)s')

    DEPTH = puzzle_options.depth
    ITERATIONS = puzzle_options.iterations
    SIZE = "15x15"
    NUM_PROCESSES = puzzle_options.processes

    TARGET = generate_targets("Valid_Boards/15x15_v2_target.txt", 1).board
    logger.info(TARGET)
    starting_puzzle = PuzzleBoard(file_name="Valid_Boards/15x15_v2.txt",
                                  target_puzzle=TARGET,
                                  total_iterations=ITERATIONS)

    new_puzzles = run_parallel(generate_new_board, NUM_PROCESSES, starting_puzzle=starting_puzzle, depth=DEPTH)
    for puzzle_num, puzzle in enumerate(new_puzzles):
        print(puzzle)
        print(puzzle.board)
        print(puzzle.validate_board())
        if puzzle.validate_board():
            random_addon = str(random.randint(1,1000))
            file_name = "Valid_Boards/testing/" + SIZE + "_Depth" + str(DEPTH) + "_Iterations" + str(ITERATIONS) + "_#" + str(puzzle_num) + "_" + random_addon
            puzzle.write_to_txt(file_name)
