from evolve_ann import evolve_generations_plateau, evolve_generations_count
from ann import GenFFANN
import random
import sys
import time


GenFFANN.INPUTSIZE = 1
GenFFANN.HIDDENSIZE = 20
GenFFANN.OUTPUTSIZE = 4 # attack, heal, inc attack, inc block


class Player():
    def __init__(self):
        self.health = 100
        self.maxhealth = 100
        self.atk = 10
        self.block = 0.0
        self.maxatk = 100
        self.bot = None
        self.move_history = []
        self.target = None # Enemy player
        self.name = "SOME PLAYER"
        pass

    def make_bot(self, chromosome):
        self.bot = GenFFANN(chromosome)

    def inc_block(self):
        self.block = max(self.block + 0.05, 0.90)
        self.move_history.append("inc_block")
        return "INCREASED BLOCK BY 5%!"

    def inc_atk(self):
        self.atk = max(self.atk + 5, self.maxatk)
        self.move_history.append("inc_atk")
        return "INCREASED ATTACK BY 5!"

    def heal(self):
        self.health = max(self.health + 30, self.maxhealth)
        self.move_history.append("heal")
        return "HEALED FOR 30 HEALTH!"

    def attack(self):
        player = self.target
        self.move_history.append("attack")
        block = (random.random() < player.block)
        if block:
            return "ATTACKED! IT WAS BLOCKED!"
        else:
            player.health -= self.atk
            return "ATTACKED! THE ATTACK HIT!"

    def translate_move_history(self):
        trans = []
        # Translates it into groups of 4
        if self.move_history:
            for m in self.move_history:
                if m == "attack":
                    trans.append( [1, 0, 0, 0] )
                elif m == "block":
                    trans.append( [0, 1, 0, 0] )
                elif m == "inc_atk":
                    trans.append( [0, 0, 1, 0])
                elif m == "inc_block":
                    trans.append( [0, 0, 0, 1] )
        return trans

    def null_moves(self, how_many):
        return [ [0,0,0,0] for  _ in xrange(how_many)]


def get_inputs(me, opp):
    # INPUTS:
    #   my health
    #   my atk
    #   my block

    # THIS HAPPENS num_steps_back TIMES
    #   my_last_move attack
    #   my_last_move heal
    #   my_last_move inc_attack
    #   my_last_move inc_block

    #   opponent health
    #   opponent atk
    #   opponent block

    # THIS HAPPENS num_steps_back TIMES
    #   opp_last_move attack
    #   opp_last_move heal
    #   opp_last_move inc_attack
    #   opp_last_move inc_block

    num_steps_back = 1

    move_hist = me.translate_move_history()
    if len(move_hist) < num_steps_back:
        move_hist.extend( me.null_moves(num_steps_back - len(move_hist)) )
    my_inputs = [me.health/me.maxhealth, me.atk/me.maxatk, me.block] + move_hist[-num_steps_back:]

    move_hist = me.translate_move_history()
    if len(move_hist) < num_steps_back:
        move_hist.extend( opp.null_moves(num_steps_back - len(move_hist)) )
    opp_inputs = [opp.health/opp.maxhealth, opp.atk/opp.maxatk, opp.block] + move_hist[-num_steps_back:]

    return my_inputs + opp_inputs


def init_bot_player(bot):
    player = Player()
    player.bot = bot
    return player

def simulate(bots):
    # Each bot competes with half of other bots
    num_competitors = len(bots)/2

    # Start with 0 fitness
    for bot in bots:
        bot.fitness = 0

    # Play against others
    for bot in bots:
        bots_cpy = list(bots)
        bots_cpy.remove(bot)
        opponents = random.sample(bots_cpy, num_competitors)
        for opp_bot in opponents:
            me = init_bot_player(bot)
            opp = init_bot_player(opp_bot)
            winner = play(me, opp, [False, False])
            if winner:
                winner.bot.fitness += 1




def get_move(me, opp, is_human):

    MOVES = {0: me.attack, 1: me.heal, 2: me.inc_atk, 3: me.inc_block}

    if not is_human:
        bot = me.bot
        inputs = get_inputs(me, opp)
        outputs = bot.send_ff_signal(inputs)
        champ = 0
        for i in xrange(len(outputs)):
            if outputs[i] > champ:
                champidx = i
                champ = outputs[i]

        return MOVES[champidx]
    else:

        while(True):
            input = raw_input("MOVES:\n1: ATTACK\n2: HEAL\n3: INCREASE ATTACK\n4: INCREASE BLOCK\n")

            input = int(input) - 1
            if input in MOVES:
                return MOVES[input]
            else:
                print "Invalid move. Try again."

def play(p1, p2, is_human_lst, stats_print_func = None):
    #print "BOT {0} PLAYING BOT {1}".format(p1, p2)
    first = p1 if random.random() >= 0.50 else p2
    second = p2 if first == p1 else p1

    first.target = second
    second.target = first

    players = [first, second]

    # IS_HUMAN_LST NEEDS TO BE FIXED!!!

    current = 0
    other = 1

    def nothing(_):
        pass
    msg = nothing

    if (True in is_human_lst):
        msg = sys.stdout.write

    turns = 0.0
    maxturns = 50
    while(True):
        turns += 0.5
        if stats_print_func:
            stats_print_func(p1, p2)

        move = get_move(players[current], players[other], is_human_lst[current])
        txt = move()
        msg(players[current].name + " " + txt + "\n")
        current = (current + 1) % 2
        other = (other + 1) % 2
        if players[current].health <= 0:
            return players[other]
        elif players[other].health <= 0:
            return players[current]

        if True in is_human_lst:
            time.sleep(2)


        if turns >= maxturns:
            return None # No winner


