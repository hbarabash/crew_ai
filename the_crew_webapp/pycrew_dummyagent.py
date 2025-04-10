from pycrew_agent import Agent
# from stable_baselines3 import PPO

class DummyAgent(Agent):

    def __init__(self, index):
        super().__init__(index)
        
    
    # def get_action(self, game, obs):
    #     """Dummy get action implementation"""
    #     return 0