import torch
import numpy as np
from pycrew_agent import Agent
from dqn import QNetwork  
import gymnasium as gym

class RLdqnAgent(Agent):

    def __init__(self, index, model_path="runs/TheCrewAI-v0__dqn__1__1744224994/dqn.cleanrl_model", env_id="TheCrewAI-v0", device="cpu"):
        super().__init__(index)
        self.device = device
        self.env = gym.make(env_id)  # Needed for obs space
        # self.model = QNetwork(self.env.observation_space, self.env.action_space).to(self.device)
        self.model = QNetwork(self.env).to(self.device)
        checkpoint = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def get_action(self, game, obs):
        """Returns action using CleanRL-trained model."""

        # legal_actions = self.get_legal_actions(game)

        # if isinstance(obs, tuple):
        #     obs = obs[0]
        # # Convert to NumPy array if it's not already
        # obs = np.asarray(obs, dtype=np.float32)

        # # Flatten if it's not already 1D
        # if obs.ndim != 1:
        #     obs = obs.flatten()

        # # Now shape should be [816], reshape to [1, 816]
        # obs_tensor = torch.from_numpy(obs).unsqueeze(0).to(self.device)

        # with torch.no_grad():
        #     q_values = self.model(obs_tensor)
        #     q_values = np.array(q_values.detach().numpy())
        #     illegal_action_mask = np.ones(len(q_values)) * -np.inf
        #     illegal_action_mask[legal_actions] = q_values[legal_actions]
        #     print("Action vals", illegal_action_mask)
        #     action = np.argmax(illegal_action_mask)

        # return action
        # Get legal action mask (list of 0s and 1s, length = 12)
        legal_actions = game.get_legal_actions()
        mask_tensor = torch.tensor(legal_actions, dtype=torch.bool).unsqueeze(0).to(self.device)
        
        if isinstance(obs, tuple):
            obs = obs[0]

        # Process observation
        obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0).to(self.device)

        # Get Q-values and mask illegal actions
        with torch.no_grad():
            q_values = self.model(obs_tensor)
            q_values[~mask_tensor] = -float('inf')  # Mask out illegal actions

        # Pick best legal action
        action = torch.argmax(q_values, dim=1).item()
        return action
