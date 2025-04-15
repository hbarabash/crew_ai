from pycrew_agent import Agent

class RuleAgent(Agent):

    def get_leading_action(self, game):
        """To see what to do if starting the round"""
        print("In get leading action")
        # get legal moves
        moves = self.get_legal_moves(game)
        tricks_left = game.tricks_left
        # check if their trick has been won yet
        my_trick = None
        other_tricks_in_deck = []
        for trick_left in tricks_left:
            if trick_left[0] == self.index:
                my_trick = trick_left[1]
                break
        
        # check if they currently have their trick card
        have_my_trick = False
        for card in self.deck:
            if card == my_trick:
                have_my_trick = True
            if card != my_trick and card in tricks_left: # check if other ppl's tricks are in their deck
                other_tricks_in_deck.append(card)
        # if they currently have their trick card and it's high-value, play it:
        if have_my_trick == True and my_trick[1] >= 6:
            return my_trick
        # if they currently have their trick card and the other tricks have been won, play it
        elif have_my_trick == True and len(tricks_left) == 1:
            return my_trick
        # if they have someone else's trick card, play it:
        elif len(other_tricks_in_deck) > 0:
            # play the lowest value one available
            min_card = other_tricks_in_deck[0]
            for card in other_tricks_in_deck:
                if card[1] < min_card[1]:
                    min_card = card
            return min_card
        # otherwise, play lowest value card
        else:
            # play the lowest value one available
            min_card = moves[0]
            for card in moves:
                if card[1] < min_card[1]:
                    min_card = card
            return min_card
    
    def get_2nd_following_action(self, game):
        """To see what to do if playing 2nd"""
        print("In get second action")
        moves = self.get_legal_moves(game)
        # check if you can follow suit or not
        can_follow_suit = (moves[0][0] == game.cards_in_play[0][1][0])

        # check if their trick card has been won yet
        trick_won = True
        my_trick = None
        other_tricks_in_deck = []
        for trick_left in game.tricks_left:
            if trick_left[0] == self.index:
                trick_won = False # trick is still left to win
                my_trick = trick_left[1]
                break
        
        my_trick_played = False
        # check if their trick card has been played, and if so, play the max value card possible
        # (only if we can follow the suit)
        for card in game.cards_in_play:
            if card[1] == my_trick:
                my_trick_played = True 
        print("my trick played:", my_trick_played)
        if my_trick_played and can_follow_suit:
            print("my trick played and can follow suit, so playing max card possible")
            max_val_card = moves[0]
            for move in moves:
                if move[1] > max_val_card[1]:
                    max_val_card = move
            return max_val_card
        # check if we could play someone else's trick and playing it COULD result in them winning it
        # check if we have 1st person's trick and they played a higher value card
        current_winner = game.get_winner() # always player 1
        for move in moves:
            print("Move:", move)
            for trick in game.tricks_left:
                print("trick: ", trick)
                # checks if a move is a trick to be won and if the first person is supposed to win it
                if move[0] == trick[1][0] and move[1] == trick[1][1] and trick[0] == current_winner[0]:
                    print("we can play first person's trick and they might win it")
                    # check if playing it could result in the first person winning the trick
                    # check if same color and if lower value (so maybe player 1 wins their trick)
                    if can_follow_suit and move[1] < current_winner[1][1]:
                        return move
                # check if move is one of our own tricks and we have a chance at winning it
                elif move[1] == trick[1][1] and trick[0] == self.index and can_follow_suit and move[1] > current_winner[1][1]:
                    print("we can play our own trick and we might win it")
                    return move
                # check if move is the last player's trick and the current max value on the table is at most 4:
                elif move[1] == trick[1][1] and move[0] == trick[1][0] and trick[0] == ((self.index + 1) % 3):
                    current_max = current_winner[1][1]
                    if can_follow_suit and move[1] > current_max:
                        current_max = move[1]
                    if current_max <= 4:
                        return move
        # if we can still follow suit and it's our trick color, play max value card possible
        if can_follow_suit and my_trick and moves[0][0] == my_trick[0]:
            print("playing max val card since it's our suit color (if possible to win)")
            max_val_card = moves[0]
            for move in moves:
                if move[1] > max_val_card[1] and move[1] > current_winner[1][1]:
                    max_val_card = move
            if max_val_card[1] > current_winner[1][1]:
                return max_val_card
        # otherwise play lowest-value card available
        # play the lowest value one available that isn't a trick
        print("playing lowest avail card")
        print("playing lowest val card available that isn't a trick")
        tricks = [trick[1] for trick in game.tricks_left]
        # play the lowest value one available
        min_card = moves[0]
        found_card = False
        print(moves)
        for card in moves:
            print(card[1], min_card[1])
            print(tricks)
            if ((card[1] < min_card[1]) and (card not in tricks)):
                min_card = card
                found_card = True
        if found_card:
            return min_card
        else:
            print("playing lowest val card available that is a trick (last resort)")
            # play the lowest value one available
            min_card = moves[0]
            for card in moves:
                print(card[1], min_card[1])
                print(tricks)
                if ((card[1] < min_card[1])):
                    min_card = card
            return min_card

    def get_3rd_following_action(self, game):
        """To see what to do if playing 3rd"""
        print("get third action")
        moves = self.get_legal_moves(game)
        # check if you can follow suit or not
        can_follow_suit = (moves[0][0] == game.cards_in_play[0][1][0])
        print("can follow suit:", can_follow_suit)
        # check if their trick card has been won yet
        trick_won = True
        my_trick = None
        other_tricks_in_deck = []
        for trick_left in game.tricks_left:
            if trick_left[0] == self.index:
                trick_won = False # trick is still left to win
                my_trick = trick_left[1]
                break
        
        my_trick_played = False
        # check if their trick card has been played, and if so, play the lowest value card that would win the trick
        # (only if we can follow the suit)
        for card in game.cards_in_play:
            if card[1] == my_trick:
                my_trick_played = True 
        print("My trick played:", my_trick_played)
        if my_trick_played and can_follow_suit:
            min_val_card = moves[0]
            for move in moves:
                print("Move:", move)
                if move[1] <= min_val_card[1] and move[1] > my_trick[1]:
                    min_val_card = move
            print("min val card that would win trick")
            return min_val_card
        # check if we could play someone else's trick and playing it would result in them winning it
        # this includes our own trick
        current_winner = game.get_winner()
        for move in moves:
            current_winner = game.get_winner()
            for trick in game.tricks_left:
                if move[1] == trick[1][1] and can_follow_suit:
                    # check if playing it would result in the right person winning the trick
                    # check if same color and if so, value is higher (check if current winner changes)
                    print("color", move[0])
                    print("winning color:", current_winner[1][0])
                    print("current val", move[1])
                    print("winning val:", current_winner[1][1])
                    print(move, current_winner)
                    if can_follow_suit and move[1] > current_winner[1][1]:
                        current_winner = (self.index, move)
                    # check if right winner:
                    if current_winner[0] == trick[0]:
                        print("current winner:", current_winner)
                        print("trick:", trick)
                        print("playing trick because it results in correct winner")
                        return move
        # otherwise play lowest-value card available (can't play a trick card or win own trick, might still help someone else win their trick)
        
        print("playing lowest val card available that isn't a trick")
        tricks = [trick[1] for trick in game.tricks_left]
        # play the lowest value one available
        min_card = moves[0]
        print(moves)
        found_card = False
        for card in moves:
            print(card[1], min_card[1])
            print(tricks)
            if ((card[1] < min_card[1]) and (card not in tricks)):
                min_card = card
                found_card = True
        if found_card:
                return min_card
        else:
                print("playing lowest val card available that is a trick (last resort)")
                # play the lowest value one available
                min_card = moves[0]
                for card in moves:
                    print(card[1], min_card[1])
                    print(tricks)
                    if ((card[1] < min_card[1])):
                        min_card = card
                return min_card


    def get_action(self, game, obs=None):
        print("in get_action")
        current_idx = len(game.cards_in_play)
        if current_idx == 0:
            move = self.get_leading_action(game)
        elif current_idx == 1:
            move = self.get_2nd_following_action(game)
        else:
            move = self.get_3rd_following_action(game)
        return self.deck.index(move)