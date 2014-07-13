"""
A chromosome will have the following structure. Say there are 2 inputs, 3 hidden and 1 output.
Structure of chromosome weights is then:
(i1 -> h1), (i1 -> h2), (i1 -> h3), (i2 -> h1), ..., (i3 -> h3),
(h1 -> o1), (h2 -> o1), (h3 -> o1)
"""
from generation import Generation
from ann import GenFFANN


def evolve_generations_count(simulation_func, max_num_generations):
    # Create start generation
    # While not done
    #	Simulate generation
    #	Check if should be done
    #	Spawn next generation
    pop_size = 60
    num_fittest = 5
    num_random = 10
    num_elites = 3
    Generator = GenFFANN
    num_params = (GenFFANN.INPUTSIZE * GenFFANN.HIDDENSIZE) + (GenFFANN.HIDDENSIZE * GenFFANN.OUTPUTSIZE)
    print num_params
    current_gen = Generation(Generator, simulation_func, pop_size, num_fittest, num_random, num_elites, num_params)
    current_gen.spawn_random_generation()

    best_fitness = -100000
    gen_num = 0
    while True:
        gen_num += 1

        print "Running generation {0}".format(gen_num)

        fitness = current_gen.run()

        print "Fitness is {0} compared to {1}".format(fitness, best_fitness)
        if fitness > best_fitness:
            best_generator = current_gen.fittest[0]
            best_fitness = best_generator.fitness

        if  gen_num >= max_num_generations:
            return best_generator

        current_gen = current_gen.spawn_next_generation()

def evolve_generations_plateau(simulation_func, negligible, max_bad_gen_count):
    # Create start generation
    # While not done
    #	Simulate generation
    #	Check if should be done
    #	Spawn next generation
    pop_size = 60
    num_fittest = 5
    num_random = 10
    num_elites = 3
    Generator = GenFFANN
    num_params = (GenFFANN.INPUTSIZE * GenFFANN.HIDDENSIZE) + (GenFFANN.HIDDENSIZE * GenFFANN.OUTPUTSIZE)
    print num_params
    current_gen = Generation(Generator, simulation_func, pop_size, num_fittest, num_random, num_elites, num_params)
    current_gen.spawn_random_generation()

    best_fitness = -100000
    bad_gen_count = 0
    gen_num = 0
    while True:
        gen_num += 1

        print "Running generation {0}".format(gen_num)

        fitness = current_gen.run()

        print "Fitness is {0} compared to {1}".format(fitness, best_fitness)
        if fitness - best_fitness <= negligible:
            bad_gen_count += 1
            print "Bad Generation #{0}".format(bad_gen_count)
        else:
            bad_gen_count = 0
            best_generator = current_gen.fittest[0]
            best_fitness = best_generator.fitness

        if bad_gen_count >= max_bad_gen_count:
            return best_generator

        current_gen = current_gen.spawn_next_generation()





