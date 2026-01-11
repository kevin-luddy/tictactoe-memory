"""
TicTacToe Memory Challenge - FastAPI Backend
Serves the game API and static frontend.
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

from tictactoe_game import TicTacToeGame, GameState, Difficulty

app = FastAPI(title="TicTacToe Memory Challenge", description="Tic-Tac-Toe with a memory twist")

# Global game instance
game = TicTacToeGame()


class MoveRequest(BaseModel):
    position: int


class NewGameRequest(BaseModel):
    difficulty: Optional[str] = None


class DifficultyRequest(BaseModel):
    difficulty: str


class GameStateResponse(BaseModel):
    board: list
    state: str
    difficulty: str
    countdown_seconds: int
    board_visible: bool
    winner: Optional[str]
    winning_cells: list
    last_move: Optional[int]
    win_streak: int
    best_streak: int
    games_played: int
    games_won: int
    loss_streak: int = 0
    message: str = ""
    tokens: int = 0
    total_tokens_earned: int = 0
    current_avatar: dict = {}
    unlocked_avatars: list = []


class AvatarRequest(BaseModel):
    avatar_id: str


def make_response(message: str = "") -> GameStateResponse:
    """Helper to create response from game state."""
    state = game.get_board_state()
    return GameStateResponse(
        board=state["board"],
        state=state["state"],
        difficulty=state["difficulty"],
        countdown_seconds=state["countdown_seconds"],
        board_visible=state["board_visible"],
        winner=state["winner"],
        winning_cells=state["winning_cells"],
        last_move=state["last_move"],
        win_streak=state["win_streak"],
        best_streak=state["best_streak"],
        games_played=state["games_played"],
        games_won=state["games_won"],
        loss_streak=state["loss_streak"],
        message=message,
        tokens=state["tokens"],
        total_tokens_earned=state["total_tokens_earned"],
        current_avatar=state["current_avatar"],
        unlocked_avatars=state["unlocked_avatars"]
    )


@app.get("/")
async def serve_frontend():
    """Serve the main HTML page."""
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))


@app.get("/api/state")
async def get_game_state():
    """Get the current game state."""
    return make_response()


@app.post("/api/new-game")
async def new_game(request: NewGameRequest = None):
    """Start a new game."""
    if request and request.difficulty:
        try:
            diff = Difficulty(request.difficulty.lower())
            game.set_difficulty(diff)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid difficulty: {request.difficulty}")

    game.reset()
    diff_names = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}
    diff_name = diff_names.get(game.difficulty.value, game.difficulty.value)
    return make_response(f"Game started on {diff_name}! Your turn - watch the countdown!")


@app.post("/api/difficulty")
async def set_difficulty(request: DifficultyRequest):
    """Set the difficulty level."""
    try:
        diff = Difficulty(request.difficulty.lower())
        game.set_difficulty(diff)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid difficulty: {request.difficulty}")

    return make_response(f"Difficulty set to {request.difficulty} ({game.get_countdown_seconds()}s countdown)")


@app.post("/api/move")
async def make_move(move: MoveRequest):
    """Player makes a move."""
    result = game.player_move(move.position)

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    return make_response(result.message)


@app.post("/api/computer-move")
async def computer_move():
    """Computer makes its move."""
    if game.state != GameState.COMPUTER_TURN:
        raise HTTPException(status_code=400, detail="Not computer's turn")

    result = game.computer_move()
    return make_response(result.message)


@app.post("/api/set-invisible")
async def set_invisible():
    """Set board to invisible mode (called when countdown ends)."""
    game.set_board_visible(False)
    return make_response("Board is now invisible! Make your move from memory!")


@app.get("/api/shop")
async def get_shop():
    """Get avatar shop data."""
    return game.get_shop_data()


@app.post("/api/purchase-avatar")
async def purchase_avatar(request: AvatarRequest):
    """Purchase an avatar with tokens."""
    result = game.purchase_avatar(request.avatar_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return {**result, "tokens": game.tokens, "unlocked_avatars": game.unlocked_avatars}


@app.post("/api/set-avatar")
async def set_avatar(request: AvatarRequest):
    """Set the current avatar (must be unlocked)."""
    result = game.set_avatar(request.avatar_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return {**result, "current_avatar": game.get_current_avatar()}


# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
