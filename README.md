# RLXwords
A Reinforcement Learning approach to crossword puzzle generation


## TODO - November 29

### Work so far

We're working on the MC/ (Monte Carlo only) section first before moving on to RL/

I've written a working version of the PuzzleBoard class and a Monte Carlo search.
Take a look and familiarize yourselves with the code.

The RL/ version of the PuzzleBoard will be a bit more complicated as all operations will be done on a 3d numpy matrix of 1s and 0s.

### Next Steps

We need larger puzzles to test. Right now I've generated 5x5 puzzles. I think we should look at at least 20x20
Chun is going to add input and output functions to the MC/PuzzleBoard class which will read and write to textfiles.
I'd like someone to do the boring work of typing out a valid 20x20 puzzle (and test that it's valid).


If someone could add continuous integration testing that'd be really useful as well.
Use the Unittest python module.

Some of the functions I wrote for MC/PuzzleBoard aren't the best (check_words_ok() I'm looking at you).
It works, but feel free to make it better.

Make sure you push to branches for now (until we have testing) and have someone check the pull request first before merging.
