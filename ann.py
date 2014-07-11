"""
The neural network will have a list of neurons.
Each neuron will keep track of its own edges with an adjacency list.
Each edge will be a (target, weight) tuple.
"""
from math import exp


def prepare_gen_ffann(inputsize, hiddensize, outputsize):
    GenFFANN.INPUTSIZE = inputsize
    GenFFANN.HIDDENSIZE = hiddensize
    GenFFANN.OUTPUTSIZE = outputsize


class GenFFANN():
    """
    Designed for genetic algorithm in particular
    """
    INPUTSIZE = 3
    HIDDENSIZE = 9
    OUTPUTSIZE = 1
    def __init__(self, chromosome):
        self.ffann = FFANN()
        self.ffann.create_feedforward_network(GenFFANN.INPUTSIZE, GenFFANN.HIDDENSIZE, GenFFANN.OUTPUTSIZE)
        self.apply_chromosome(self.ffann, chromosome)
        self.fitness = 0

    def apply_chromosome(self, ffann, chromosome):
        inputs = range(ffann.inputrange[0], ffann.inputrange[1] + 1)
        hiddens = range(ffann.hiddenrange[0], ffann.hiddenrange[1] + 1)
        outputs = range(ffann.outputrange[0], ffann.outputrange[1] + 1)

        pos = 0
        for n in inputs:
            for h in hiddens:
                ffann.set_edge_weight(n,h,chromosome[pos])
                pos += 1
        for h in hiddens:
            for o in outputs:
                ffann.set_edge_weight(h, o, chromosome[pos])
                pos += 1

    def send_ff_signal(self, input_signals):
        return self.ffann.send_ff_signal(input_signals)

class FFANN():
    def __init__(self):
        self.neurons = []
        self.inputrange = ()
        self.hiddenrange = ()
        self.outputrange = ()

    def create_feedforward_network(self, inputsize, hiddensize, outputsize):
        inf, inl = self.add_input_layer(inputsize)
        hidf, hidl = self.add_hidden_layer(hiddensize, inf, inl)
        outf, outl = self.add_output_layer(outputsize, hidf, hidl)
        return inf, inl, outf, outl

    def add_input_layer(self, size):
        first = len(self.neurons)
        for _ in xrange(size):
            self.add_neuron()
        last = len(self.neurons) - 1
        self.inputrange = (first, last)
        return (first, last)

    def add_hidden_layer(self, size, inputstart, inputend):
        first = len(self.neurons)
        for _ in xrange(size):
            self.add_neuron()
        last = len(self.neurons) - 1

        # Connect all input neurons to hidden layer with edge weight 0
        for i in xrange(inputstart, inputend+1):
            for h in xrange(first, last+1):
                self.add_edge(i, h, 0)

        self.hiddenrange = (first, last)
        return (first, last)

    def add_output_layer(self, size, hiddenstart, hiddenend):
        first = len(self.neurons)
        for _ in xrange(size):
            self.add_neuron()
        last = len(self.neurons) - 1

        # Connect all hidden neurons to output layer with edge weight 0
        for h in xrange(hiddenstart, hiddenend+1):
            for o in xrange(first, last+1):
                self.add_edge(h, o, 0)

        self.outputrange = (first, last)
        return (first, last)

    def add_edge(self, a, b, weight):
        self.set_edge_weight(a, b, weight)

    def set_edge_weight(self, a, b, weight):
        self.neurons[a]["edges"][b] = weight
        self.neurons[b]["incoming_edges"][a] = weight

    def add_neuron(self):
        new_neuron = {"edges": {}, "incoming_edges": {}, "value": 0}
        self.neurons.append(new_neuron)
        return len(self.neurons) - 1

    def act_func(self, sum_input):
        return 1.0 / (1.0 + exp(-sum_input))

    def send_ff_signal(self, input_signals):
        inputs = range(self.inputrange[0], self.inputrange[1] + 1)
        hiddens = range(self.hiddenrange[0], self.hiddenrange[1] + 1)
        outputs = range(self.outputrange[0], self.outputrange[1] + 1)

        # Evaluate input layer
        for idx, i in enumerate(inputs):
            self.neurons[i]["value"] = input_signals[idx]

        # Evaluate hidden layer
        for h in hiddens:
            total = 0
            for n in self.neurons[h]["incoming_edges"].keys():
                total += self.neurons[n]["value"] * self.neurons[n]["edges"][h]
            self.neurons[h]["value"] = self.act_func(total)

        # Evaluate output layer
        for o in outputs:
            total = 0
            for n in self.neurons[o]["incoming_edges"]:
                total += self.neurons[n]["value"] * self.neurons[n]["edges"][o]
            self.neurons[o]["value"] = self.act_func(total)

        # Return all output layer values
        return [self.neurons[o]["value"] for o in outputs]