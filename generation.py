import random

class Generation :
    
    '''***************** FIELDS *****************'''
    
    # The top "num_fittest" generators will be taken from each generation
    # for breeding.
    num_fittest = 0
    # Size of each new generation
    pop_size = 0
    # Fittest members of current population
    fittest = []
    # Generator objects in population
    generators = []
    # Number of random generators to add each time
    num_random = 0
    # Number of members from the fittest generators to keep in the population. Implements "elitism" so best genes are allowed to survive.
    num_elites = 0

    '''***************** METHODS *****************'''
    
    ''' __init__
    Constructor. Initializes num_fittest, pop_size, num_random and num_elites.
    RETURNS: No return value.
    -num_fit (int): Assigned to self.num_fittest
    -int pop_sz (int) : Assigned to self.pop_size
    -num_rnd (int) : Assigned to self.num_random
    -elites (int) : Assigned to self.num_elites
    '''    
    def __init__(self,generator, simulation_func, pop_sz,num_fit,num_rnd,elites, generator_param_count) :
        self.pop_size = pop_sz
        self.num_fittest = num_fit
        self.num_random = num_rnd
        self.num_elites = elites
        self.Generator = generator
        self.simulation_func = simulation_func
        self.generator_param_count = generator_param_count
    
    ''' simulate_generators
    In situations where all generators compete, this allows an external function to
    calculate their "fitness" attribute.
    RETURNS: No return value.
    '''
    def simulate_generators(self):
        self.simulation_func( self.generators )

    ''' update_fittest
    Updates self.fittest with the most fit Generators in self.generators (the population).
    RETURNS: No return value.
    '''   
    def update_fittest(self) :
        self.generators.sort(key = lambda x: x.fitness)
        self.generators.reverse()
        self.fittest = self.generators[:self.num_fittest]

    ''' spawn_random_generation
    Spawns a new Generation of Generators with random parameters. Stores the result in self.generators.
    RETURNS: No return value
    '''
    def spawn_random_generation(self) :
        self.generators = self.__make_random_generators(self.pop_size)
    
    ''' __make_random_generators
    Creates a list of "count" Generators with random parameters.
    RETURNS: The list of Generators. (Generator list)
    -count (int) : The number of generators to create.
    '''
    def __make_random_generators(self,count) :
        rand_gens = []
        for i in range(0, count) :
            new_gen = self.Generator([-1 + 2*random.random() for x in range (0,self.generator_param_count)])
            rand_gens.append(new_gen)
        return rand_gens

    ''' __add_probabilities
    Associates each generator in a list of generators with a number based on their fitness for the purposes of probability. More fit generators have more space between the previous number and their own, increasing the likelihood of them being selected by __ger_probabilistic_random. Used to prepare a list of generators for __get_probabilistic_random.
    RETURNS: A list of pairs, each containing (original generator, associated number). (Generator * int) list
    -gens (Generator list) : The original list of generators.
    '''
    def __add_probabilities(self,gens) :
        prob_list = []
        upper_bound = 0
        for g in gens :
            upper_bound = upper_bound + abs(g.fitness)
            prob_list.append((g, upper_bound))
        return prob_list
    
    ''' __get_probabilistic_random
    Returns the first part of a tuple (the generator) in a random element from prob_list. Elements whose associated number ranges cover more distance are more likely to be chosen. These number ranges are decided based on fitness in __add_probabilities.
    RETURNS: A pair containing the selected element's generator and the original list without that element. (Generator * ((Generator * int) list))
    -prob_list (Generator * int) list : List of generator * time pairs outputted from __add_probabilities.
    '''
    def __get_probabilistic_random(self,prob_list) :
        # Get upper bound for random number (2nd part of tuple in last element of list)
        upper_bound = prob_list[-1][1]
        num = random.random()*upper_bound

        prob_list_cpy = list(prob_list)

        # Figure out which element was selected
        # By default, winner = last element
        winner = prob_list[-1]
        for o in prob_list :
            if (num <= o[1]) :
                winner = o[0]
                prob_list_cpy.remove(o)
                break
        return (winner, prob_list_cpy)
      
    ''' spawn_next_generation
    Spawns a new generation of generators created by breeding the Generators contained in fittest. The new generation contains the children resulting from this breeding, self.num_elites of the fittest Generators from the previous generation, and self.num_random new random Generators.
    RETURNS: The newly spawned Generation. (Generation)
    '''
    def spawn_next_generation(self) :

        prob_fittest = self.__add_probabilities(self.fittest)

        children = []
        for i in range(0, self.pop_size - self.num_random - self.num_elites) :
            children.append(self.__spawn_child(prob_fittest))
            
        new_gen = Generation(self.Generator, self.simulation_func, self.pop_size,self.num_fittest,self.num_random,self.num_elites, self.generator_param_count)
        new_gen.generators = children + self.__make_random_generators(self.num_random) + self.fittest[:self.num_elites]
        return new_gen
    
    ''' __spawn_child
    Outputs one child of two probabilistically selected members of prob_fittest. Probability weight is based on fitness (runtimes), so the argument list of Generators should be one that was outputted by __add_probabilities.
    RETURNS: The child Generator (Generator)
    -prob_fittest (Generator * int) list : A list of generators to spawn children from. Should be the result of calling __add_probabilities on a list of Generators.
    '''
    def __spawn_child (self,prob_fittest) :
        # Select the first parent.
        p1_tuple = self.__get_probabilistic_random(prob_fittest)
        p1 = p1_tuple[0]
        # Select the second parent from the remaining potential parents.
        p2 = self.__get_probabilistic_random(p1_tuple[1])[0]
        # Breed a child and return it
        return self.__breed(p1, p2)
    
    ''' __mutate
    Mutates a gene (parameter) based on a Gaussian centered at its original value.
    RETURNS: The mutated gene (float)
    -gene (float) : The gene (parameter) to mutate. Expected to be between 0 and 1.
    '''
    def __mutate(self,gene) :
        chance = 0.1
        stddev = 0.2
        # Gaussian distribution mutation
        if random.random() < chance :
            return min(1.0, max(0.0, random.gauss(gene,stddev)))
        else :
            return gene
            
        # Uniform distribution mutation
        # amplitude = 0.2
        #chance = 0.1
        #if random.random() < chance :
        #    gene = min(1.0, max(0.0, gene + amplitude*(random.random()-0.5)))
        #else :
        #    gene
        #return gene
    
    ''' __breed
    Breeds g1 and g2 via some crossing over method.
    RETURNS: The resulting child (Generator)
    -g1 (Generator) : The first parent of the child.
    -g2 (Generator) : The second parent of the child.
    '''
    def __breed(self,g1, g2) :
    
    
        # THIS IS A WEIGHTED UNIFORM CROSSOVER.
        # http://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#Uniform_Crossover_and_Half_Uniform_Crossover
        # More fit = more likely to pass on genes.
        g1r = float(g1.fitness)
        g2r = float(g2.fitness)
        if (g1r + g2r == 0):
            # If sum is 0, just choose arbitrarily
            weight = 0.5
        else:
            weight = g1r / (g1r + g2r)

        # THIS IS A WEIGHTED AVERAGE CROSSOVER. Child is the weighted average of its parents.
        '''
        params1 = g1.chromosome
        params2 = g2.chromosome
        newparams = []
        for i in range(0,self.generator_param_count) :
            gene = weight * params1[i] + (1.0 - weight) * params2[i]
            newparams = newparams + [self.__mutate(gene)]
        '''
        
        # Cross over parameters randomly
        params1 = g1.chromosome
        params2 = g2.chromosome
        newparams = []
        for i in range(0,self.generator_param_count) :
            if (random.random() < weight) :
                gene = params1[i]
            else :
                gene = params2[i]
            newparams = newparams + [self.__mutate(gene)]
        return self.Generator(newparams)
    
    ''' run
    Creates a list of the most fit Generators in the current generation and outputs the average runtime of the fittest one.
    RETURNS: The average runtime of the most fit generators (float).
    '''
    def run(self) :
        if self.simulation_func is not None:
            self.simulate_generators()
        self.update_fittest()
        return self.fittest[0].fitness
    
  