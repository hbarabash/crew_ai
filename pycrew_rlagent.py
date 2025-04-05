from pycrew_agent import Agent
from stable_baselines3 import PPO

class RLAgent(Agent):

    def __init__(self, index, model_path='None'):
        super().__init__(index)
        if model_path != 'None':
            self.model = PPO.load(model_path)  # Load trained model
        else:
            # raise ValueError("No trained model path provided!")
            self.model = None
    
    def get_action(self, game, obs):
        """Returns action using trained model."""
        action, _ = self.model.predict(obs)  
        return action