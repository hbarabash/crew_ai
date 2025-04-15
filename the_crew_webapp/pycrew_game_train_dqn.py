import random
import random      
from pycrew_rlagent_ppo import RLAgent
from pycrew_randomagent import RandAgent
# from pycrew_rlagent_dqn import RLdqnAgent
from pycrew_humanagent import HumanAgent
# from pycrew_helper import plot
from gymnasium import Env
from gymnasium.spaces import Discrete, Box
import numpy as np
from pycrew_ruleagent import RuleAgent
import gymnasium
import pycrew_env
from pycrew_env import AICrewGame
from pycrew_rlagent_dqn import RLdqnAgent

# from gymnasium.envs.registration import register

# register(
# id='TheCrewAI-v0',
# entry_point='pycrew_env:AICrewGame',
# )

def test_model_performance(model_path= "runs/TheCrewAI-v0__dqn__1__1744315938/dqn.cleanrl_model"): #TheCrewAI-v0__dqn__1__1744315355/dqn.cleanrl_model"): #"runs/TheCrewAI-v0__dqn__1__1744004106/dqn.cleanrl_model"):
    # agent1 = RLdqnAgent(index=0, model_path=model_path)
    # agent2 = RLdqnAgent(index=1, model_path=model_path)
    # agent3 = RLdqnAgent(index=2, model_path=model_path)
    agent1 = RandAgent(index=0)
    agent2 = RandAgent(index=1)
    agent3 = RandAgent(index=2)
    # agent1 = RuleAgent(index=0)
    # agent2 = RuleAgent(index=1)
    # agent3 = RuleAgent(index=2)

    num_games = 10000
    win_count = 0  # Track how many games the AI team wins

    for game_num in range(num_games):
        env = AICrewGame(agent1, agent2, last_agent=agent3, tricks=[[0, 1], [1, 3], [3, 2]])  # Create new game instance
        obs = env.reset()
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
    #Training the AI agent using rainbow
    import os
    import subprocess

    # # Optional: ensure runs/ folder exists to store models
    os.makedirs("runs", exist_ok=True)

    # Train the model using CleanRL's Rainbow DQN implementation
    # You can add more flags (like --track or --capture-video) if needed
    # subprocess.run([
    #     "python3", "dqn.py",
    #     "--env-id", "TheCrewAI-v0",
    #     "--total-timesteps", "100000",
    #     "--track",   # set to "True" if using wandb tracking
    #     "--save-model",
    #     "--wandb-project-name", "the-crew-ai"
    # ])
    test_model_performance()