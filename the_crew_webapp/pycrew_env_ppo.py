import random
import random
from typing import Optional      
from pycrew_dummyagent import DummyAgent
from pycrew_rlagent_ppo import RLAgent
from pycrew_randomagent import RandAgent
from pycrew_humanagent import HumanAgent
# from pycrew_helper import plot
# from gym import Env
# from gym.spaces import Discrete, Box
from gymnasium import Env
from gymnasium.spaces import Discrete, Box
import numpy as np
from pycrew_ruleagent import RuleAgent
# from sb3_contrib import MaskablePPO
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

# from gymnasium.envs.registration import register

# register(
#     id='TheCrewAI-v0',
#     entry_point='pycrew_env:AICrewGame',
# )


colors = [0,1,2,3] #TODO: ADD BLACK CARDS
TRICKS = [(0, 3), (1, 2), (3, 4)]
DECK = [[color, number] for color in colors for number in range(9)]
MAX_CARDS = 12 # Max num cards in hand
NUM_PLAYERS = 3
NUM_COLORS = 4
NUM_NUMBERS = 9
MAX_HISTORY = 36
MAX_TRICKS = 3
MAX_CARDS = 12
random.shuffle(DECK)

class AICrewGamePPO(Env):

    def __init__(self, agent1=HumanAgent(0), agent2=HumanAgent(1), last_agent=HumanAgent(2), tricks=None) -> None:
        # 0 = human agent
        # 1 = random
        # 2 = rule-based
        # 3 = RL agent (for agent_type)
        super(AICrewGamePPO, self).__init__()
        self.action_space = Discrete(MAX_CARDS)
        obs_size = (NUM_PLAYERS + NUM_COLORS + NUM_NUMBERS) * (MAX_CARDS + MAX_HISTORY + MAX_TRICKS + MAX_TRICKS)
        self.observation_space = Box(low=0, high=1, shape=(obs_size,), dtype=np.float32)
        self.score = 0
        self.player1 = agent1
        self.player2 = agent2
        self.player3 = last_agent
        self.seed=1

        self.current_table = []
        self.cards_in_play = []
        # get random start player
        self.start_idx = random.randint(0,2)
        # get tricks needed
        if tricks == None:
            colors = random.sample(range(4), 3)
            numbers = [random.randint(0, 8) for _ in range(3)]
            trick_cards = [[colors[i], numbers[i]] for i in range(3)]
            self.tricks_left = [[i, trick_cards[i]] for i in range(3)]
        else:
            self.tricks_left = [[i, tricks[i]] for i in range(3)]
        self.fixed_tricks = tricks

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

    def reset(self, seed=None, options=None):
        # init game state
        self.score = 0
        self.current_table = []
        self.cards_in_play = []
        #TODO: add these to player class instead
        self.player1.deck = []
        self.player2.deck = []
        self.player3.deck = []
        # get random start player
        self.start_idx = random.randint(0,2)
        # get tricks needed
        if self.fixed_tricks:
            self.tricks_left = [[i, self.fixed_tricks[i]] for i in range(3)]
        else:
            colors = random.sample(range(4), 3)
            numbers = [random.randint(0, 8) for _ in range(3)]
            trick_cards = [[colors[i], numbers[i]] for i in range(3)]
            self.tricks_left = [[i, trick_cards[i]] for i in range(3)]
        # deal out cards
        random.shuffle(DECK)
        for i in range(len(DECK)):
            if i%3 == 0:
                self.player1.deck.append(DECK[i])
            elif i%3 == 1:
                self.player2.deck.append(DECK[i])
            else:
                self.player3.deck.append(DECK[i])
        players = [self.player1, self.player2, self.player3]
        return players[self.start_idx].encode_observation(self.start_idx, players[self.start_idx].deck, self.current_table, self.tricks_left, self.cards_in_play), {}

    def get_winner(self):
        current_color = self.cards_in_play[0][1][0] # color of first card played
        max_num = 0
        current_winner = None
        for card in self.cards_in_play:
            if card[1][0] == current_color and card[1][1] >= max_num:
                max_num = card[1][1]
                current_winner = card 
        return current_winner
    
    def get_legal_actions(self):
        """Gets a mask of the legal actions for a current player"""
        mask = [0] * 12
        current_idx = (self.start_idx + len(self.cards_in_play)) % 3
        if current_idx == 0:
            legal_actions = self.player1.get_legal_actions(self)
        elif current_idx == 1:
            legal_actions = self.player2.get_legal_actions(self)
        else:
            legal_actions = self.player3.get_legal_actions(self)
        for idx in legal_actions:
            mask[idx] = 1
        print("MASK", mask)
        mask = np.array(mask, dtype=np.int8)
        return mask

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
        #check if action picked is legal, stop if not - only illegal if out of cards
        if action not in current_player.get_legal_actions(self):
            obs = current_player.encode_observation(current_player.index, current_player.deck, self.current_table, self.tricks_left, self.cards_in_play)
            print("Illegal move - out of cards")
            return obs, 0, False, False, {}

        # update decks
        # add cards played to current table and cards_in_play
        action_card = current_player.deck[action] 
        self.current_table.append((current_player.get_index(),action_card))
        self.cards_in_play.append((current_player.get_index(),action_card))
        current_player.remove_card(action_card)

        reward = 0
        done = False

        
        players = [self.player1, self.player2, self.player3]
        next_player = players[self.start_idx]

        # check if round over:
        if len(self.cards_in_play) == 3:
            winning_card = self.get_winner()
            print("Winning card:", winning_card)
            self.tricks_won.append(winning_card)
            # update start index
            self.start_idx = winning_card[0]
            next_player = players[self.start_idx]
            current_cards = [card[1] for card in self.cards_in_play]
            # check if any of the tricks were won
            for trick in self.tricks_left:
                print("trick checked: ", trick)
                print("winner player:", winning_card[0])
                print("trick player:", trick[0])
                if winning_card[0] == trick[0] and ([trick[1][0], trick[1][1]] in current_cards): # card is on table and correct winner
                    # update tricks_left
                    self.tricks_left.remove(trick)
                    print(f"Trick {trick[1]} won!")
             # check if game over because we got all the tricks

            if len(self.tricks_left) == 0:
                print("Won all tricks!")
                done = True
                reward = 1
                # obs doesn't matter, done
                obs = current_player.encode_observation(current_player.index, current_player.deck, self.current_table, self.tricks_left, self.cards_in_play)
                return obs, reward, done, False, {}
            
            elif len(self.player1.deck) == 0:
                print("Ran out of cards")
                done = True
                reward = 0
                # obs doesn't matter, done
                obs = current_player.encode_observation(current_player.index, current_player.deck, self.current_table, self.tricks_left, self.cards_in_play)
                return obs, reward, done, False, {}
                
            # clear cards in play
            self.cards_in_play = []

        obs = next_player.encode_observation(next_player.index, next_player.deck, self.current_table, self.tricks_left, self.cards_in_play)
        # obs = current_player.encode_observation(current_player.index, current_player.deck, self.current_table, self.tricks_left, self.cards_in_play)
        return obs, reward, done, False, {}
    
    def get_tricks(self):
        return self.tricks_won
    
    def get_goals(self):
        return self.tricks_left
    
    def get_cards_in_play(self):
        return self.cards_in_play
    
    def get_current_table(self):
        return self.current_table
    
    def get_tricks_left(self):
        return self.tricks_left
    
    def get_current_player(self):
        return ((self.start_idx + len(self.cards_in_play)) % 3)
    
    def get_player_decks(self):
        return {
            0: self.player1.deck,
            1: self.player2.deck,
            2: self.player3.deck
        }
    
    def get_player_deck(self):
        current_player = self.get_current_player()
        if current_player == 0:
            return { 0: self.player1.deck}
        elif current_player == 1:
            return {1 : self.player2.deck}
        else:
            return {2: self.player3.deck}
    def done(self):
        return ((len(self.tricks_left) == 0) or (len(self.player3.deck) == 0) and (len(self.player2.deck) == 0) and (len(self.player1.deck) == 0))
    
    def is_game_over(self):
        return (self.done() and (len(self.tricks_left) > 0))
    
    def is_winner(self):
        return (self.done() and (not self.is_game_over()))


def test_model_performance(model_path= "crew_ai_trained"):
    agent1 = RLAgent(index=0, model_path=model_path)
    agent2 = RLAgent(index=1, model_path=model_path)
    agent3 = RLAgent(index=2, model_path=model_path)
    # agent1 = RandAgent(index=0)
    # agent2 = RandAgent(index=1)
    # agent3 = RandAgent(index=2)
    # agent1 = RuleAgent(index=0)
    # agent2 = RuleAgent(index=1)
    # agent3 = RuleAgent(index=2)

    num_games = 10000
    win_count = 0  # Track how many games the AI team wins

    for game_num in range(num_games):
        env = AICrewGamePPO(agent1, agent2, last_agent=agent3)  # Create new game instance
        obs = env.reset()[0]
        print(f"Game {game_num + 1} started! Initial Observation: {obs}")
        done = False

        while not done:
            player_index = (env.start_idx + len(env.cards_in_play)) % 3
            current_agent = [agent1, agent2, agent3][player_index]
            action = current_agent.get_action(env, obs)
            print(f"Agent {current_agent.index} took action: {action}")

            # Step in environment
            obs, reward, done, _, _ = env.step(action)
            # print(f"Observation: {obs}, Reward: {reward}, Done: {done}")

        if reward == 1:
            win_count += 1
            print(f"Game {game_num + 1} finished! ✅ WIN")
        else:
            print(f"Game {game_num + 1} finished! ❌ LOSS")

    win_rate = (win_count / num_games) * 100
    print("\n🏆 FINAL RESULTS AFTER 100 GAMES 🏆")
    print(f"Total Wins: {win_count} / {num_games}")
    print(f"Win Rate: {win_rate:.2f}%")

if __name__ == '__main__':
    agent1 = DummyAgent(index=0, )
    agent2 = DummyAgent(index=1,)
    agent3 = DummyAgent(index=2,)
    num_envs = 3  # One per player
    env = DummyVecEnv([lambda: AICrewGamePPO(agent1, agent2, agent3) for _ in range(num_envs)])

    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=100000)
    model.save("crew_ai_trained")
    # test_model_performance()