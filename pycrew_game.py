import random
from pycrew_rlagent import RLAgent
from pycrew_randomagent import RandAgent
from pycrew_humanagent import HumanAgent
from pycrew_helper import plot

colors = ['Y', 'G', 'P', 'B'] #TODO: ADD BLACK CARDS
TRICKS = [('Y', 3), ('G', 2), ('P', 4)]
DECK = [(color, number) for color in colors for number in range(9)]
random.shuffle(DECK)

class Game:

    def __init__(self, last_agent=RandAgent) -> None:
        # 0 = human agent
        # 1 = random
        # 2 = rule-based
        # 3 = RL agent (for agent_type)
        self.score = 0
        self.player1 = HumanAgent(0)
        self.player2 = HumanAgent(1)
        
        # #TODO: add rule-based agent
        # else:
        #     self.player3 = RLAgent()
        self.player3 = last_agent
        self.current_table = []
        self.cards_in_play = []
        
        players = [self.player1, self.player2, self.player3]
        # get random start player
        self.start_idx = random.randint(0,2)
        # get tricks needed
        self.tricks_left = [(players[i], trick) for i, trick in enumerate(TRICKS)]
        # deal out cards
        random.shuffle(DECK)
        for i in range(len(DECK)):
            if i%3 == 0:
                self.player1.deck.append(DECK[i])
            elif i%3 == 1:
                self.player2.deck.append(DECK[i])
            else:
                self.player3.deck.append(DECK[i])
        self.tricks_won = []

    def reset(self):
        # init game state
        self.score = 0
        self.current_table = []
        #TODO: add these to player class instead
        self.player1.deck = []
        self.player2.deck = []
        self.player3.deck = []
        # get random start player
        self.start_idx = random.randint(0,2)
        # deal out cards
        random.shuffle(DECK)
        for i in range(len(DECK)):
            if i%3 == 0:
                self.player1.deck.append(DECK[i])
            elif i%3 == 1:
                self.player2.deck.append(DECK[i])
            else:
                self.player3.deck.append(DECK[i])

    def get_winner(self):
        current_color = self.cards_in_play[0][1][0] # color of first card played
        max_num = 0
        current_winner = None
        for card in self.cards_in_play:
            if card[1][0] == current_color and card[1][1] >= max_num:
                max_num = card[1][1]
                current_winner = card 
        return current_winner

    def play_step(self):
        # this is one round of the crew
        # place cards
        
        # start with different player depending on who won last time
        if self.start_idx == 0:
            self._move(self.player1, self.player1.get_action(self))
            self._move(self.player2, self.player2.get_action(self))
            self._move(self.player3, self.player3.get_action(self))
        elif self.start_idx == 1:
            self._move(self.player2, self.player2.get_action(self))
            self._move(self.player3, self.player3.get_action(self))
            self._move(self.player1, self.player1.get_action(self))
        else:
            self._move(self.player3, self.player3.get_action(self))
            self._move(self.player1, self.player1.get_action(self))
            self._move(self.player2, self.player2.get_action(self))


        winning_card = self.get_winner()
        print("WINNER: PLAYER", winning_card[0].get_index)
        self.tricks_won.append(winning_card)
        # update start index
        self.start_idx = winning_card[0].get_index()
        current_cards = [card[1] for card in self.cards_in_play]
        # check if any of the tricks were won
        for trick in self.tricks_left:
            if winning_card[0] == trick[0] and trick[1] in current_cards: # card is on table and correct winner
                # update tricks_left
                self.tricks_left.remove(trick)
                print(f"Trick {trick[1]} won!")
        
        # check if game over because we got all the tricks
        reward = 0
        game_over = False
        if len(self.tricks_left) == 0:
            game_over = True
            reward = 10
            return reward, game_over, self.score
        
        # check if out of cards
        if len(self.player1.deck) == 0:
            game_over = True
            reward = 0
        
        # clear cards in play
        self.cards_in_play = []
        return reward, game_over, self.score
    

    def _move(self, player, action):
        # add cards played to current table and cards_in_play 
        self.current_table.append((player,action))
        self.cards_in_play.append((player,action))
        player.remove_card(action)
    
    def get_tricks(self):
        return self.tricks_won
    
    def get_goals(self):
        return self.tricks_left
    
    def get_cards_in_play(self):
        return self.cards_in_play


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = RandAgent(2)

    game = Game(last_agent=agent)
    while True:
        # play cards if needed
        # game.cards_in_play = [] #TODO: make sure to clear this in the play_step and add this info in
        # get old state
        state_old = agent.get_state(game)

        # get move (FINAL MOVE IS JUST AI MOVE)
        # final_move = agent.get_action(game)
        # print("MOVE", final_move)
        # perform move and get new state
        reward, done, score = game.play_step()
        state_new = agent.get_state(game)

        # train short memory
        # agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        # agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            print("GAME DONE! RESULT:", reward)
            # train long memory, plot result
            # game.reset()
            # agent.n_games += 1
            # agent.train_long_memory()

            # if score > record:
            #     record = score
            #     agent.model.save()

            # print('Game', agent.n_games, 'Score', score, 'Record:', record)

            # plot_scores.append(score)
            # total_score += score
            # mean_score = total_score / agent.n_games
            # plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)
            return


if __name__ == '__main__':
    train()