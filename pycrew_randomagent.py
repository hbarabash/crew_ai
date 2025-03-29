import random
from pycrew_agent import Agent

class RandAgent(Agent):

    def get_action(self, game):
        # random moves: tradeoff exploration / exploitation
        # get legal moves
        moves = self.get_legal_moves(game)
        move = random.randint(0, len(moves)-1)
        return moves[move]
    