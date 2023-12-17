# SimpleNode

SimpleNode is a small package for working with Neural Networks in python

## Features

- Easily create a Neural Network
- Create Labled Data
- Train the Neural Network using Labled Data
- Save trained models
- Load previously saved models
- Make predictions with new inputs

## Example

```
from NeuralNetwork import NeuralNetwork

// Sample XOR dataset
x = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [[0, 1], [1, 0], [1, 0], [0, 1]]

Network = NeuralNetwork([2, 3, 2])

// Params: trainDataX, trainDataY, epochs, reportFreq
Network.Learn(x, y, 10, 1)

// Save Network
Network.SaveNetwork("MyNetwork.csv")

// Predict
print( Network.Predict([1, 0]) )
```

Created by Artyom Yesayan
