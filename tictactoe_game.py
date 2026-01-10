"""
TicTacToe Memory Challenge - Core Game Logic
A tic-tac-toe game with a memory twist where the board becomes invisible.
"""
from typing import Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class Mark(Enum):
    EMPTY = ""
    X = "X"      # Player
    O = "O"      # Computer


class GameState(Enum):
    IDLE = "idle"
    PLAYER_TURN = "player_turn"
    INVISIBLE = "invisible"  # Board hidden, still player's turn
    COMPUTER_TURN = "computer_turn"
    PLAYER_WINS = "player_wins"
    COMPUTER_WINS = "computer_wins"
    DRAW = "draw"


class Difficulty(Enum):
    EASY = "easy"      # 10 seconds
    MEDIUM = "medium"  # 5 seconds
    HARD = "hard"      # 1 second


# Countdown times for each difficulty
COUNTDOWN_TIMES = {
    Difficulty.EASY: 10,
    Difficulty.MEDIUM: 5,
    Difficulty.HARD: 1,
}


# All possible winning patterns (indices 0-8)
WIN_PATTERNS = [
    [0, 1, 2],  # Top row
    [3, 4, 5],  # Middle row
    [6, 7, 8],  # Bottom row
    [0, 3, 6],  # Left column
    [1, 4, 7],  # Middle column
    [2, 5, 8],  # Right column
    [0, 4, 8],  # Diagonal top-left to bottom-right
    [2, 4, 6],  # Diagonal top-right to bottom-left
]


@dataclass
class MoveResult:
    success: bool
    position: int
    mark: Mark
    winning_cells: Optional[List[int]] = None
    message: str = ""


@dataclass
class TicTacToeGame:
    """TicTacToe Memory Challenge game engine."""

    board: List[Mark] = field(default_factory=list)
    state: GameState = GameState.IDLE
    difficulty: Difficulty = Difficulty.EASY
    countdown_seconds: int = 10
    board_visible: bool = True
    winner: Optional[Mark] = None
    winning_cells: List[int] = field(default_factory=list)
    last_move: Optional[int] = None

    # Stats
    win_streak: int = 0
    best_streak: int = 0
    games_played: int = 0
    games_won: int = 0

    def __post_init__(self):
        if not self.board:
            self.reset()

    def reset(self):
        """Initialize/reset the game board."""
        self.board = [Mark.EMPTY for _ in range(9)]
        self.state = GameState.PLAYER_TURN
        self.board_visible = True
        self.winner = None
        self.winning_cells = []
        self.last_move = None
        # Keep difficulty and stats

    def set_difficulty(self, difficulty: Difficulty):
        """Set the difficulty level (affects countdown time)."""
        self.difficulty = difficulty
        self.countdown_seconds = COUNTDOWN_TIMES[difficulty]

    def get_countdown_seconds(self) -> int:
        """Get countdown seconds for current difficulty."""
        return COUNTDOWN_TIMES[self.difficulty]

    def set_board_visible(self, visible: bool):
        """Set whether the board marks are visible."""
        self.board_visible = visible
        if not visible and self.state == GameState.PLAYER_TURN:
            self.state = GameState.INVISIBLE

    def is_position_valid(self, position: int) -> bool:
        """Check if a position is valid and empty."""
        return 0 <= position < 9 and self.board[position] == Mark.EMPTY

    def get_empty_positions(self) -> List[int]:
        """Get all empty positions on the board."""
        return [i for i in range(9) if self.board[i] == Mark.EMPTY]

    def check_win(self, mark: Mark) -> bool:
        """Check if the specified mark has won."""
        for pattern in WIN_PATTERNS:
            if all(self.board[i] == mark for i in pattern):
                return True
        return False

    def get_winning_cells(self, mark: Mark) -> List[int]:
        """Get the winning cells if mark has won."""
        for pattern in WIN_PATTERNS:
            if all(self.board[i] == mark for i in pattern):
                return pattern
        return []

    def is_board_full(self) -> bool:
        """Check if the board is full (draw)."""
        return all(cell != Mark.EMPTY for cell in self.board)

    def player_move(self, position: int) -> MoveResult:
        """Player (X) makes a move."""
        if self.state not in [GameState.PLAYER_TURN, GameState.INVISIBLE, GameState.IDLE]:
            return MoveResult(False, position, Mark.X, message="Not your turn")

        if self.state == GameState.IDLE:
            self.reset()

        if not self.is_position_valid(position):
            return MoveResult(False, position, Mark.X, message="Invalid position")

        # Place the mark
        self.board[position] = Mark.X
        self.last_move = position
        self.board_visible = True  # Board becomes visible after move

        # Check for win
        if self.check_win(Mark.X):
            self.state = GameState.PLAYER_WINS
            self.winner = Mark.X
            self.winning_cells = self.get_winning_cells(Mark.X)
            self._record_game_result(won=True)
            return MoveResult(True, position, Mark.X, self.winning_cells, "You win!")

        # Check for draw
        if self.is_board_full():
            self.state = GameState.DRAW
            self._record_game_result(won=False, draw=True)
            return MoveResult(True, position, Mark.X, message="It's a draw!")

        # Switch to computer's turn
        self.state = GameState.COMPUTER_TURN
        return MoveResult(True, position, Mark.X, message="Computer's turn")

    def computer_move(self) -> MoveResult:
        """Computer (O) makes its move using simple AI."""
        if self.state != GameState.COMPUTER_TURN:
            return MoveResult(False, -1, Mark.O, message="Not computer's turn")

        position = self._calculate_best_move()
        self.board[position] = Mark.O
        self.last_move = position

        # Check for win
        if self.check_win(Mark.O):
            self.state = GameState.COMPUTER_WINS
            self.winner = Mark.O
            self.winning_cells = self.get_winning_cells(Mark.O)
            self._record_game_result(won=False)
            return MoveResult(True, position, Mark.O, self.winning_cells, "Computer wins!")

        # Check for draw
        if self.is_board_full():
            self.state = GameState.DRAW
            self._record_game_result(won=False, draw=True)
            return MoveResult(True, position, Mark.O, message="It's a draw!")

        # Switch to player's turn
        self.state = GameState.PLAYER_TURN
        return MoveResult(True, position, Mark.O, message="Your turn!")

    def _calculate_best_move(self) -> int:
        """Simple AI: win, block, center, corner, edge."""
        empty = self.get_empty_positions()

        # Priority 1: Win if possible
        for pos in empty:
            self.board[pos] = Mark.O
            if self.check_win(Mark.O):
                self.board[pos] = Mark.EMPTY
                return pos
            self.board[pos] = Mark.EMPTY

        # Priority 2: Block player win
        for pos in empty:
            self.board[pos] = Mark.X
            if self.check_win(Mark.X):
                self.board[pos] = Mark.EMPTY
                return pos
            self.board[pos] = Mark.EMPTY

        # Priority 3: Take center
        if 4 in empty:
            return 4

        # Priority 4: Take a corner
        corners = [0, 2, 6, 8]
        for corner in corners:
            if corner in empty:
                return corner

        # Priority 5: Take an edge
        edges = [1, 3, 5, 7]
        for edge in edges:
            if edge in empty:
                return edge

        # Fallback
        return empty[0]

    def _record_game_result(self, won: bool, draw: bool = False):
        """Record game result for streak tracking."""
        self.games_played += 1
        if won:
            self.games_won += 1
            self.win_streak += 1
            if self.win_streak > self.best_streak:
                self.best_streak = self.win_streak
        elif not draw:
            # Loss resets streak
            self.win_streak = 0
        # Draw doesn't affect streak

    def get_board_state(self) -> dict:
        """Get current state as dictionary for JSON serialization."""
        return {
            "board": [cell.value for cell in self.board],
            "state": self.state.value,
            "difficulty": self.difficulty.value,
            "countdown_seconds": self.get_countdown_seconds(),
            "board_visible": self.board_visible,
            "winner": self.winner.value if self.winner else None,
            "winning_cells": self.winning_cells,
            "last_move": self.last_move,
            "win_streak": self.win_streak,
            "best_streak": self.best_streak,
            "games_played": self.games_played,
            "games_won": self.games_won,
        }

    def set_board_for_testing(self, positions: List[int], mark: Mark):
        """Set specific positions for testing purposes."""
        for pos in positions:
            if 0 <= pos < 9:
                self.board[pos] = mark
