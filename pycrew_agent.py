import numpy as np

NUM_PLAYERS = 3
NUM_COLORS = 4
NUM_NUMBERS = 9
MAX_HISTORY = 36
MAX_TRICKS = 3
MAX_CARDS = 12

class Agent:

    def __init__(self, index):
        self.index = index
        self.deck = []

    def encode_card(self, player_id, color, number):
        """Encode a (player_id, color, number) tuple into a one-hot vector."""
        player_encoding = np.eye(NUM_PLAYERS)[player_id]  # One-hot encode player
        color_encoding = np.eye(NUM_COLORS)[color]  # One-hot encode color
        number_encoding = np.eye(NUM_NUMBERS)[number]  # One-hot encode number
        return np.concatenate([player_encoding, color_encoding, number_encoding])
    
    def encode_deck(self, deck):
        """Encode AI's deck as a binary vector of size 36 (4 colors × 9 numbers)."""
        deck_encoding = np.zeros(MAX_CARDS)
        for (color, number) in deck:
            index = color * NUM_NUMBERS + (number)
            deck_encoding[index] = 1  # Mark card as owned
        return deck_encoding
    
    def encode_tricks(self, tricks):
        """Encode up to 3 tricks into a fixed-length vector."""
        encoded_tricks = []
        
        for trick in tricks:
            encoded_tricks.append(self.encode_card(trick[0], trick[1][0], trick[1][1]))  # Encode each trick tuple

        # If fewer than MAX_TRICKS tricks, pad with zeros
        while len(encoded_tricks) < MAX_TRICKS:
            encoded_tricks.append(np.zeros(NUM_PLAYERS + NUM_COLORS + NUM_NUMBERS))  # Zero-padding

        return np.concatenate(encoded_tricks)  # Flatten into a single vector
    
    def encode_observation(self, player_id, hand, history, tricks):
        """Encodes the observation for the AI player."""
        # Encode player's hand (fixed size MAX_CARDS, zero-pad if needed)
        encoded_hand = [self.encode_card(player_id, c, n) for (c, n) in hand]
        while len(encoded_hand) < MAX_CARDS:
            encoded_hand.append(np.zeros(NUM_PLAYERS + NUM_COLORS + NUM_NUMBERS))  # Zero-padding
        
        # Encode history (fixed size MAX_HISTORY, zero-pad if needed)
        encoded_history = [self.encode_card(p, c, n) for (p, (c, n)) in history]
        while len(encoded_history) < MAX_HISTORY:
            encoded_history.append(np.zeros(NUM_PLAYERS + NUM_COLORS + NUM_NUMBERS))  # Zero-padding
        
        # Encode tricks left to be won
        encoded_tricks = self.encode_tricks(tricks)
        
        # Flatten and return
        return np.concatenate(encoded_hand + encoded_history + [encoded_tricks])
    
    def get_state(self, game):
        state = self.encode_observation(self.index, self.deck, game.current_table, game.tricks_left)
        return np.array(state, dtype=int)
    
    def get_legal_moves(self, game):
        on_table = game.get_cards_in_play()
        # print("ON TABLE", on_table)
        # if first player can play anything (will add later: except black unless black is only card left)
        if len(on_table) == 0:
            return self.deck
        else:
            played_color = on_table[0][1][0]
            # check if you have any of that suit
            filtered_deck = [card for card in self.deck if card[0] == played_color]
            if len(filtered_deck) != 0:
                return filtered_deck
            else:
                return self.deck
    
    def get_legal_actions(self, game):
        """Returns indices of legal actions."""
        on_table = game.get_cards_in_play()
        # print("ON TABLE", on_table)
        # if first player can play anything (will add later: except black unless black is only card left)
        if len(on_table) == 0:
            return [i for i in range(len(self.deck))]
        else:
            played_color = on_table[0][1][0]
            # check if you have any of that suit
            filtered_deck = [i for i, card in enumerate(self.deck) if card[0] == played_color]
            if len(filtered_deck) != 0:
                return filtered_deck
            else:
                return [i for i in range(len(self.deck))]

    def get_action(self, game):
        pass
    
    def remove_card(self, card):
        """Remove card from deck."""
        self.deck.remove(card)
        print("played", card)
    
    def get_index(self):
        return self.index