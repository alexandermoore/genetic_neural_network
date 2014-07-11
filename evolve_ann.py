"""
A chromosome will have the following structure. Say there are 2 inputs, 3 hidden and 1 output.
Structure of chromosome weights is then:
(i1 -> h1), (i1 -> h2), (i1 -> h3), (i2 -> h1), ..., (i3 -> h3),
(h1 -> o1), (h2 -> o1), (h3 -> o1)
"""
from generation import Generation
from ann import GenFFANN

def evolve_generations(simulation_func):
    # Create start generation
    # While not done
    #	Simulate generation
    #	Check if should be done
    #	Spawn next generation
    pop_size = 50
    num_fittest = 5
    num_random = 10
    num_elites = 3
    Generator = GenFFANN
    current_gen = Generation(Generator, simulation_func, pop_size, num_fittest, num_random, num_elites)

    MAX_BAD_GEN_COUNT = 0
    best_fitness = 0
    bad_gen_count = 0
    negligible = 0.25
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

        if bad_gen_count >= MAX_BAD_GEN_COUNT:
            return best_generator

        current_gen = current_gen.spawn_next_generation()





