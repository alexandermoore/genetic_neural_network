from battle_game import play, simulate, Player
from evolve_ann import evolve_generations_plateau, evolve_generations_count
import json
import argparse # IMPLEMENT ARGUMENTS TO DETERMINE WHETHER OR NOT HUMAN PLAYER SHOULD EXIST!



def status_display(p1, p2):
    px = p1
    print "{0} STATS:".format(px.name)
    print "HEALTH: {0}/{1}\nATTACK: {2}/{3}\nBLOCK CHANCE:{4}%".format(px.health, px.maxhealth, px.atk, px.maxatk, px.block*100)

    px = p2
    print "\n\n"
    print "{0} STATS:".format(px.name)
    print "HEALTH: {0}/{1}\nATTACK: {2}/{3}\nBLOCK CHANCE:{4}%".format(px.health, px.maxhealth, px.atk, px.maxatk, px.block*100)
    print "\n\n"


if __name__ == "__main__":

    vs_human = True
    if not vs_human:
        best_bot = evolve_generations_count(simulate, 200, pop_size=10, num_random=2, num_fittest=3, num_elites=2)
        # best_bot = evolve_generations_count(simulate, 150)
        print "\n"
        print " CHROMOSOME:\n", best_bot.chromosome
        with open("winner.json", "w") as f:
            f.write(json.dumps(best_bot.chromosome))
    else:
        chromosome = []
        with open("winner.json", "r") as f:
            chromosome = json.load(f)
        human = Player()
        human.name = "HUMAN"
        ai = Player()
        ai.make_bot(chromosome)
        play(human, ai, [True, False], stats_print_func=status_display)
