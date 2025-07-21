import random
import math
import copy

NUM_CARS = 25
MUTATION_RATE = 0.1

class NeuralNetwork:
    def __init__(self, input_size=5, hidden_size=6, output_size=1):
        self.weights1 = [[random.uniform(-1, 1) for _ in range(input_size)] for _ in range(hidden_size)]
        self.bias1 = [random.uniform(-1, 1) for _ in range(hidden_size)]
        self.weights2 = [[random.uniform(-1, 1) for _ in range(hidden_size)] for _ in range(output_size)]
        self.bias2 = [random.uniform(-1, 1) for _ in range(output_size)]

    def forward(self, inputs):
        hidden = []
        for i in range(len(self.weights1)):
            s = sum(w * inp for w, inp in zip(self.weights1[i], inputs)) + self.bias1[i]
            hidden.append(math.tanh(s))

        output = []
        for i in range(len(self.weights2)):
            s = sum(w * h for w, h in zip(self.weights2[i], hidden)) + self.bias2[i]
            output.append(sigmoid(s))
        return output

    def mutate(self):
        def mutate_val(val):
            if random.random() < MUTATION_RATE:
                return val + random.uniform(-0.5, 0.5)
            return val

        self.weights1 = [[mutate_val(w) for w in row] for row in self.weights1]
        self.bias1 = [mutate_val(b) for b in self.bias1]
        self.weights2 = [[mutate_val(w) for w in row] for row in self.weights2]
        self.bias2 = [mutate_val(b) for b in self.bias2]

    def copy(self):
        return copy.deepcopy(self)

def evolve_population(cars):
    cars.sort(key=lambda c: c.fitness, reverse=True)
    survivors = cars[:NUM_CARS//2]
    new_brains = [c.brain.copy() for c in survivors]

    for brain in new_brains:
        brain.mutate()

    while len(new_brains) < NUM_CARS:
        parent = random.choice(survivors).brain.copy()
        parent.mutate()
        new_brains.append(parent)
    
    return new_brains

def sigmoid(x):
    return 1 / (1 + math.exp(-x))
