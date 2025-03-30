from pycrew_game_train import AICrewGame
from pycrew_humanagent import HumanAgent
from pycrew_rlagent import RLAgent



if __name__ == '__main__':

    # get AI agent
    model_path = "crew_ai_trained"
    agent1 = HumanAgent(0)
    agent2 = HumanAgent(1)
    agent3 = RLAgent(index=2, model_path=model_path)

    env = AICrewGame(agent1, agent2, last_agent=agent3)  # Create new game instance
    obs = env.reset()
    done = False

    while not done:
        # Determine current player
        player_index = (env.start_idx + len(env.cards_in_play)) % 3
        current_agent = [agent1, agent2, agent3][player_index]

        if player_index <= 1:
            action = current_agent.get_action(env)
        else:
            # AI chooses action
            action = current_agent.get_action(obs)
        
        # Step in environment
        obs, reward, done, _ = env.step(action)


    print(f"Game finished! {'✅ WIN' if reward == 1 else '❌ LOSS'}")
