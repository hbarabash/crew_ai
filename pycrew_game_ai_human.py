from pycrew_game_train import AICrewGame
from pycrew_humanagent import HumanAgent
from pycrew_randomagent import RandAgent
from pycrew_rlagent import RLAgent
from pycrew_ruleagent import RuleAgent
import argparse

def test_rule_performace():
    agent1 = RuleAgent(index=0)
    agent2 = RuleAgent(index=1)
    agent3 = RuleAgent(index=2)

    # Run 100 games and track results
    num_games = 1000
    win_count = 0  # Track how many games the AI team wins

    for game_num in range(num_games):
        env = AICrewGame(agent1, agent2, last_agent=agent3)  # Create new game instance
        obs = env.reset()
        done = False

        while not done:
            # Determine current player
            player_index = (env.start_idx + len(env.cards_in_play)) % 3
            current_agent = [agent1, agent2, agent3][player_index]

            # AI chooses action
            action = current_agent.get_action(env, obs)
            
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

    # parser=argparse.ArgumentParser()
    # parser.add_argument("--agent")
    # args=parser.parse_args()
    # agent_type = args.agent
    # print('agent type', agent_type)
    # if agent_type == 'rand':
    #     agent3 = RandAgent(2)
    # elif agent_type == 'rule':
    #     agent3 = RuleAgent(2)
    # else:
    #     # get AI agent
    #     model_path = "crew_ai_trained"
    #     agent3 = RLAgent(index=2, model_path=model_path)
    # agent1 = HumanAgent(0)
    # agent2 = HumanAgent(1)
    

    # env = AICrewGame(agent1, agent2, last_agent=agent3)  # Create new game instance
    # obs = env.reset()
    # done = False

    # while not done:
    #     # Determine current player
    #     player_index = (env.start_idx + len(env.cards_in_play)) % 3
    #     current_agent = [agent1, agent2, agent3][player_index]

    #     if player_index <= 1:
    #         action = current_agent.get_action(env)
    #     else:
    #         # AI chooses action
    #         action = current_agent.get_action(env, obs)
    #     # Step in environment
    #     obs, reward, done, _ = env.step(action)


    # print(f"Game finished! {'✅ WIN' if reward == 1 else '❌ LOSS'}")
    test_rule_performace()
