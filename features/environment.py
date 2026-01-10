"""
Behave environment configuration for TicTacToe Memory Challenge.
"""
from tictactoe_game import TicTacToeGame


def before_scenario(context, scenario):
    """Reset game state before each scenario."""
    context.game = TicTacToeGame()
    context.last_result = None
