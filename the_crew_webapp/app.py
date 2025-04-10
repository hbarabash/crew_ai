from flask import Flask, render_template, jsonify, request
import os
from pycrew_env import AICrewGame
from pycrew_randomagent import RandAgent
# from pycrew_rlagent_ppo import RLAgent
from pycrew_humanagent import HumanAgent
from pycrew_ruleagent import RuleAgent
from pycrew_rlagent_dqn import RLdqnAgent 

app = Flask(__name__)
# model_path = "crew_ai_trained"
# game = AICrewGame(last_agent=RuleAgent(2), tricks=[[0, 3], [1, 2], [3, 4]])  # Initialize the game
game = AICrewGame(last_agent=RLdqnAgent(2), tricks=[[0, 3], [1, 2], [3, 4]])  # Initialize the game
# obs = game.reset() # get initial obs for last agent

def serialize_game_state():
    return {
        "player_decks": game.get_player_decks(),
        "current_player_deck": game.get_player_deck(),
        "current_table": game.get_current_table(),
        "cards_in_play": game.get_cards_in_play(),
        "tricks_left": game.get_tricks_left(),
        "current_player": game.get_current_player(),
        "is_game_over": game.is_game_over(),
        "is_winner": game.is_winner(),
        "done": game.done(),

    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state")
def state():
    # check if game done:
    if game.done():
        jsonify(serialize_game_state())
    # check if not human player
    if game.get_current_player() == 2:
        print("LAST PLAYER")
        agent = game.player3
        obs = game.obs
        action = agent.get_action(game, obs)
        obs, reward, done, _, _ = game.step(action)

        return jsonify({
            "status": "success",
            "reward": reward,
            "done": done,
            **serialize_game_state()
        })
    return jsonify(serialize_game_state())

@app.route("/play", methods=["POST"])
def play():
    data = request.get_json()
    player_id = data["player_id"]
    card = data["card"]

    player_deck = game.get_player_decks()[player_id]
    if card not in player_deck:
        print(player_deck)
        print(card)
        return jsonify({f"status": "error", "message": "Card not in player's hand"})

    try:
        data = request.get_json()
        card = data.get("card")
        player_id = data.get("player_id", game.get_current_player())
        current_player = game.get_current_player()

        # Only act if it's the correct player's turn
        if player_id != current_player:
            return jsonify({"status": "error", "message": "Not your turn."})

        # Get the agent object
        agent = {
            0: game.player1,
            1: game.player2,
            2: game.player3
        }[current_player]

        # If it's a human agent, wait for card input
        if isinstance(agent, HumanAgent):
            if card is None:
                return jsonify({
                    "status": "awaiting_input",
                    **serialize_game_state()
                })

            # Validate card
            player_deck = game.get_player_decks()[player_id]
            if card not in player_deck:
                return jsonify({
                    "status": "error",
                    "message": "Card not in player's hand"
                })

            action_idx = player_deck.index(card)
            obs, reward, done, _, _ = game.step(action_idx)

        else:
            # AI agent — automatically play legal move
            action = agent.get_action(obs, game)
            obs, reward, done, _, _ = game.step(action)

        return jsonify({
            "status": "success",
            "reward": reward,
            "done": done,
            **serialize_game_state()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/reset", methods=["POST"])
def reset():
    global game
    game.reset()  # Reset the game
    return jsonify({"status": "reset"})

if __name__ == '__main__':
    app.run(debug=True, port=5007)
