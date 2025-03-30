import random

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from pycrew_rlagent import RLAgent
from pycrew_randomagent import RandAgent
from pycrew_humanagent import HumanAgent
from pycrew_helper import plot
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
colors = [0,1,2,3] #TODO: ADD BLACK CARDS
TRICKS = [(0, 3), (1, 2), (3, 4)]
DECK = [(color, number) for color in colors for number in range(9)]
MAX_CARDS = 12 # Max num cards in hand
NUM_PLAYERS = 3
NUM_COLORS = 4
NUM_NUMBERS = 9
MAX_HISTORY = 36
MAX_TRICKS = 3
MAX_CARDS = 12
random.shuffle(DECK)

class AICrewGame(Env):

    def __init__(self, agent1, agent2, last_agent=RandAgent(2)) -> None:
        # 0 = human agent
        # 1 = random
        # 2 = rule-based
        # 3 = RL agent (for agent_type)
        super(AICrewGame, self).__init__()
        self.action_space = Discrete(MAX_CARDS)
        obs_size = (NUM_PLAYERS + NUM_COLORS + NUM_NUMBERS) * (MAX_CARDS + MAX_HISTORY + MAX_TRICKS)
        self.observation_space = Box(low=0, high=1, shape=(obs_size,), dtype=np.float32)
        self.score = 0
        self.player1 = agent1
        self.player2 = agent2
        
        # #TODO: add rule-based agent
        # else:
        #     self.player3 = RLAgent()
        self.player3 = last_agent
        self.current_table = []
        self.cards_in_play = []
        # get random start player
        self.start_idx = random.randint(0,2)
        # get tricks needed
        self.tricks_left = [(i, trick) for i, trick in enumerate(TRICKS)]
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
        # get tricks needed
        players = [self.player1, self.player2, self.player3]
        self.tricks_left = [(i, trick) for i, trick in enumerate(TRICKS)]
        # deal out cards
        random.shuffle(DECK)
        for i in range(len(DECK)):
            if i%3 == 0:
                self.player1.deck.append(DECK[i])
            elif i%3 == 1:
                self.player2.deck.append(DECK[i])
            else:
                self.player3.deck.append(DECK[i])
        return self.player3.encode_observation(2, self.player3.deck, self.current_table, self.tricks_left)

    def get_winner(self):
        current_color = self.cards_in_play[0][1][0] # color of first card played
        max_num = 0
        current_winner = None
        for card in self.cards_in_play:
            if card[1][0] == current_color and card[1][1] >= max_num:
                max_num = card[1][1]
                current_winner = card 
        return current_winner

    def step(self, action):
        # this is one AI within a round of the crew
        # get current player
        player_num = (self.start_idx + len(self.cards_in_play)) % 3
        if player_num == 0:
            current_player = self.player1
        elif player_num == 1:
            current_player = self.player2
        else:
            current_player = self.player3
        # place card
        # check if action picked is legal, stop if not
        if action not in current_player.get_legal_actions(self):
            obs = current_player.encode_observation(current_player.index, current_player.deck, self.current_table, self.tricks_left)
            # print("Illegal move!")
            return obs, -1, False, {}

        # update decks
        # add cards played to current table and cards_in_play
        action_card = current_player.deck[action] 
        self.current_table.append((current_player.get_index(),action_card))
        self.cards_in_play.append((current_player.get_index(),action_card))
        current_player.remove_card(action_card)

        reward = 0
        done = False

        # check if round over:
        if len(self.cards_in_play) == 3:
            winning_card = self.get_winner()
            self.tricks_won.append(winning_card)
            # update start index
            self.start_idx = winning_card[0]
            current_cards = [card[1] for card in self.cards_in_play]
            # check if any of the tricks were won
            for trick in self.tricks_left:
                if winning_card[0] == trick[0] and trick[1] in current_cards: # card is on table and correct winner
                    # update tricks_left
                    self.tricks_left.remove(trick)
                    print(f"Trick {trick[1]} won!")
             # check if game over because we got all the tricks

            if len(self.tricks_left) == 0:
                print("Won all tricks!")
                done = True
                reward = 1
                obs = current_player.encode_observation(current_player.index, current_player.deck, self.current_table, self.tricks_left)
                return obs, reward, done, {}
            
            elif len(self.player1.deck) == 0:
                print("Ran out of cards")
                done = True
                reward = 0
                obs = current_player.encode_observation(current_player.index, current_player.deck, self.current_table, self.tricks_left)
                return obs, reward, done, {}
                
            # clear cards in play
            self.cards_in_play = []

        obs = current_player.encode_observation(current_player.index, current_player.deck, self.current_table, self.tricks_left)
        return obs, reward, done, {}
    
    def get_tricks(self):
        return self.tricks_won
    
    def get_goals(self):
        return self.tricks_left
    
    def get_cards_in_play(self):
        return self.cards_in_play
    
def test_model_performace(model_path="crew_ai_trained"):
    agent1 = RLAgent(index=0, model_path=model_path)
    agent2 = RLAgent(index=1, model_path=model_path)
    agent3 = RLAgent(index=2, model_path=model_path)

    # Run 100 games and track results
    num_games = 100
    win_count = 0  # Track how many games the AI team wins

    for game_num in range(num_games):
        env = AICrewGame(last_agent=agent3)  # Create new game instance
        obs = env.reset()
        done = False

        while not done:
            # Determine current player
            player_index = (env.start_idx + len(env.cards_in_play)) % 3
            current_agent = [agent1, agent2, agent3][player_index]

            # AI chooses action
            action = current_agent.get_model_action(obs)
            
            # Step in environment
            obs, reward, done, _ = env.step(action)

        # If the game is won, all players get +1 (cooperative game)
        if reward == 1:
            win_count += 1

        print(f"Game {game_num + 1} finished! {'✅ WIN' if reward == 1 else '❌ LOSS'}")

    # Print final results
    win_rate = (win_count / num_games) * 100
    print("\n🏆 FINAL RESULTS AFTER 100 GAMES 🏆")
    print(f"Total Wins: {win_count} / {num_games}")
    print(f"Win Rate: {win_rate:.2f}%")

if __name__ == '__main__':
    # Training the AI agent
    # env = DummyVecEnv([lambda: AICrewGame()])
    # model = PPO("MlpPolicy", env, verbose=1)
    # model.learn(total_timesteps=10000)
    # model.save("crew_ai_trained")
    # Load trained AI model for all three agents
    
    test_model_performace()