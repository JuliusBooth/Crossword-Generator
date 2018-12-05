# RLXwords
A Reinforcement Learning approach to crossword puzzle generation


## TODO - December 5

### Work so far

We have a working 4x4 change suggesting Network.

We can use this to guide directed Monte Carlo Tree Search.

### Next Steps

If someone could add continuous integration testing that'd be really useful as well.
Use the Unittest python module.

Some of the functions I wrote for PuzzleBoard aren't the best (check_words_ok() I'm looking at you).
It works, but feel free to make it better.

Make sure you push to branches for now (until we have testing) and have someone check the pull request first before merging.

I was having some intense pathing troubles (it was due to Pycharm but I figured that out after) and I got rid of any file structure we once had. Someone could help with that.

We need to change the Model object so that it's easier to use it for predictions. I think that would involve adding a separate method for predictions. That would involve converting all variables to object variables (x to self.x).


### Readings

1. http://cs231n.github.io/convolutional-networks/ --talks about ConvNeuralNet for visual recognition 
2. https://www.tensorflow.org/tutorials/estimators/cnn --TensorFlow Tutorial on Build ConvNeuralNet using Estimators 
