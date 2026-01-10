# Domain Model - TicTacToe Memory Challenge

## Bounded Context
Memory-Enhanced Tic-Tac-Toe Game - A single-player game against AI with a memory training twist.

## Aggregates

### Game Aggregate
- **Root Entity**: TicTacToeGame
- **Value Objects**:
  - Position (0-8 representing 3x3 grid)
  - Mark (X for player, O for computer)
  - Difficulty (easy/medium/hard with countdown times)
- **Business Rules**:
  - Board has 9 positions (0-8)
  - Player is always X, Computer is always O
  - Player goes first
  - Countdown starts on player's turn
  - Board becomes invisible when countdown ends
  - Board becomes visible after player moves

### Stats Aggregate
- **Root Entity**: PlayerStats
- **Value Objects**:
  - WinStreak (current consecutive wins)
  - BestStreak (all-time best)
- **Business Rules**:
  - Win streak increases on player win
  - Win streak resets on loss
  - Best streak updates when current exceeds it

## Domain Events
1. **GameStarted** - New game begins, board cleared
2. **CountdownEnded** - Timer hit zero, board becomes invisible
3. **MoveMade** - Player or computer placed a mark
4. **GameEnded** - Win, loss, or draw determined

## Ubiquitous Language
- **Position**: A cell on the 3x3 grid (0-8, left-to-right, top-to-bottom)
- **Mark**: X (player) or O (computer)
- **Countdown**: Timer showing seconds until board goes invisible
- **Invisible Mode**: Board state where marks are hidden
- **Difficulty**: Controls countdown duration (easy=10s, medium=5s, hard=1s)
- **Win Streak**: Consecutive games won by player
- **Memory Challenge**: The core mechanic of hiding the board
