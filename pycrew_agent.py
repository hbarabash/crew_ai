import numpy as np

class Agent:

    def __init__(self, index):
        self.index = index
        self.deck = []


    def get_state(self, game):
        # get info of state from environment
        # list of card numbers and colors in deck
        deck = self.deck
        # list of tricks already played (triple of cards played complete with index, number, color)
        tricks = game.get_tricks()
        # current goals remaining
        goals = game.get_goals()

        state = [
            deck, tricks, goals
            ]

        return np.array(state, dtype=list)
    #, dtype=int)
    
    def get_legal_moves(self, game):
        on_table = game.get_cards_in_play()
        # print("ON TABLE", on_table)
        # if first player can play anything (will add later: except black unless black is only card left)
        if len(on_table) == 0:
            return self.deck
        else:
            played_color = on_table[0][1][0]
            # check if you have any of that suit
            print("DECK" ,self.deck)
            filtered_deck = [card for card in self.deck if card[0] == played_color]
            if len(filtered_deck) != 0:
                return filtered_deck
            else:
                return self.deck

    def get_action(self, game):
        # random moves: tradeoff exploration / exploitation
        # get legal moves
        moves = self.get_legal_moves(game)
        # get user input for move

        print("Your legal moves are: ", moves)
        move = int(input(f"Player {self.index + 1}, enter the index of the card you want to play (0-{len(moves) -1}): "))
        return moves[move]
    
    def remove_card(self, card):
        """Remove card from deck."""
        self.deck.remove(card)
        print("played", card)
    
    def get_index(self):
        return self.index