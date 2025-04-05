from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple

app = FastAPI()

# Game state
game_state = {
    "current_table": [],
    "players": [
        {"id": 0, "type": "human", "deck": []},
        {"id": 1, "type": "human", "deck": []},
        {"id": 2, "type": "ai", "deck": []},
    ],
}

class Move(BaseModel):
    player_id: int
    card: Tuple[int, int]  # (color, number)

@app.get("/state")
def get_state():
    """Returns the current game state"""
    return game_state

@app.post("/play")
def play_card(move: Move):
    """Handles player moves"""
    player = game_state["players"][move.player_id]
    if move.card in player["deck"]:
        player["deck"].remove(move.card)
        game_state["current_table"].append((move.player_id, move.card))
        return {"status": "success", "game_state": game_state}
    return {"status": "error", "message": "Invalid move"}
