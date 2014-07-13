from evolve_ann import evolve_generations_plateau, evolve_generations_count
from ann import GenFFANN
import random
import math

GenFFANN.INPUTSIZE = 1
GenFFANN.HIDDENSIZE = 20
GenFFANN.OUTPUTSIZE = 20

def simulate(bots):
    for bot in bots:
        inputs = [random.random() for _ in xrange(GenFFANN.INPUTSIZE)]
        outputs = bot.send_ff_signal(inputs)
        point = - 5 + random.random() * 10
        total = 0
        for idx, out in enumerate(outputs):
            total += outputs[idx] * (GenFFANN.OUTPUTSIZE - idx - 1)
        bot.fitness = -abs(math.cos(inputs[0]) - total)

if __name__ == "__main__":
    best_bot = evolve_generations_plateau(simulate, 0.0001, 15)
    # best_bot = evolve_generations_count(simulate, 150)
    print "\n"
    print " CHROMOSOME:\n", best_bot.chromosome
    outputs = best_bot.send_ff_signal([random.random() for _ in xrange(GenFFANN.INPUTSIZE)])
    print "\n SIGNAL FOR FITNESS:", outputs
    print "\n FITNESS:", best_bot.fitness, "\n\n"
    s = ""
    for n in range(0,len(outputs)):
        s += "{0} * x^({1}) + ".format(outputs[n], len(outputs) - n - 1)
    with open("output.txt", "w") as f:
        f.write(s)