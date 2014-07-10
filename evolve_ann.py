"""
A chromosome will have the following structure. Say there are 2 inputs, 3 hidden and 1 output.
Structure of chromosome weights is then:
(i1 -> h1), (i1 -> h2), (i1 -> h3), (i2 -> h1), ..., (i3 -> h3),
(h1 -> o1), (h2 -> o1), (h3 -> o1)
"""

def evolve_generations(simulation_func):
	# Create start generation
	# While not done
	#	Simulate generation
	#	Check if should be done
	#	Spawn next generation

def apply_chromosome(ffann, chromosome):
	ffann.chromosome = chromosome
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



