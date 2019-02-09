from PuzzleBoard import PuzzleBoard
import copy
import logging
import multiprocessing as mp


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
    return root_puzzle


def run_parallel(func, num_processes, **kwargs):
    pool = mp.Pool(processes=num_processes)

    # Setup a list of processes that we want to run
    results = [pool.apply_async(func, (kwargs['starting_puzzle'], kwargs['depth'])) for p in range(num_processes)]

    # Get process results from the output queue
    generated_puzzles = [result.get() for result in results]

    return generated_puzzles


def generate_british_puzzle():
    starting_puzzle = PuzzleBoard(file_name="Valid_Boards/15x15_v1_target.txt",
                                  target_file_name="Valid_Boards/15x15_v1_target2.txt",
                                  total_iterations=100000)
    result_puzzle = generate_new_board(starting_puzzle, depth=3)
    print(result_puzzle.board)
    print(result_puzzle)

if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    #new_puzzle = generate_new_board(starting_puzzle, depth=1, iterations=10000)

    DEPTH = 2
    ITERATIONS = 10000
    SIZE = "15x15"
    NUM_PROCESSES = 2
    TARGET = "15x15_v1_target2.txt"
    starting_puzzle = PuzzleBoard(file_name="Valid_Boards/15x15_v1.txt",
                                  target_file_name="Valid_Boards/" + TARGET,
                                  total_iterations=ITERATIONS)

    new_puzzles = run_parallel(generate_new_board, NUM_PROCESSES, starting_puzzle=starting_puzzle, depth=DEPTH)
    for puzzle_num, puzzle in enumerate(new_puzzles):
        print(puzzle)
        print(puzzle.board)
        print(puzzle.validate_board())
        file_name = "Valid_Boards/testing/" + SIZE + "_Depth" + str(DEPTH) + "_Iterations" + str(ITERATIONS) + "_#" + str(puzzle_num) + "_"+ TARGET
        #puzzle.write_to_txt(file_name)
