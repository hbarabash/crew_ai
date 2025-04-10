import numpy as np
from pycrew_agent import Agent

class HumanAgent(Agent):

    def get_action(self, game, obs=None):
        # random moves: tradeoff exploration / exploitation
        # get legal moves
        moves = self.get_legal_moves(game)
        # get user input for move
        print("Currently on the table are:", game.cards_in_play)
        print("The tricks left we want to win are: ", game.tricks_left)
        print("Your legal moves are:", moves)
        move = int(input(f"Player {self.index + 1}, enter the index of the card you want to play (0-{len(moves) -1}): "))
        
        return self.deck.index(moves[move])
    